# 导入 BatchInfoCalculator 节点类
# 确保你的 batch_info_calculator.py 文件与此 __init__.py 在同一目录下
from .batch_info_calculator import BatchInfoCalculator

# 定义节点类映射
NODE_CLASS_MAPPINGS = {
    "BatchInfoCalculator": BatchInfoCalculator
}

# 定义节点显示名称映射
NODE_DISPLAY_NAME_MAPPINGS = {
    "BatchInfoCalculator": "Batch Info Calculator / 批处理信息计算器"
}

# __all__ 导出模块的公共名称
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

# 打印加载信息
print("✅ MyVideoTools: Loaded Batch Info Calculator / 批处理信息计算器 node")
# 你可以根据你的包名修改 "MyVideoTools" 这部分