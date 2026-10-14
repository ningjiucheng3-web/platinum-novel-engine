"""Universal Novel Engine - Production Context & Prompt Compiler v2.1
Compiles fine-grained writing prompts grounded in the UniversalChapterBeatSchema,
Four-Dimensional Narrative Ratios, and Chekhov's Gun Cadence.
"""

import os
from .state_manager import StateManager

def compile_chapter_prompt(target_chapter_idx: int, mode: str = "history", workspace_dir: str = ".") -> str:
    sm = StateManager(workspace_dir)
    prev_tail = sm.get_chapter_tail(target_chapter_idx - 1)
    char_reg = sm.get_character_registry()
    clues_ledger = sm.get_clues_ledger()
    cooldown_data = sm.get_imagery_cooldown()
    outline = sm.get_volume_outline()

    curr_beat = outline.get("chapter_beats", {}).get(str(target_chapter_idx), {})

    # Extract cooldown forbidden phrases
    forbidden_words = []
    for word, meta in cooldown_data.get("active_cooldowns", {}).items():
        if target_chapter_idx <= meta.get("cooldown_until", 0):
            forbidden_words.append(word)

    # Resolve active clues
    active_clue_directives = []
    # 1. From beat schema clue_action or active_clue_to_water
    clue_actions = []
    if "scene_beats" in curr_beat:
        for sc in curr_beat["scene_beats"]:
            ca = sc.get("clue_action")
            if ca and ca.get("clue_id"):
                clue_actions.append(ca)
    elif curr_beat.get("active_clue_to_water"):
        clue_actions.append({
            "clue_id": curr_beat["active_clue_to_water"],
            "action_type": "WATER",
            "concrete_detail": "借助微小器物或次要生活细节自然带过"
        })

    for ca in clue_actions:
        cid = ca["clue_id"]
        for c in clues_ledger:
            if c["id"] == cid:
                active_clue_directives.append(
                    f"- **【{ca.get('action_type', 'WATER')}】{c['id']}（{c['name']}）**\n"
                    f"  - 表面伪装：{c.get('surface_mask', '普通器物/日常细节')}\n"
                    f"  - 执行细则：{ca.get('concrete_detail', '严禁直接掀底牌，仅通过物理触碰或微弱反常呈现')}"
                )

    # Protagonist details
    protagonist = char_reg.get("protagonist", {})
    if not protagonist and "characters" in char_reg:
        for ch in char_reg["characters"]:
            if ch.get("role") == "protagonist":
                protagonist = ch
                break

    # Paragraph and narrative budgets
    pb = curr_beat.get("paragraph_budget", {
        "total_target": 65,
        "short_paragraphs_target_pct": 52,
        "max_paragraph_length": 110
    })
    dims = curr_beat.get("narrative_four_dimensions", {
        "action_and_physical_friction_pct": 48.0,
        "interleaved_dialogue_pct": 42.0,
        "environment_and_logistics_pct": 9.0,
        "pure_monologue_pct": 1.0
    })

    # Format scenes
    scenes_text = ""
    if "scene_beats" in curr_beat and curr_beat["scene_beats"]:
        for idx, sc in enumerate(curr_beat["scene_beats"], 1):
            char_lines = []
            for cp in sc.get("characters_present", []):
                char_lines.append(
                    f"    * **{cp.get('name', '在场人物')}**：动作目标: {cp.get('action_objective', '推进动作')} | "
                    f"隐秘动机: {cp.get('hidden_motivation', '暗中试探')} | "
                    f"感官微动作: {cp.get('sensory_micro_gesture', '按刀/搓手')}"
                )
            char_block = "\n".join(char_lines) if char_lines else "    * （无在场特定角色标记）"
            scenes_text += f"""
### 场景 {idx}：{sc.get('location', '具象物理空间')}
- **在场人物动态**：
{char_block}
- **核心物理受阻点**：{sc.get('physical_friction_point', '动作受阻')}
- **言外之意与潜台词**：{sc.get('spoken_subtext', '话里藏针')}
"""
    else:
        # Fallback to legacy format
        scenes_text = f"""
- **核心博弈**：{curr_beat.get('conflict_pivot', '推进当前局面')}
- **专属物理题眼**：{curr_beat.get('combat_motif', '具象微观动作')}
"""

    tail_hook = curr_beat.get("chapter_tail_hook", {})
    tail_text = ""
    if tail_hook:
        tail_text = f"""
## 5. 章末物理定格与悬念尾流（严禁以旁白感慨收尾）
- **最后一刻物理定格动作**：{tail_hook.get('tail_physical_state', '主角手中的动作悬停')}
- **下一秒未决物理危机**：{tail_hook.get('unresolved_friction', '危机逼近，悬而未决')}
"""

    prompt = f"""# 第 {target_chapter_idx} 章生产级写作指令（题材模式: {mode}）

## 1. 严格承接上一章物理尾流（禁止总结重述与空降）
【上一章第 {target_chapter_idx - 1} 章真实末尾】：
```text
{prev_tail if prev_tail else "（此为卷首开篇，直接以微观具象物理场景切入）"}
```
> **接力契约**：第一自然段必须顺延上述物理动作、余波与环境！严禁出现“上一回/且说”等空洞套话。

## 2. 单章宏观参数与四维叙事配比（白金工业化黄金律）
- **章节标题**：{curr_beat.get('title', f'第{target_chapter_idx}章')}
- **字数预算**：{curr_beat.get('word_budget', 3500)} 字 | **段落总预算**：约 {pb.get('total_target', 65)} 段
- **段落呼吸律动**：短段落(<50字)占比 ≥{pb.get('short_paragraphs_target_pct', 50)}%，单段最大长度 ≤{pb.get('max_paragraph_length', 120)} 字
- **叙事四维配比**：
  * **动作与物理受阻（{dims.get('action_and_physical_friction_pct', 48.0)}%）**：每组动作必写物理阻力、受力形变与肌肉力竭
  * **动作交织对白（{dims.get('interleaved_dialogue_pct', 42.0)}%）**：说话必须配合肢体动作，90%引导词用“道/说”，禁止静止对侃
  * **环境风物度支（{dims.get('environment_and_logistics_pct', 9.0)}%）**：仅用于开篇定场与转场，精准交代物价、文书、米粮、甲胄等硬核风物
  * **纯内心独白（≤{dims.get('pure_monologue_pct', 1.0)}%）**：**严禁大段心理独白灌水**，一切心机借微动作与算盘声外化！

## 3. 微观细纲分镜（限制 1~2 个事件，禁止流水账多场景切换）
{scenes_text}

## 4. 契诃夫之枪（伏笔动作推进）
{chr(10).join(active_clue_directives) if active_clue_directives else '- 本章无强制伏笔操作，保持常态细节铺陈'}
{tail_text}
## 6. 在场主角声纹与习惯微动作
- **主角【{protagonist.get('name', '主角')}】**：
  - 语调风格：{protagonist.get('voice_tone', '沉稳冷静，言辞有制')}
  - 微动作习惯：{', '.join(protagonist.get('habitual_gestures', ['按刀四顾', '指扣案几']))}
  - 行为禁忌：{', '.join(protagonist.get('forbidden_behaviors', ['严禁狂笑咆哮', '严禁无脑发表热血演讲']))}

## 7. 动态冷却期黑名单（本章出现立即扣分）
{', '.join([f'「{w}」' for w in forbidden_words]) if forbidden_words else '暂无处于冷却期的词汇'}
"""
    return prompt
