"""Universal Novel Engine - Production QA Inspector v2.1
Enforces the 48/42/9/1 Narrative Ratio, Single-Chapter Micro-Scene Density (1.2-1.8 scenes),
Physical Friction Verbs, and Imagery Cooldowns.
"""

import os
import re
import json
from typing import Dict, Any, List

# Core physical resistance & physiological feedback keywords from Platinum masterworks
PHYSICAL_FRICTION_KEYWORDS = [
    '崩裂', '受阻', '骨', '窒息', '发黑', '脱手', '泥泞', '力竭', '血沫', '折断', 
    '剧颤', '滞涩', '冷汗', '青筋', '喘息', '酸软', '顿挫', '发麻', '撕扯', '重压',
    '刀柄', '甲胄', '算筹', '铁锈', '冰冷', '火星', '震颤', '脱力'
]

# Monologue & introspective cues (prohibited in large quantities)
MONOLOGUE_CUES = [
    '心中暗想', '心中暗道', '心道', '暗想', '心念电转', '不禁想到', '暗暗思索', 
    '心头微沉', '心中冷笑', '暗自忖度', '在他看来', '他知道这一切', '思来想去'
]

# Logistics & material culture cues
LOGISTICS_CUES = [
    '钱', '贯', '文', '两', '石', '斗', '升', '斤', '粮', '草料', '马料', 
    '驿站', '公文', '账册', '凭由', '勘合', '度支', '关牒', '官廨', '宵禁', '里'
]

# Scene hop / transition markers
SCENE_TRANSITION_CUES = [
    r'半个时辰[后之]', r'次日[清晨早]', r'翌日', r'及至夜[深色]', r'数日后', r'转眼[间便]',
    r'三更[天分]', r'未及午后', r'回[到去]官[廨舍]', r'步入[偏正]厅', r'出得城门', r'行至[官驿野]',
    r'\*{3,}', r'——{2,}'
]

def inspect_chapter(chapter_idx: int, text: str, workspace_dir: str = ".") -> Dict[str, Any]:
    """Runs deep four-dimensional narrative inspection and rhythm verification on chapter text."""
    state_dir = os.path.join(os.path.abspath(workspace_dir), "state")
    chapters_dir = os.path.join(state_dir, "chapters")
    cooldown_path = os.path.join(state_dir, "imagery_cooldown.json")
    
    cooldown_data = {"active_cooldowns": {}}
    if os.path.exists(cooldown_path):
        with open(cooldown_path, "r", encoding="utf-8") as f:
            cooldown_data = json.load(f)

    raw_paras = [p.strip() for p in text.split('\n') if p.strip()]
    word_count = sum(len(p) for p in raw_paras)
    para_lens = [len(p) for p in raw_paras]
    total_paras = max(1, len(raw_paras))

    # 1. 冷却期违禁词与高频套话
    active_forbidden = []
    for word, meta in cooldown_data.get("active_cooldowns", {}).items():
        if chapter_idx <= meta.get("cooldown_until", 0):
            if word in text:
                active_forbidden.append(word)

    # 2. 开头连贯性 (接力契约)
    first_para = raw_paras[0] if raw_paras else ""
    header_cliche = any(w in first_para for w in ["上一回", "且说", "话说上一章", "却说那一日", "上章说道"])

    # 3. 律动指标 (段落长短与对话穿插)
    short_paras = [p for p in raw_paras if len(p) < 50]
    short_ratio = len(short_paras) / total_paras
    max_para_len = max(para_lens) if para_lens else 0
    mean_para_len = word_count / total_paras

    quotes = re.findall(r'[“「](.*?)[”」]', text, re.S)
    dialogue_chars = sum(len(q) for q in quotes)
    dialogue_char_ratio = dialogue_chars / max(1, word_count)

    diag_paras = [p for p in raw_paras if '“' in p or '「' in p]
    interleaved = [p for p in diag_paras if len(re.sub(r'[“「].*?[”」]', '', p).strip()) > 6]
    interleave_ratio = len(interleaved) / max(1, len(diag_paras))

    # 4. 四维叙事配比估算 (48/42/9/1 标准)
    monologue_paras = 0
    logistics_paras = 0
    action_paras = 0

    for p in raw_paras:
        is_diag = ('“' in p or '「' in p)
        has_mono = any(cue in p for cue in MONOLOGUE_CUES)
        has_logi = any(cue in p for cue in LOGISTICS_CUES)
        has_fric = any(kw in p for kw in PHYSICAL_FRICTION_KEYWORDS)

        if has_mono and not is_diag:
            monologue_paras += 1
        elif has_logi and not is_diag:
            logistics_paras += 1
        elif has_fric or not is_diag:
            action_paras += 1

    mono_ratio = monologue_paras / total_paras
    logi_ratio = logistics_paras / total_paras
    dialogue_composite_ratio = len(diag_paras) / total_paras
    action_composite_ratio = max(0.0, 1.0 - (mono_ratio + logi_ratio + dialogue_composite_ratio * 0.5))

    # Normalize 4-dimensional composition to percentages
    denom = max(0.01, action_composite_ratio + (dialogue_composite_ratio * 0.5) + logi_ratio + mono_ratio)
    four_dim_ratios = {
        "action_friction_pct": round((action_composite_ratio / denom) * 100, 1),
        "interleaved_dialogue_pct": round(((dialogue_composite_ratio * 0.5) / denom) * 100, 1),
        "environment_logistics_pct": round((logi_ratio / denom) * 100, 1),
        "pure_monologue_pct": round((mono_ratio / denom) * 100, 1)
    }

    # 5. 微场景切换密度估算 (目标 1.2~1.8 个)
    scene_switches = 0
    for p in raw_paras:
        for cue in SCENE_TRANSITION_CUES:
            if re.search(cue, p):
                scene_switches += 1
                break
    estimated_scene_count = 1 + scene_switches

    # 6. 具象物理词统计
    found_phys = [w for w in PHYSICAL_FRICTION_KEYWORDS if w in text]

    # 7. 严格裁决与质检告警
    passed = True
    critiques = []

    if active_forbidden:
        passed = False
        critiques.append(f"【冷却期违规】包含禁用高频套话: {active_forbidden}")
    if header_cliche:
        passed = False
        critiques.append("【接力契约破损】开篇第一段使用了'且说/上一回'等说书式空套话，未顺延上一章末尾物理微观动作")
    if max_para_len > 140:
        passed = False
        critiques.append(f"【段落臃肿】存在 >140 字的巨型段落（最大段 {max_para_len} 字），破坏白金行文呼吸律动")
    if short_ratio < 0.38:
        passed = False
        critiques.append(f"【短段落不足】短段落(<50字)比例偏低（{round(short_ratio*100, 1)}% < 38%），建议切碎长句")
    if interleave_ratio < 0.65:
        passed = False
        critiques.append(f"【对话脱靶】对话动作穿插率偏低（{round(interleave_ratio*100, 1)}% < 65%），台词未前后绑定微动作")
    if mono_ratio > 0.025:
        passed = False
        critiques.append(f"【心理独白超标】纯内心独白段落占比偏高（{round(mono_ratio*100, 1)}% > 2.5%），大师级网文严禁内心独白灌水，必须借动作外化")
    if estimated_scene_count > 3:
        critiques.append(f"【场景切分过碎】单章检测到约 {estimated_scene_count} 个场景切换（白金单章平均仅 1.2~1.8 个），谨防流水账")
    if len(found_phys) < 3:
        critiques.append("【缺乏阻碍触感】具象物理受阻词汇偏少，缺乏兵刃、器物或生理力竭反馈")

    report = {
        "chapter_idx": chapter_idx,
        "passed": passed,
        "word_count": word_count,
        "total_paragraphs": total_paras,
        "mean_para_len": round(mean_para_len, 1),
        "short_para_ratio": round(short_ratio, 3),
        "dialogue_char_ratio": round(dialogue_char_ratio, 3),
        "interleave_ratio": round(interleave_ratio, 3),
        "four_dimensional_composition": four_dim_ratios,
        "estimated_scene_count": estimated_scene_count,
        "found_phys_cues": list(set(found_phys)),
        "critiques": critiques
    }

    if passed:
        # Save chapter text
        os.makedirs(chapters_dir, exist_ok=True)
        ch_file_path = os.path.join(chapters_dir, f"chapter_{chapter_idx:03d}.txt")
        with open(ch_file_path, "w", encoding="utf-8") as f:
            f.write(text)

        # Update clues ledger
        clues_path = os.path.join(state_dir, "clues_ledger.json")
        if os.path.exists(clues_path):
            with open(clues_path, "r", encoding="utf-8") as f:
                clues = json.load(f)
            for c in clues:
                keywords = [c.get("name", "")] + [w for w in re.split(r'[的与和之\s]', c.get("name", "")) if len(w) >= 2]
                if any(kw in text for kw in keywords if kw):
                    watered = c.setdefault("watered_chapters", [])
                    if chapter_idx not in watered and c.get("planted_chapter") != chapter_idx:
                        watered.append(chapter_idx)
            with open(clues_path, "w", encoding="utf-8") as f:
                json.dump(clues, f, ensure_ascii=False, indent=2)

        # Update cooldown
        candidates = ["深吸一口气", "嘴角勾起", "冷笑一声", "心中大骇", "面面相觑", "暗骂一声", "倒吸一口凉气"]
        for t in candidates:
            if t in text:
                cooldown_data.setdefault("active_cooldowns", {})[t] = {
                    "last_used_chapter": chapter_idx,
                    "cooldown_until": chapter_idx + 4
                }
        with open(cooldown_path, "w", encoding="utf-8") as f:
            json.dump(cooldown_data, f, ensure_ascii=False, indent=2)

        # Update volume outline status
        outline_path = os.path.join(state_dir, "volume_outline.json")
        if os.path.exists(outline_path):
            with open(outline_path, "r", encoding="utf-8") as f:
                outline = json.load(f)
            beats = outline.get("chapter_beats", {})
            if str(chapter_idx) in beats:
                beats[str(chapter_idx)]["status"] = "completed"
            with open(outline_path, "w", encoding="utf-8") as f:
                json.dump(outline, f, ensure_ascii=False, indent=2)

    return report
