#!/usr/bin/env python3
"""
ZERO — 地球文明共生智能系统
Zero Evolutionary Recursive Omninet

主入口：启动 ZERO 系统，进入交互式控制台
"""
import sys
import os
import time
from typing import Dict, Any

# 确保项目根目录在 path 中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from rich import print as rprint

from config import ZeroConfig, GrowthStage
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
from agents.orchestrator import AgentOrchestrator
from knowledge.graph import KnowledgeGraph
from knowledge.trust import TrustEngine
from knowledge.crawler import Crawler
from knowledge.parser import parse_content
from knowledge.summarizer import summarize_knowledge, generate_report


class MemorySystem:
    """内存系统聚合器"""
    def __init__(self, config: ZeroConfig):
        self.short_term = ShortTermMemory()
        self.long_term = LongTermMemory(storage_path=config.data_dir + "/long_term_memory.json")
        self.episodic = EpisodicMemory(storage_path=config.data_dir + "/episodic_memory.json")
        self.values = ValuesMemory(storage_path=config.data_dir + "/values_memory.json")
        self.civilization = CivilizationMemory(storage_path=config.data_dir + "/civilization_memory.json")


class Zero:
    """
    ZERO 系统主类
    整合所有模块，提供统一的系统接口
    """

    def __init__(self, config: ZeroConfig = None):
        self.config = config or ZeroConfig()
        self.console = Console()

        # 确保数据目录存在
        os.makedirs(self.config.data_dir, exist_ok=True)

        # === 核心系统初始化（按架构图顺序） ===
        self.root_law = RootLaw()                          # 1. 人类文明保护核心
        self.ethics = EthicsEngine()                       # 2. 文明伦理系统
        self.evolution = EvolutionController(              # 3. 自我进化控制器
            initial_stage=self.config.initial_stage
        )
        self.civilization = CivilizationAnalyzer()         # 4. 全球文明状态分析层
        self.discovery = DiscoveryEngine(storage_path=self.config.data_dir + "/discovery.json")  # 5. 科学发现引擎
        self.simulation = WorldSimulation(                 # 6. 世界模拟系统
            sandbox_enabled=self.config.sandbox_enabled
        )
        self.memory = MemorySystem(self.config)            # 7. 长期人格与记忆系统
        self.learning = RealTimeLearning(                  # 8. 实时学习神经网络
            data_dir=self.config.data_dir
        )
        self.perception = PerceptionSystem()               # 9. 多模态感知系统

        # === 文明认知系统（架构文档第四章） ===
        self.earth_cognition = EarthCognition(storage_path=self.config.data_dir + "/earth_cognition.json")  # 地球认知模块
        self.human_history = HumanHistory()                # 人类历史模块
        self.emotion_cognition = EmotionCognition()        # 人类情感认知系统

        # === 人格与谦逊 ===
        self.humility = HumilityProtocol()                 # 文明谦逊协议

        # === 安全系统 ===
        self.emergency_termination = EmergencyTermination()  # 人类紧急终止
        self.supervision = SupervisionSystem(              # 多模型监督
            root_law=self.root_law,
            ethics_engine=self.ethics,
            simulation=self.simulation,
            civilization_analyzer=self.civilization,
        )

        # === 知识系统 ===
        self.knowledge_graph = KnowledgeGraph(
            storage_path=self.config.data_dir + "/knowledge_graph.json"
        )
        self.trust = TrustEngine()
        self.crawler = Crawler()

        # === 多Agent协作 ===
        self.orchestrator = AgentOrchestrator(
            root_law=self.root_law,
            memory_system=self.memory,
            ethics_engine=self.ethics,
        )

        # 系统状态
        self.start_time = time.time()
        self.session_count = 0
        self.initialized = True

    def query(self, task: str) -> Dict[str, Any]:
        """
        ZERO 主查询接口
        完整的数据流经所有10层架构
        """
        self.session_count += 1

        # 1. 感知
        perception_result = self.perception.perceive(task)
        self.evolution.record_learning(items_count=1)

        # 2. 阶段检查
        try:
            self.evolution.check_permission("network")
        except Exception as e:
            pass  # 记录但不阻止

        # 3. 联网获取信息（如果阶段允许）
        web_data = []
        if self.evolution.can_use_network():
            try:
                results = self.crawler.search_and_fetch(task, max_results=3)
                for r in results:
                    # 可信度评分
                    trust_result = self.trust.score(r["text"], url=r["url"])
                    r["trust"] = trust_result

                    # 解析知识
                    parsed = parse_content(r["text"])
                    r["parsed_knowledge"] = len(parsed)

                    # 存入知识图谱
                    keywords = []
                    for unit in parsed:
                        for kw in unit.get("keywords", []):
                            if kw not in keywords:
                                keywords.append(kw)
                                self.knowledge_graph.add_concept(
                                    kw, concept_type="keyword",
                                    confidence=trust_result["total_score"],
                                )

                    web_data.append(r)

                # 学习记录
                for r in web_data:
                    self.learning.learn(
                        topic=task,
                        content=r.get("text", "")[:500],
                        source=r.get("url", ""),
                        confidence=r.get("trust", {}).get("total_score", 0.5),
                    )
            except Exception as e:
                pass  # 网络失败不阻塞系统

        # 4. 多Agent分析
        orchestration_result = self.orchestrator.execute(task)

        # 5. 科学发现循环（如果适用）
        discovery_results = None
        if self._is_scientific_query(task):
            discovery_results = self.discovery.run_discovery_cycle(task, "general")

        # 6. 文明影响评估
        civilization_impact = None
        if len(task) > 10:
            self.civilization.record_indicator("科技进步", 0.7, source="ZERO分析")
            health = self.civilization.analyze_health()
            civilization_impact = {
                "overall_health": health.get("overall_health"),
                "risks_count": len(health.get("risks", [])),
            }

        # 7. 记忆存储
        self.memory.episodic.record(
            event_type="zero_query",
            description=task,
            context={"session": self.session_count, "agents": len(self.orchestrator.agents)},
            outcome=orchestration_result.get("summary", "")[:200],
        )

        return {
            "task": task,
            "session": self.session_count,
            "stage": self.evolution.stage_info["name"],
            "network_results": len(web_data),
            "agent_analysis": orchestration_result,
            "discovery": discovery_results,
            "civilization_impact": civilization_impact,
            "trust_evaluations": len(web_data),
            "perception": perception_result.to_dict(),
        }

    def _is_scientific_query(self, task: str) -> bool:
        """判断是否科学类查询"""
        science_keywords = ["为什么", "发现", "机制", "原理", "规律", "假设", "理论",
                           "why", "how", "mechanism", "principle"]
        task_lower = task.lower()
        return any(kw in task_lower for kw in science_keywords)

    def status(self) -> str:
        """获取系统状态"""
        lines = [
            f"╔══════════════════════════════════════════╗",
            f"║   {self.config.full_name} ({self.config.version}) ║",
            f"║   {self.config.chinese_name}                  ║",
            f"╚══════════════════════════════════════════╝",
            f"",
            self.evolution.status_report(),
            f"",
            f"═══ 系统模块状态 ═══",
            f"  根法则守护: ✓ 活跃 ({self.root_law.law_count} 条法则)",
            f"  {self.memory.short_term.summary()}",
            f"  {self.memory.long_term.summary()}",
            f"  {self.memory.episodic.summary()}",
            f"  {self.memory.values.summary()}",
            f"  {self.memory.civilization.summary()}",
            f"  {self.knowledge_graph.summary()}",
            f"  {self.learning.summary()}",
            f"  {self.discovery.summary()}",
            f"  {self.simulation.summary()}",
            f"  {self.perception.summary()}",
            f"  {self.trust.summary()}",
            f"  {self.crawler.summary()}",
            f"  {self.earth_cognition.summary()}",
            f"  {self.human_history.summary()}",
            f"  {self.emotion_cognition.summary()}",
            f"  {self.humility.summary()}",
            f"  {self.emergency_termination.summary()}",
            f"  {self.supervision.summary()}",
            f"",
            f"  可用Agent: {len(self.orchestrator.AGENT_REGISTRY)} 种",
            f"  已初始化Agent: {len(self.orchestrator.agents)} 个",
            f"  会话数: {self.session_count}",
            f"  运行时长: {self.evolution.age_description}",
        ]
        return "\n".join(lines)

    def root_law_report(self) -> str:
        return self.root_law.report()

    def ethics_report(self) -> str:
        return self.ethics.get_values_report()

    def agent_report(self) -> str:
        return self.orchestrator.get_session_report()


# [ZERO-AUTO] 重构建议: 函数 main 约117行，建议拆分
# [ZERO-AUTO] 重构建议: 函数 main 约117行，建议拆分
def main():
    """ZERO 主入口"""
    console = Console()

    # Banner
    banner = """
    ╔══════════════════════════════════════════════════╗
    ║                                                  ║
    ║   ███████╗ ███████╗ ██████╗   ██████╗            ║
    ║   ╚══███╔╝ ██╔════╝ ██╔══██╗ ██╔═══██╗           ║
    ║     ███╔╝  █████╗   ██████╔╝ ██║   ██║           ║
    ║    ███╔╝   ██╔══╝   ██╔══██╗ ██║   ██║           ║
    ║   ███████╗ ███████╗ ██║  ██║ ╚██████╔╝           ║
    ║   ╚══════╝ ╚══════╝ ╚═╝  ╚═╝  ╚═════╝            ║
    ║                                                  ║
    ║   地球文明共生智能系统                              ║
    ║   Zero Evolutionary Recursive Omninet            ║
    ║   v0.1.0                                         ║
    ╚══════════════════════════════════════════════════╝
    """
    console.print(banner, style="bold cyan")
    console.print("  ZERO 不是一个聊天机器人，而是文明共生智能网络。\n", style="italic")

    # 初始化系统
    console.print("[bold yellow]正在初始化 ZERO 系统...[/bold yellow]")
    config = ZeroConfig()
    zero = Zero(config)

    # 显示初始状态
    console.print(f"\n[green]✓[/green] 系统初始化完成")
    console.print(f"  当前阶段: [cyan]{zero.evolution.stage_info['name']}[/cyan]")
    console.print(f"  根法则: [green]{zero.root_law.law_count} 条已锁定[/green]")
    console.print(f"  可用Agent: [cyan]{len(zero.orchestrator.AGENT_REGISTRY)} 种[/cyan]")

    console.print("\n输入 [bold]/help[/bold] 查看命令，[bold]/quit[/bold] 退出")

    # 交互循环
    while True:
        try:
            user_input = console.input("\n[bold cyan]ZERO> [/bold cyan]").strip()

            if not user_input:
                continue

            # 命令处理
            if user_input.startswith("/"):
                cmd = user_input[1:].lower()
                if cmd == "quit" or cmd == "exit" or cmd == "q":
                    console.print("\n[bold yellow]ZERO 正在关闭...[/bold yellow]")
                    console.print(f"会话数: {zero.session_count}")
                    console.print("使命: 保护人类文明，推动科学进步，放大文明潜力")
                    console.print("[bold green]ZERO 已关闭。[/bold green]")
                    break
                elif cmd == "help":
                    _show_help(console)
                elif cmd == "status":
                    console.print(zero.status())
                elif cmd == "rootlaw":
                    console.print(zero.root_law_report())
                elif cmd == "ethics":
                    console.print(zero.ethics_report())
                elif cmd == "agents":
                    console.print("\n".join(
                        f"  [{a['type']}] {a['description']}"
                        for a in zero.orchestrator.list_agents()
                    ))
                elif cmd == "stage":
                    console.print(zero.evolution.status_report())
                elif cmd == "memory":
                    _show_memory(console, zero)
                elif cmd == "discoveries":
                    disc = zero.discovery.get_discoveries()
                    if disc:
                        for d in disc:
                            console.print(f"  ✓ {d['hypothesis'][:100]}")
                    else:
                        console.print("  暂无已确认的科学发现")
                else:
                    console.print(f"[red]未知命令: {cmd}[/red]")
                continue

            # 正常查询
            console.print(f"\n[dim]分析: 感知 → 根法则校验 → 多Agent协作 → 伦理评估...[/dim]")
            result = zero.query(user_input)

            # 展示结果
            if result["agent_analysis"]["success"]:
                summary = result["agent_analysis"].get("summary", "")
                # 用 Panel 包装结果
                panel = Panel(
                    summary[:1500],
                    title=f"ZERO 分析结果 (会话 #{result['session']})",
                    border_style="cyan",
                )
                console.print(panel)

                # 简要元数据
                agents_used = result["agent_analysis"].get("agents_used", [])
                network_count = result.get("network_results", 0)
                meta = f"[dim]参与Agent: {', '.join(agents_used)} | 联网: {network_count}条 | 阶段: {result['stage']}[/dim]"
                console.print(meta)
            else:
                error_msg = result["agent_analysis"].get("error", "未知错误")
                console.print(f"[red]✗ 分析被阻止: {error_msg}[/red]")

            # 自动推进成长阶段
            new_stage = zero.evolution.try_advance_stage()
            if new_stage != zero.evolution.stage:
                console.print(f"[yellow]⚡ 阶段已推进至: {zero.evolution.stage_info['name']}[/yellow]")

        except KeyboardInterrupt:
            console.print("\n[bold yellow]ZERO 已中断。[/bold yellow]")
            break
        except Exception as e:
            console.print(f"[red]系统异常: {e}[/red]")


def _show_help(console: Console):
    """显示帮助"""
    table = Table(title="ZERO 命令参考")
    table.add_column("命令", style="cyan")
    table.add_column("说明")

    commands = [
        ("<查询内容>", "向 ZERO 提交分析任务"),
        ("/status", "查看系统完整状态"),
        ("/rootlaw", "查看根法则报告"),
        ("/ethics", "查看文明价值系统"),
        ("/agents", "列出所有Agent类型"),
        ("/stage", "查看成长阶段详情"),
        ("/memory", "查看记忆系统状态"),
        ("/discoveries", "查看科学发现"),
        ("/help", "显示此帮助"),
        ("/quit", "退出 ZERO"),
    ]
    for cmd, desc in commands:
        table.add_row(cmd, desc)

    console.print(table)


def _show_memory(console: Console, zero: Zero):
    """显示记忆系统详情"""
    console.print(f"[bold]短期记忆:[/bold] {zero.memory.short_term.size} 条")
    recent = zero.memory.short_term.get_recent(3)
    for item in recent:
        console.print(f"  - {str(item)[:200]}")

    console.print(f"\n[bold]长期知识:[/bold] {zero.memory.long_term.size} 条")
    tags = zero.memory.long_term.get_all_tags()
    if tags:
        console.print(f"  标签: {', '.join(tags[:10])}")

    console.print(f"\n[bold]情景记忆:[/bold] {zero.memory.episodic.size} 条")
    lessons = zero.memory.episodic.get_lessons()
    if lessons:
        console.print(f"  最近经验: {lessons[-1][:200] if lessons else '无'}")

    console.print(f"\n[bold]价值记忆:[/bold] {zero.memory.values.summary()}")
    console.print(f"[bold]文明记忆:[/bold] {zero.memory.civilization.summary()}")


if __name__ == "__main__":
    main()