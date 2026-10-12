import os
from .state_manager import StateManager

def compile_chapter_prompt(target_chapter_idx, mode="history", workspace_dir="."):
    sm = StateManager(workspace_dir)
    prev_tail = sm.get_chapter_tail(target_chapter_idx - 1)
    char_reg = sm.get_character_registry()
    clues_ledger = sm.get_clues_ledger()
    cooldown_data = sm.get_imagery_cooldown()
    outline = sm.get_volume_outline()

    curr_beat = outline["chapter_beats"].get(str(target_chapter_idx), {})

    forbidden_words = []
    for word, meta in cooldown_data.get("active_cooldowns", {}).items():
        if target_chapter_idx <= meta.get("cooldown_until", 0):
            forbidden_words.append(word)

    active_clue_directive = ""
    clue_id = curr_beat.get("active_clue_to_water")
    if clue_id:
        for c in clues_ledger:
            if c["id"] == clue_id:
                active_clue_directive = (
                    f"【本章伏笔要求：滋养/唤醒 {c['id']}（{c['name']}）】\n"
                    f"- 表面伪装：{c['surface_mask']}\n"
                    f"- 执行规则：只能以微小次要功能或生活细节自然带过，严禁揭示终极秘密。"
                )

    protagonist = char_reg.get("protagonist", {})

    prompt = f"""# 第 {target_chapter_idx} 章生产级写作指令（题材模式: {mode}）

## 1. 严格承接上一章物理尾流（禁止总结重述与空降）
【上一章第 {target_chapter_idx - 1} 章真实末尾】：
```text
{prev_tail if prev_tail else "（此为卷首开篇，直接以微观具象场景切入）"}
```
> **接力契约**：第一自然段必须顺延上述物理动作、余波与环境！严禁出现“上一回/且说”等空洞套话。

## 2. 本章剧情题眼与节拍
- **标题**：{curr_beat.get('title', '待定')}
- **核心博弈**：{curr_beat.get('conflict_pivot', '推进当前局面')}
- **专属物理题眼**：{curr_beat.get('combat_motif', '具象微观动作')}
{active_clue_directive}

## 3. 在场核心人物声纹与习惯微动作
- **主角【{protagonist.get('name', '主角')}】**：
  - 语调风格：{protagonist.get('voice_tone', '沉稳冷静')}
  - 微动作习惯：{', '.join(protagonist.get('habitual_gestures', []))}
  - 行为禁忌：{', '.join(protagonist.get('forbidden_behaviors', []))}

## 4. 动态冷却期黑名单（本章出现立即扣分）
{', '.join([f'「{w}」' for w in forbidden_words]) if forbidden_words else '暂无处于冷却期的词汇'}

## 5. 量化语言律动要求（SKILL.md v2.0）
- 段落平均长 50~60 字，短段落(<50字)占比 >50%，严禁出现 >120 字长段；
- 75% 以上对话前后绑定肢体微动作（按刀、递茶、冷眼旁观）；
- 90% 对话引导词使用中性“道”、“说”，情绪词收敛于“正色”、“笑道/失笑”、“冷笑”；
- 战斗与动作必写受力阻滞、兵刃形变与机体生理衰竭。
"""
    return prompt
