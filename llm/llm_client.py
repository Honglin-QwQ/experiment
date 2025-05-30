# llm/llm_client.py
import json
import re
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import httpx
import openai
from tenacity import retry, wait_random_exponential, stop_after_attempt
from loguru import logger
import os

from config.system_config import SystemConfig


@dataclass
class LLMResponse:
    """LLM响应结构"""
    content: str
    model: str
    usage: Dict[str, int]
    raw_response: Any


class OpenRouterClient:
    """OpenRouter LLM客户端"""

    def __init__(self, config: SystemConfig):
        self.config = config
        self.client = openai.OpenAI(
            api_key=config.openrouter_api_key,
            base_url=config.openrouter_base_url,
            http_client=httpx.Client(
                base_url=config.openrouter_base_url,
                follow_redirects=True,
            )
        )
        self.conversation_history: Dict[str, List[Dict]] = {}

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def generate(self,
                 prompt: str,
                 system_prompt: Optional[str] = None,
                 model: Optional[str] = None,
                 temperature: float = 0.7,
                 max_tokens: int = 10000,
                 conversation_id: Optional[str] = None) -> LLMResponse:
        """生成响应"""
        try:
            messages = []

            # 添加系统提示词
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})

            # 添加对话历史
            if conversation_id and conversation_id in self.conversation_history:
                messages.extend(self.conversation_history[conversation_id])

            # 添加当前提示词
            messages.append({"role": "user", "content": prompt})

            # 使用指定模型或默认模型
            model = model or self.config.models.get("pm_agent")

            # 调用API
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                extra_headers={
                    "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
                    "HTTP-Referer": "https://quantinvest.ai",
                    "X-Title": "Multi-Agent Portfolio Management System"
                },
                response_format={"type": "json_object"},
            )

            # 保存对话历史
            if conversation_id:
                if conversation_id not in self.conversation_history:
                    self.conversation_history[conversation_id] = []
                self.conversation_history[conversation_id].append({"role": "user", "content": prompt})
                self.conversation_history[conversation_id].append({
                    "role": "assistant",
                    "content": response.choices[0].message.content
                })

            if not response or not response.choices:
                logger.error("Empty or invalid response from LLM.")
                raise RuntimeError("LLM returned empty response")

            content = response.choices[0].message.content


            return LLMResponse(
                content=content,
                model=response.model,
                usage=response.usage.dict() if response.usage else {},
                raw_response=response
            )

        except Exception as e:
            logger.error(f"LLM generation error: {str(e)}")
            raise


def parse_json_response(response):
    """更robust的JSON解析"""
    try:
        # 尝试直接解析
        return json.loads(response)
    except json.JSONDecodeError as e:
        logger.warning(f"Direct JSON parse failed: {e}")

        # 尝试清理和修复JSON
        cleaned_response = response.strip()

        # 检查是否是截断的JSON，尝试补全
        if cleaned_response.count('{') > cleaned_response.count('}'):
            # 缺少结尾花括号，尝试补全
            missing_braces = cleaned_response.count('{') - cleaned_response.count('}')
            cleaned_response += '}' * missing_braces
            logger.info(f"Added {missing_braces} closing braces")

            try:
                return json.loads(cleaned_response)
            except json.JSONDecodeError:
                logger.warning("Failed to fix with closing braces")

        # 尝试提取完整的JSON块
        json_pattern = r'\{(?:[^{}]|{[^{}]*})*\}'
        matches = re.findall(json_pattern, cleaned_response, re.DOTALL)

        for match in matches:
            try:
                return json.loads(match)
            except json.JSONDecodeError:
                continue

        # 如果都失败了，尝试提取部分有效的JSON
        try:
            # 找到第一个 { 和最后一个 }
            start = cleaned_response.find('{')
            end = cleaned_response.rfind('}')
            if start != -1 and end != -1 and end > start:
                partial_json = cleaned_response[start:end + 1]
                return json.loads(partial_json)
        except json.JSONDecodeError:
            pass

        logger.error(f"All JSON parsing methods failed. Response: {response[:200]}...")
        return {}
