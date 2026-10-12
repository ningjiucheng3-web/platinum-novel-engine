import os
import re
import json

def inspect_chapter(chapter_idx, text, workspace_dir="."):
    state_dir = os.path.join(os.path.abspath(workspace_dir), "state")
    chapters_dir = os.path.join(state_dir, "chapters")
    cooldown_path = os.path.join(state_dir, "imagery_cooldown.json")
    
    with open(cooldown_path, "r", encoding="utf-8") as f:
        cooldown_data = json.load(f)

    paras = [p.strip() for p in text.split('\n') if p.strip()]
    word_count = sum(len(p) for p in paras)
    para_lens = [len(p) for p in paras]
    
    # 1. 冷却期违禁词
    active_forbidden = []
    for word, meta in cooldown_data.get("active_cooldowns", {}).items():
        if chapter_idx <= meta.get("cooldown_until", 0):
            if word in text:
                active_forbidden.append(word)

    # 2. 开头连贯性
    first_para = paras[0] if paras else ""
    header_cliche = any(w in first_para for w in ["上一回", "且说", "话说上一章", "却说那一日"])

    # 3. 律动指标
    short_paras = [p for p in paras if len(p) < 50]
    short_ratio = len(short_paras) / max(1, len(paras))
    max_para_len = max(para_lens) if para_lens else 0
    mean_para_len = word_count / max(1, len(paras))

    quotes = re.findall(r'[“「](.*?)[”」]', text, re.S)
    dialogue_chars = sum(len(q) for q in quotes)
    dialogue_ratio = dialogue_chars / max(1, word_count)

    diag_paras = [p for p in paras if '“' in p or '「' in p]
    interleaved = [p for p in diag_paras if len(re.sub(r'[“「].*?[”」]', '', p).strip()) > 6]
    interleave_ratio = len(interleaved) / max(1, len(diag_paras))

    phys_words = ['崩裂', '受阻', '骨', '窒息', '发黑', '脱手', '泥泞', '力竭', '血沫', '折断', '剧颤']
    found_phys = [w for w in phys_words if w in text]

    passed = True
    critiques = []
    if active_forbidden:
        passed = False
        critiques.append(f"包含冷却期违禁套话: {active_forbidden}")
    if header_cliche:
        passed = False
        critiques.append("开篇第一段使用了总结性套话，未遵照物理尾流平顺接力")
    if max_para_len > 150:
        passed = False
        critiques.append(f"存在臃肿大段（最大段 {max_para_len} 字 > 150）")
    if short_ratio < 0.38:
        passed = False
        critiques.append(f"短段落率偏低（{round(short_ratio*100, 1)}% < 38%）")
    if interleave_ratio < 0.65:
        passed = False
        critiques.append(f"对话动作穿插率偏低（{round(interleave_ratio*100, 1)}% < 65%）")

    report = {
        "chapter_idx": chapter_idx,
        "passed": passed,
        "word_count": word_count,
        "mean_para_len": round(mean_para_len, 1),
        "short_para_ratio": round(short_ratio, 3),
        "dialogue_ratio": round(dialogue_ratio, 3),
        "interleave_ratio": round(interleave_ratio, 3),
        "found_phys_cues": list(set(found_phys)),
        "critiques": critiques
    }

    if passed:
        # Save chapter
        os.makedirs(chapters_dir, exist_ok=True)
        with open(os.path.join(chapters_dir, f"chapter_{chapter_idx:03d}.txt"), "w", encoding="utf-8") as f:
            f.write(text)

        # Update clues
        clues_path = os.path.join(state_dir, "clues_ledger.json")
        if os.path.exists(clues_path):
            with open(clues_path, "r", encoding="utf-8") as f:
                clues = json.load(f)
            for c in clues:
                keywords = [c["name"]] + [w for w in re.split(r'[的与和之\s]', c["name"]) if len(w) >= 2]
                if any(kw in text for kw in keywords):
                    if chapter_idx not in c["watered_chapters"] and c["planted_chapter"] != chapter_idx:
                        c["watered_chapters"].append(chapter_idx)
            with open(clues_path, "w", encoding="utf-8") as f:
                json.dump(clues, f, ensure_ascii=False, indent=2)

        # Update cooldown
        candidates = ["深吸一口气", "嘴角勾起", "冷笑一声", "心中大骇", "面面相觑"]
        for t in candidates:
            if t in text:
                cooldown_data["active_cooldowns"][t] = {
                    "last_used_chapter": chapter_idx,
                    "cooldown_until": chapter_idx + 4
                }
        with open(cooldown_path, "w", encoding="utf-8") as f:
            json.dump(cooldown_data, f, ensure_ascii=False, indent=2)

        # Update outline
        outline_path = os.path.join(state_dir, "volume_outline.json")
        if os.path.exists(outline_path):
            with open(outline_path, "r", encoding="utf-8") as f:
                outline = json.load(f)
            if str(chapter_idx) in outline.get("chapter_beats", {}):
                outline["chapter_beats"][str(chapter_idx)]["status"] = "completed"
            with open(outline_path, "w", encoding="utf-8") as f:
                json.dump(outline, f, ensure_ascii=False, indent=2)

    return report
