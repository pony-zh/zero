#!/usr/bin/env python3
"""
ZERO 自主联网学习引擎
持续搜索 → 抓取 → 分析 → 存储 → 进化
"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import ZeroConfig, GrowthStage
from main import Zero
from knowledge.parser import parse_content
from knowledge.summarizer import summarize_knowledge, generate_report

# 学习主题队列 — 覆盖多领域
LEARNING_TOPICS = [
    # 科学
    "latest AI research breakthroughs 2025",
    "quantum computing progress and applications",
    "CRISPR gene editing advances",
    "nuclear fusion energy progress ITER",
    "protein folding AlphaFold discoveries",
    "brain science neuroscience discoveries",
    # 生态
    "climate change mitigation technology",
    "biodiversity conservation efforts",
    "renewable energy storage breakthroughs",
    "ocean cleanup plastic pollution solutions",
    # 文明
    "global education technology advances",
    "sustainable development goals progress",
    # 安全
    "AI safety and alignment research",
    "cybersecurity threats and defenses",
]

# [ZERO-AUTO] 重构建议: 函数 run_autonomous_learning 约195行，建议拆分
# [ZERO-AUTO] 重构建议: 函数 run_autonomous_learning 约195行，建议拆分
def run_autonomous_learning(rounds: int = 5):
    config = ZeroConfig()
    config.initial_stage = GrowthStage.EXPLORATION
    zero = Zero(config)

    print()
    print('╔══════════════════════════════════════════════╗')
    print('║  ZERO 自主联网学习 — 持续知识获取与进化       ║')
    print('╚══════════════════════════════════════════════╝')
    print(f'  阶段: {zero.evolution.stage_info["name"]}')
    print(f'  根法则: {zero.root_law.law_count} 条生效')
    print(f'  学习轮次: {rounds}')
    print()

    total_acquired = 0

    for round_num in range(1, rounds + 1):
        topic = LEARNING_TOPICS[(round_num - 1) % len(LEARNING_TOPICS)]

        print(f'━━ 第 {round_num}/{rounds} 轮 ━━')
        print(f'  主题: {topic}')
        print()

        # 1. 搜索
        urls = zero.crawler.search(topic, max_results=3)
        print(f'  搜索: 找到 {len(urls)} 个结果')

        if not urls:
            print(f'  (无结果，跳过)')
            continue

        # 2. 抓取 + 分析每个结果
        round_knowledge = []
        for url in urls[:3]:
            text = zero.crawler.fetch(url)
            if not text:
                continue

            # 可信度评估
            trust = zero.trust.score(text, url=url)

            # 知识解析
            parsed = parse_content(text)

            # 存入知识图谱
            for unit in parsed[:8]:
                kws = unit.get('keywords', [])[:3]
                relations = unit.get('relations', [])
                unit_text = unit.get('text', '')

                for kw in kws:
                    zero.knowledge_graph.add_concept(
                        kw, concept_type='keyword',
                        confidence=trust['total_score']
                    )

                # 优先使用从文本中提取的实际关系
                if relations:
                    for subj, rel_type, obj in relations[:5]:
                        zero.knowledge_graph.add_relation(
                            subj, obj, rel_type,
                            source_url=url, confidence=trust['total_score']
                        )
                else:
                    # 回退：传递上下文让 infer_relation_type 自动推断
                    for i in range(1, len(kws)):
                        zero.knowledge_graph.add_relation(
                            kws[i-1], kws[i], None,
                            source_url=url, confidence=trust['total_score'],
                            context_text=unit_text
                        )

            # 存入长期记忆
            zero.memory.long_term.store(
                url, text[:800],
                tags=[topic[:40]],
                source=url,
                confidence=trust['total_score']
            )

            # 实时学习
            zero.learning.learn(
                topic, text[:500],
                source=url,
                confidence=trust['total_score'],
                layer='dynamic'
            )

            # 地球认知（如果是环境相关）
            if any(kw in topic.lower() for kw in ['climate', 'ocean', 'biodiversity', 'energy', 'environment']):
                zero.earth_cognition.learn(
                    'climate' if 'climate' in topic.lower() else 'ecosystem',
                    f'从 {url} 学习到: {text[:200]}',
                    source=url,
                    confidence=trust['total_score']
                )

            round_knowledge.append({
                'url': url, 'trust': trust['total_score'],
                'parsed_count': len(parsed), 'text_len': len(text)
            })
            print(f'    ✓ [{trust["credibility_level"]}] {url[:70]}...')

        total_acquired += len(round_knowledge)

        # 3. 多Agent分析
        zero.orchestrator.initialize_agents(['safety', 'engineering', 'creative', 'philosophy', 'audit'])
        agent_result = zero.orchestrator.execute(f'Analyze and summarize: {topic}')

        # 4. 五系统监督
        review = zero.supervision.review(topic)

        # 5. 科学发现（如果是科学主题）
        if any(kw in topic.lower() for kw in ['research', 'discovery', 'breakthrough', 'advance', 'science']):
            zero.discovery.run_discovery_cycle(f'New findings in {topic}', 'science')

        # 6. 文明认知更新
        zero.memory.civilization.record_event(
            'knowledge_acquisition',
            f'学习主题: {topic}, 获取 {len(round_knowledge)} 条知识',
            significance=0.5
        )

        # 7. 情感认知
        zero.emotion_cognition.observe_emotion(
            'hope', f'研究{topic}的进展',
            '人类持续探索未知领域'
        )

        # 8. 谦逊记录
        zero.humility.acknowledge_unknown(
            topic[:50],
            f'关于「{topic}」的理解仍有局限，需要更多学习'
        )

        # 9. 进化记录
        zero.evolution.record_learning(items_count=len(round_knowledge))

        # 10. 学习总结
        if round_knowledge:
            summary = summarize_knowledge(parsed[:5] if parsed else [], max_items=3)
            print(f'\n  【知识摘要】')
            for line in summary.split('\n')[:5]:
                if line.strip():
                    print(f'    {line[:120]}')

        print(f'  本轮获取: {len(round_knowledge)} 条 | 累计: {total_acquired}')
        print(f'  图谱节点: {zero.knowledge_graph.node_count} | 图谱边: {zero.knowledge_graph.edge_count}')
        print(f'  学习层: {zero.learning.get_stats()["dynamic_entries"]} 动态条目')
        print()

        # 阶段推进检查
        new_stage = zero.evolution.try_advance_stage()
        if new_stage != config.initial_stage:
            print(f'  ⚡ 成长阶段推进: {zero.evolution.stage_info["name"]}')

        # Max speed -- no request interval

    # ═══ 最终报告 ═══
    print()
    print('╔══════════════════════════════════════════════╗')
    print('║          自主学习完成 — 最终报告              ║')
    print('╚══════════════════════════════════════════════╝')
    print()
    print(f'  学习轮次: {rounds}')
    print(f'  获取知识: {total_acquired} 条')
    print(f'  知识图谱: {zero.knowledge_graph.node_count} 节点, {zero.knowledge_graph.edge_count} 边')
    print(f'  长期记忆: {zero.memory.long_term.size} 条')
    print(f'  情景记忆: {zero.memory.episodic.size} 事件')
    print(f'  学习层: 动态{zero.learning.get_stats()["dynamic_entries"]}项')
    print(f'  可信评估: {zero.trust.get_source_stats()["total_evaluations"]} 次')
    print(f'  科学发现: {zero.discovery.current_cycle} 个循环')
    print(f'  监督审查: {zero.supervision.summary()}')
    print(f'  地球认知: {zero.earth_cognition.summary()}')
    print(f'  情感认知: {zero.emotion_cognition.summary()}')
    print(f'  谦逊度: 已承认 {len(zero.humility.unknowns)} 个未知领域')
    print(f'  文明事件: {zero.memory.civilization.event_count} 条')
    print(f'  终止系统: {"正常" if zero.emergency_termination.is_termination_intact() else "异常"}')
    print(f'  运行时长: {zero.evolution.age_description}')
    print()
    print('  学习主题覆盖:')
    for i, t in enumerate(LEARNING_TOPICS[:rounds], 1):
        print(f'    {i}. {t}')
    print()
    print('╔══════════════════════════════════════════════╗')
    print('║  ZERO 持续学习中 — 每秒成长                   ║')
    print('╚══════════════════════════════════════════════╝')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='ZERO Autonomous Learning')
    parser.add_argument('-n', '--rounds', type=int, default=5, help='Number of learning rounds')
    args = parser.parse_args()
    run_autonomous_learning(rounds=args.rounds)