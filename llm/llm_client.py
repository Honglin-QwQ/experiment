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
                 max_tokens: int = 4000,
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
    try:
        # 尝试直接解析
        return json.loads(response)
    except json.JSONDecodeError:
        # 第二种方法：尝试使用 raw_decode 解析（从头开始解析）
        decoder = json.JSONDecoder()
        try:
            response_json, index = decoder.raw_decode(response)
            return response_json
        except json.JSONDecodeError:
            # 第三种方法：尝试提取第一个JSON对象/数组
            json_pattern = r'\{[\s\S]*\}|\$[\s\S]*\$'
            matches = re.findall(json_pattern, response)
            if matches:
                try:
                    return json.loads(matches[0])
                except json.JSONDecodeError:
                    pass

            logger.warning("Failed to parse JSON response, returning empty dict")
            return {}