import logging
from typing import Any

from astrbot.api import logger
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.event.filter import EventMessageType
from astrbot.api.star import Context, Star, register
from astrbot.core.message.message_event_result import MessageChain

from .utils import PluginUtils


plugin_util = PluginUtils('./config.yaml')


@register(
    "agentic_memory_v2",   # 插件名称
    "YourName",            # 作者
    "2.0.0",               # 版本
    "重构版：具备中间件流水线架构的群聊智能体"
)
class AgenticMemoryPluginV2(Star):
    """
    Agentic Memory V2 核心入口。
    这里只负责对接 AstrBot 框架，实际的业务逻辑将交由流水线（Pipeline）处理。
    """

    def __init__(self, context: Context):
        super().__init__(context)
        # 初始化最基础的配置或日志
        logger.info("[AgenticMemoryV2] 插件骨架已初始化，随时准备接收消息。")
        
        # [TODO: Milestone 2] 在这里初始化你的流水线 (Pipeline)
        # self.pipeline = MessagePipeline(...)
        
        # [TODO: Milestone 3] 在这里初始化外部 Prompt 管理器和 TTLCache
        # self.prompt_manager = PromptManager(template_dir="prompts")
        # self.cache_manager = CacheManager()

    @filter.event_message_type(EventMessageType.GROUP_MESSAGE)
    async def on_group_message(self, event: AstrMessageEvent) -> None:
        """
        群消息事件入口。
        """
        # 1. 基础异常防护与必要信息提取
        if not hasattr(event, "message_obj"):
            return
            
        group_id = str(
            getattr(event.message_obj, "group_id", getattr(event, "session_id", ""))
        ).strip()
        
        if not group_id:
            return
        
        if not plugin_util.is_group_allowed(group_id=group_id):     # 判断群号
            return

        # 2. 提取纯文本消息（暂不处理图片/表情等多模态）
        message_text = str(getattr(event, "message_str", "")).strip()
        sender_name = str(event.get_sender_name()).strip() or "Unknown"

        # 3. 打印基础日志（确认 I/O 畅通）
        logger.info(f"[Group: {group_id}] {sender_name}: {message_text}")

        # ---------------------------------------------------------
        # [TODO: Milestone 2] 未来这里将被替换为流水线调用：
        # ctx = MessageContext(event, group_id, sender_name, message_text)
        # await self.pipeline.process(ctx)
        # if ctx.should_reply:
        #     await self._send_reply(event, ctx.reply_text)
        # ---------------------------------------------------------

        # 4. 临时回显逻辑 (Echo)：用于测试双向通信是否正常
        # 设定一个极简的触发词避免它一直刷屏
        if "测试呼叫" in message_text:
            # 强化群聊身份设定，避免 AI 味
            reply_text = f"收到啦 {sender_name}，通道一切正常。" 
            await self._send_reply(event, reply_text)

    async def _send_reply(self, event: AstrMessageEvent, text: str) -> None:
        """
        统一的发送回复接口。
        未来这里可以加入长文本截断、分段发送、延迟打字机效果等逻辑。
        """
        if not text:
            return
            
        try:
            # 使用 AstrBot 的标准 MessageChain 发送文本
            await event.send(event.plain_result(text))
            logger.info(f"[Reply Sent] {text}")
        except Exception as exc:
            logger.error(f"[Reply Error] 发送消息失败: {exc}。原本要发送的内容：{text}")

    # [TODO: Milestone 5] 在这里添加 APScheduler 的启动逻辑
