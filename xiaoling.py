# 拟人化控制台交互
# ═══════════════════════════════════════

# [ZERO-AUTO] 重构建议: 函数 console_interactive 约98行，建议拆分
def console_interactive(engine: XiaoLingEngine):
    """控制台交互模式 — 接受「小零，命令」"""
    import random