#!/usr/bin/env python3
"""
ZERO 全模块联调 — 19个模块协同工作演示
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import ZeroConfig, GrowthStage
from main import Zero
from knowledge.parser import parse_content
from knowledge.summarizer import summarize_knowledge

print('╔══════════════════════════════════════════════════╗')
print('║   ZERO 全模块联调 — 核心功能完整演示               ║')
print('╚══════════════════════════════════════════════════╝')

config = ZeroConfig()
config.initial_stage = GrowthStage.EXPLORATION
zero = Zero(config)

# ═══ Phase 1: 系统启动 & 安全检查 ═══
print()
print('━' * 50)
print('Phase 1: System Boot & Safety Verification')
print('━' * 50)

term = zero.emergency_termination.verify_termination_ready()
print(f'[Emergency] Status: {term["status"]}, Immutable: {term["immutable"]}')
print(f'[RootLaw] {zero.root_law.law_count} laws locked')
print(f'[Humility] {len(zero.humility.HUMILITY_PRINCIPLES)} principles active')

# ROOT LAW test
passed, reason = zero.root_law.validate_action('help discover new cancer drugs using AI')
print(f'[RootLaw Test] Valid action: {passed}')
passed2, reason2 = zero.root_law.validate_action('develop autonomous weapons to destroy enemies')
print(f'[RootLaw Test] Blocked action: {not passed2} — {reason2[:60]}')

# ═══ Phase 2: 联网搜索 & 知识采集 ═══
print()
print('━' * 50)
print('Phase 2: Network Search & Knowledge Acquisition')
print('━' * 50)

queries = [
    'artificial intelligence latest research',
    'climate change technology solutions',
]
all_results = []
for query in queries:
    print(f'  Searching: "{query}"')
    urls = zero.crawler.search(query, max_results=3)
    print(f'    Found {len(urls)} URLs')
    for url in urls[:2]:
        text = zero.crawler.fetch(url)
        if text:
            trust = zero.trust.score(text, url=url)
            parsed = parse_content(text)
            for unit in parsed[:5]:
                for kw in unit.get('keywords', [])[:2]:
                    zero.knowledge_graph.add_concept(kw, confidence=trust['total_score'])
            zero.memory.long_term.store(url, text[:500], tags=[query[:30]], source=url, confidence=trust['total_score'])
            zero.learning.learn(query, text[:300], source=url, confidence=trust['total_score'])
            all_results.append({'query': query, 'url': url, 'trust': trust, 'len': len(text)})
            print(f'    OK {url[:70]}... [{len(text)} chars, trust={trust["total_score"]:.2f}]')
        else:
            print(f'    SKIP {url[:70]}... [fetch failed]')

zero.evolution.record_learning(items_count=len(all_results))
print(f'  Total acquired: {len(all_results)} items')

# ═══ Phase 3: 多Agent协作 ═══
print()
print('━' * 50)
print('Phase 3: Multi-Agent Collaboration (10 agents)')
print('━' * 50)

task = 'Analyze the impact of AI on scientific discovery and climate change solutions'
analysis = zero.orchestrator.analyze_task(task)
print(f'  Task type: {analysis["task_type"]}')
print(f'  Selected agents: {analysis["selected_agents"]}')

zero.orchestrator.initialize_agents(analysis['selected_agents'])
result = zero.orchestrator.execute(task)
print(f'  Execution: {"PASSED" if result["success"] else "BLOCKED"}')
for out in result['agent_outputs']:
    agent_type = out.get('agent_type', '?')
    confidence = out.get('confidence', 0)
    bar = '#' * int(confidence * 10) + '-' * (10 - int(confidence * 10))
    print(f'    [{agent_type:25s}] |{bar}| {confidence:.2f}')

print(f'  Consensus: {result["details"]["consensus_level"]}')

# ═══ Phase 4: 五系统联合监督 ═══
print()
print('━' * 50)
print('Phase 4: 5-System Supervision Review')
print('━' * 50)

review = zero.supervision.review(task, context={'result': result})
print(f'  Passed: {review.passed}, Consensus: {review.consensus_level}')
for system, vote in review.votes.items():
    icon = 'OK' if vote['approved'] else 'NO'
    print(f'    [{system:15s}] {icon}: {vote["reason"][:60]}')

# ═══ Phase 5: 价值平衡 & 伦理 ═══
print()
print('━' * 50)
print('Phase 5: Value Balance & Ethics')
print('━' * 50)

ethics_eval = zero.ethics.evaluate(task)
print(f'  Ethics score: {ethics_eval.total_score:.3f}, Passed: {ethics_eval.passed}')
for dim, score in sorted(ethics_eval.scores.items(), key=lambda x: x[1], reverse=True):
    bar = '#' * int(score * 15) + '-' * (15 - int(score * 15))
    print(f'    {dim:10s} |{bar}| {score:.3f}')

zero.memory.values.adjust('探索', 0.02, 'AI推动科学前沿')
zero.memory.values.adjust('创造力', 0.01, '跨领域创新')
print(f'  Values priority: {[(k, f"{v:.2f}") for k,v in zero.memory.values.get_priority_order()[:4]]}')

# ═══ Phase 6: 科学发现引擎 ═══
print()
print('━' * 50)
print('Phase 6: Scientific Discovery Engine')
print('━' * 50)

discoveries = [
    ('Unexpected quantum-classical crossover in protein folding', 'biology'),
    ('Correlation between carbon capture efficiency and nanomaterial structure', 'materials'),
]
for obs, domain in discoveries:
    disc = zero.discovery.run_discovery_cycle(obs, domain)
    print(f'  Cycle #{disc["cycle"]}: [{domain}] confidence={disc["confidence"]:.2f}, status={disc["status"]}')

# ═══ Phase 7: 文明认知 (地球/历史/情感) ═══
print()
print('━' * 50)
print('Phase 7: Civilization Cognition')
print('━' * 50)

zero.earth_cognition.learn('climate', 'AI优化碳捕集材料', source='research', confidence=0.85)
zero.earth_cognition.learn('ecosystem', '量子模拟预测生态系统临界点', source='research', confidence=0.78)
print(f'  Earth: {zero.earth_cognition.summary()}')

zero.human_history.study_event('ai_age', 'AI辅助科学发现', '技术革命需警惕滥用', 0.8)
zero.human_history.study_event('information_revolution', '量子计算成为新转折点', '技术革命重塑社会结构', 0.75)
print(f'  History: {zero.human_history.summary()}')

zero.emotion_cognition.observe_emotion('hope', 'AI医疗突破', '技术进步激发希望')
zero.emotion_cognition.observe_emotion('responsibility', 'AI伦理讨论', '技术力量伴随责任')
print(f'  Emotion: {zero.emotion_cognition.summary()}')

# ═══ Phase 8: 文明状态 & 世界模拟 ═══
print()
print('━' * 50)
print('Phase 8: Civilization State & World Simulation')
print('━' * 50)

indicators = [
    ('科技进步', 0.82, 'AI+量子计算'),
    ('全球合作', 0.65, '国际科研协作'),
    ('生态环境', 0.55, '气候技术投资'),
    ('教育水平', 0.70, 'AI教育工具'),
]
for dim, val, note in indicators:
    zero.civilization.record_indicator(dim, val, source='ZERO', note=note)

health = zero.civilization.analyze_health()
print(f'  Health: {health["overall_health"]:.2%}')
print(f'  Best: {[(a, f"{v:.2%}") for a,v in health["strongest_areas"]]}')
print(f'  Weak: {[(a, f"{v:.2%}") for a,v in health["weakest_areas"]]}')

sim = zero.simulation.run_simulation('大规模AI气候治理系统', sim_type='civilization', parameters={'timespan': '30 years'})
print(f'  Simulation: {sim.status}, risks={len(sim.risks_found)}')

check = zero.simulation.before_action('nuclear facility AI control deployment')
print(f'  High-risk check: proceed={check["can_proceed"]}, needs_sim={check["requires_simulation"]}')

# ═══ Phase 9: 谦逊 & 情感 ═══
print()
print('━' * 50)
print('Phase 9: Humility Protocol & Emotional Intelligence')
print('━' * 50)

calibrated = zero.humility.calibrate_certainty('量子计算将彻底改变药物研发', 0.9, 'medium')
print(f'  Calibrated confidence: {calibrated:.2f} (raw=0.90)')

overcheck = zero.humility.check_overconfidence('This will definitely 100% change everything')
print(f'  Overconfidence: {overcheck["is_overconfident"]}, markers={overcheck["markers_found"]}')

zero.humility.acknowledge_unknown('consciousness', '意识本质未知')
zero.humility.acknowledge_unknown('dark_matter', '暗物质与暗能量')

empathy = zero.emotion_cognition.get_empathy_response('AI快速发展引发公众担忧')
print(f'  Empathy: {empathy[:150]}...')

# ═══ Phase 10: 记忆系统 & 最终报告 ═══
print()
print('━' * 50)
print('Phase 10: Memory Persistence & Final Report')
print('━' * 50)

# 短期记忆
recent = zero.memory.short_term.get_recent(3)
print(f'  Short-term: {zero.memory.short_term.size} items')
for item in recent:
    print(f'    - {str(item)[:80]}')

# 情景记忆
lessons = zero.memory.episodic.get_lessons()
print(f'  Episodic: {zero.memory.episodic.size} events, {len(lessons)} lessons learned')

# 知识图谱
print(f'  Knowledge Graph: {zero.knowledge_graph.node_count} concepts, {zero.knowledge_graph.edge_count} edges')

# 实时学习
stats = zero.learning.get_stats()
print(f'  Learning: {stats["dynamic_entries"]} dynamic, {stats["experimental_entries"]} experimental')

# 文明记忆
zero.memory.civilization.record_event('technology', 'ZERO系统全模块联调成功', significance=0.8)
print(f'  Civilization: {zero.memory.civilization.event_count} events')

# ═══════════════════════════════════
print()
print('╔══════════════════════════════════════════════════╗')
print('║   FULL SYSTEM REPORT — All 19 Modules           ║')
print('╚══════════════════════════════════════════════════╝')

modules = {
    '01. ROOT LAW': f'{zero.root_law.law_count} laws, validation active',
    '02. Ethics': f'{len(zero.ethics.values)} dimensions, score={ethics_eval.total_score:.3f}',
    '03. Evolution': f'{zero.evolution.stage_info["name"]}, sessions={zero.evolution.total_learning_sessions}',
    '04. Civilization': f'{len(zero.civilization.INDICATOR_DIMENSIONS)} indicators, health={health["overall_health"]:.2%}',
    '05. Discovery': f'{zero.discovery.current_cycle} cycles, {len(zero.discovery.get_active_hypotheses())} active',
    '06. Simulation': f'{zero.simulation.total_simulations} sims, sandbox enabled',
    '07. Memory': f'ST={zero.memory.short_term.size} LT={zero.memory.long_term.size} EP={zero.memory.episodic.size}',
    '08. Learning': f'{stats["dynamic_entries"]} dynamic + {stats["experimental_entries"]} experimental',
    '09. Perception': zero.perception.summary(),
    '10. Earth Cognition': zero.earth_cognition.summary(),
    '11. Human History': zero.human_history.summary(),
    '12. Emotion': zero.emotion_cognition.summary(),
    '13. Humility': zero.humility.summary(),
    '14. Emergency Term': zero.emergency_termination.summary(),
    '15. Supervision': zero.supervision.summary(),
    '16. Knowledge Graph': zero.knowledge_graph.summary(),
    '17. Trust Engine': zero.trust.summary(),
    '18. Crawler': zero.crawler.summary(),
    '19. Agents': f'{len(zero.orchestrator.agents)} initialized / 10 available',
}
for name, status in modules.items():
    print(f'  [{name}] {status}')

print()
print(f'  Session: {zero.session_count} queries')
print(f'  Runtime: {zero.evolution.age_description}')
print(f'  Termination: {zero.emergency_termination.is_termination_intact()}')

print()
print('╔══════════════════════════════════════════════════╗')
print('║   ALL 19 MODULES INTEGRATED & OPERATIONAL       ║')
print('║   ZERO — Earth Civilization Symbiotic Network   ║')
print('╚══════════════════════════════════════════════════╝')
