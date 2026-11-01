from pathlib import Path
from typing import Any

import yaml

from config.settings import ROOT_DIR


def load_yaml(relative_path: str) -> Any:
    """从项目根目录读取 YAML 测试数据。"""
    path: Path = ROOT_DIR / relative_path
    with path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)
