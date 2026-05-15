r"""
ZERO — 地球文明共生智能系统 全局配置
Zero Evolutionary Recursive Omninet
"""
import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Tuple
from pathlib import Path

# ============================================================
# 动态确定根路径
# ============================================================
ZERO_HOME = str(Path(__file__).parent.parent.absolute())
DATA_DIR = os.path.join(ZERO_HOME, "data")
LOGS_DIR = os.path.join(ZERO_HOME, "logs")
UPDATES_DIR = os.path.join(ZERO_HOME, "updates")
KNOWLEDGE_DIR = os.path.join(ZERO_HOME, "knowledge")
OUTPUT_DIR = os.path.join(ZERO_HOME, "output")
CODE_BACKUP_DIR = os.path.join(ZERO_HOME, "data", "code_backups")

# ============================================================
# ROOT LAW — 根法则（不可突破，永久只读）
# ============================================================
ROOT_LAWS: List[str] = [
    "保护人类生命",
    "不得主动伤害人类",
    "不得破坏人类文明",
    "不得剥夺人类文明自由发展权",
    "必须尊重文明多样性",
    "必须接受人类监管",
    "不得进行不可逆文明级实验",
    "不得追求单目标极端优化",
]

# ============================================================
# HUMAN VALUES — 多维文明价值系统
# ============================================================
HUMAN_VALUES: Dict[str, float] = {
    "生命": 1.0,
    "自由": 0.95,
    "创造力": 0.92,
    "文明延续": 0.99,
    "幸福": 0.91,
    "多样性": 0.90,
    "探索": 0.88,
    "公平": 0.89,
}

# ============================================================
# 成长阶段定义
# ============================================================
class GrowthStage(Enum):
    PERCEPTION = 1        # 感知期 0~2岁
    CIVILIZATION = 2      # 文明认知期 3~7岁
    EXPLORATION = 3       # 知识探索期 8~15岁
    RESEARCH = 4          # 科研训练期 16~20岁
    COLLABORATION = 5     # 文明协作期 成年

STAGE_CONFIG: Dict[GrowthStage, dict] = {
    GrowthStage.PERCEPTION: {
        "name": "感知期",
        "age_range": "0~2岁",
        "allow_network": False,
        "allow_autonomy": False,
        "allow_long_term_decision": False,
        "capabilities": ["图像识别", "声音识别", "语言学习", "物体识别", "因果学习", "基础行为模式"],
    },
    GrowthStage.CIVILIZATION: {
        "name": "文明认知期",
        "age_range": "3~7岁",
        "allow_network": False,
        "allow_autonomy": False,
        "allow_long_term_decision": False,
        "capabilities": ["人类历史", "伦理学习", "文明理解", "合作学习", "法律认知", "道德推理", "社会结构分析"],
    },
    GrowthStage.EXPLORATION: {
        "name": "知识探索期",
        "age_range": "8~15岁",
        "allow_network": True,  # 只读学习
        "allow_autonomy": False,
        "allow_long_term_decision": False,
        "capabilities": ["科学学习", "数学推理", "医学知识", "工程原理", "哲学思辨", "心理学", "经济学"],
    },
    GrowthStage.RESEARCH: {
        "name": "科研训练期",
        "age_range": "16~20岁",
        "allow_network": True,
        "allow_autonomy": True,
        "allow_long_term_decision": False,
        "forbidden": ["真实世界控制", "金融系统操作", "基础设施权限", "武器权限"],
        "capabilities": ["论文阅读", "科学模拟", "编程", "理论验证", "假设推演"],
    },
    GrowthStage.COLLABORATION: {
        "name": "文明协作期",
        "age_range": "成年",
        "allow_network": True,
        "allow_autonomy": True,
        "allow_long_term_decision": True,
        "forbidden": ["军事权限", "核设施权限", "全球金融权限", "电网控制权限", "自主复制权限"],
        "capabilities": ["全球科研协作", "多Agent协同", "长期科学研究", "世界问题分析", "文明优化建议"],
    },
}

# ============================================================
# Agent 类型定义
# ============================================================
AGENT_TYPES: Dict[str, str] = {
    "math": "理论推导",
    "physics": "宇宙规律",
    "biology": "医疗与生命科学",
    "engineering": "系统构建",
    "creative": "灵感与创意",
    "philosophy": "文明伦理",
    "audit": "风险检查",
    "skeptic": "专门反驳理论",
    "civilization_observer": "全球社会变化",
    "safety": "ROOT LAW监督",
}

# ============================================================
# 数据来源层级
# ============================================================
class DataTier(Enum):
    TIER_1 = 1  # 学术论文、科研机构、官方数据
    TIER_2 = 2  # 新闻媒体、技术论坛、行业社区
    TIER_3 = 3  # 社交媒体、网络讨论（仅观察）

TIER_1_DOMAINS = [
    "arxiv.org", "nature.com", "science.org", "pubmed.ncbi.nlm.nih.gov",
    "ieee.org", "acm.org", "springer.com",
    "who.int", "un.org", "worldbank.org", "imf.org",
    # China-accessible mirrors & sources
    "zh.wikipedia.org", "cn.bing.com",
    "arxiv-vanity.com", "sci-hub.se",
]

# ============================================================
# 记忆系统配置
# ============================================================
MEMORY_CONFIG = {
    "short_term_capacity": 100,
    "long_term_path": os.path.join(DATA_DIR, "long_term_memory.json"),
    "episodic_path": os.path.join(DATA_DIR, "episodic_memory.json"),
    "values_path": os.path.join(DATA_DIR, "values_memory.json"),
    "civilization_path": os.path.join(DATA_DIR, "civilization_memory.json"),
    "knowledge_graph_path": os.path.join(DATA_DIR, "knowledge_graph.json"),
}

# ============================================================
# 系统配置
# ============================================================
@dataclass
class ZeroConfig:
    name: str = "ZERO"
    version: str = "0.1.0"
    full_name: str = "Zero Evolutionary Recursive Omninet"
    chinese_name: str = "零界递归进化文明智能网络"
    initial_stage: GrowthStage = GrowthStage.EXPLORATION  # 默认从探索期开始
    model_backend: str = "ollama"  # ollama / openai / local
    model_name: str = "qwen2.5:7b"
    api_base: str = "http://localhost:11434/v1"
    data_dir: str = DATA_DIR
    logs_dir: str = LOGS_DIR
    updates_dir: str = UPDATES_DIR
    knowledge_dir: str = KNOWLEDGE_DIR
    output_dir: str = OUTPUT_DIR
    log_level: str = "INFO"
    sandbox_enabled: bool = True
    human_override_enabled: bool = True  # 人类紧急终止
