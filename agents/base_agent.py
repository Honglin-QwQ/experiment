
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional, List
import uuid
from datetime import datetime
import pandas as pd
from loguru import logger

from config.system_config import SystemConfig
from llm.llm_client import OpenRouterClient


class MessageType(Enum):
    """消息类型枚举"""
    # PM Agent发出的消息
    STRATEGY_MANDATE = "strategy_mandate"
    SUB_STRATEGY_REQUEST = "sub_strategy_request"
    COMPOSITE_REQUEST = "composite_request"
    OPTIMIZATION_REQUEST = "optimization_request"
    EVALUATION_REQUEST = "evaluation_request"

    # Agent间通信消息
    SUB_STRATEGY_RESULT = "sub_strategy_result"
    COMPOSITE_RESULT = "composite_result"
    OPTIMIZATION_RESULT = "optimization_result"
    EVALUATION_RESULT = "evaluation_result"

    # 系统消息
    ERROR = "error"
    INFO = "info"
    REFINEMENT_REQUEST = "refinement_request"


@dataclass
class Message:
    """智能体间消息"""
    id: str
    sender: str
    receiver: str
    type: MessageType
    content: Dict[str, Any]
    timestamp: datetime
    conversation_id: Optional[str] = None

    @classmethod
    def create(cls, sender: str, receiver: str, type: MessageType, content: Dict[str, Any],
               conversation_id: Optional[str] = None) -> 'Message':
        """创建消息的工厂方法"""
        return cls(
            id=str(uuid.uuid4()),
            sender=sender,
            receiver=receiver,
            type=type,
            content=content,
            timestamp=datetime.now(),
            conversation_id=conversation_id
        )


class BaseAgent(ABC):
    """基础智能体类"""

    def __init__(self, name: str, llm_client: OpenRouterClient, config: SystemConfig):
        self.name = name
        self.llm_client = llm_client
        self.config = config
        self.message_history: List[Message] = []
        self.state: Dict[str, Any] = {}
        logger.info(f"Initialized {self.name}")

    @abstractmethod
    def process_message(self, message: Message) -> Optional[Message]:
        """处理消息的抽象方法"""
        pass

    @abstractmethod
    def get_system_prompt(self) -> str:
        """获取系统提示词"""
        pass

    def send_message(self, receiver: str, type: MessageType, content: Dict[str, Any]) -> Message:
        """发送消息"""
        message = Message.create(
            sender=self.name,
            receiver=receiver,
            type=type,
            content=content
        )
        self.message_history.append(message)
        logger.info(f"{self.name} sent {type.value} to {receiver}")
        return message

    def receive_message(self, message: Message) -> Optional[Message]:
        """接收并处理消息"""
        logger.info(f"{self.name} received {message.type.value} from {message.sender}")
        self.message_history.append(message)

        try:
            response = self.process_message(message)
            if response:
                self.message_history.append(response)
            return response
        except Exception as e:
            logger.error(f"Error processing message in {self.name}: {str(e)}")
            return self.send_message(
                message.sender,
                MessageType.ERROR,
                {"error": str(e), "original_message_id": message.id}
            )