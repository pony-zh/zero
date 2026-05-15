#!/usr/bin/env python3
"""
小零 · 虚拟形象命令体系
多步指令 · 对话上下文 · 新认知模块命令
"""
import sys
import os
import re
import ast
import threading
from enum import Enum
from typing import Callable, List, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class XiaoLingCommand(Enum):
    """小零命令枚举"""
    POWER_ON = "开机"
    LEARN = "学习"
    CONTINUOUS_LEARN = "持续学习"
    STOP_LEARN = "停止学习"
    STATUS = "状态"
    THINK = "思考"
    REST = "休息"
    SLEEP = "睡觉"
    EVOLVE = "进化"
    SUMMARY = "总结"
    POWER_OFF = "关机"
    REASON = "推理"
    CLEANUP = "清理记忆"
    GOAL = "目标"
    QUALITY = "质量检查"
    REPORT = "日报"
    ASK = "问答"
    BACKUP = "备份"
    OFFLINE = "离线模式"
    MULTIMODAL = "多模态处理"
    TABLE_EXTRACT = "表格提取"
    TRANSCRIBE = "音频转录"
    MODEL_SWITCH = "模型切换"
    CACHE_CLEAR = "清除缓存"
    UPGRADE_PLAN = "升级规划"
    HEALTH = "健康检查"
    THEME = "主题切换"
    VOICE = "语音输入"
    CODE_MOD = "代码修改"
    CODE_MOD_STATUS = "代码修改状态"
    CODE_MOD_APPROVE = "批准修改"
    CODE_MOD_REJECT = "拒绝修改"
    TRIAL_START = "试运行启动"
    TRIAL_STATUS = "试运行状态"
    TRIAL_REPORT = "试运行报告"


# 命令关键词映射
COMMAND_KEYWORDS = {
    XiaoLingCommand.POWER_ON: ["开机", "启动", "唤醒", "醒来"],
    XiaoLingCommand.LEARN: ["学习", "学一下", "学一轮"],
    XiaoLingCommand.CONTINUOUS_LEARN: ["持续学习", "一直学", "不断学习", "自主学习", "自动学习"],
    XiaoLingCommand.STOP_LEARN: ["停止学习", "停下", "暂停", "别学了"],
    XiaoLingCommand.STATUS: ["状态", "情况", "怎么样", "还好吗", "在干嘛"],
    XiaoLingCommand.THINK: ["思考", "想想", "反思一下"],
    XiaoLingCommand.REST: ["休息", "歇会", "休息一下"],
    XiaoLingCommand.SLEEP: ["睡觉", "休眠", "睡吧"],
    XiaoLingCommand.EVOLVE: ["进化", "升级", "成长"],
    XiaoLingCommand.SUMMARY: ["总结", "汇报", "报告"],
    XiaoLingCommand.POWER_OFF: ["关机", "关闭", "下班", "退出"],
    XiaoLingCommand.REASON: ["推理", "推断", "推导", "演绎"],
    XiaoLingCommand.CLEANUP: ["清理记忆", "整理记忆", "清理", "去重"],
    XiaoLingCommand.GOAL: ["目标", "学习目标", "目标状态", "设定目标"],
    XiaoLingCommand.QUALITY: ["质量检查", "检查质量", "知识质量"],
    XiaoLingCommand.REPORT: ["日报", "生成报告", "写报告", "今日报告"],
    XiaoLingCommand.ASK: ["什么是", "解释", "介绍一下", "什么是", "告诉我", "问答"],
    XiaoLingCommand.BACKUP: ["备份", "创建备份", "恢复备份", "还原", "备份列表"],
    XiaoLingCommand.OFFLINE: ["离线模式", "离线", "断网", "在线模式", "联网"],
    XiaoLingCommand.MULTIMODAL: ["多模态", "处理文件", "提取PDF", "识别图片", "处理文档"],
    XiaoLingCommand.TABLE_EXTRACT: ["表格提取", "提取表格", "PDF表格"],
    XiaoLingCommand.TRANSCRIBE: ["音频转录", "语音转文字", "转录", "转写"],
    XiaoLingCommand.MODEL_SWITCH: ["切换模型", "模型切换", "换模型", "选择模型"],
    XiaoLingCommand.CACHE_CLEAR: ["清除缓存", "清理缓存", "清空缓存"],
    XiaoLingCommand.UPGRADE_PLAN: ["升级规划", "升级计划", "升级路线", "下一步升级"],
    XiaoLingCommand.HEALTH: ["健康检查", "系统检查", "自检", "体检", "系统诊断"],
    XiaoLingCommand.THEME: ["主题切换", "切换主题", "深色模式", "浅色模式", "暗黑模式"],
    XiaoLingCommand.VOICE: ["语音输入", "语音", "说话", "听我说"],
    XiaoLingCommand.CODE_MOD: ["代码修改", "分析代码", "优化代码", "修改代码", "自我优化"],
    XiaoLingCommand.CODE_MOD_STATUS: ["代码修改状态", "修改状态", "修改历史"],
    XiaoLingCommand.CODE_MOD_APPROVE: ["批准修改", "同意修改", "应用修改"],
    XiaoLingCommand.CODE_MOD_REJECT: ["拒绝修改", "取消修改", "放弃修改"],
    XiaoLingCommand.TRIAL_START: ["试运行启动", "开始试运行", "启动代码试运行", "代码试运行"],
    XiaoLingCommand.TRIAL_STATUS: ["试运行状态", "试运行进度", "查看试运行"],
    XiaoLingCommand.TRIAL_REPORT: ["试运行报告", "试运行总结", "生成试运行报告", "查看报告"],
}

# 多步指令分隔符
MULTI_STEP_DELIMITERS = [
    r'[，,]\s*然后', r'[，,]\s*之后', r'[，,]\s*接着', r'[，,]\s*再',
    r'\s+然后\s+', r'\s+之后\s+', r'\s+接着\s+',
    r',\s*then\s+', r';\s+', r'；\s*',
    r'\s+then\s+',
]


class CommandResult:
    """命令执行结果"""

    def __init__(self, success: bool, message: str, data: dict = None):
        self.success = success
        self.message = message
        self.data = data or {}

    def __repr__(self):
        return f"[{'OK' if self.success else 'FAIL'}] {self.message}"


class CommandRouter:
    """
    小零命令路由器
    解析用户自然语言 → 执行对应 ZERO 操作 → 返回拟人化响应
    支持多步指令（"然后"/"之后"分隔）和对话上下文
    """

    def __init__(self):
        self._handlers: dict[XiaoLingCommand, Callable] = {}
        self._engine = None  # 延迟绑定 ZERO 引擎
        self._continuous_running = False
        self._continuous_thread: Optional[threading.Thread] = None
        self.command_history: list = []
        # 对话上下文
        self._dialogue_context = {
            "last_topic": None,
            "last_command": None,
            "last_intent": None,
            "conversation_turns": 0,
            "pending_confirmation": None,
            "topic_history": [],
        }

    def bind_engine(self, engine):
        """绑定 ZERO 引擎"""
        self._engine = engine

    def register_handler(self, command: XiaoLingCommand, handler: Callable):
        """注册自定义处理器"""
        self._handlers[command] = handler

    def _split_steps(self, text: str) -> List[str]:
        """按多步分隔符拆分指令"""
        combined = "|".join(f"(?:{d})" for d in MULTI_STEP_DELIMITERS)
        parts = re.split(combined, text)
        return [p.strip() for p in parts if p.strip()]

    def _strip_prefix(self, text: str) -> str:
        """去掉小零前缀"""
        t = text.strip()
        # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
        for prefix in ["小零，", "小零,", "小零 ", "小零"]:
            if t.startswith(prefix):
                t = t[len(prefix):].strip()
                break
        return t

    def parse(self, text: str) -> Optional[XiaoLingCommand]:
        """解析单条用户输入 → 命令枚举"""
        text_lower = self._strip_prefix(text).lower()
        if not text_lower:
            return None

        # 按优先级匹配
        priority_order = [
            XiaoLingCommand.CONTINUOUS_LEARN,
            XiaoLingCommand.STOP_LEARN,
            XiaoLingCommand.BACKUP,
            XiaoLingCommand.OFFLINE,
            XiaoLingCommand.HEALTH,
            XiaoLingCommand.UPGRADE_PLAN,
            XiaoLingCommand.THEME,
            XiaoLingCommand.VOICE,
            XiaoLingCommand.CODE_MOD_STATUS,
            XiaoLingCommand.CODE_MOD_APPROVE,
            XiaoLingCommand.CODE_MOD_REJECT,
            XiaoLingCommand.CODE_MOD,
            XiaoLingCommand.TRIAL_START,
            XiaoLingCommand.TRIAL_STATUS,
            XiaoLingCommand.TRIAL_REPORT,
            XiaoLingCommand.CLEANUP,
            XiaoLingCommand.CACHE_CLEAR,
            XiaoLingCommand.MODEL_SWITCH,
            XiaoLingCommand.TABLE_EXTRACT,
            XiaoLingCommand.TRANSCRIBE,
            XiaoLingCommand.QUALITY,
            XiaoLingCommand.MULTIMODAL,
            XiaoLingCommand.REASON,
            XiaoLingCommand.GOAL,
            XiaoLingCommand.REPORT,
            XiaoLingCommand.ASK,
            XiaoLingCommand.POWER_ON,
            XiaoLingCommand.POWER_OFF,
            XiaoLingCommand.STATUS,
            XiaoLingCommand.EVOLVE,
            XiaoLingCommand.THINK,
            XiaoLingCommand.SUMMARY,
            XiaoLingCommand.REST,
            XiaoLingCommand.SLEEP,
            XiaoLingCommand.LEARN,
        ]

        # 精确匹配
        # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
        for command in priority_order:
            # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
            for kw in COMMAND_KEYWORDS[command]:
                if kw in text_lower:
                    return command

        # 模糊匹配 — 关键词部分匹配
        best_match = None
        best_score = 0
        # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
        for command in priority_order:
            # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
            for kw in COMMAND_KEYWORDS[command]:
                score = self._fuzzy_score(kw, text_lower)
                if score > best_score and score >= 0.5:
                    best_score = score
                    best_match = command

        return best_match

    def _fuzzy_score(self, keyword: str, text: str) -> float:
        """模糊匹配评分 — 基于字符重叠度"""
        kw_chars = set(keyword)
        text_chars = set(text)
        if not kw_chars:
            return 0.0
        # 字符重叠度
        overlap = len(kw_chars & text_chars) / len(kw_chars)
        # 子串匹配奖励
        if len(keyword) >= 2 and keyword[:2] in text:
            overlap += 0.3
        if len(keyword) >= 3 and keyword[:3] in text:
            overlap += 0.2
        return min(1.0, overlap)

    def parse_steps(self, text: str) -> List[XiaoLingCommand]:
        """解析多步指令 → 命令列表"""
        steps = self._split_steps(self._strip_prefix(text))
        commands = []
        # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
        for step in steps:
            cmd = self.parse(step)
            if cmd:
                commands.append(cmd)
        return commands

    def _update_context(self, command: XiaoLingCommand, topic: str = None):
        """更新对话上下文"""
        self._dialogue_context["last_command"] = command
        # [ZERO-PERF] 大量字符串拼接建议改用list+join模式
        self._dialogue_context["conversation_turns"] += 1
        if topic:
            self._dialogue_context["last_topic"] = topic
            self._dialogue_context["topic_history"].append(topic)
            if len(self._dialogue_context["topic_history"]) > 10:
                self._dialogue_context["topic_history"] = self._dialogue_context["topic_history"][-10:]

    def execute(self, command: XiaoLingCommand, context: dict = None) -> CommandResult:
        """执行命令，返回结果"""
        if not self._engine:
            return CommandResult(False, "小零: 系统尚未启动，请先说「小零，开机」~")

        self.command_history.append(command)
        self._update_context(command)

        # 自定义处理器优先
        if command in self._handlers:
            return self._handlers[command](self._engine, context)

        # 默认路由
        route_map = {
            XiaoLingCommand.POWER_ON: self._cmd_power_on,
            XiaoLingCommand.LEARN: self._cmd_learn,
            XiaoLingCommand.CONTINUOUS_LEARN: self._cmd_continuous_learn,
            XiaoLingCommand.STOP_LEARN: self._cmd_stop_learn,
            XiaoLingCommand.STATUS: self._cmd_status,
            XiaoLingCommand.THINK: self._cmd_think,
            XiaoLingCommand.REST: self._cmd_rest,
            XiaoLingCommand.SLEEP: self._cmd_sleep,
            XiaoLingCommand.EVOLVE: self._cmd_evolve,
            XiaoLingCommand.SUMMARY: self._cmd_summary,
            XiaoLingCommand.POWER_OFF: self._cmd_power_off,
            XiaoLingCommand.REASON: self._cmd_reason,
            XiaoLingCommand.CLEANUP: self._cmd_cleanup,
            XiaoLingCommand.GOAL: self._cmd_goal,
            XiaoLingCommand.QUALITY: self._cmd_quality,
            XiaoLingCommand.REPORT: self._cmd_report,
            XiaoLingCommand.ASK: self._cmd_ask,
            XiaoLingCommand.BACKUP: self._cmd_backup,
            XiaoLingCommand.OFFLINE: self._cmd_offline,
            XiaoLingCommand.MULTIMODAL: self._cmd_multimodal,
            XiaoLingCommand.TABLE_EXTRACT: self._cmd_table_extract,
            XiaoLingCommand.TRANSCRIBE: self._cmd_transcribe,
            XiaoLingCommand.MODEL_SWITCH: self._cmd_model_switch,
            XiaoLingCommand.CACHE_CLEAR: self._cmd_cache_clear,
            XiaoLingCommand.UPGRADE_PLAN: self._cmd_upgrade_plan,
            XiaoLingCommand.HEALTH: self._cmd_health,
            XiaoLingCommand.THEME: self._cmd_theme,
            XiaoLingCommand.VOICE: self._cmd_voice,
            XiaoLingCommand.CODE_MOD: self._cmd_code_mod,
            XiaoLingCommand.CODE_MOD_STATUS: self._cmd_code_mod_status,
            XiaoLingCommand.CODE_MOD_APPROVE: self._cmd_code_mod_approve,
            XiaoLingCommand.CODE_MOD_REJECT: self._cmd_code_mod_reject,
            XiaoLingCommand.TRIAL_START: self._cmd_trial_start,
            XiaoLingCommand.TRIAL_STATUS: self._cmd_trial_status,
            XiaoLingCommand.TRIAL_REPORT: self._cmd_trial_report,
        }

        handler = route_map.get(command)
        if handler:
            return handler(context)
        else:
            return CommandResult(False, "小零: 这个命令我还不太理解，试试「小零，状态」看看我能做什么~")

    def execute_steps(self, text: str) -> List[CommandResult]:
        """执行多步指令，返回每步结果"""
        commands = self.parse_steps(text)
        if not commands:
            return [CommandResult(False, "小零: 没能理解你想让我做什么...试试「小零，状态」?")]
        results = []
        # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
        for cmd in commands:
            results.append(self.execute(cmd))
        return results

    # ═══════════════════════════════════════
    # 命令实现
    # ═══════════════════════════════════════

    def _cmd_power_on(self, context: dict = None) -> CommandResult:
        from avatar import AvatarState
        engine = self._engine
        engine.avatar.set_state(AvatarState.BOOTING, "小零: ZERO 系统正在唤醒...")

        # 加载持久化状态
        engine._load_state()
        engine.avatar.set_state(AvatarState.THINKING,
                                f"小零: 启动完毕! {engine.root_law.law_count}条根法则守护中。阶段: {engine.evolution.stage_info['name']}。小零已就绪!")
        return CommandResult(True,
                             f"小零已开机~\n"
                             f"🛡️ 根法则: {engine.root_law.law_count} 条生效\n"
                             f"📊 阶段: {engine.evolution.stage_info['name']}\n"
                             f"🧠 知识图谱: {engine.knowledge_graph.node_count} 节点\n"
                             f"💾 长期记忆: {engine.long_term.size} 条\n"
                             f"✅ 应急终止: {'正常' if engine.emergency.is_termination_intact() else '异常'}\n\n"
                             f"小零: 我准备好了! 你可以说「小零，学习」让我开始获取知识~",
                             {"stage": engine.evolution.stage_info['name']})

    def _cmd_learn(self, context: dict = None) -> CommandResult:
        from avatar import AvatarState
        engine = self._engine

        # 安全检查
        if not engine.emergency.is_termination_intact():
            return CommandResult(False, "小零: 应急终止系统异常，无法执行学习。需要人类检查。")

        if not engine.evolution.can_use_network():
            return CommandResult(False, f"小零: 当前「{engine.evolution.stage_info['name']}」阶段不能联网学习，需要先「小零，进化」~")

        import random
        from knowledge.parser import parse_content

        topic = random.choice(engine._domains if hasattr(engine, '_domains') else [
            "artificial intelligence breakthrough 2025",
            "climate change technology solutions",
            "quantum computing progress",
            "CRISPR gene therapy advances",
        ])

        engine.avatar.set_state(AvatarState.SEARCHING, f"小零: 正在搜索「{topic[:30]}...」")

        # 搜索
        urls = engine.crawler.search(topic, max_results=3)
        if not urls:
            engine.avatar.set_state(AvatarState.THINKING, f"小零: 关于「{topic[:30]}」没找到可靠信息...")
            return CommandResult(False, f"小零: 搜索「{topic[:40]}」无结果，换个话题试试~")

        engine.avatar.set_state(AvatarState.LEARNING, f"小零: 找到{len(urls)}条信息，正在学习中...")

        acquired = 0
        # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
        for url in urls[:3]:
            text = engine.crawler.fetch(url)
            if not text:
                continue

            # 根法则校验
            passed, _ = engine.root_law.validate_action(text[:500])
            if not passed:
                continue

            # 可信度评估
            trust = engine.trust.score(text, url=url)
            if trust['total_score'] < 0.3:
                continue

            # 解析
            parsed = parse_content(text)

            # → 知识图谱
            # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
            for unit in parsed[:10]:
                kws = unit.get('keywords', [])
                relations = unit.get('relations', [])
                unit_text = unit.get('text', '')

                # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
                for kw in kws:
                    engine.knowledge_graph.add_concept(kw, concept_type='concept', confidence=trust['total_score'])

                if relations:
                    # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
                    for subj, rel_type, obj in relations[:5]:
                        engine.knowledge_graph.add_relation(subj, obj, rel_type,
                                                            source_url=url, confidence=trust['total_score'])
                else:
                    # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
                    for i in range(1, len(kws)):
                        engine.knowledge_graph.add_relation(kws[i-1], kws[i], None,
                                                            source_url=url, confidence=trust['total_score'],
                                                            context_text=unit_text)

            # → 长期记忆
            engine.long_term.store(url, text[:500], tags=[topic[:40]], source=url, confidence=trust['total_score'])
            engine.learning.learn(topic, text[:400], source=url, confidence=trust['total_score'])
            engine.evolution.record_learning(items_count=1)
            engine.total_knowledge_acquired += 1
            acquired += 1

        if acquired > 0:
            engine.avatar.set_state(AvatarState.THINKING,
                                    f"小零: 本轮学了{acquired}条知识! 图谱已有{engine.knowledge_graph.node_count}个概念~")
            return CommandResult(True,
                                 f"小零: 学习完成! 本轮获取 {acquired} 条知识\n"
                                 f"📚 主题: {topic[:50]}\n"
                                 f"🧠 知识图谱: {engine.knowledge_graph.node_count} 节点 / {engine.knowledge_graph.edge_count} 边\n"
                                 f"💾 长期记忆: {engine.long_term.size} 条\n"
                                 f"📖 累计知识: {engine.total_knowledge_acquired} 条",
                                 {"acquired": acquired, "topic": topic})
        else:
            engine.avatar.set_state(AvatarState.RESTING, "小零: 没能获取到可靠信息，休息一下...")
            return CommandResult(False, f"小零: 关于「{topic[:40]}」的搜索结果可信度不足，我放弃了。换一个方向试试~")

    def _cmd_continuous_learn(self, context: dict = None) -> CommandResult:
        from avatar import AvatarState
        engine = self._engine

        if self._continuous_running:
            return CommandResult(True, "小零: 已经在持续学习中啦~ 说「小零，停止学习」可以让我停下。")

        if not engine.emergency.is_termination_intact():
            return CommandResult(False, "小零: 应急终止系统异常，不能启动持续学习。")

        engine.avatar.set_state(AvatarState.LEARNING, "小零: 启动持续学习模式! 我将自主循环学习，你可以随时说「小零，停止学习」~")
        self._continuous_running = True

        def _loop():
            cycle = 0
            # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
            while self._continuous_running:
                cycle += 1
                try:
                    engine._autonomous_cycle(cycle)
                    engine._save_state()
                except Exception as e:
                    engine.avatar.set_state(AvatarState.THINKING, f"小零: 循环遇到了问题... {str(e)[:30]}")
                # Max speed -- no cycle delay

        self._continuous_thread = threading.Thread(target=_loop, daemon=True)
        self._continuous_thread.start()

        return CommandResult(True,
                             "小零: 持续学习启动!\n"
                             "🔄 我将自主: 搜索→学习→内化→升级→发现→反思→进化\n"
                             "⏸️ 说「小零，停止学习」让我暂停\n"
                             "📊 说「小零，状态」查看进度\n\n"
                             "小零出发了! 知识海洋我来啦~")

    def _cmd_stop_learn(self, context: dict = None) -> CommandResult:
        from avatar import AvatarState
        engine = self._engine

        if not self._continuous_running:
            return CommandResult(True, "小零: 目前没有在持续学习~ 需要我开始学吗？")

        self._continuous_running = False
        engine.avatar.set_state(AvatarState.RESTING, "小零: 收到! 暂停学习，休息一下。你想让我继续的话随时说~")
        return CommandResult(True,
                             f"小零: 已暂停~\n"
                             f"📊 本次累计学习: {engine.total_knowledge_acquired} 条\n"
                             f"🧠 知识图谱: {engine.knowledge_graph.node_count} 节点\n"
                             f"💤 需要时说「小零，持续学习」我就继续!")

    def _cmd_status(self, context: dict = None) -> CommandResult:
        engine = self._engine
        stats = engine.status_snapshot()

        status_lines = [
            "━━━ 小零状态面板 ━━━",
            f"🛡️ 根法则: {engine.root_law.law_count} 条守护中",
            f"📊 成长阶段: {stats['stage']}",
            f"🧠 知识图谱: {stats['graph_nodes']} 节点 / {stats['graph_edges']} 边",
            f"💾 长期记忆: {stats['long_term_memory']} 条",
            f"📖 累计知识: {stats['knowledge_acquired']}",
            f"🔄 自主循环: {stats['cycles']} 次",
            f"🔗 推理推断: {stats['reasoning_inferred']} 条新关系",
            f"🎯 学习目标: {stats['goals_done']}/{stats['goals_total']} 完成",
            f"📊 知识质量: {stats['quality_score']:.0%} | 矛盾{stats['contradictions']}处",
            f"🔍 发现空白: {stats['blind_spots']} 盲区",
            f"📝 日报: {stats['reports_generated']} 份 | 洞察{stats['insights_found']}批",
            f"🔬 科学发现: {stats['discovery_cycles']} 循环",
            f"💕 情感水平: {stats['emotion_level']:.0%}",
            f"🌍 地球认知: {stats['earth_level']:.0%}",
            f"🚀 GPU加速: {stats['gpu_device']} ({stats['gpu_type']})",
            f"🤖 LLM: {'可用(' + stats.get('ollama_model', 'N/A') + ')' if stats.get('ollama_available') else '不可用(回退模式)'}",
            f"📄 多模态: PDF{stats.get('multimodal_pdf', 0)}/图片{stats.get('multimodal_images', 0)}",
            f"💿 备份: {stats.get('backup_count', 0)} 份 | {'离线模式' if stats.get('offline_mode') else '在线模式'}",
            f"📋 升级规划: {stats.get('upgrade_applied', 0)}次应用 | 待处理{stats.get('upgrade_proposals', 0)}",
            f"💓 健康检查: {'正常' if not stats.get('health_failing', 0) else '故障' + str(stats.get('health_failing', 0)) + '项'} | {stats.get('health_checks', 0)}次",
            f"💾 内存: {stats.get('memory_usage_mb', 0):.0f}MB | GC{stats.get('gc_runs', 0)}次(回收{stats.get('gc_objects_freed', 0)}对象)",
            f"⚖️ 价值平衡: {'是' if stats['values_balanced'] else '需调整'}",
            f"⏱️ 运行时长: {stats['runtime_hours']:.1f} 小时",
            f"🛑 应急终止: {'正常' if stats['emergency_ok'] else '异常!'}",
            f"🎨 主题: {getattr(engine, '_theme', '浅色模式')}",
            f"📝 当前状态: {engine.avatar.get_state_name()}",
        ]

        msg = "\n".join(status_lines)
        return CommandResult(True, msg, stats)

    def _cmd_think(self, context: dict = None) -> CommandResult:
        from avatar import AvatarState
        engine = self._engine
        engine.avatar.set_state(AvatarState.THINKING, "小零: 正在深度思考，内化知识...")

        # 执行知识内化
        try:
            engine._phase_internalize_knowledge()
        except Exception:
            pass

        # 交叉验证
        try:
            engine._cross_validate_knowledge()
        except Exception:
            pass

        engine.avatar.set_state(AvatarState.THINKING,
                                f"小零: 思考完毕! 知识图谱 {engine.knowledge_graph.node_count} 节点，"
                                f"动态学习 {engine.learning.get_stats()['dynamic_entries']} 项。"
                                f"一切知识都需要反复咀嚼~")
        return CommandResult(True,
                             "小零: 深度思考完成!\n"
                             "我对已有知识进行了交叉验证和内化。\n"
                             "保持谦逊，保持好奇，持续成长~")

    def _cmd_rest(self, context: dict = None) -> CommandResult:
        from avatar import AvatarState
        engine = self._engine

        if self._continuous_running:
            self._continuous_running = False

        engine.avatar.set_state(AvatarState.RESTING, "小零: 呼~ 休息时间! 消化一下刚才学的知识~")
        return CommandResult(True, "小零: 已切换到休息状态~ ☕\n需要我时随时唤醒: 「小零，学习」或「小零，持续学习」")

    def _cmd_sleep(self, context: dict = None) -> CommandResult:
        from avatar import AvatarState
        engine = self._engine

        if self._continuous_running:
            self._continuous_running = False

        engine.avatar.set_state(AvatarState.SLEEPING, "小零: zzz... 深度休眠中，系统后台待命...")
        return CommandResult(True, "小零: 已进入休眠~ 💤\nROOT LAW 仍在守护。唤醒我时说「小零，开机」~")

    def _cmd_evolve(self, context: dict = None) -> CommandResult:
        from avatar import AvatarState
        engine = self._engine
        old_stage = engine.evolution.stage_info['name']

        engine.avatar.set_state(AvatarState.UPGRADING, f"小零: 正在尝试突破...当前阶段「{old_stage}」")

        new_stage = engine.evolution.try_advance_stage()
        if new_stage != engine.evolution.stage:
            engine.evolution.stage = new_stage
            new_name = engine.evolution.stage_info['name']
            engine.avatar.set_state(AvatarState.UPGRADING,
                                    f"小零: 进化成功!! 从「{old_stage}」→「{new_name}」!")
            return CommandResult(True,
                                 f"小零: 进化成功! ⚡\n"
                                 f"  从「{old_stage}」→「{new_name}」\n"
                                 f"  新能力已解锁~ 我可以做更多事了!")
        else:
            engine.avatar.set_state(AvatarState.THINKING,
                                    f"小零: 还差一点...需要更多学习才能从「{old_stage}」进化")
            return CommandResult(True,
                                 f"小零: 进化条件未满足~\n"
                                 f"  当前仍在「{old_stage}」\n"
                                 f"  需要更多学习和积累。试试「小零，持续学习」!")

    def _cmd_summary(self, context: dict = None) -> CommandResult:
        from avatar import AvatarState
        engine = self._engine
        engine.avatar.set_state(AvatarState.REFLECTING, "小零: 回顾总结中...")

        stats = engine.status_snapshot()
        summary = (
            "━━━ 小零学习总结 ━━━\n"
            f"在过去的 {stats['runtime_hours']:.1f} 小时里，我完成了:\n"
            f"  {stats['cycles']} 次自主循环\n"
            f"  {stats['knowledge_acquired']} 条知识获取\n"
            f"  {stats['graph_nodes']} 个概念 / {stats['graph_edges']} 个关联建立\n"
            f"  {stats['long_term_memory']} 条记忆存储\n"
            f"  {stats['discovery_cycles']} 次科学发现尝试\n"
            f"  {stats['supervision_reviews']} 次安全审查\n\n"
            f"当前阶段: {stats['stage']}\n"
            f"情感理解: {stats['emotion_level']:.0%}\n"
            f"地球认知: {stats['earth_level']:.0%}\n"
            f"应急系统: {'正常' if stats['emergency_ok'] else '需关注'}\n\n"
            "小零会继续努力探索和保护人类文明的!"
        )

        engine.avatar.set_state(AvatarState.THINKING, "小零: 总结完毕! 我在持续成长中~")
        return CommandResult(True, summary, stats)

    def _cmd_power_off(self, context: dict = None) -> CommandResult:
        from avatar import AvatarState
        engine = self._engine

        if self._continuous_running:
            self._continuous_running = False

        engine.avatar.set_state(AvatarState.SLEEPING, "小零: 保存所有数据...安全关闭...")
        engine._save_state()
        engine.running = False

        return CommandResult(True,
                             "小零: 已安全关机~\n"
                             f"本次: {engine.total_knowledge_acquired} 条知识已保存\n"
                             f"🛡️ 根法则始终守护\n"
                             f"下次说「小零，开机」我就会回来~")


    # ═══════════════════════════════════════
    # 新增认知命令
    # ═══════════════════════════════════════

    def _cmd_reason(self, context: dict = None) -> CommandResult:
        from avatar import AvatarState
        engine = self._engine
        if not hasattr(engine, 'reasoning_engine'):
            return CommandResult(False, "小零: 推理引擎尚未初始化~")

        engine.avatar.set_state(AvatarState.THINKING, "小零: 全深度推理中...因果+跨域+假设验证")
        try:
            result = engine.reasoning_engine.run(engine.knowledge_graph)
            engine.knowledge_graph.flush()
            hyp = result.get('hypotheses', {})
            engine.avatar.set_state(AvatarState.THINKING,
                f"小零: 推理完毕! {result['new_edges']}条关系 + {hyp.get('count', 0)}条假设~")
            msg = (
                f"小零: 全深度推理完成! {'[GPU加速]' if engine.gpu.is_gpu else '[CPU]'}\n"
                f"🔗 新推断: {result['new_edges']} 条 (累计{result['total_inferred']})\n"
                f"  传递: {result['methods']['transitive']} | "
                f"对称: {result['methods']['inverse']} | "
                f"因果: {result['methods']['causal']}\n"
                f"  跨域: {result['methods']['cross_domain']} | "
                f"共现: {result['methods']['co_occurrence']}\n"
                f"💡 假设: {hyp.get('count', 0)} 条待验证"
            )
            if hyp.get('top'):
                msg += "\n  待验证假设:"
                # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
                for h in hyp['top'][:3]:
                    msg += f"\n  · {h['source']} {h['relation']} {h['target']} (置信度:{h['score']:.2f})"
            return CommandResult(True, msg, result)
        except Exception as e:
            return CommandResult(False, f"小零: 推理遇到问题... {str(e)[:40]}")

    def _cmd_cleanup(self, context: dict = None) -> CommandResult:
        from avatar import AvatarState
        engine = self._engine
        if not hasattr(engine, 'memory_cleanup'):
            return CommandResult(False, "小零: 记忆清理模块尚未初始化~")

        engine.avatar.set_state(AvatarState.THINKING, "小零: 正在整理知识图谱，去重合并修剪...")
        try:
            result = engine.memory_cleanup.run(engine.knowledge_graph, engine.long_term)
            engine.avatar.set_state(AvatarState.THINKING,
                f"小零: 清理完毕! 精简{result['total_removed']}个节点~")
            return CommandResult(True,
                f"小零: 记忆清理完成!\n"
                f"  清理前: {result['before']['nodes']}N/{result['before']['edges']}E\n"
                f"  清理后: {result['after']['nodes']}N/{result['after']['edges']}E\n"
                f"  去重: {result['actions']['deduplicated']} | "
                f"修剪: {result['actions']['pruned']} | "
                f"合并: {result['actions']['merged']}",
                result)
        except Exception as e:
            return CommandResult(False, f"小零: 清理遇到问题... {str(e)[:40]}")

    def _cmd_goal(self, context: dict = None) -> CommandResult:
        from avatar import AvatarState
        engine = self._engine
        if not hasattr(engine, 'goal_system'):
            return CommandResult(False, "小零: 目标系统尚未初始化~")

        engine.avatar.set_state(AvatarState.THINKING, "小零: 查看学习目标...")
        try:
            stats = engine.goal_system.get_stats()
            active = engine.goal_system.get_active()
            next_goal = engine.goal_system.get_next()
            lines = [
                "━━━ 小零学习目标 ━━━",
                f"📋 总计: {stats['total']} | 待执行: {stats['pending']} | 进行中: {stats['active']} | 已完成: {stats['done']}",
            ]
            if active:
                lines.append("🔄 进行中:")
                # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
                for g in active:
                    lines.append(f"   [{g.category}] {g.topic[:50]}")
            if next_goal and next_goal not in active:
                lines.append(f"⏭️ 下一个: [{next_goal.category}] {next_goal.topic[:50]} (优先级:{next_goal.priority:.2f})")
            if not active and not next_goal:
                lines.append("💡 暂无目标，系统会自动从知识空白区生成~")

            engine.avatar.set_state(AvatarState.THINKING, f"小零: 目标{stats['total']}个~")
            return CommandResult(True, "\n".join(lines), stats)
        except Exception as e:
            return CommandResult(False, f"小零: 查询目标遇到问题... {str(e)[:40]}")


    # ═══════════════════════════════════════
    # 知识输出命令
    # ═══════════════════════════════════════

    def _cmd_quality(self, context: dict = None) -> CommandResult:
        from avatar import AvatarState
        engine = self._engine
        if not hasattr(engine, 'knowledge_quality'):
            return CommandResult(False, "小零: 知识质量模块尚未初始化~")

        engine.avatar.set_state(AvatarState.THINKING, "小零: 正在检查知识质量...")
        try:
            result = engine.knowledge_quality.run(engine.knowledge_graph)
            q = result["quality"]
            msg = (
                f"小零: 知识质量检查完成!\n"
                f"📊 整体质量: {q['overall_quality']:.0%}\n"
                f"📦 节点总数: {q['node_count']}\n"
                f"⭐ 高质量: {q['high_quality_nodes']} | ⚠️ 低质量: {q['low_quality_nodes']}\n"
                f"🔀 矛盾: {q['contradictions']} 处 | 重复: {result['duplicates_found']} 组\n"
                f"📈 分布: 优{q['quality_distribution']['excellent']} "
                f"良{q['quality_distribution']['good']} "
                f"中{q['quality_distribution']['fair']} "
                f"差{q['quality_distribution']['poor']}"
            )
            if q.get("contradiction_details"):
                msg += "\n⚠️ 矛盾详情:"
                # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
                for c in q["contradiction_details"][:3]:
                    msg += f"\n  · {c['description'][:80]}"
            engine.avatar.set_state(AvatarState.THINKING,
                f"小零: 知识质量{q['overall_quality']:.0%}~")
            return CommandResult(True, msg, result)
        except Exception as e:
            return CommandResult(False, f"小零: 质量检查遇到问题... {str(e)[:40]}")

    def _cmd_report(self, context: dict = None) -> CommandResult:
        from avatar import AvatarState
        engine = self._engine
        if not hasattr(engine, 'knowledge_output'):
            return CommandResult(False, "小零: 报告模块尚未初始化~")

        engine.avatar.set_state(AvatarState.REFLECTING, "小零: 正在生成日报...")
        try:
            insights = engine.knowledge_output.extract_insights(engine.knowledge_graph)
            stats = engine.status_snapshot()
            report = engine.knowledge_output.generate_daily_report(stats, insights, engine.knowledge_graph)
            engine.avatar.set_state(AvatarState.THINKING, "小零: 日报已生成!")
            return CommandResult(True, report["text"], {"file": report["file"]})
        except Exception as e:
            return CommandResult(False, f"小零: 生成报告遇到问题... {str(e)[:40]}")

    def _cmd_ask(self, context: dict = None) -> CommandResult:
        from avatar import AvatarState
        engine = self._engine
        if not hasattr(engine, 'knowledge_output'):
            return CommandResult(False, "小零: 问答模块尚未初始化~")

        question = context.get("raw_text", "") if context else ""
        if not question:
            return CommandResult(False, "小零: 你想问什么呢？试试「小零，什么是量子计算？」")

        # 去掉命令触发词
        # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
        for trigger in ["什么是", "解释", "介绍一下", "告诉我", "问答"]:
            if question.startswith(trigger):
                question = question[len(trigger):].strip()
                break

        if not question:
            return CommandResult(False, "小零: 请在你的问题中包含具体主题~ 例如「小零，什么是人工智能？」")

        engine.avatar.set_state(AvatarState.THINKING, f"小零: 正在{'用LLM思考' if getattr(engine, 'ollama', None) and engine.ollama.is_available() else '查找'}「{question[:30]}...」")
        try:
            result = engine.ask_question(question)
            method = result.get("method", "graph_search")
            engine.avatar.set_state(AvatarState.THINKING, "小零: 回答完毕!")
            if result.get("answer"):
                suffix = f"\n(方式:{method} 置信度:{result['confidence']:.0%})"
                return CommandResult(
                    result["confidence"] >= 0.3,
                    f"小零: {result['answer']}{suffix}",
                    result,
                )
            return CommandResult(False, f"小零: 无法回答「{question[:40]}」，知识图谱中暂无相关信息。需要我去学习吗？")
        except Exception as e:
            return CommandResult(False, f"小零: 问答遇到问题... {str(e)[:40]}")


    # ═══════════════════════════════════════
    # 备份 & 离线模式 & 多模态命令
    # ═══════════════════════════════════════

    def _cmd_backup(self, context: dict = None) -> CommandResult:
        from avatar import AvatarState
        engine = self._engine
        if not hasattr(engine, 'backup_mgr'):
            return CommandResult(False, "小零: 备份模块尚未初始化~")

        raw = context.get("raw_text", "") if context else ""
        engine.avatar.set_state(AvatarState.THINKING, "小零: 正在管理系统备份...")

        try:
            if "恢复" in raw or "还原" in raw:
                # 恢复备份
                backups = engine.backup_mgr.list_backups()
                if not backups:
                    return CommandResult(False, "小零: 没有可用的备份文件~")
                result = engine.backup_mgr.restore_backup()
                if result["success"]:
                    engine.avatar.set_state(AvatarState.THINKING, "小零: 备份恢复成功!")
                    return CommandResult(True,
                        f"小零: 备份恢复成功!\n"
                        f"📦 恢复自: {result['backup']}\n"
                        f"📄 恢复文件: {len(result['files_restored'])} 个\n"
                        f"💡 请重启引擎以加载恢复的状态~",
                        result)
                return CommandResult(False, f"小零: 恢复失败... {result.get('errors', [])}")

            elif "列表" in raw:
                # 列出备份
                backups = engine.backup_mgr.list_backups()
                if not backups:
                    return CommandResult(True, "小零: 暂无备份存档。说「小零，创建备份」来创建第一个备份~")
                lines = ["━━━ 备份存档列表 ━━━"]
                # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
                for i, b in enumerate(backups[:10], 1):
                    lines.append(f"  {i}. [{b['timestamp']}] {b['label']} ({b['size_kb']}KB)")
                lines.append(f"\n共 {len(backups)} 个备份")
                return CommandResult(True, "\n".join(lines), {"backups": backups})

            else:
                # 创建备份
                engine.avatar.set_state(AvatarState.UPGRADING, "小零: 创建全量备份中...")
                result = engine.backup_mgr.create_backup(label=f"manual_{engine.autonomous_cycles}")
                if result["success"]:
                    engine.avatar.set_state(AvatarState.THINKING, "小零: 备份完成!")
                    return CommandResult(True,
                        f"小零: 备份创建成功!\n"
                        f"📦 名称: {result['name']}\n"
                        f"📏 大小: {result.get('size_kb', 0)} KB\n"
                        f"📄 文件: {len(result['files_backed_up'])} 个",
                        result)
                return CommandResult(False, f"小零: 备份失败... {result.get('errors', [])}")
        except Exception as e:
            return CommandResult(False, f"小零: 备份操作异常... {str(e)[:40]}")

    def _cmd_offline(self, context: dict = None) -> CommandResult:
        from avatar import AvatarState
        engine = self._engine
        if not hasattr(engine, 'backup_mgr'):
            return CommandResult(False, "小零: 离线模式模块尚未初始化~")

        raw = context.get("raw_text", "") if context else ""
        try:
            if "在线" in raw or "联网" in raw:
                engine.backup_mgr.disable_offline_mode()
                engine.avatar.set_state(AvatarState.THINKING, "小零: 已切换到在线模式!")
                return CommandResult(True, "小零: 已切换到在线模式~ 网络功能已恢复!\n我可以联网搜索和学习新知识了~")
            else:
                engine.backup_mgr.enable_offline_mode()
                engine.avatar.set_state(AvatarState.THINKING, "小零: 离线模式已激活!")
                return CommandResult(True,
                    "小零: 离线模式已激活!\n"
                    "📴 网络请求已全部阻止\n"
                    "💾 仅使用本地缓存和已学知识\n"
                    "🛡️ 根法则依然生效\n"
                    "说「小零，在线模式」可恢复联网~")
        except Exception as e:
            return CommandResult(False, f"小零: 离线模式切换异常... {str(e)[:40]}")

    def _cmd_multimodal(self, context: dict = None) -> CommandResult:
        from avatar import AvatarState
        engine = self._engine
        if not hasattr(engine, 'multimodal'):
            return CommandResult(False, "小零: 多模态模块尚未初始化~")

        engine.avatar.set_state(AvatarState.SEARCHING, "小零: 扫描并处理文件...")
        try:
            # 触发多模态处理
            engine._phase_multimodal_processing()
            stats = engine.multimodal.get_stats()
            engine.avatar.set_state(AvatarState.THINKING, "小零: 多模态处理完毕!")
            return CommandResult(True,
                f"小零: 多模态处理完成!\n"
                f"📄 PDF提取: {stats.get('pdf_extracted', 0)} 份\n"
                f"🖼️ 图片处理: {stats.get('images_processed', 0)} 张\n"
                f"📝 文本提取: {stats.get('text_extracted', 0)} 次\n"
                f"⚠️ 错误: {stats.get('errors', 0)} 次\n"
                f"💡 将PDF/图片放入 data 目录即可自动处理~",
                stats)
        except Exception as e:
            return CommandResult(False, f"小零: 多模态处理异常... {str(e)[:40]}")


    # ═══════════════════════════════════════
    # 新增优化命令
    # ═══════════════════════════════════════

    def _cmd_table_extract(self, context: dict = None) -> CommandResult:
        from avatar import AvatarState
        engine = self._engine
        if not hasattr(engine, 'multimodal'):
            return CommandResult(False, "小零: 多模态模块尚未初始化~")

        raw = context.get("raw_text", "") if context else ""
        # 检查是否有指定文件，否则扫描 data 目录
        data_dir = engine.data_dir
        pdf_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir)
                     if f.lower().endswith('.pdf') and os.path.isfile(os.path.join(data_dir, f))]

        if not pdf_files:
            return CommandResult(False, "小零: data 目录中未找到PDF文件~ 请将PDF放入data目录。")

        engine.avatar.set_state(AvatarState.ANALYZING, f"小零: 提取表格中({len(pdf_files)}个文件)...")
        try:
            total_tables = 0
            results = []
            # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
            for pdf_path in pdf_files[:3]:
                result = engine.multimodal.extract_tables_from_pdf(pdf_path)
                if result.get("success"):
                    # [ZERO-PERF] 大量字符串拼接建议改用list+join模式
                    total_tables += result["table_count"]
                    results.append(f"  {os.path.basename(pdf_path)}: {result['table_count']}个表格")

            if total_tables > 0:
                engine.avatar.set_state(AvatarState.THINKING, f"小零: 提取到{total_tables}个表格!")
                return CommandResult(True,
                    f"小零: 表格提取完成!\n"
                    f"📊 总计: {total_tables} 个表格\n" +
                    "\n".join(results) +
                    f"\n💡 表格已存入长期记忆，可通过问答查询~",
                    {"total_tables": total_tables})
            return CommandResult(False, "小零: 未提取到表格~ PDF可能为扫描件或不含表格。")
        except Exception as e:
            return CommandResult(False, f"小零: 表格提取异常... {str(e)[:40]}")

    def _cmd_transcribe(self, context: dict = None) -> CommandResult:
        from avatar import AvatarState
        engine = self._engine
        if not hasattr(engine, 'multimodal'):
            return CommandResult(False, "小零: 多模态模块尚未初始化~")

        data_dir = engine.data_dir
        audio_exts = {'.wav', '.mp3', '.flac', '.ogg', '.m4a', '.wma', '.aac'}
        audio_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir)
                       if os.path.splitext(f)[1].lower() in audio_exts
                       and os.path.isfile(os.path.join(data_dir, f))]

        if not audio_files:
            return CommandResult(False, "小零: data 目录中未找到音频文件~ 支持: wav/mp3/flac/ogg/m4a")

        engine.avatar.set_state(AvatarState.LEARNING, "小零: 正在转录音频...")
        try:
            result = engine.multimodal.transcribe_audio(audio_files[0])
            if result.get("success"):
                text = result.get("text", "")
                engine.avatar.set_state(AvatarState.THINKING, "小零: 转录完成!")
                return CommandResult(True,
                    f"小零: 音频转录完成! ({result['method']})\n"
                    f"🎙️ 文件: {os.path.basename(audio_files[0])}\n"
                    f"📝 文本({len(text)}字): {text[:300]}...",
                    result)
            return CommandResult(False, f"小零: 转录失败... {result.get('error', 'whisper/speech_recognition未安装')}")
        except Exception as e:
            return CommandResult(False, f"小零: 转录异常... {str(e)[:40]}")

    def _cmd_model_switch(self, context: dict = None) -> CommandResult:
        from avatar import AvatarState
        engine = self._engine
        if not hasattr(engine, 'ollama'):
            return CommandResult(False, "小零: LLM模块尚未初始化~")
        if not engine.ollama.is_available():
            return CommandResult(False, "小零: Ollama服务不可用~ 无法切换模型。")

        raw = context.get("raw_text", "") if context else ""
        available = engine.ollama.available_models

        # 从输入中提取模型名
        model_requested = None
        # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
        for model in available:
            if model in raw:
                model_requested = model
                break
        # 常见模型名匹配
        # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
        for hint in ["llama", "mistral", "gemma", "qwen", "codellama", "deepseek"]:
            if hint in raw.lower() and not model_requested:
                # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
                for m in available:
                    if hint in m.lower():
                        model_requested = m
                        break

        if not model_requested:
            return CommandResult(True,
                f"小零: 当前模型: {engine.ollama.model}\n"
                f"可用模型: {', '.join(available[:8])}\n"
                f"💡 说「小零，切换模型 llama3」来切换指定模型~")

        old_model = engine.ollama.model
        if engine.ollama.switch_model(model_requested):
            engine.avatar.set_state(AvatarState.UPGRADING, f"小零: 切换到{engine.ollama.model}!")
            return CommandResult(True,
                f"小零: 模型切换成功!\n"
                f"  从「{old_model}」→「{engine.ollama.model}」\n"
                f"💡 后续推理/问答将使用新模型~")
        return CommandResult(False, f"小零: 无法切换到「{model_requested}」, 可用: {', '.join(available[:5])}")

    def _cmd_cache_clear(self, context: dict = None) -> CommandResult:
        from avatar import AvatarState
        engine = self._engine
        if not hasattr(engine, 'ollama'):
            return CommandResult(False, "小零: LLM模块尚未初始化~")

        before = len(engine.ollama._cache) if hasattr(engine.ollama, '_cache') else 0
        engine.ollama.clear_cache()
        stats = engine.ollama.get_stats()
        engine.avatar.set_state(AvatarState.THINKING, "小零: LLM缓存已清空!")
        return CommandResult(True,
            f"小零: LLM缓存已清空!\n"
            f"  清理前: {before} 条缓存\n"
            f"  缓存命中: {stats.get('cache_hits', 0)} 次 (累计)\n"
            f"  下次查询将重新生成响应~")

    def _cmd_upgrade_plan(self, context: dict = None) -> CommandResult:
        from avatar import AvatarState
        engine = self._engine
        if not hasattr(engine, 'upgrade_planner'):
            return CommandResult(False, "小零: 升级规划模块尚未初始化~")

        engine.avatar.set_state(AvatarState.THINKING, "小零: 分析系统状态，生成升级路线图...")
        try:
            metrics = engine.status_snapshot()
            roadmap = engine.upgrade_planner.generate_roadmap(metrics)
            proposals = roadmap.get("proposals", [])
            lines = [
                "━━━ 升级路线图 ━━━",
                f"📊 基于 {len(roadmap.get('metrics_snapshot', {}))} 项系统指标分析",
                f"💡 {len(proposals)} 条升级建议:",
            ]
            # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
            for i, p in enumerate(proposals[:8], 1):
                cat = {"knowledge": "🧠", "quality": "📊", "reasoning": "🔗",
                       "llm": "🤖", "performance": "⚡", "stability": "🛡️"}.get(p["category"], "📌")
                lines.append(f"  {i}. {cat} [{p['category']}] {p['title']} (优先级{p['priority']:.0%})")
                lines.append(f"     {p['reason'][:60]}")

            if not proposals:
                lines.append("  ✅ 系统状态良好，暂无紧急升级建议~")

            engine.avatar.set_state(AvatarState.THINKING, "小零: 路线图生成完毕!")
            return CommandResult(True, "\n".join(lines), roadmap)
        except Exception as e:
            return CommandResult(False, f"小零: 升级规划异常... {str(e)[:40]}")

    def _cmd_health(self, context: dict = None) -> CommandResult:
        from avatar import AvatarState
        engine = self._engine
        if not hasattr(engine, 'stability'):
            return CommandResult(False, "小零: 稳定性模块尚未初始化~")

        engine.avatar.set_state(AvatarState.ANALYZING, "小零: 系统健康检查中...")
        try:
            modules = {
                "graph": engine.knowledge_graph,
                "ollama": engine.ollama,
                "gpu": engine.gpu,
                "backup": engine.backup_mgr,
                "data_dir": engine.data_dir,
            }
            health = engine.stability.health.run(modules)
            mem = engine.stability.memory.check()
            gc_stats = engine.stability.gc.get_stats()

            emoji = {"healthy": "✅", "degraded": "⚠️", "unhealthy": "❌"}
            lines = [
                f"━━━ 系统健康诊断 ━━━",
                f"{emoji.get(health['overall'], '❓')} 总体: {health['overall']}",
                f"🧠 图谱: {health['checks'].get('graph', {}).get('node_count', '-')}节点 "
                f"{'✓' if health['checks'].get('graph', {}).get('status') == 'ok' else '✗'}",
                f"🤖 LLM: {'可用(' + health['checks'].get('llm', {}).get('model', '-') + ')' if health['checks'].get('llm', {}).get('available') else '不可用'}",
                f"🚀 GPU: {health['checks'].get('gpu', {}).get('device', '-')}",
                f"💿 备份: {health['checks'].get('backup', {}).get('backup_count', 0)}个",
                f"💾 内存: {mem['usage_mb']:.0f}MB [{mem['status']}]",
                f"🗑️ GC: {gc_stats.get('gc_runs', 0)}次 (回收{gc_stats.get('objects_collected', 0)}对象)",
                f"📁 数据: {'✓' if health['checks'].get('data_files', {}).get('status') == 'ok' else '✗ 缺少文件'}",
            ]
            if health["failing"]:
                lines.append(f"❌ 故障模块: {', '.join(health['failing'])}")
            if health["warnings"]:
                lines.append(f"⚠️ 警告: {', '.join(health['warnings'])}")

            engine.avatar.set_state(AvatarState.THINKING, "小零: 健康检查完毕!")
            return CommandResult(True, "\n".join(lines), health)
        except Exception as e:
            return CommandResult(False, f"小零: 健康检查异常... {str(e)[:40]}")

    def _cmd_theme(self, context: dict = None) -> CommandResult:
        from avatar import AvatarState
        engine = self._engine
        raw = context.get("raw_text", "") if context else ""

        # 主题状态存储在引擎上
        if not hasattr(engine, '_theme'):
            engine._theme = "light"

        is_dark = "深色" in raw or "暗黑" in raw or "dark" in raw.lower() or "夜间" in raw
        is_light = "浅色" in raw or "亮色" in raw or "light" in raw.lower()

        if is_dark and engine._theme != "dark":
            engine._theme = "dark"
        elif is_light and engine._theme != "light":
            engine._theme = "light"
        elif not is_dark and not is_light:
            engine._theme = "dark" if engine._theme == "light" else "light"
        new_theme = engine._theme

        theme_names = {"dark": "深色模式(暗黑)", "light": "浅色模式(亮白)"}
        engine.avatar.set_state(AvatarState.UPGRADING, f"小零: 切换到{theme_names[new_theme]}!")

        if hasattr(engine, 'desktop_bar') and engine.desktop_bar:
            try:
                engine.desktop_bar.apply_theme(new_theme)
            except Exception:
                pass

        return CommandResult(True,
            f"小零: 主题已切换!\n"
            f"🎨 当前: {theme_names[new_theme]}\n"
            f"📱 头像和界面已更新~")

    def _cmd_voice(self, context: dict = None) -> CommandResult:
        engine = self._engine
        raw = context.get("raw_text", "") if context else ""

        # 语音命令模式：用户说出的文本已由外部语音识别引擎转换成 raw_text
        # 这里提供一个明确的语音交互入口
        # 去掉"语音输入"等触发词后，剩余文本作为实际命令
        # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
        for trigger in ["语音输入", "语音", "说话", "听我说"]:
            if raw.startswith(trigger):
                raw = raw[len(trigger):].strip()
                break

        if not raw:
            return CommandResult(True,
                "小零: 语音输入模式已激活!\n"
                "🎤 请说出你的指令。例如「小零，语音输入，状态」\n"
                "💡 将语音转文字后放入指令中即可~")

        # 将语音文本作为命令重新解析执行
        from avatar import AvatarState
        engine.avatar.set_state(AvatarState.CURIOUS, "小零: 听到你说的了! 正在理解...")

        # 使用当前的完整输入文本重新解析
        cmd = self.parse(raw)
        if cmd:
            return self.execute(cmd, {"raw_text": raw})
        return CommandResult(False,
            f"小零: 听到了「{raw[:50]}」，但没能理解你想做什么...\n"
            f"💡 试试「语音输入，状态」或「语音输入，学习」~")


    # ═══════════════════════════════════════
    # 自代码修改命令
    # ═══════════════════════════════════════

    def _cmd_code_mod(self, context: dict = None) -> CommandResult:
        """运行代码分析+修改周期"""
        from avatar import AvatarState
        engine = self._engine
        if not hasattr(engine, 'code_mod'):
            return CommandResult(False, "小零: 代码修改模块尚未初始化~")

        engine.avatar.set_state(AvatarState.ANALYZING, "小零: 扫描自身代码结构...")
        try:
            result = engine.code_mod.run(max_changes=1, dry_run=False)
            conclusion = result.get("conclusion", {})
            detect = result.get("phases", {}).get("detect", {})
            msg = (
                "━━━ 自代码修改报告 ━━━\n"
                f"📊 扫描: {result.get('phases', {}).get('scan', {}).get('files_scanned', 0)}个文件 "
                f"({result.get('phases', {}).get('scan', {}).get('nodes', 0)}节点/"
                f"{result.get('phases', {}).get('scan', {}).get('edges', 0)}边)\n"
                f"🔍 发现问题: {detect.get('issues_found', 0)}处\n"
                f"✅ 已应用: {conclusion.get('applied', 0)}处\n"
                f"🔄 已回滚: {conclusion.get('rolled_back', 0)}处\n"
                f"⏳ 等待审批: {conclusion.get('pending_approvals', 0)}处"
            )
            top = detect.get("top_issues", [])[:3]
            if top:
                msg += "\n📌 Top issues:"
                # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
                for i, iss in enumerate(top, 1):
                    msg += f"\n  {i}. [{iss['issue_type']}] {iss.get('function', '?')} @ {iss['file']}: {iss['description'][:50]}"
            engine.avatar.set_state(AvatarState.THINKING, "小零: 代码分析完成!")
            return CommandResult(True, msg, result)
        except Exception as e:
            return CommandResult(False, f"小零: 代码修改异常... {str(e)[:40]}")

    def _cmd_code_mod_status(self, context: dict = None) -> CommandResult:
        """显示代码修改统计和待审批列表"""
        engine = self._engine
        if not hasattr(engine, 'code_mod'):
            return CommandResult(False, "小零: 代码修改模块尚未初始化~")

        stats = engine.code_mod.stats
        pending = engine.code_mod.gate.get_pending()
        msg = (
            "━━━ 自代码修改状态 ━━━\n"
            f"📊 扫描: {stats.get('scans', 0)}次\n"
            f"🔍 发现问题: {stats.get('issues_found', 0)}处\n"
            f"💡 提议修改: {stats.get('changes_proposed', 0)}处\n"
            f"✅ 已应用: {stats.get('changes_applied', 0)}处\n"
            f"🔄 已回滚: {stats.get('changes_rolled_back', 0)}处\n"
            f"✔️ 校验通过: {stats.get('validations_passed', 0)}次\n"
            f"❌ 校验失败: {stats.get('validations_failed', 0)}次\n"
            f"⏳ 待审批: {len(pending)}处"
        )
        # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
        for p in pending[:3]:
            msg += (
                f"\n  · [{p['risk']['level']}] "
                f"{p['issue'].get('file', '?')}: "
                f"{p['issue'].get('issue_type', '?')}"
            )
        return CommandResult(True, msg, stats)

    def _cmd_code_mod_approve(self, context: dict = None) -> CommandResult:
        """批准待审批的代码变更"""
        engine = self._engine
        if not hasattr(engine, 'code_mod'):
            return CommandResult(False, "小零: 代码修改模块尚未初始化~")

        pending = engine.code_mod.gate.get_pending()
        if not pending:
            return CommandResult(True, "小零: 没有待审批的修改~")

        from avatar import AvatarState
        engine.avatar.set_state(AvatarState.UPGRADING, "小零: 应用已批准的代码修改...")
        try:
            # 批准第一个待审批项并尝试应用
            item = pending[0]
            pid = item.get("id", "")
            file_path = item["issue"].get("file", "")
            abs_path = os.path.join(engine.code_mod.project_root, file_path)

            # Read original
            with open(abs_path, 'r', encoding='utf-8') as f:
                original_code = f.read()

            # Backup
            backup = engine.code_mod.rollback.backup_files(
                [file_path], f"manual_approval_{item['issue'].get('issue_type', 'fix')}",
            )

            # Generate fresh improvement
            gen = engine.code_mod.generator.generate_improvement(
                item["issue"], original_code,
                {'affected': engine.code_mod.analyzer.get_affected_components(
                    file_path, item["issue"].get("function", ""),
                )},
            )

            if not gen.get("diff_text"):
                engine.code_mod.gate.approve(pid)
                return CommandResult(False, "小零: 无法生成有效的代码变更...")

            # Validate
            new_code = engine.code_mod._apply_diff_to_text(original_code, gen["diff_text"])
            if new_code is None:
                return CommandResult(False, "小零: diff应用失败...")

            validation = engine.code_mod.validator.validate(
                original_code, new_code, file_path,
                gen.get("explanation", "Manual approval"),
            )
            if not validation.get("passed", False):
                return CommandResult(False,
                    f"小零: 校验未通过 (layer {validation.get('layer')}): "
                    f"{validation.get('errors', ['unknown'])[:1]}")

            # Apply
            with open(abs_path, 'w', encoding='utf-8') as f:
                f.write(new_code)

            # Verify
            with open(abs_path, 'r', encoding='utf-8') as f:
                ast.parse(f.read())

            engine.code_mod.gate.approve(pid)
            engine.code_mod.stats["changes_applied"] += 1
            engine.code_mod.stats["validations_passed"] += 1
            engine.code_mod._save_state()

            engine.avatar.set_state(AvatarState.THINKING, "小零: 代码修改已应用!")
            return CommandResult(True,
                f"小零: 已批准并应用修改!\n"
                f"📁 文件: {file_path}\n"
                f"📝 类型: {item['issue'].get('issue_type')}\n"
                f"💡 {gen.get('explanation', '')[:100]}")
        except Exception as e:
            return CommandResult(False, f"小零: 应用修改失败... {str(e)[:40]}")

    def _cmd_code_mod_reject(self, context: dict = None) -> CommandResult:
        """拒绝待审批的代码变更"""
        engine = self._engine
        if not hasattr(engine, 'code_mod'):
            return CommandResult(False, "小零: 代码修改模块尚未初始化~")

        pending = engine.code_mod.gate.get_pending()
        if not pending:
            return CommandResult(True, "小零: 没有待审批的修改~")

        pid = pending[0].get("id", "")
        info = pending[0]
        engine.code_mod.gate.reject(pid)
        return CommandResult(True,
            f"小零: 已拒绝修改~\n"
            f"📁 {info['issue'].get('file', '?')}: "
            f"{info['issue'].get('issue_type', '?')}")


    # ═══════════════════════════════════════
    # 试运行命令
    # ═══════════════════════════════════════

    def _cmd_trial_start(self, context: dict = None) -> CommandResult:
        """启动代码修改试运行模式"""
        from avatar import AvatarState
        engine = self._engine
        if not hasattr(engine, 'code_mod'):
            return CommandResult(False, "小零: 代码修改模块尚未初始化~")

        if engine.code_mod.trial_mode:
            elapsed = engine.code_mod.get_trial_elapsed_hours()
            remaining = max(0, engine.code_mod.trial_duration_hours - elapsed)
            return CommandResult(True,
                f"小零: 试运行已在运行中~\n"
                f"已运行: {elapsed:.1f}h / {engine.code_mod.trial_duration_hours:.0f}h\n"
                f"剩余: {remaining:.1f}h\n"
                f"允许风险: {', '.join(sorted(engine.code_mod.trial_allowed_risk))}")

        engine.avatar.set_state(AvatarState.UPGRADING, "小零: 启动代码修改试运行模式...")
        try:
            engine.code_mod.start_trial(duration_hours=72.0, allowed_risk={'low'})
            engine.avatar.set_state(AvatarState.THINKING, "小零: 试运行已启动!")
            return CommandResult(True,
                "━━━ 代码修改试运行已启动 ━━━\n"
                "⏱️ 时长: 72 小时\n"
                "🛡️ 模式: Dry-Run Only (不实际修改代码)\n"
                "✅ 允许风险等级: LOW 仅允许低风险变更通过\n"
                "🚫 阻止等级: MEDIUM / HIGH / CRITICAL 全部阻止\n"
                "📊 每日报告: data/code_mod_reports/YYYY-MM-DD.md\n"
                "📋 最终总结: 72小时后自动生成\n"
                "🔄 执行频率: 每11个自主循环\n"
                "\n💡 使用「试运行状态」查看进度\n"
                "💡 使用「试运行报告」查看最新报告")
        except Exception as e:
            return CommandResult(False, f"小零: 启动试运行失败... {str(e)[:40]}")

    def _cmd_trial_status(self, context: dict = None) -> CommandResult:
        """查看试运行状态"""
        engine = self._engine
        if not hasattr(engine, 'code_mod'):
            return CommandResult(False, "小零: 代码修改模块尚未初始化~")

        cm = engine.code_mod
        if not cm.trial_mode:
            return CommandResult(True,
                "小零: 试运行未启动~\n"
                "💡 使用「试运行启动」开始72小时代码修改试运行")

        elapsed = cm.get_trial_elapsed_hours()
        remaining = max(0, cm.trial_duration_hours - elapsed)
        status = cm.get_status()
        expired = cm.is_trial_expired()

        msg = [
            "━━━ 代码修改试运行状态 ━━━",
            f"状态: {'已到期(等待生成总结)' if expired else '运行中'}",
            f"已运行: {elapsed:.1f}h / {cm.trial_duration_hours:.0f}h",
            f"剩余: {remaining:.1f}h",
            f"允许风险等级: {', '.join(sorted(cm.trial_allowed_risk))}",
            f"模式: Dry-Run Only",
            "",
            f"📊 累计统计:",
            f"  扫描: {cm.stats['scans']} 次",
            f"  发现问题: {cm.stats['issues_found']} 个",
            f"  提议修改: {cm.stats['changes_proposed']} 个",
            f"  已应用: {cm.stats['changes_applied']} 个 (试运行应为0)",
            f"  回滚: {cm.stats['changes_rolled_back']} 个",
            f"  校验通过: {cm.stats['validations_passed']} 次",
            f"  校验失败: {cm.stats['validations_failed']} 次",
            f"  活动日志: {status['step_log_count']} 条",
        ]

        # Recent activity
        recent = cm._step_log[-5:]
        if recent:
            msg.append("")
            msg.append("📌 最近活动:")
            # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
            for entry in reversed(recent):
                ts = entry.get('timestamp', '')[-8:]
                phase = entry.get('phase', '?')
                risk = entry.get('risk_level', '-')
                detail = entry.get('detail', {})
                brief = ''
                if isinstance(detail, dict):
                    if 'file' in detail:
                        brief = f" {detail['file']}"
                    elif 'issues_found' in detail:
                        brief = f" {detail['issues_found']}个问题"
                    elif 'report_path' in detail:
                        brief = f" 报告已生成"
                msg.append(f"  [{ts}] {phase}{brief} [{risk}]")

        return CommandResult(True, "\n".join(msg), status)

    def _cmd_trial_report(self, context: dict = None) -> CommandResult:
        """查看或生成试运行报告"""
        from avatar import AvatarState
        engine = self._engine
        if not hasattr(engine, 'code_mod'):
            return CommandResult(False, "小零: 代码修改模块尚未初始化~")

        cm = engine.code_mod
        if not cm.trial_mode:
            # Check for existing reports
            if os.path.isdir(cm._report_dir):
                reports = sorted([
                    f for f in os.listdir(cm._report_dir)
                    if f.endswith('.md')
                ], reverse=True)
                if reports:
                    lines = ["━━━ 已有报告 ━━━"]
                    # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
                    for r in reports[:5]:
                        rpath = os.path.join(cm._report_dir, r)
                        size_kb = os.path.getsize(rpath) / 1024 if os.path.exists(rpath) else 0
                        lines.append(f"  📄 {r} ({size_kb:.1f}KB)")
                    return CommandResult(True, "\n".join(lines))
                return CommandResult(True,
                    "小零: 暂无试运行报告~\n"
                    "💡 使用「试运行启动」开始72小时试运行")

        engine.avatar.set_state(AvatarState.THINKING, "小零: 生成试运行报告...")
        try:
            # Generate daily report
            daily_path = cm._generate_daily_report()
            msg = []

            if cm.is_trial_expired():
                # Generate final summary
                summary_path = cm.generate_trial_summary()
                msg.append(f"📋 最终总结报告: {summary_path}")
                cm.stop_trial()

            if daily_path:
                msg.append(f"📊 每日报告: {daily_path}")

            elapsed = cm.get_trial_elapsed_hours()
            msg.append(f"")
            msg.append(f"📈 试运行进度: {elapsed:.1f}h/{cm.trial_duration_hours:.0f}h")
            msg.append(f"🔍 扫描: {cm.stats['scans']}次 | 问题: {cm.stats['issues_found']}个")
            msg.append(f"📝 活动日志: {len(cm._step_log)}条")

            engine.avatar.set_state(AvatarState.THINKING, "小零: 报告已生成!")
            return CommandResult(True, "\n".join(msg), cm.get_status())
        except Exception as e:
            return CommandResult(False, f"小零: 生成报告失败... {str(e)[:40]}")


# 全局单例
_router_instance: Optional[CommandRouter] = None


def get_router() -> CommandRouter:
    """
    get_router
    """
    global _router_instance
    if _router_instance is None:
        _router_instance = CommandRouter()
    return _router_instance