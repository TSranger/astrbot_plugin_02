import yaml
from typing import Any, Dict

from astrbot.api.message_components import Plain, Image, At, Face, Poke, Record



class PluginUtils:
    def __init__(self, config_path: str):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        self.config = config
        self.group_scope = config.get('group_scope', {})

    def is_group_allowed(self, group_id: str) -> bool:
        """判断插件是否允许在某个群内运行。

        Args:
            group_id: 群号。

        Returns:
            群被允许时返回 ``True``。
        """
        if not self.group_scope.get("enabled", True):
            return True
        whitelist = {
            str(item).strip()
            for item in self.group_scope.get("group_whitelist", [])
            if str(item).strip()
        }
        return group_id in whitelist if whitelist else False

    def get_message(self, event):
        '''
        Returns:
            消息内容
        '''
        message_chain = event.get_messages()

        sender_id = event.get_sender_id()
        sender_name = str(event.get_sender_name()).strip() or "Unknown"

        result = {'id': sender_id, 'name': sender_name}
        
        for component in message_chain:
            if isinstance(component, Plain):
                print(f"文本: {component.text}")
                result['text'] = component.text
            
            elif isinstance(component, Image):
                print(f"图片URL: {component.url}")
                result['image'] = component.url
            
            elif isinstance(component, At):
                print(f"@了QQ: {component.qq}")
                result['at'] = component.qq
            
            elif isinstance(component, Face):
                print(f"表情: {component.id}")
                result['emoji'] = component.id
            
            elif isinstance(component, Poke):
                print(f"戳一戳类型: {component.type}")
                result['poke'] = component.type
            
            elif isinstance(component, Record):
                print(f"语音URL: {component.url}")
                result['record'] = component.url
        
        return result

