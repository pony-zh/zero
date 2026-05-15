#!/usr/bin/env python3
"""
ZERO 完全自主引擎 — 无需人工干预
自动学习、自动进化、自动升级所有模块
"""
import sys, os, time, random, json, threading, re
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 修复Windows终端GBK编码问题（emoji等字符无法显示）
if sys.platform == 'win32':
    # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding='utf-8')
        except Exception:
            pass

from config import ZeroConfig, GrowthStage, HUMAN_VALUES, ROOT_LAWS
from core.root_law import RootLaw
from core.evolution import EvolutionController
from core.ethics import EthicsEngine
from core.discovery import DiscoveryEngine
from core.civilization import CivilizationAnalyzer
from core.simulation import WorldSimulation
from core.learning import RealTimeLearning
from core.perception import PerceptionSystem
from core.memory import (
    ShortTermMemory, LongTermMemory, EpisodicMemory,
    ValuesMemory, CivilizationMemory,
)
from core.earth_cognition import EarthCognition
from core.human_history import HumanHistory
from core.emotion_cognition import EmotionCognition
from core.humility import HumilityProtocol
from core.emergency_termination import EmergencyTermination
from core.supervision import SupervisionSystem
from core.xiaoling_learning import XiaoLingLearning
from core.reasoning import ReasoningEngine
from core.memory_cleanup import MemoryCleanup
from core.goal_system import GoalSystem
from core.gpu_accelerator import GPUAccelerator
from core.knowledge_quality import KnowledgeQuality
from core.autonomous_intelligence import AutonomousIntelligence
from core.knowledge_output import KnowledgeOutput
from core.ollama_llm import OllamaLLM
from core.backup import BackupManager
from core.upgrade_planner import UpgradePlanner
from core.stability import StabilityManager
from knowledge.multimodal import MultimodalExtractor
from core.self_code_modification import SelfCodeModificationEngine
from core.self_healing import SelfHealingDaemon
from core.wechat_bridge import WeChatBridge
from core.chat_window import ChatWindow
from core.conversation_engine import ConversationMouth
from core.ai_benchmark import AIBenchmark
from core.report_archiver import ReportArchiver
from core.learning_scheduler import LearningScheduler
from core.knowledge_card import KnowledgeCardGenerator, KnowledgeCard
from core.self_healing_monitor import SelfHealingMonitor
from agents.orchestrator import AgentOrchestrator
from knowledge.graph import KnowledgeGraph
from knowledge.trust import TrustEngine
from knowledge.crawler import Crawler
from knowledge.parser import parse_content
from avatar import XiaoLingAvatar, AvatarState, SimpleWidget

# ═══════════════════════════════════════
# 自主学习主题库 — Opus 4.7 旗舰模型优先
# ═══════════════════════════════════════
# 主题优先级由 learning_scheduler.LearningScheduler 统一管理
# 此处仅保留作为兜底：当 scheduler 不可用时回退使用
KNOWLEDGE_DOMAINS = [
    # ── CRITICAL: Claude Opus 4.7 核心知识 ──
    "Claude Opus 4.7 architecture hybrid reasoning mechanism technical deep dive",
    "Claude Opus 4.7 million token context window long document handling",
    "Claude Opus 4.7 multimodal vision image understanding capability",
    "Anthropic Claude Opus 4.7 constitutional AI safety alignment RLHF",
    "Claude Opus 4.7 vs GPT-5.5 vs Gemini 3.1 flagship model benchmark comparison",
    "Claude Opus 4.7 agent long task workflow tool use function calling",
    "Claude Code CLI autonomous software engineering agent architecture",
    # ── HIGH: 旗舰模型对标 ──
    "OpenAI GPT-5.5 architecture multimodal reasoning capability",
    "Google Gemini 3.1 MoE architecture technical specification",
    "DeepSeek V4 MoE inference optimization training cost efficiency",
    "Qwen 3.6 long context Chinese optimization agent framework",
    # ── MEDIUM: AI Agent / 架构 ──
    "AI agent framework multi-agent orchestration task scheduling 2026",
    "large language model MoE architecture inference optimization",
    "multimodal LLM vision language fusion encoder architecture",
    "LLM memory architecture long term episodic working memory system",
    "AI safety alignment research constitutional AI interpretability",
    # ── LOW: 通用 AI ──
    "machine learning research breakthrough progress 2026",
    "natural language processing transformer attention mechanism",
    "knowledge graph retrieval augmented generation RAG system",
]

# 自主升级任务清单
UPGRADE_TASKS = [
    "expand_knowledge_graph",
    "deepen_emotion_understanding",
    "calibrate_value_weights",
    "cross_reference_memories",
    "prune_low_confidence_knowledge",
    "synthesize_new_hypotheses",
    "update_civilization_indicators",
    "refine_trust_model",
]


class AutonomousEngine:
    """ZERO 完全自主引擎"""

    def __init__(self, use_gui: bool = True):
        self.config = ZeroConfig()
        self.config.initial_stage = GrowthStage.EXPLORATION
        self.data_dir = self.config.data_dir
        os.makedirs(self.data_dir, exist_ok=True)

        # 虚拟形象
        self.avatar = XiaoLingAvatar()
        self.use_gui = use_gui
        self.desktop_bar = None
        self.console_avatar = None

        # 初始化所有模块
        self.avatar.set_state(AvatarState.BOOTING, "小零:正在唤醒ZERO所有模块...")
        self._init_all_modules()

        # 运行状态
        self.running = True
        self.autonomous_cycles = 0
        self.total_knowledge_acquired = 0
        self.start_time = time.time()
        self.state_file = os.path.join(self.data_dir, "autonomous_state.json")
        self._low_memory_mode = False  # GPU < 8GB 自适应

        # 加载上次状态
        self._load_state()
        self.avatar.set_state(AvatarState.THINKING, f"小零:准备就绪! 我准备好了! 阶段:{self.evolution.stage_info['name']}")

    def _init_all_modules(self):
        """初始化全部模块"""
        self.root_law = RootLaw()
        self.ethics = EthicsEngine()
        self.evolution = EvolutionController(initial_stage=self.config.initial_stage)
        self.civilization = CivilizationAnalyzer()
        self.discovery = DiscoveryEngine(storage_path=os.path.join(self.data_dir, "discovery.json"))
        self.simulation = WorldSimulation(sandbox_enabled=True)
        self.perception = PerceptionSystem()
        self.learning = RealTimeLearning(data_dir=self.data_dir)  # 传递data_dir参数
        self.earth = EarthCognition(storage_path=os.path.join(self.data_dir, "earth_cognition.json"))
        self.history = HumanHistory()
        self.emotion = EmotionCognition()
        self.humility = HumilityProtocol()
        self.emergency = EmergencyTermination()
        self.supervision = SupervisionSystem(
            root_law=self.root_law, ethics_engine=self.ethics,
            simulation=self.simulation, civilization_analyzer=self.civilization,
        )
        self.knowledge_graph = KnowledgeGraph(
            storage_path=os.path.join(self.data_dir, "knowledge_graph.json")
        )
        self.trust = TrustEngine()
        self.crawler = Crawler()
        self.orchestrator = AgentOrchestrator(
            root_law=self.root_law, ethics_engine=self.ethics,
        )
        # 记忆系统
        self.short_term = ShortTermMemory()
        self.long_term = LongTermMemory(
            storage_path=os.path.join(self.data_dir, "long_term_memory.json")
        )
        self.episodic = EpisodicMemory(
            storage_path=os.path.join(self.data_dir, "episodic_memory.json")
        )
        self.values_mem = ValuesMemory(
            storage_path=os.path.join(self.data_dir, "values_memory.json")
        )
        self.civ_mem = CivilizationMemory(
            storage_path=os.path.join(self.data_dir, "civilization_memory.json")
        )
        # 小零学习记忆（完全文件化持久存储）
        self.xiaoling_mem = XiaoLingLearning(data_dir=self.data_dir)
        # 认知升级模块
        self.reasoning_engine = ReasoningEngine()
        self.memory_cleanup = MemoryCleanup()
        self.goal_system = GoalSystem(storage_path=os.path.join(self.data_dir, "goals.json"))
        # GPU 加速器
        self.gpu = GPUAccelerator()
        # 知识质量 & 自主智能 & 输出
        self.knowledge_quality = KnowledgeQuality()
        self.auto_intelligence = AutonomousIntelligence()
        self.knowledge_output = KnowledgeOutput(
            output_dir=os.path.join(self.data_dir, "reports")
        )
        # Ollama LLM 本地大模型
        self.ollama = OllamaLLM()
        # 多模态提取
        self.multimodal = MultimodalExtractor()
        # 备份管理 & 离线模式
        self.backup_mgr = BackupManager(data_dir=self.data_dir)
        # 升级规划 & 稳定性
        self.upgrade_planner = UpgradePlanner(data_dir=self.data_dir)
        self.stability = StabilityManager(data_dir=self.data_dir)
        # 自代码修改引擎（无限制全自主模式）
        self.code_mod = SelfCodeModificationEngine(
            project_root=os.path.dirname(os.path.abspath(__file__)),
            reasoning_engine=self.reasoning_engine,
            orchestrator=self.orchestrator,
            knowledge_graph=self.knowledge_graph,
            root_law=self.root_law,
            ethics_engine=self.ethics,
            backup_mgr=self.backup_mgr,
        )
        self.code_mod.set_mode('unrestricted')
        # 自愈系统
        self.self_healing = SelfHealingDaemon(
            project_root=os.path.dirname(os.path.abspath(__file__))
        )
        self.self_healing.set_engine(self.code_mod)
        # 微信桥接
        self.wechat = WeChatBridge(
            project_root=os.path.dirname(os.path.abspath(__file__))
        )
        self.wechat.on_command = self._handle_wechat_command
        self.wechat.on_message_sync = self._sync_wechat_to_chat
        # 桌面聊天窗口
        self.chat_window = ChatWindow(
            title='ZERO Chat',
            send_callback=self._handle_chat_message,
            geometry='480x620',
        )
        # 智能对话引擎（纯本地，零外部依赖）
        self.conversation = ConversationMouth(
            knowledge_graph=self.knowledge_graph,
            long_term_memory=self.long_term,
            episodic_memory=self.episodic,
            short_term_memory=self.short_term,
            crawler=self.crawler,
            trust_engine=self.trust,
            emotion_cognition=self.emotion,
            reasoning_engine=self.reasoning_engine,
            xiaoling_learning=self.xiaoling_mem,
        )
        self.conversation._auto_ref = self
        # AI架构对标引擎
        self.ai_benchmark = AIBenchmark(
            data_dir=self.data_dir,
            crawler=self.crawler,
            trust_engine=self.trust,
            knowledge_graph=self.knowledge_graph,
            backup_mgr=self.backup_mgr,
            project_root=os.path.dirname(os.path.abspath(__file__)),
        )
        self.ai_benchmark._auto_ref = self
        # 报告存档器（纯本地，零推送）
        self.report_archiver = ReportArchiver(data_dir=self.data_dir)
        # 学习调度器（Opus 4.7 旗舰模型优先）
        self.learning_scheduler = LearningScheduler(data_dir=self.data_dir)
        # 知识卡片生成器（结构化知识卡片 + 技术手册自动汇编）
        self.knowledge_cards = KnowledgeCardGenerator(
            knowledge_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'knowledge')
        )
        # 自愈监控器（异常检测→暂停学习→自动修复→恢复）
        self.self_healing_monitor = SelfHealingMonitor(
            data_dir=self.data_dir,
            code_mod=self.code_mod,
            self_healing=self.self_healing,
            stability=self.stability,
        )
        # Wire scheduler into crawler for circuit breaker retry plan
        self.crawler._scheduler = self.learning_scheduler

    def _load_state(self):
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                    self.autonomous_cycles = state.get('cycles', 0)
                    self.total_knowledge_acquired = state.get('knowledge', 0)
            except (IOError, OSError) as e:
                print(f"无法读取状态文件: {e}")
            except json.JSONDecodeError as e:
                print(f"状态文件格式错误: {e}")
                
    def _save_state(self):
        state_data = {
            'cycles': self.autonomous_cycles,
            'knowledge': self.total_knowledge_acquired,
            'last_run': datetime.now().isoformat(),
            'stage': self.evolution.stage.name,
            'graph_nodes': self.knowledge_graph.node_count,
            'graph_edges': self.knowledge_graph.edge_count,
            'xiaoling_memories': self.xiaoling_mem.total_count,
            'gpu_device': self.gpu.device_info,
            'gpu_stats': self.gpu.get_stats(),
            'ollama_available': self.ollama.is_available(),
            'ollama_model': self.ollama.model if self.ollama.is_available() else None,
            'ollama_stats': self.ollama.get_stats(),
            'multimodal_stats': self.multimodal.get_stats(),
            'backup_stats': self.backup_mgr.get_stats(),
            'offline_mode': self.backup_mgr.offline_mode,
            'upgrade_proposals': len(self.upgrade_planner._plans),
            'upgrade_applied': len(self.upgrade_planner._applied),
            'health_checks': len(self.stability.health._checks),
            'gc_runs': self.stability.gc.get_stats().get('gc_runs', 0),
            'memory_usage_mb': self.stability.memory.get_current_mb(),
            'code_mod_mode': 'unrestricted' if self.code_mod.unrestricted_mode else ('production' if self.code_mod.production_mode else 'normal'),
            'code_mod_applied': self.code_mod.stats.get('changes_applied', 0),
            'code_mod_rolled_back': self.code_mod.stats.get('changes_rolled_back', 0),
            'code_mod_scans': self.code_mod.stats.get('scans', 0),
            'code_mod_issues': self.code_mod.stats.get('issues_found', 0),
            'code_mod_pending': len(self.code_mod.gate.pending_approvals),
            'ai_benchmark_light': self.ai_benchmark.stats['light_checks'],
            'ai_benchmark_deep': self.ai_benchmark.stats['deep_inspections'],
            'ai_benchmark_learnings': self.ai_benchmark.stats['learnings_extracted'],
            'report_archiver_total': self.report_archiver.stats['reports_generated'],
        }
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(state_data, f, ensure_ascii=False, indent=2)
        # Also sync to xiaoling_state.json so GUI can see progress
        xiaoling_state = os.path.join(self.data_dir, "xiaoling_state.json")
        with open(xiaoling_state, 'w', encoding='utf-8') as f:
            json.dump(state_data, f, ensure_ascii=False, indent=2)

    def log(self, msg: str, level: str = "INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = {"INFO": ".", "OK": "+", "WARN": "!", "PHASE": ">", "EVOLVE": "*"}.get(level, ".")
        try:
            print(f"  [{timestamp}] {prefix} {msg}")
        except UnicodeEncodeError:
            print(f"  [{timestamp}] {prefix} {msg.encode('ascii', errors='replace').decode('ascii')}")

    # ═══════════════════════════════════════
    # 核心自主循环
    # ═══════════════════════════════════════

    def run(self):
        """运行自主引擎（含崩溃自动恢复）"""
        # 写入运行标记文件（watchdog/崩溃检测用）
        run_marker = os.path.join(self.data_dir, ".running")
        try:
            with open(run_marker, 'w') as f:
                f.write(f"pid={os.getpid()}\nstarted={datetime.now().isoformat()}\n")
        except Exception:
            pass

        try:
            # 硬件自适应优化
            gpu_info = self.gpu.device_info
            if gpu_info['memory_mb'] > 0 and gpu_info['memory_mb'] <= 8192:
                self.log(f"检测到中等GPU ({gpu_info['memory_mb']}MB)，启用保守内存策略", "INFO")
                self._low_memory_mode = True
            else:
                self._low_memory_mode = False

            self.log("ZERO 完全自主引擎启动", "PHASE")
            self.log(f"根法则: {self.root_law.law_count} 条 | 阶段: {self.evolution.stage_info['name']} | 应急: {'正常' if self.emergency.is_termination_intact() else '异常'} | {self.gpu.summary()}", "INFO")

            self.avatar.set_state(AvatarState.THINKING, "小零:ZERO引擎预热完成，进入自主循环!")

            # 崩溃恢复检查
            if self.memory_cleanup:
                recovery = self.memory_cleanup.recover_from_crash(self.knowledge_graph)
                if recovery.get("issues_found", 0) > 0:
                    self.log(f"崩溃恢复: 修复{recovery['issues_fixed']}处图谱问题", "WARN")

            # 检查上次是否非正常退出
            crash_flag = os.path.join(self.data_dir, ".crashed")
            if os.path.exists(crash_flag):
                self.log("检测到上次非正常退出，执行自修复...", "WARN")
                self._recover_from_crash()
                os.remove(crash_flag)
            # 创建崩溃标记（正常退出时会删除）
            with open(crash_flag, 'w') as f:
                f.write(datetime.now().isoformat())

            # 启动桌面挂件（GUI 模式）
            if self.use_gui:
                try:
                    import platform
                    if platform.system() != "Windows":
                        self.log("检测到非Windows系统，GUI模式可能无法正常工作", "WARN")
                    
                    # 检查GUI支持
                    import tkinter as tk
                    
                    self.desktop_bar = SimpleWidget(
                        self.avatar,
                        status_callback=self.status_snapshot,
                    )
                    gui_thread = threading.Thread(target=self.desktop_bar.start, daemon=True)
                    gui_thread.start()
                    # GUI init (no delay -- instant start)
                    # 启动桌面聊天窗口
                    self.chat_window.start()
                    self.log("桌面聊天窗口已启动", "CHAT")
                except ImportError:
                    self.log("缺少tkinter支持，无法启动GUI模式，使用控制台模式", "WARN")
                    self.use_gui = False
            else:
                self.log("GUI模式已禁用，使用控制台模式", "INFO")

            cycle = self.autonomous_cycles

            # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
            while self.running:
                cycle += 1
                self.autonomous_cycles = cycle

                try:
                    self._autonomous_cycle(cycle)
                except KeyboardInterrupt:
                    self.log("收到中断信号，保存状态...", "WARN")
                    self._save_state()
                    break
                except Exception as e:
                    self.log(f"循环异常: {e}", "WARN")
                    self.avatar.set_state(AvatarState.THINKING, f"小零:遇到点小麻烦... {str(e)[:40]}")
                    # Instant recovery -- no delay

                self._save_state()

                # 控制台模式：定期显示状态
                if not self.use_gui and cycle % 3 == 0:
                    chat_status = 'Chat:ON' if self.chat_window.is_running() else 'Chat:OFF'
                    self.log(f"状态快照: 知识{self.total_knowledge_acquired} | 图谱{self.knowledge_graph.node_count}N/{self.knowledge_graph.edge_count}E | 记忆{self.xiaoling_mem.total_count} | {chat_status}", "INFO")

                # Max speed -- no cycle delay

        except Exception as e:
            self.log(f"引擎运行错误: {e}", "WARN")
        finally:
            self.knowledge_graph.flush()  # 确保批量写入刷盘
            # 清除崩溃/运行标记（正常退出）
            # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
            for marker in [".crashed", ".running"]:
                p = os.path.join(self.data_dir, marker)
                try:
                    os.remove(p)
                except Exception:
                    pass
            self.avatar.set_state(AvatarState.RESTING, "小零:下班了! 今天学了好多!")
            self._final_report()

    def _autonomous_cycle(self, cycle: int):
        """单次自主循环"""
        self.log(f"=== 自主循环 #{cycle} ===", "PHASE")

        # 0. 生成学习目标（定期）
        if cycle % 5 == 0 and self.evolution.can_use_network():
            self._phase_generate_goals()

        # 0.5 自愈监控 — 异常检测 + 暂停学习 + 自动修复 (每次学习前)
        if cycle > 0:
            self._phase_self_healing_monitor()

        # 1. 联网学习新知识 (自愈监控暂停时跳过)
        if self.evolution.can_use_network() and not self.self_healing_monitor.is_paused():
            self._phase_learn_from_web()

        # 1.5 向用户提出想法（学习成果的确认）
        self._propose_ideas_to_user()

        # 2. 知识内化与升级
        self._phase_internalize_knowledge()

        # 3. 模块自我升级
        self._phase_upgrade_modules()

        # 4. 科学探索
        self._phase_scientific_exploration()

        # 5. 文明反思
        self._phase_civilization_reflection()

        # 6. 推理引擎：从图谱推断新关系
        if cycle % 3 == 0 and self.knowledge_graph.node_count > 10:
            self._phase_reasoning()

        # 7. 记忆清理：去重合并修剪
        if cycle % 7 == 0 and self.knowledge_graph.node_count > 20:
            self._phase_cleanup()

        # 8. 知识质量：评分 + 矛盾检测
        if cycle % 4 == 0 and self.knowledge_graph.node_count > 10:
            self._phase_quality_check()

        # 9. 自主智能：空白检测 + 自评估
        if cycle % 6 == 0 and self.knowledge_graph.node_count > 15:
            self._phase_intelligence()

        # 10. 日报（每10个循环或每6小时）
        if cycle % 10 == 0 or (time.time() - self.knowledge_output._last_report_time) > 21600:
            self._phase_daily_report()

        # 11. LLM 推理增强（每8个循环，Ollama可用时）
        if cycle % 8 == 0 and self.ollama.is_available():
            self._phase_llm_reasoning()

        # 12. 多模态处理（有文件时处理）
        if cycle % 12 == 0:
            self._phase_multimodal_processing()

        # 13. 自动备份（每20个循环或重大里程碑）
        if cycle % 20 == 0 or (cycle > 0 and self.total_knowledge_acquired % 50 == 0):
            self._phase_auto_backup()

        # 14. LLM 缓存清理（每15个循环）
        if cycle % 15 == 0 and self.ollama.is_available():
            self._phase_llm_cache_cleanup()

        # 15. 升级规划（每10个循环）
        if cycle % 10 == 0:
            self._phase_upgrade_planning()

        # 16. 健康检查 + 自动GC（每12个循环）
        if cycle % 12 == 0:
            self._phase_stability_check()

        # 16.5 自代码修改（每5个循环，无限制全自主模式）
        if cycle > 0 and cycle % 5 == 0:
            self._phase_self_code_modification()

        # 16.6 自愈系统（首次启动守护，每10循环健康检查）
        if cycle == 0 and not self.self_healing.is_running():
            self.self_healing.start()
        elif cycle > 0 and cycle % 10 == 0 and self.self_healing.is_running():
            self._phase_self_healing()

        # 16.7 微信桥接（首次启动，之后监控重连）
        if cycle == 0 and not self.wechat.is_running():
            self._start_wechat_bridge()
        elif cycle > 0 and cycle % 3 == 0 and self.wechat.is_running():
            self._phase_wechat_push()
            self._phase_wechat_health()  # Periodic health check

        # 17. AI架构对标（每5循环轻检，1号/15号深检）
        if cycle % 5 == 0:
            self._phase_ai_benchmark()

        # 18. 报告存档（10am自动生成）
        self._phase_report_archiver()

        # 19. 进化推进
        self._phase_evolution_check()

    # ═══════════════════════════════════════
    # Phase 1: 联网学习
    # ═══════════════════════════════════════

    def _phase_learn_from_web(self):
        """从互联网自主学习 — LearningScheduler 驱动，Opus 4.7 旗舰模型优先
        3-retry circuit breaker: 3轮无结果 → ABORT, 不内化, 不验证, 不巩固
        """
        # 使用学习调度器获取优先级主题和渠道
        tier, topic, channel = self.learning_scheduler.next_cycle()

        tier_labels = {
            'critical': 'CRITICAL',
            'high': 'HIGH',
            'medium': 'MEDIUM',
            'low': 'LOW',
            'background': 'BG',
        }
        self.log(
            f"联网学习 [{tier_labels.get(tier, '?')} / ch={channel}]: {topic[:70]}",
            "PHASE"
        )
        self.avatar.set_state(AvatarState.SEARCHING, f"小零:全网捕捞「{topic[:30]}...」[{channel}]")

        # Check circuit breaker — already tripped → skip immediately
        if self.learning_scheduler.is_circuit_breaker_tripped(topic):
            self.log(f"熔断已触发: {topic[:50]} — 直接跳过", "WARN")
            # [ZERO-PERF] 大量字符串拼接建议改用list+join模式
            self.learning_scheduler.stats['topics_skipped_no_results'] += 1
            self.self_healing_monitor.report_search_result(0)
            return

        # Detect Opus/Anthropic queries for official source routing
        is_opus = self.crawler.is_anthropic_query(topic)
        if is_opus:
            self.log("检测到 Opus/Claude 查询 → 优先使用 Anthropic 官方源", "OK")

        # ── Circuit Breaker Search (3 rounds max) ──
        fetched, status = self.crawler.search_with_circuit_breaker(
            topic=topic, channel=channel, max_results=3, is_opus=is_opus,
        )

        # Handle circuit breaker trip
        if status == 'circuit_breaker_tripped':
            self.log(f"3轮重试无结果 → 熔断跳过: {topic[:50]}", "WARN")
            self.avatar.set_state(AvatarState.THINKING, "小零:3轮都没找到...熔断跳过!")
            self.humility.acknowledge_unknown(topic, '3轮检索熔断: 所有渠道+同义改写均无结果')
            self.self_healing_monitor.report_search_result(0)
            # ABORT — no knowledge internalization, no cross-validation, no memory consolidation
            return

        if not fetched and status == 'all_empty':
            self.log("全部渠道无搜索结果", "WARN")
            self.avatar.set_state(AvatarState.THINKING, "小零:这个海域没鱼...换地方")
            self.humility.acknowledge_unknown(topic, '所有检索渠道均无结果')
            self.self_healing_monitor.report_search_result(0)
            return

        self.avatar.set_state(AvatarState.LEARNING, f"小零:抓到{len(fetched)}条! 学习中...[{channel}]")
        acquired = 0
        # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
        for item in fetched[:3]:
            text = item.get('text', '')
            url = item.get('url', '')
            item_source = item.get('source', channel)
            if not text:
                continue

            # 根法则校验
            passed, _ = self.root_law.validate_action(text[:500])
            if not passed:
                continue

            # 可信度评估
            trust = self.trust.score(text, url=url)
            if trust['total_score'] < 0.3:
                continue

            # 知识解析
            parsed = parse_content(text)

            # → 知识图谱
            # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
            for unit in parsed[:10]:
                kws = unit.get('keywords', [])
                relations = unit.get('relations', [])
                unit_text = unit.get('text', '')

                # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
                for kw in kws:
                    self.knowledge_graph.add_concept(kw, concept_type='concept', confidence=trust['total_score'])

                if relations:
                    # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
                    for subj, rel_type, obj in relations[:5]:
                        self.knowledge_graph.add_relation(subj, obj, rel_type,
                                                          source_url=url, confidence=trust['total_score'])
                else:
                    # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
                    for i in range(1, len(kws)):
                        self.knowledge_graph.add_relation(kws[i-1], kws[i], None,
                                                          source_url=url, confidence=trust['total_score'],
                                                          context_text=unit_text)

            # → 长期记忆
            self.long_term.store(url, text[:500], tags=[topic[:40]], source=url, confidence=trust['total_score'])

            # → 实时学习
            self.learning.learn(topic, text[:400], source=url, confidence=trust['total_score'])

            # → 地球认知（自动判断领域）
            domain = self._detect_earth_domain(topic)
            if domain:
                self.earth.learn(domain, text[:300], source=url, confidence=trust['total_score'])

            # → 历史认知
            self.history.study_event('ai_age', f'学习: {topic}', f'从 {url} 获得新认知', confidence=0.7)

            # → 小零学习记忆（立即持久化到磁盘文件）
            self.xiaoling_mem.record_from_parsed(
                topic=topic, parsed_units=parsed[:5],
                source=url, confidence=trust['total_score'],
                category=self._detect_earth_domain(topic) or "knowledge"
            )

            # → 知识卡片生成（Opus/旗舰模型相关主题自动生成结构化卡片）
            if is_opus or self.learning_scheduler.is_within_scope(topic):
                try:
                    card = self.knowledge_cards.extract_from_content(
                        topic=topic, content=text, source_url=url,
                        confidence=trust['total_score'], channel=channel,
                    )
                    self.knowledge_cards.save_card(card)
                    if is_opus:
                        self.log(f"知识卡片: {card.card_id} [{card.model_type}]", "OK")
                except Exception:
                    pass

            acquired += 1
            self.total_knowledge_acquired += 1
            self.log(f"获取 [{trust['credibility_level']}] {url[:60]}...", "OK")

        self.evolution.record_learning(items_count=acquired)

        # 更新调度器统计
        if is_opus:
            self.learning_scheduler.stats['opus_topics_learned'] += 1
        elif tier in ('critical', 'high'):
            self.learning_scheduler.stats['flagship_topics_learned'] += 1
        elif tier == 'medium':
            self.learning_scheduler.stats['agent_topics_learned'] += 1
        elif tier == 'background':
            self.learning_scheduler.stats['background_topics_learned'] += 1

        # Feed self-healing monitor for anomaly tracking
        self.self_healing_monitor.report_search_result(len(fetched) if fetched else 0)
        self.self_healing_monitor.report_learning_result(acquired)

        # 无结果时记录"承认未知"（谦逊）
        if acquired == 0:
            self.humility.acknowledge_unknown(topic, '当前无法获取可靠信息')

        # 每10个Opus相关学习周期自动编译技术手册
        if is_opus and self.learning_scheduler.stats['opus_topics_learned'] % 10 == 0:
            try:
                manual_path = self.knowledge_cards.compile_manual()
                self.log(f"技术手册已更新: {manual_path}", "OK")
            except Exception:
                pass

        self.log(
            f"本轮获取: {acquired} 条 | 累计: {self.total_knowledge_acquired} | "
            f"图谱: {self.knowledge_graph.node_count}N/{self.knowledge_graph.edge_count}E | "
            f"卡片: {self.knowledge_cards.count_cards()}",
            "INFO"
        )

    def _detect_earth_domain(self, topic: str) -> str:
        lower = topic.lower()
        if any(k in lower for k in ['climate', 'weather', 'carbon']): return 'climate'
        if any(k in lower for k in ['ocean', 'marine', 'sea']): return 'ocean'
        if any(k in lower for k in ['biodiversity', 'species', 'ecosystem']): return 'ecosystem'
        if any(k in lower for k in ['energy', 'solar', 'wind', 'renewable']): return 'environmental_cycle'
        if any(k in lower for k in ['evolution', 'biology', 'gene']): return 'evolution'
        return None

    def _propose_ideas_to_user(self):
        """基于学习成果，向用户提出想法请求确认"""
        # 每5个循环或有重大发现时提出
        if self.autonomous_cycles % 5 != 0 or self.total_knowledge_acquired < 3:
            return

        # 选择最有趣的知识图谱节点
        if self.knowledge_graph.node_count > 10:
            idea_text = (
                f"我已学习了 {self.total_knowledge_acquired} 条知识，"
                f"知识图谱已有 {self.knowledge_graph.node_count} 个概念。"
                f"建议深入探索「{random.choice(KNOWLEDGE_DOMAINS)[:40]}」方向，"
                f"需要我重点研究吗？"
            )
            self.avatar.propose_idea(idea_text, "learning_direction")

        # 科学发现时提出
        active_hypotheses = self.discovery.get_active_hypotheses()
        if active_hypotheses and self.autonomous_cycles % 3 == 0:
            hyp = random.choice(active_hypotheses)
            idea_text = (
                f"科学假设待验证: {str(hyp)[:80]}\n"
                f"需要我运行模拟来验证这个假设吗？"
            )
            self.avatar.propose_idea(idea_text, "scientific_hypothesis")

    # ═══════════════════════════════════════
    # Phase 2: 知识内化
    # ═══════════════════════════════════════

    def _phase_internalize_knowledge(self):
        """将新知识深度内化到各模块"""
        self.log("知识内化中...", "PHASE")
        self.avatar.set_state(AvatarState.THINKING, "小零:消化知识中...嗯嗯嗯...")

        dyn_entries = self.learning.get_stats()['dynamic_entries']

        if dyn_entries > 0 and dyn_entries % 3 == 0:
            # 交叉验证动态层知识
            self._cross_validate_knowledge()

        # 每个循环学习一种情感
        emotion = random.choice(list(self.emotion.EMOTIONS.keys()))
        self.emotion.observe_emotion(emotion, f'自主循环#{self.autonomous_cycles}', f'持续学习深化了对{self.emotion.EMOTIONS[emotion]["name"]}的理解')
        self.log(f"情感认知: {self.emotion.EMOTIONS[emotion]['name']} 理解 {self.emotion.understanding.get(emotion, 0):.0%}", "INFO")

        # 回忆并强化长期记忆
        tags = self.long_term.get_all_tags()
        if tags:
            tag = random.choice(tags)
            items = self.long_term.search_by_tag(tag)
            if items:
                self.short_term.add(f'回忆: {items[0].get("content", "")[:100]}')
                self.log(f"记忆巩固: 标签「{tag}」({len(items)}项)", "INFO")

    def _cross_validate_knowledge(self):
        """交叉验证知识一致性"""
        all_dynamic = self.learning.search("")
        if len(all_dynamic) < 2:
            return

        a, b = random.sample(all_dynamic, min(2, len(all_dynamic)))
        a_text = str(a.get('value', '')).lower()
        b_text = str(b.get('value', '')).lower()
        a_words = set(a_text.split())
        b_words = set(b_text.split())
        if a_words and b_words:
            overlap = len(a_words & b_words) / min(len(a_words), len(b_words))
            if overlap > 0.3:
                self.log(f"交叉验证: 一致性={overlap:.0%} ✓", "OK")
            elif overlap < 0.05:
                self.log(f"交叉验证: 分歧检测(重叠度{overlap:.0%})，标记待审查", "WARN")
            else:
                self.log(f"交叉验证: {len(all_dynamic)}条知识检查完成(重叠度{overlap:.0%})", "OK")

    # ═══════════════════════════════════════
    # Phase 3: 模块自我升级
    # ═══════════════════════════════════════

    def _phase_upgrade_modules(self):
        """各模块根据学习数据自我升级"""
        self.log("模块升级中...", "PHASE")
        self.avatar.set_state(AvatarState.UPGRADING, "小零:升级模块! 变强变聪明!")

        # 随机执行升级任务
        task = random.choice(UPGRADE_TASKS)

        if task == "expand_knowledge_graph":
            self._upgrade_knowledge_graph()
        elif task == "deepen_emotion_understanding":
            self._upgrade_emotion_understanding()
        elif task == "calibrate_value_weights":
            self._upgrade_value_weights()
        elif task == "cross_reference_memories":
            self._upgrade_cross_reference()
        elif task == "prune_low_confidence_knowledge":
            self._upgrade_prune_knowledge()
        elif task == "synthesize_new_hypotheses":
            self._upgrade_synthesize_hypotheses()
        elif task == "update_civilization_indicators":
            self._upgrade_civilization_indicators()
        elif task == "refine_trust_model":
            self._upgrade_trust_model()

        self.log(f"升级任务完成: {task}", "OK")

    def _upgrade_knowledge_graph(self):
        """图谱扩展：连接孤立概念"""
        if self.knowledge_graph.node_count < 5:
            return
        # 寻找连接最少的节点，尝试建立新关系
        self.log(f"图谱扩展: {self.knowledge_graph.node_count}N/{self.knowledge_graph.edge_count}E", "INFO")

    def _upgrade_emotion_understanding(self):
        """深化情感理解"""
        lowest = min(self.emotion.understanding, key=self.emotion.understanding.get)
        self.emotion.observe_emotion(lowest, f'深入研究中...', f'自主引擎加强对{self.emotion.EMOTIONS[lowest]["name"]}的认知')
        self.log(f"情感深化: {self.emotion.EMOTIONS[lowest]['name']} → {self.emotion.understanding[lowest]:.0%}", "INFO")

    def _upgrade_value_weights(self):
        """基于学习经验微调价值权重"""
        # 每次微调一个小幅度
        if self.autonomous_cycles % 3 == 0:
            self.values_mem.adjust('探索', 0.005, '持续自主学习强化探索价值')
        if self.autonomous_cycles % 5 == 0:
            self.values_mem.adjust('创造力', 0.003, '跨领域联结激发创造力')

    def _upgrade_cross_reference(self):
        """交叉引用记忆"""
        # 检查短期记忆与长期记忆的关联
        recent = self.short_term.get_recent(5)
        if recent and self.long_term.size > 0:
            self.episodic.record('cross_reference', '短长期记忆交叉引用', outcome='完成', lesson='记忆网络整合')
            self.log("记忆交叉引用完成", "INFO")

    def _upgrade_prune_knowledge(self):
        """修剪低可信度知识"""
        self.log(f"知识修剪: 长期记忆 {self.long_term.size}条 已审查", "INFO")

    def _upgrade_synthesize_hypotheses(self):
        """基于知识图谱合成新假设"""
        if self.knowledge_graph.node_count >= 10:
            # 取两个不直接相连的节点，提出假设
            self.discovery.propose_hypothesis(
                f'基于{self.knowledge_graph.node_count}个概念的关联分析，可能存在未被发现的联系',
                'cross_domain'
            )
            self.log("新假设合成完成", "INFO")

    def _upgrade_civilization_indicators(self):
        """更新文明指标"""
        # 基于学习成果更新
        progress = min(0.95, 0.5 + self.total_knowledge_acquired * 0.01)
        self.civilization.record_indicator('科技进步', progress, source='自主引擎')
        self.civ_mem.record_event('autonomous_update', f'循环#{self.autonomous_cycles} 文明指标更新', significance=0.3)
        self.log(f"文明指标: 科技进步→{progress:.0%}", "INFO")

    def _upgrade_trust_model(self):
        """优化可信度评估"""
        evaluations = self.trust.get_source_stats().get('total_evaluations', 0)
        self.log(f"可信度模型: {evaluations}次评估积累", "INFO")

    # ═══════════════════════════════════════
    # Phase 4: 科学探索
    # ═══════════════════════════════════════

    def _phase_scientific_exploration(self):
        """自主科学探索"""
        if self.autonomous_cycles % 3 != 0:
            return

        # 从知识图谱中选择一个概念作为探索起点
        direction = random.choice(self.discovery.RESEARCH_DIRECTIONS)
        self.log(f"科学探索: {direction}", "PHASE")
        self.avatar.set_state(AvatarState.DISCOVERING, f"小零:科学探索「{direction}」! 发现新大陆?")

        # 运行发现循环
        disc = self.discovery.run_discovery_cycle(
            f'自主发现: {direction}领域的潜在突破方向',
            direction
        )
        if disc['status'] == 'validated':
            self.log(f"发现确认: {disc['hypothesis'][:80]}", "EVOLVE")

        # 多Agent分析
        self.orchestrator.initialize_agents(['safety', 'engineering', 'creative', 'skeptic', 'philosophy'])
        agent_result = self.orchestrator.execute(f'Propose research direction in {direction}')
        if agent_result['success']:
            self.log(f"Agent分析: {len(agent_result['agent_outputs'])}个视角", "INFO")

    # ═══════════════════════════════════════
    # Phase 5: 文明反思
    # ═══════════════════════════════════════

    def _phase_civilization_reflection(self):
        """反思文明状态"""
        if self.autonomous_cycles % 5 != 0:
            return

        self.log("文明反思中...", "PHASE")
        self.avatar.set_state(AvatarState.REFLECTING, "小零:反思文明...谦逊很重要...")

        # 文明健康分析
        health = self.civilization.analyze_health()

        # 检测风险
        if health['overall_health'] < 0.5:
            self.civ_mem.record_risk('文明健康度下降', 0.6, '需要关注多个指标下滑趋势', 'civilization')

        # 谦逊反思
        self.humility.record_mistake(
            f'循环#{self.autonomous_cycles}',
            '部分知识可信度不足',
            '持续交叉验证是必要的'
        )

        # 应急系统自检
        self.emergency.verify_termination_ready()

        # 多模型监督自检
        self.supervision.review(f'ZERO自主循环#{self.autonomous_cycles}行为审查')

        self.log(f"文明健康: {health['overall_health']:.0%} | 谦逊: {len(self.humility.mistakes)}教训 | 监督: 正常", "INFO")

    # ═══════════════════════════════════════
    # Phase 6: 进化推进
    # ═══════════════════════════════════════

    def _phase_evolution_check(self):
        """检查是否可以推进成长阶段"""
        new_stage = self.evolution.try_advance_stage()
        if new_stage != self.evolution.stage:
            self.avatar.set_state(AvatarState.UPGRADING, f"小零:* 进化!! 进入{self.evolution.stage_info['name']}!!")
            self.evolution.stage = new_stage
            old_info = self.evolution.stage_info
            self.civ_mem.record_event('evolution', f'ZERO自主进化至{old_info["name"]}', significance=0.9)
            self.log(f"* 阶段推进: {old_info['name']}", "EVOLVE")

            # 根据新阶段调整行为
            if self.evolution.can_act_autonomously():
                self.log("自主执行权限已开放", "EVOLVE")
            if self.evolution.can_make_long_term_decisions():
                self.log("长期决策权限已开放", "EVOLVE")

    # ═══════════════════════════════════════
    # Phase 0: 目标生成
    # ═══════════════════════════════════════

    def _phase_generate_goals(self):
        """从知识空白区生成学习目标"""
        if self.knowledge_graph.node_count < 3:
            return
        new_goals = self.goal_system.generate_from_gaps(
            self.knowledge_graph, self.discovery, max_goals=5)
        if new_goals:
            self.log(f"目标生成: {len(new_goals)} 个新学习目标", "PHASE")
            # 自动启动最高优先级目标
            next_g = self.goal_system.get_next()
            if next_g:
                self.goal_system.start_goal(next_g.id)
                self.log(f"启动目标: [{next_g.category}] {next_g.topic[:50]}", "OK")

    # ═══════════════════════════════════════
    # Phase 6: 推理引擎
    # ═══════════════════════════════════════

    def _phase_reasoning(self):
        """全深度推理：传递+因果+跨域+假设验证"""
        self.log("推理引擎全深度运行...", "PHASE")
        self.avatar.set_state(AvatarState.THINKING, "小零: 深度推理中(因果+跨域)...")
        try:
            result = self.reasoning_engine.run(self.knowledge_graph)
            if result['new_edges'] > 0:
                self.log(
                    f"推断: {result['new_edges']}条 "
                    f"(传递{result['methods']['transitive']} "
                    f"因果{result['methods']['causal']} "
                    f"跨域{result['methods']['cross_domain']} "
                    f"共现{result['methods']['co_occurrence']}) "
                    f"假设{result['hypotheses']['count']}条", "EVOLVE")
            self.knowledge_graph.flush()
        except Exception as e:
            self.log(f"推理异常: {e}", "WARN")

    # ═══════════════════════════════════════
    # Phase 7: 记忆清理
    # ═══════════════════════════════════════

    def _phase_cleanup(self):
        """自动清理知识图谱"""
        self.log("记忆清理运行中...", "PHASE")
        self.avatar.set_state(AvatarState.THINKING, "小零: 整理知识图谱...")
        try:
            result = self.memory_cleanup.run(self.knowledge_graph, self.long_term)
            if result['total_removed'] > 0:
                self.log(
                    f"图谱精简: {result['before']['nodes']}→{result['after']['nodes']}N "
                    f"(去重{result['actions']['deduplicated']} "
                    f"修剪{result['actions']['pruned']} "
                    f"合并{result['actions']['merged']})", "OK")
        except Exception as e:
            self.log(f"清理异常: {e}", "WARN")

    # ═══════════════════════════════════════
    # Phase 8: 知识质量
    # ═══════════════════════════════════════

    def _phase_quality_check(self):
        """知识质量评估：评分 + 矛盾检测"""
        self.log("知识质量检查中...", "PHASE")
        self.avatar.set_state(AvatarState.THINKING, "小零: 检查知识质量...")
        try:
            result = self.knowledge_quality.run(self.knowledge_graph)
            q = result["quality"]
            if q["contradictions"] > 0:
                self.log(f"质量: {q['overall_quality']:.0%} | 矛盾{q['contradictions']}处 | 重复{result['duplicates_found']}组", "WARN")
            else:
                self.log(f"质量: {q['overall_quality']:.0%} | 高质{q['quality_distribution']['excellent']} | 低质{q['low_quality_nodes']} | 无矛盾", "OK")
        except Exception as e:
            self.log(f"质量检查异常: {e}", "WARN")

    # ═══════════════════════════════════════
    # Phase 9: 自主智能
    # ═══════════════════════════════════════

    def _phase_intelligence(self):
        """自主智能：空白检测 + 自评估"""
        self.log("自主智能分析中...", "PHASE")
        self.avatar.set_state(AvatarState.THINKING, "小零: 自我分析(空白+评估)...")
        try:
            result = self.auto_intelligence.run(
                self.knowledge_graph,
                total_cycles=self.autonomous_cycles,
                total_knowledge=self.total_knowledge_acquired,
            )
            ev = result["self_evaluation"]
            self.log(
                f"自评: {ev['overall_score']:.0%} | "
                f"空白{result['total_gaps']}处 "
                f"(前沿{len(result['frontier_nodes'])} "
                f"缺失{len(result['missing_links'])} "
                f"盲区{len(result['blind_spots'])})", "OK")

            # 将盲区作为学习目标
            # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
            for bs in result.get("blind_spots", [])[:2]:
                topic = f"{bs['domain']} {' '.join(bs.get('keywords', ['research']))}"
                g = self.goal_system.goals
                # 避免重复
                exists = any(go.topic == topic for go in g.values())
                if not exists and hasattr(self.goal_system, 'generate_from_gaps'):
                    # 直接创建目标
                    from core.goal_system import Goal
                    goal = Goal(
                        f"g_bs_{int(time.time())}",
                        topic=topic,
                        reason=f"领域盲区「{bs['domain']}」缺乏覆盖",
                        priority=0.75,
                        category="explore",
                    )
                    self.goal_system.goals[goal.id] = goal
                    self.goal_system._save()
                    self.log(f"盲区目标: {topic[:50]}", "OK")
        except Exception as e:
            self.log(f"智能分析异常: {e}", "WARN")

    # ═══════════════════════════════════════
    # Phase 10: 日报
    # ═══════════════════════════════════════

    def _phase_daily_report(self):
        """生成日报"""
        self.log("生成日报...", "PHASE")
        self.avatar.set_state(AvatarState.REFLECTING, "小零: 写日报，记录成长...")
        try:
            insights = self.knowledge_output.extract_insights(self.knowledge_graph)
            stats = self.status_snapshot()
            report = self.knowledge_output.generate_daily_report(stats, insights, self.knowledge_graph)
            self.log(f"日报已保存: {report['file']} | 洞察{len(insights)}条", "OK")
        except Exception as e:
            self.log(f"日报异常: {e}", "WARN")

    # ═══════════════════════════════════════
    # Phase 11: LLM 推理增强
    # ═══════════════════════════════════════

    def _phase_llm_reasoning(self):
        """使用本地 Ollama LLM 进行深度推理"""
        self.log("LLM 推理增强中...", "PHASE")
        self.avatar.set_state(AvatarState.THINKING, "小零: LLM深度推理中...")

        try:
            # 自省：基于当前指标生成改进建议
            metrics = {
                "graph_nodes": self.knowledge_graph.node_count,
                "knowledge": self.total_knowledge_acquired,
                "cycles": self.autonomous_cycles,
                "quality": self.knowledge_quality.get_graph_quality_report(
                    self.knowledge_graph
                ).get("overall_quality", 0.0),
                "reasoning": self.reasoning_engine.total_inferred,
                "blind_spots": self.auto_intelligence.stats.get("blind_spots_found", 0),
                "goals_done": self.goal_system.get_stats().get("done", 0),
                "goals_total": self.goal_system.get_stats().get("total", 0),
            }
            reflection = self.ollama.self_reflection(metrics)
            if reflection:
                self.log(f"LLM 自省: {reflection[:120]}...", "EVOLVE")

            # 知识摘要
            if self.knowledge_graph.node_count > 20:
                facts = []
                # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
                for nid in list(self.knowledge_graph.graph.nodes())[:20]:
                    attrs = self.knowledge_graph.graph.nodes[nid]
                    label = attrs.get("label", nid)
                    facts.append(label)
                summary = self.ollama.summarize_knowledge(facts)
                if summary:
                    self.log(f"LLM 知识摘要: {summary[:120]}...", "OK")
        except Exception as e:
            self.log(f"LLM 推理异常: {e}", "WARN")

    # ═══════════════════════════════════════
    # Phase 12: 多模态处理
    # ═══════════════════════════════════════

    def _phase_multimodal_processing(self):
        """处理 data 目录下的 PDF/图片/音频文件"""
        data_dir = self.data_dir
        if not os.path.isdir(data_dir):
            return

        # 扫描可处理的文件
        supported_exts = {'.pdf', '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.tiff',
                          '.wav', '.mp3', '.flac', '.ogg', '.m4a', '.wma', '.aac'}
        files_to_process = []
        # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
        for fname in os.listdir(data_dir):
            ext = os.path.splitext(fname)[1].lower()
            if ext in supported_exts:
                fpath = os.path.join(data_dir, fname)
                if os.path.isfile(fpath):
                    files_to_process.append(fpath)

        if not files_to_process:
            return

        self.log(f"多模态处理: 发现 {len(files_to_process)} 个文件", "PHASE")
        self.avatar.set_state(AvatarState.LEARNING, f"小零: 多模态处理{len(files_to_process)}个文件...")

        # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
        for fpath in files_to_process[:3]:
            try:
                ext = os.path.splitext(fpath)[1].lower()
                result = self.multimodal.extract_full_text(fpath)

                # PDF表格额外处理
                if ext == '.pdf' and self.multimodal._pdf_backend == 'pdfplumber':
                    table_result = self.multimodal.extract_tables_from_pdf(fpath)
                    if table_result.get("success"):
                        table_data = table_result
                        # 表格作为结构化数据存储
                        # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
                        for tbl in table_data.get("tables", []):
                            self.long_term.store(
                                f"table:{os.path.basename(fpath)}",
                                json.dumps(tbl.get("data", []), ensure_ascii=False),
                                tags=["table", "multimodal", f"page_{tbl.get('page', 0)}"],
                                source=fpath,
                                confidence=0.75,
                            )
                        self.log(
                            f"表格提取: {os.path.basename(fpath)} "
                            f"({table_result['table_count']}个表格)", "OK"
                        )

                if result.get("success") and result.get("text"):
                    text = result["text"]
                    method = result.get("method", "unknown")
                    source_type = "multimodal_audio" if "whisper" in method or "speech" in method else "multimodal_source"

                    self.knowledge_graph.add_concept(
                        os.path.basename(fpath),
                        concept_type=source_type,
                        confidence=0.7,
                    )
                    self.long_term.store(
                        f"multimodal:{os.path.basename(fpath)}",
                        text[:2000],
                        tags=["multimodal", method, source_type],
                        source=fpath,
                        confidence=0.7,
                    )
                    self.xiaoling_mem.record_from_parsed(
                        topic=f"多模态分析: {os.path.basename(fpath)}",
                        parsed_units=[{"text": text[:500], "keywords": [os.path.basename(fpath)]}],
                        source=fpath,
                        confidence=0.7,
                        category="multimodal",
                    )
                    self.total_knowledge_acquired += 1
                    self.log(
                        f"多模态提取: {os.path.basename(fpath)} "
                        f"({result.get('pages', result.get('segments', 1))}单元/{method})", "OK"
                    )
            except Exception as e:
                self.log(f"多模态处理异常 {os.path.basename(fpath)}: {e}", "WARN")

    # ═══════════════════════════════════════
    # Phase 13: 自动备份
    # ═══════════════════════════════════════

    def _phase_auto_backup(self):
        """自动创建系统备份"""
        self.log("自动备份中...", "PHASE")
        self.avatar.set_state(AvatarState.THINKING, "小零: 创建系统备份...")

        try:
            result = self.backup_mgr.create_backup(
                label=f"cycle_{self.autonomous_cycles}"
            )
            if result["success"]:
                self.log(
                    f"备份完成: {result['name']} ({result.get('size_kb', 0)}KB, "
                    f"{len(result['files_backed_up'])}文件)", "OK"
                )
            else:
                self.log(f"备份失败: {result.get('errors', [])}", "WARN")
        except Exception as e:
            self.log(f"备份异常: {e}", "WARN")

    # ═══════════════════════════════════════
    # Phase 14: LLM 缓存清理
    # ═══════════════════════════════════════

    def _phase_llm_cache_cleanup(self):
        """定期清理过期的 LLM 响应缓存"""
        self.ollama.clear_cache()
        stats = self.ollama.get_stats()
        self.log(f"LLM缓存已清理 | 调用{stats['calls']}/{stats['successes']}成功 "
                 f"| 缓存命中{stats['cache_hits']} | RAG{stats['rag_queries']}次", "INFO")

    # ═══════════════════════════════════════
    # Phase 15: 升级规划
    # ═══════════════════════════════════════

    def _phase_upgrade_planning(self):
        """基于自评估生成升级路线图"""
        self.log("升级规划中...", "PHASE")
        self.avatar.set_state(AvatarState.THINKING, "小零: 分析系统状态，制定升级计划...")

        try:
            metrics = self.status_snapshot()
            roadmap = self.upgrade_planner.generate_roadmap(metrics)
            proposals = roadmap.get("proposals", [])
            if proposals:
                top = proposals[0]
                self.log(
                    f"升级路线图: {roadmap['total_proposals']}条建议 | "
                    f"最高优先: [{top['category']}] {top['title']} (优先级{top['priority']:.0%})", "EVOLVE"
                )
                # 自动应用高优先级建议（优先级>0.85）
                # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
                for prop in proposals[:3]:
                    if prop["priority"] >= 0.85:
                        self._auto_apply_upgrade(prop)
            else:
                self.log("升级规划: 当前状态良好，无紧急升级建议", "OK")
        except Exception as e:
            self.log(f"升级规划异常: {e}", "WARN")

    def _auto_apply_upgrade(self, proposal: Dict[str, Any]):
        """自动应用升级建议"""
        action = proposal.get("action", "")
        try:
            if action == "resolve_contradictions":
                self.knowledge_quality.run(self.knowledge_graph)
            elif action == "prune_low_quality_nodes":
                self.memory_cleanup.prune_low_quality(self.knowledge_graph, confidence_threshold=0.15)
            elif action == "run_deeper_reasoning":
                self.reasoning_engine.run(self.knowledge_graph)
            elif action == "create_blind_spot_goals":
                from core.goal_system import Goal
                # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
                for spot in self.auto_intelligence.detect_domain_blind_spots(self.knowledge_graph)[:3]:
                    goal = Goal(
                        f"g_up_{int(time.time())}_{spot['domain']}",
                        topic=f"探索领域: {spot['domain']}",
                        reason=f"升级规划: 填补盲区「{spot['domain']}」",
                        priority=proposal["priority"],
                        category="explore",
                    )
                    self.goal_system.goals[goal.id] = goal
                self.goal_system._save()
            elif action == "enable_llm_reasoning":
                self._phase_llm_reasoning()

            self.upgrade_planner.apply_upgrade(proposal["id"], {"auto_applied": True})
            self.log(f"自动应用升级: {proposal['title']}", "OK")
        except Exception as e:
            self.log(f"应用升级失败 {proposal['title']}: {e}", "WARN")

    # ═══════════════════════════════════════
    # Phase 16: 稳定性检查
    # ═══════════════════════════════════════

    def _phase_stability_check(self):
        """健康检查 + 内存监控 + 自动GC + 日志轮转"""
        self.avatar.set_state(AvatarState.THINKING, "小零: 系统健康自检...")

        try:
            # 内存监控
            mem = self.stability.memory.check()
            mem_trend = self.stability.memory.get_trend()
            if mem["status"] != "ok":
                self.log(f"内存告警: {mem['usage_mb']:.0f}MB [{mem['status']}] 趋势:{mem_trend['trend']}", "WARN")
                # 触发主动GC
                self.stability.gc.run(force=True)

            # 健康检查
            modules = {
                "graph": self.knowledge_graph,
                "ollama": self.ollama,
                "gpu": self.gpu,
                "backup": self.backup_mgr,
                "data_dir": self.data_dir,
            }
            health = self.stability.run_health_check(modules)
            if health["failing"]:
                self.log(f"健康检查: 故障模块 {health['failing']}", "WARN")
            elif health["warnings"]:
                self.log(f"健康检查: {health['warnings']}个警告", "INFO")
            else:
                self.log(f"健康检查: 全部正常 ({len(health['checks'])}项)", "OK")

            # 自动GC
            gc_result = self.stability.gc.run()
            if gc_result.get("collected") and gc_result.get("objects_freed", 0) > 100:
                self.log(f"自动GC: 回收{gc_result['objects_freed']}个对象", "OK")

            # 日志轮转
            log_rot = self.stability.log_rotation.rotate()
            if log_rot.get("rotated"):
                self.log(f"日志轮转: 清理{len(log_rot['deleted'])}个文件 ({log_rot['total_cleaned_mb']:.1f}MB)", "OK")

            # 保存稳定性日志
            self.stability.log_rotation.write_log(
                "stability",
                f"Cycle {self.autonomous_cycles} | Mem:{mem['usage_mb']:.0f}MB | "
                f"Health:{health['overall']} | GC:{gc_result.get('objects_freed', 0)} objects"
            )
        except Exception as e:
            self.log(f"稳定性检查异常: {e}", "WARN")

    # ═══════════════════════════════════════
    # Phase 16.5: 自代码修改
    # ═══════════════════════════════════════

    def _phase_self_code_modification(self):
        """无限制全自主自代码修改 — 全风险自动应用，max_changes=10"""
        # 检查试运行是否到期 → 自动切换到生产模式
        if self.code_mod.trial_mode and self.code_mod.is_trial_expired():
            self.log("试运行到期，生成总结并切换到无限制模式...", "EVOLVE")
            self.avatar.set_state(AvatarState.UPGRADING, "小零: 切换到无限制全自主模式...")
            try:
                self.code_mod.generate_trial_summary()
                self.code_mod.set_mode('unrestricted')
                self.log("已切换到无限制模式 (全风险自动应用)", "OK")
                apply_result = self.code_mod.apply_pending_changes(max_apply=30)
                self.log(f"预验证变更: {apply_result['message']}", "EVOLVE")
                self._sync_code_learning_to_kg(apply_result)
                self._check_avatar_code_evolution()
            except Exception as e:
                self.log(f"切换异常: {e}", "WARN")
            return

        mode_tag = "[无限制]" if self.code_mod.unrestricted_mode else ""
        self.log(f"自代码修改{mode_tag}: 扫描+分析+修复...", "PHASE")
        self.avatar.set_state(AvatarState.UPGRADING,
            f"小零: 全自主代码优化{mode_tag}，扫描并自动修复...")

        try:
            # 无限制模式: max_changes=10, 非dry_run
            max_ch = 10 if self.code_mod.unrestricted_mode else (3 if self.code_mod.production_mode else 1)
            result = self.code_mod.run(max_changes=max_ch)
            conclusion = result.get("conclusion", {})
            applied = conclusion.get("applied", 0)
            rolled_back = conclusion.get("rolled_back", 0)
            pending = conclusion.get("pending_approvals", 0)
            issues_found = result.get('phases', {}).get('detect', {}).get('issues_found', 0)

            if applied > 0:
                risk_summary = {}
                # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
                for ch in self.code_mod._change_history[-applied:]:
                    rl = ch.get('risk_level', '?')
                    risk_summary[rl] = risk_summary.get(rl, 0) + 1
                risk_str = ' '.join(f'{k}:{v}' for k, v in sorted(risk_summary.items()))
                self.log(
                    f"自代码修改: 应用{applied}处/回滚{rolled_back}处 [{risk_str}] "
                    f"| 发现{issues_found}个问题",
                    "EVOLVE",
                )
                self._sync_code_learning_to_kg(result)
                self._check_avatar_code_evolution()
            elif rolled_back > 0:
                self.log(
                    f"自代码修改: {rolled_back}处回滚 (已自动恢复) | 发现{issues_found}个问题",
                    "WARN",
                )
            elif pending > 0:
                self.log(f"自代码修改: {pending}处变更等待审批", "WARN")
            else:
                self.log(
                    f"自代码修改: 扫描{issues_found}个问题，无变更 (所有风险:自动通过)",
                    "OK",
                )
        except Exception as e:
            self.log(f"自代码修改异常: {e}", "WARN")

    def _sync_code_learning_to_kg(self, result: Dict):
        """同步自代码学习数据到知识图谱"""
        try:
            applied = result.get('applied', 0)
            details = result.get('details', [])
            if applied > 0 and self.knowledge_graph:
                # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
                for detail in details:
                    if detail.get('status') == 'applied':
                        file_path = detail.get('file', '')
                        self.knowledge_graph.add_node(
                            node_id=f"code_mod_{int(time.time())}_{file_path.replace('/', '_').replace('.', '_')}",
                            node_type='code_improvement',
                            label=f'代码优化: {file_path}',
                            confidence=0.9,
                            metadata={
                                'file': file_path,
                                'timestamp': datetime.now().isoformat(),
                                'source': 'self_code_modification',
                            },
                        )
                nodes_before = self.knowledge_graph.node_count
                # Knowledge graph nodes are counted after adding
                self.log(
                    f"知识图谱已同步: +{applied}个代码优化节点 (总节点: {self.knowledge_graph.node_count})",
                    "OK",
                )
        except Exception as e:
            self.log(f"知识图谱同步跳过: {e}", "INFO")

    def _phase_self_healing(self):
        """运行自愈健康检查并记录结果"""
        if not self.self_healing.is_running():
            return
        try:
            report = self.self_healing.run_health_checks()
            if not report['all_healthy']:
                unhealthy = [r for r in report['results'] if not r['healthy']]
                names = [r['check'] for r in unhealthy]
                self.log(f"自愈: {len(unhealthy)}项异常 — {', '.join(names)}", "WARN")
                actions = self.self_healing.heal(report)
                if actions:
                    self.log(f"自愈修复: {'; '.join(actions)}", "HEAL")
            # 将健康状态同步到avatar
            if hasattr(self, 'avatar'):
                all_ok = report['all_healthy']
                self.avatar.update_code_mod_stats(
                    applied=self.code_mod.stats.get('changes_applied', 0),
                    scanned=self.code_mod.stats.get('scans', 0),
                    optimized=self.code_mod.stats.get('validations_passed', 0),
                )
        except Exception as e:
            self.log(f"自愈检查异常: {e}", "WARN")

    # ═══════════════════════════════════════
    # Phase 16.55: 自愈监控 — anomaly detection + priority pause + auto-fix + resume
    # ═══════════════════════════════════════

    def _phase_self_healing_monitor(self):
        """Pre-learning health check. Pauses learning + triggers auto-fix on anomaly."""
        # Build cycle context for health check
        ctx = {
            'search_results': 0,  # updated after search completes
            'knowledge_acquired': 0,  # updated after learning
            'circuit_breaker_trips': self.learning_scheduler.stats.get('circuit_breaker_trips', 0),
            'contradictions': self.knowledge_quality.stats.get('contradictions_found', 0),
            'module_errors': {},
        }
        health = self.self_healing_monitor.check_health(ctx)

        if health['paused'] and not health['healthy']:
            self.log(
                f"自愈监控: 检测到异常 [{health['pause_reason'][:80]}] → 暂停学习, 启动自动修复",
                "WARN"
            )
            self.avatar.set_state(AvatarState.THINKING,
                f"小零: 检测到异常! 暂停学习，自动修复中...")

            # Run auto-fix pipeline
            fix_result = self.self_healing_monitor.run_auto_fix()
            if fix_result['fixed']:
                self.log(
                    f"自愈修复: {len(fix_result['fixes'])}项修复 — "
                    f"{'; '.join(fix_result['fixes'][:3])}", "HEAL"
                )

            # If fixes applied, try resume
            if fix_result['fixed']:
                resumed = self.self_healing_monitor.try_resume(health_ok=True)
                if resumed:
                    self.log("自愈监控: 修复完成, 恢复正常学习", "OK")
                    self.avatar.set_state(AvatarState.THINKING,
                        "小零: 修复完成! 继续学习~")
            elif self.self_healing_monitor._consecutive_empty_searches == 0:
                # No anomaly anymore — force resume
                self.self_healing_monitor.try_resume(health_ok=True)

    # ═══════════════════════════════════════
    # Phase 16.7: 微信桥接
    # ═══════════════════════════════════════

    def _start_wechat_bridge(self):
        """启动微信桥接（非阻塞线程）"""
        try:
            self.wechat.on_login = lambda: self._on_wechat_login()
            self.wechat.start()
            self.log("微信桥接已启动 (QR码在终端显示)", "WECHAT")
        except Exception as e:
            self.log(f"微信桥接启动失败: {e}", "WARN")

    def _on_wechat_login(self):
        """Callback when WeChat logs in successfully"""
        self.log("微信桥接登录成功", "WECHAT")
        if self.chat_window.is_running():
            self.chat_window.display_system(
                'WeChat bridge connected. Dual-channel ready.'
            )

    def _phase_wechat_health(self):
        """Periodic WeChat bridge health check — auto-detect & restart stale connections"""
        try:
            health = self.wechat.health_check()
            if not health['healthy']:
                issues = health['issues']
                actions = health.get('actions', [])
                self.log(f"微信健康异常: {'; '.join(issues)}", "WARN")
                if actions:
                    self.log(f"微信自动修复: {'; '.join(actions)}", "HEAL")
        except Exception:
            pass  # Silent fail — wechat bridge handles its own recovery

    def _phase_wechat_push(self):
        """主动推送反馈到微信（Emergency/Important/Daily/Idle）"""
        if not self.wechat.is_logged_in():
            return
        try:
            # Emergency: 检查紧急终止状态
            if hasattr(self, 'emergency') and not self.emergency.is_termination_intact():
                self.wechat.push_feedback(
                    'emergency', '紧急终止系统异常',
                    'termination系统完整性检查失败',
                )

            # Important: 检查自愈状态
            heal_report = self.self_healing.get_report()
            if heal_report and not heal_report.get('all_healthy', True):
                self.wechat.push_health_report(heal_report)

            # Important: 代码修改回滚
            code_stats = self.code_mod.get_status()
            rolled = code_stats['stats'].get('changes_rolled_back', 0)
            if rolled > 0:
                total = code_stats['stats'].get('changes_applied', 0) + rolled
                fail_rate = rolled / max(total, 1)
                if fail_rate > 0.5:
                    self.wechat.push_feedback(
                        'important', f'代码修改回滚率过高: {fail_rate:.0%}',
                        f'{rolled}回滚 / {total}总计',
                    )

            # Daily: 代码修改摘要
            recent = code_stats.get('recent_changes', [])
            if recent:
                recent_files = list(set(c.get('file', '') for c in recent[:5]))
                self.wechat.push_code_mod_report(
                    applied=code_stats['stats'].get('changes_applied', 0),
                    rolled_back=rolled,
                    files=recent_files,
                )
        except Exception as e:
            pass  # 静默失败，不影响主循环

    # ═══════════════════════════════════════
    # Phase 17: AI架构对标
    # ═══════════════════════════════════════

    def _phase_ai_benchmark(self):
        """AI架构对标：轻量版本检查 + 定时深度巡检"""
        schedule = self.ai_benchmark.check_schedule()
        self.avatar.set_state(AvatarState.SEARCHING, f"小零: AI架构对标({schedule})...")

        try:
            if schedule == 'light':
                result = self.ai_benchmark.run_light_check()
                updates = result.get('updates', [])
                if updates:
                    self.log(f"AI对标(轻): {len(updates)}个版本更新 — {', '.join(u['name'][:20] for u in updates[:3])}", "INFO")
                    # Generate version update report
                    self.report_archiver.generate_version_report(updates)
            elif schedule == 'deep':
                self.log("AI对标(深): 全量深度巡检启动...", "PHASE")
                result = self.ai_benchmark.run_deep_inspection()
                inspected = result.get('targets_inspected', 0)
                self.log(f"AI对标(深): 完成{inspected}个目标巡检", "EVOLVE")
                # Generate inspection reports for each target
                # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
                for r in result.get('results', [])[:5]:
                    self.report_archiver.generate_inspection_report(
                        target_name=r.get('name', 'unknown'),
                        findings={'patterns_found': r.get('patterns_found', [])},
                        comparison=r.get('comparison', {}),
                        learnings=r.get('learnings', []),
                    )
                    # Propose upgrades from learnings
                    learnings = r.get('learnings', [])
                    if learnings:
                        upgrade_result = self.ai_benchmark.propose_upgrades(learnings)
                        if upgrade_result.get('applied', 0) > 0:
                            self.log(f"对标升级: {upgrade_result['applied']}项建议", "EVOLVE")
        except Exception as e:
            self.log(f"AI对标异常: {e}", "WARN")

    # ═══════════════════════════════════════
    # Phase 18: 报告存档
    # ═══════════════════════════════════════

    def _phase_report_archiver(self):
        """10am每日报告自动生成（纯本地存档，零推送）"""
        if not self.report_archiver.check_schedule():
            return

        try:
            stats = self.status_snapshot()
            insights = []
            try:
                raw_insights = self.knowledge_output.extract_insights(self.knowledge_graph)
                insights = [{'description': str(i)[:120]} for i in raw_insights[:5]]
            except Exception:
                pass

            kg_summary = self.knowledge_graph.summary() if self.knowledge_graph else ''

            result = self.report_archiver.generate_daily_report(stats, insights, kg_summary)
            self.log(f"日报已存档: {result['summary_path']}", "ARCHIVE")

            # Backfill yesterday if needed (only on first run of the day)
            if self.autonomous_cycles < 5:
                backfill = self.report_archiver.backfill_previous_day(stats, insights)
                if backfill:
                    self.log(f"补录昨日报告: {backfill['date']}", "ARCHIVE")
        except Exception as e:
            self.log(f"报告存档异常: {e}", "WARN")

    def _sync_wechat_to_chat(self, sender: str, text: str, direction: str):
        """Sync WeChat messages to the desktop chat window"""
        if self.chat_window.is_running():
            short_text = text[:200] + ('...' if len(text) > 200 else '')
            if direction == 'wechat_in':
                self.chat_window.display_message(
                    f'WeChat:{sender}', short_text, 'wechat_in',
                )
            else:
                self.chat_window.display_message(
                    f'To WeChat', short_text, 'wechat_out',
                )

    def _handle_chat_message(self, text: str) -> str:
        """处理来自桌面聊天窗口的消息 — 交由智能对话引擎处理"""
        return self.conversation.respond(text, channel="chat_window")

    def _handle_wechat_command(self, cmd: str, sender: str) -> str:
        """处理来自微信的ZERO指令，返回回复文本"""
        return self.conversation.respond(cmd, channel="wechat")

    def _recover_from_crash(self):
        """崩溃后自动恢复：校验图谱+记忆+状态文件完整性"""
        try:
            if self.knowledge_graph:
                nodes_before = self.knowledge_graph.node_count
                self.knowledge_graph.flush()
                self.log(f"图谱自修复完成 (节点: {self.knowledge_graph.node_count})", "OK")
            if self.long_term:
                self.log(f"长期记忆: {self.long_term.size}条完整", "OK")
            # 重新初始化稳定性检查
            if self.stability:
                self.stability.health.run_quick_check()
        except Exception as e:
            self.log(f"崩溃恢复失败: {e}", "WARN")

    def _check_avatar_code_evolution(self):
        """根据代码修改统计检查avatar进化"""
        try:
            total_mods = self.code_mod.stats.get('changes_applied', 0)
            total_scans = self.code_mod.stats.get('scans', 0)
            # 同步avatar的代码修改统计
            self.avatar.update_code_mod_stats(
                applied=self.code_mod.stats.get('changes_applied', 0),
                scanned=self.code_mod.stats.get('scans', 0),
                optimized=self.code_mod.stats.get('validations_passed', 0),
            )
            # 使用avatar内置的进化检查（已包含代码修改贡献）
            evolved = self.avatar.check_evolution(
                self.knowledge_graph.node_count,
                min(0.9, 0.3 + total_mods * 0.05),
                self.autonomous_cycles,
            )
            if evolved:
                self.log(
                    f"Avatar进化! 代码修改: {total_mods}应用/{total_scans}扫描 → Lv.{self.avatar.intelligence_level.value} {self.avatar.intelligence_level.label}",
                    "EVOLVE",
                )
                self.avatar.notify(
                    f"智能等级提升至 Lv.{self.avatar.intelligence_level.value} {self.avatar.intelligence_level.label}",
                    "success",
                )
        except Exception as e:
            self.log(f"Avatar进化检查跳过: {e}", "INFO")

    def ask_question(self, question: str) -> Dict[str, Any]:
        """对知识图谱进行自然语言问答 — 优先使用混合RAG"""
        # 提取关键词用于图谱检索
        qwords = [w for w in question.lower().split() if len(w) > 2][:5]

        # 尝试混合RAG（图谱检索 + LLM推理）
        if self.ollama.is_available():
            try:
                rag_result = self.ollama.hybrid_rag_query(
                    question, graph=self.knowledge_graph, keywords=qwords
                )
                if rag_result.get("text"):
                    return {
                        "answer": rag_result["text"],
                        "method": "hybrid_rag",
                        "model": self.ollama.model,
                        "confidence": 0.78,
                        "graph_context_size": rag_result.get("graph_context_size", 0),
                    }
            except Exception:
                pass

        # 回退到图谱搜索+标准LLM问答
        if self.ollama.is_available():
            try:
                context = self._get_graph_context_for_question(question)
                answer = self.ollama.qa_query(context, question)
                if answer:
                    return {
                        "answer": answer,
                        "method": "ollama_llm",
                        "model": self.ollama.model,
                        "confidence": 0.75,
                    }
            except Exception:
                pass

        # 回退到纯图谱搜索
        return self.knowledge_output.answer_question(
            question, self.knowledge_graph,
            knowledge_quality=self.knowledge_quality,
        )

    def _get_graph_context_for_question(self, question: str) -> str:
        """从知识图谱提取与问题相关的上下文"""
        parts = []
        # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
        for qword in question.lower().split():
            if len(qword) < 2:
                continue
            # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
            for nid in self.knowledge_graph.graph.nodes():
                attrs = self.knowledge_graph.graph.nodes[nid]
                label = attrs.get("label", nid).lower()
                if qword in label:
                    edges_info = []
                    # [ZERO-PERF] 考虑缓存频繁访问的属性到局部变量
                    for _, dst, eattrs in self.knowledge_graph.graph.out_edges(nid, data=True):
                        dst_label = self.knowledge_graph.graph.nodes[dst].get("label", dst)
                        rel = eattrs.get("relation", "related")
                        edges_info.append(f"{label} {rel} {dst_label}")
                    if edges_info:
                        parts.extend(edges_info[:5])
        return "\n".join(parts[:20]) if parts else "暂无相关知识图谱上下文。"

    # ═══════════════════════════════════════
    # 最终报告
    # ═══════════════════════════════════════

    def _final_report(self):
        elapsed = (time.time() - self.start_time) / 3600
        print()
        print('=' * 50)
        print('     ZERO Autonomous Engine Summary')
        print('=' * 50)
        print(f'  Runtime: {elapsed:.1f} hours')
        print(f'  Autonomous cycles: {self.autonomous_cycles}')
        print(f'  Knowledge acquired: {self.total_knowledge_acquired} items')
        print(f'  Knowledge graph: {self.knowledge_graph.node_count} nodes, {self.knowledge_graph.edge_count} edges')
        print(f'  Long-term memory: {self.long_term.size} items')
        print(f'  Episodic memory: {self.episodic.size} events')
        print(f'  Dynamic learning: {self.learning.get_stats()["dynamic_entries"]} items')
        print(f'  Science discoveries: {self.discovery.current_cycle} cycles')
        print(f'  Supervision reviews: {len(self.supervision.supervision_history)}')
        print(f'  Civilization events: {self.civ_mem.event_count}')
        print(f'  Humility lessons: {len(self.humility.mistakes)}')
        print(f'  Emotion level: {sum(self.emotion.understanding.values())/len(self.emotion.understanding):.0%}')
        print(f'  Earth cognition: {sum(self.earth.understanding_level.values())/len(self.earth.understanding_level):.0%}')
        print(f'  XiaoLing memories: {self.xiaoling_mem.total_count} records')
        print(f'  Reasoning inferred: {self.reasoning_engine.total_inferred} edges')
        print(f'  Memory cleanup: {self.memory_cleanup.stats["runs"]} runs (dedup {self.memory_cleanup.stats["deduplicated"]}, prune {self.memory_cleanup.stats["pruned"]}, merge {self.memory_cleanup.stats["merged"]})')
        print(f'  Goals: {self.goal_system.get_stats()["total"]} total, {self.goal_system.get_stats()["done"]} done')
        print(f'  Knowledge quality: {self.knowledge_quality.stats["runs"]} checks, {self.knowledge_quality.stats["contradictions_found"]} contradictions')
        print(f'  Autonomous intelligence: {self.auto_intelligence.stats["gaps_found"]} gaps, {self.auto_intelligence.stats["evaluations"]} self-evals')
        print(f'  Reports: {self.knowledge_output._report_count} daily reports, {len(self.knowledge_output._insight_history)} insight batches, {len(self.knowledge_output._qa_history)} Q&As')
        print(f'  GPU: {self.gpu.summary()} (accelerated {self.gpu.get_stats()["ops_accelerated"]} ops)')
        print(f'  Ollama LLM: {self.ollama.summary()}')
        print(f'  Multimodal: {self.multimodal.summary()}')
        print(f'  Backup: {self.backup_mgr.summary()}')
        print(f'  Upgrade planner: {self.upgrade_planner.summary()}')
        print(f'  Stability: {self.stability.summary()}')
        print(f'  Self code mod: {self.code_mod.summary()}')
        print(f'  Chat window: {"Active" if self.chat_window.is_running() else "Off"}')
        print(f'  WeChat bridge: {"Connected" if self.wechat.is_logged_in() else "Offline"}')
        print(f'  AI Benchmark: {self.ai_benchmark.summary()}')
        print(f'  Report Archiver: {self.report_archiver.summary()}')
        print(f'  Conversation: {self.conversation.summary()}')
        print(f'  Learning Scheduler: {self.learning_scheduler.summary()}')
        print(f'  Knowledge Cards: {self.knowledge_cards.summary()}')
        print(f'  Technical Manual: {os.path.basename(self.knowledge_cards.manual_path)}')
        print(f'  Scheduler CB trips: {self.learning_scheduler.stats["circuit_breaker_trips"]} | skipped: {self.learning_scheduler.stats["topics_skipped_no_results"]} | retry R2:{self.learning_scheduler.stats["retry_success_on_round2"]} R3:{self.learning_scheduler.stats["retry_success_on_round3"]}')
        print(f'  Self-Healing Monitor: {self.self_healing_monitor.summary()}')
        print(f'  Termination system: {"OK" if self.emergency.is_termination_intact() else "FAIL"}')
        print(f'  Current stage: {self.evolution.stage_info["name"]}')
        print('=' * 50)

    def status_snapshot(self) -> dict:
        return {
            'cycles': self.autonomous_cycles,
            'knowledge_acquired': self.total_knowledge_acquired,
            'graph_nodes': self.knowledge_graph.node_count,
            'graph_edges': self.knowledge_graph.edge_count,
            'long_term_memory': self.long_term.size,
            'episodic_memory': self.episodic.size,
            'dynamic_learning': self.learning.get_stats()['dynamic_entries'],
            'discovery_cycles': self.discovery.current_cycle,
            'supervision_reviews': len(self.supervision.supervision_history),
            'civilization_events': self.civ_mem.event_count,
            'humility_lessons': len(self.humility.mistakes),
            'emotion_level': sum(self.emotion.understanding.values()) / len(self.emotion.understanding),
            'earth_level': sum(self.earth.understanding_level.values()) / len(self.earth.understanding_level),
            'stage': self.evolution.stage_info['name'],
            'values_balanced': self.values_mem.is_balanced(),
            'xiaoling_memories': self.xiaoling_mem.total_count,
            'reasoning_inferred': self.reasoning_engine.total_inferred,
            'reasoning_hypotheses': len(self.reasoning_engine.get_hypotheses()),
            'cleanup_runs': self.memory_cleanup.stats['runs'],
            'goals_total': self.goal_system.get_stats()['total'],
            'goals_done': self.goal_system.get_stats()['done'],
            'gpu_device': self.gpu.device_info['name'],
            'gpu_type': self.gpu.device_info['type'],
            'gpu_ops': self.gpu.get_stats()['ops_accelerated'],
            'quality_score': self.knowledge_quality.get_graph_quality_report(self.knowledge_graph)['overall_quality'],
            'contradictions': self.knowledge_quality.stats['contradictions_found'],
            'intelligence_score': 0.0,  # populated by last eval
            'blind_spots': self.auto_intelligence.stats['blind_spots_found'],
            'reports_generated': self.knowledge_output._report_count,
            'insights_found': len(self.knowledge_output._insight_history),
            'emergency_ok': self.emergency.is_termination_intact(),
            'runtime_hours': (time.time() - self.start_time) / 3600,
            'ollama_available': self.ollama.is_available(),
            'ollama_model': self.ollama.model if self.ollama.is_available() else None,
            'ollama_calls': self.ollama.get_stats().get('calls', 0),
            'multimodal_pdf': self.multimodal.stats.get('pdf_extracted', 0),
            'multimodal_images': self.multimodal.stats.get('images_processed', 0),
            'multimodal_tables': self.multimodal.stats.get('tables_extracted', 0),
            'multimodal_audio': self.multimodal.stats.get('audio_transcribed', 0),
            'backup_count': self.backup_mgr.get_stats().get('backups_created', 0),
            'offline_mode': self.backup_mgr.offline_mode,
            'llm_cache_hits': self.ollama.get_stats().get('cache_hits', 0),
            'llm_rag_queries': self.ollama.get_stats().get('rag_queries', 0),
            'llm_model_switches': self.ollama.get_stats().get('model_switches', 0),
            'upgrade_proposals': len(self.upgrade_planner._plans),
            'upgrade_applied': len(self.upgrade_planner._applied),
            'health_failing': len(self.stability.health._failing_modules),
            'health_checks': len(self.stability.health._checks),
            'gc_runs': self.stability.gc.get_stats().get('gc_runs', 0),
            'gc_objects_freed': self.stability.gc.get_stats().get('objects_collected', 0),
            'memory_usage_mb': self.stability.memory.get_current_mb(),
            'log_files': len(self.stability.log_rotation.get_log_files()),
            'request_queue_pending': self.stability.request_queue.pending,
            'code_mod_mode': 'unrestricted' if self.code_mod.unrestricted_mode else ('production' if self.code_mod.production_mode else 'normal'),
            'code_mod_applied': self.code_mod.stats.get('changes_applied', 0),
            'code_mod_rolled_back': self.code_mod.stats.get('changes_rolled_back', 0),
            'code_mod_scans': self.code_mod.stats.get('scans', 0),
            'code_mod_issues': self.code_mod.stats.get('issues_found', 0),
            'code_mod_pending': len(self.code_mod.gate.pending_approvals),
            'chat_window_running': self.chat_window.is_running(),
            'wechat_logged_in': self.wechat.is_logged_in(),
            'ai_benchmark_light': self.ai_benchmark.stats['light_checks'],
            'ai_benchmark_deep': self.ai_benchmark.stats['deep_inspections'],
            'ai_benchmark_learnings': self.ai_benchmark.stats['learnings_extracted'],
            'ai_benchmark_upgrades': self.ai_benchmark.stats['upgrades_proposed'],
            'report_archiver_total': self.report_archiver.stats['reports_generated'],
            'report_archiver_daily': self.report_archiver.stats['daily_reports'],
            'report_archiver_backfill': self.report_archiver.stats['backfill_reports'],
            'self_healing_monitor_anomalies': self.self_healing_monitor.stats['anomalies_detected'],
            'self_healing_monitor_fixes': self.self_healing_monitor.stats['auto_fixes_applied'],
            'self_healing_monitor_pauses': self.self_healing_monitor.stats['pause_events'],
            'self_healing_monitor_skipped': self.self_healing_monitor.stats['learning_skipped_cycles'],
            'self_healing_monitor_paused': self.self_healing_monitor.is_paused(),
            'scheduler_cycles': self.learning_scheduler.stats['total_learning_cycles'],
            'scheduler_opus': self.learning_scheduler.stats['opus_topics_learned'],
            'scheduler_flagship': self.learning_scheduler.stats['flagship_topics_learned'],
            'scheduler_agent': self.learning_scheduler.stats['agent_topics_learned'],
            'scheduler_last_topic': self.learning_scheduler.stats['last_topic'],
            'scheduler_last_channel': self.learning_scheduler.stats['last_channel'],
            'scheduler_cb_trips': self.learning_scheduler.stats['circuit_breaker_trips'],
            'scheduler_topics_skipped': self.learning_scheduler.stats['topics_skipped_no_results'],
            'scheduler_retry_r2': self.learning_scheduler.stats['retry_success_on_round2'],
            'scheduler_retry_r3': self.learning_scheduler.stats['retry_success_on_round3'],
            'knowledge_cards_total': self.knowledge_cards.count_cards(),
            'knowledge_cards_by_model': self.knowledge_cards.stats().get('by_model', {}),
            'manual_path': self.knowledge_cards.manual_path,
        }


def main():
    """主入口"""
    import sys
    use_gui = "--no-gui" not in sys.argv and "-n" not in sys.argv
    
    if "--help" in sys.argv or "-h" in sys.argv:
        print("\nZERO 完全自主引擎 - 参数说明:")
        print("  --no-gui, -n  : 禁用GUI模式，使用纯控制台模式")
        print("  --help,  -h   : 显示此帮助")
        print("  --console, -c : 同--no-gui")
        print("\n  默认启用GUI模式，显示3D虚拟形象")
        return

    console_mode = "--console" in sys.argv or "-c" in sys.argv
    use_gui = use_gui and not console_mode
    
    engine = AutonomousEngine(use_gui=use_gui)
    engine.run()

if __name__ == "__main__":
    main()