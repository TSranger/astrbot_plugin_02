import yaml
from typing import Any, Dict



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
