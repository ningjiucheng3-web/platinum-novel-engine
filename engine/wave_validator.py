"""Universal Novel Engine - Character Cadence & Clue Lifecycle Validator
Enforces the Four-Wave Character Debut Pulse, Du Meng Guide Exit Rule, and Chekhov's Gun Cadence.
"""

from typing import Dict, Any, List, Tuple

WAVE_DEFINITIONS = {
    "WAVE_1": {
        "name": "生存破局期 (Survival Loop)",
        "chapter_range": (1, 10),
        "target_roles": ["protagonist", "mentor", "guide", "loyal_escort", "enforcer"],
        "max_debuts": 5,
        "desc": "主角、引路人、忠勇伴行及远景势力虚写；严格限制出场人物数量，避免新手轰炸式报菜名"
    },
    "WAVE_2": {
        "name": "体制接入期 (Institutional Entry)",
        "chapter_range": (20, 45),
        "target_roles": ["peer_rival", "institutional_gatekeeper", "academic_rival"],
        "min_debuts": 1,
        "desc": "入仕或入宗门，引出平辈竞争者与宿敌镜像（如曹操/袁绍第26章登场，司马正第33章登场）"
    },
    "WAVE_3": {
        "name": "秩序崩塌期 (Great Cataclysm)",
        "chapter_range": (80, 180),
        "target_roles": ["rebel_comrade", "core_cadre", "martial_champion"],
        "desc": "旧秩序解体，核心战斗力与反贼班底爆发式涌现"
    },
    "WAVE_4": {
        "name": "战略蜕变期 (Strategic Metamorphosis)",
        "chapter_range": (230, 330),
        "target_roles": ["institutional_strategist", "senior_politician", "grand_schemer"],
        "desc": "制度型谋士与阴鸷政治家进场（如贾诩第254章、陈斌第306章）"
    }
}

def validate_character_waves(character_registry: Dict[str, Any]) -> Tuple[bool, List[str], Dict[str, Any]]:
    """Validates character debuts across the four waves and enforces the Du Meng Exit Rule."""
    critiques = []
    stats = {
        "wave_counts": {"WAVE_1": 0, "WAVE_2": 0, "WAVE_3": 0, "WAVE_4": 0, "OTHER": 0},
        "debut_timeline": [],
        "guide_npcs": []
    }

    # Normalize character list
    characters = []
    if "characters" in character_registry and isinstance(character_registry["characters"], list):
        characters = character_registry["characters"]
    else:
        # Dictionary format with protagonist / mentors / rivals
        for k, v in character_registry.items():
            if isinstance(v, dict):
                v_copy = dict(v)
                v_copy["_registry_key"] = k
                characters.append(v_copy)

    # Analyze debut chapters
    wave1_chars = []
    wave2_rivals = []
    
    for ch in characters:
        name = ch.get("name", ch.get("_registry_key", "未知"))
        debut_ch = ch.get("debut_chapter", 1)
        role = ch.get("role", "supporting")
        stats["debut_timeline"].append({"name": name, "chapter": debut_ch, "role": role})

        if 1 <= debut_ch <= 10:
            stats["wave_counts"]["WAVE_1"] += 1
            wave1_chars.append(ch)
            # Check guide / mentor exit rule
            if role in ["mentor", "guide", "elder", "引路人", "师长"]:
                stats["guide_npcs"].append(name)
                exit_plan = ch.get("exit_mechanism") or ch.get("exit_chapter_window")
                if not exit_plan:
                    critiques.append(
                        f"【杜盟代谢律告警】引路人NPC【{name}】（第{debut_ch}章登场）未配置退出机制 (exit_mechanism)！"
                        f"白金法则：启蒙导师必须在第15~35章内通过调离、重伤、壮烈牺牲或理念决裂退场，严禁长期待在主角身边沦为智能拐杖。"
                    )
        elif 20 <= debut_ch <= 45:
            stats["wave_counts"]["WAVE_2"] += 1
            if role in ["peer_rival", "rival", "宿敌", "平辈竞争者", "同僚"]:
                wave2_rivals.append(name)
        elif 80 <= debut_ch <= 180:
            stats["wave_counts"]["WAVE_3"] += 1
        elif 230 <= debut_ch <= 330:
            stats["wave_counts"]["WAVE_4"] += 1
        else:
            stats["wave_counts"]["OTHER"] += 1

    # Wave 1 crowd explosion check
    if len(wave1_chars) > 5:
        critiques.append(
            f"【第一波次人物过载】前10章出场主要人物达到 {len(wave1_chars)} 位（上限建议 <= 4 位）。"
            "过早引入过多有名有姓的配角会导致读者认知过载，请合并或推迟次要配角登场。"
        )

    # Wave 2 peer rival mirror check
    if stats["wave_counts"]["WAVE_2"] > 0 and not wave2_rivals:
        critiques.append(
            "【第二波次宿敌缺失】第20~45章体制期未规划明确的平辈宿敌/体制竞争者 (role: 'peer_rival')。"
            "参考《覆汉》曹操/袁绍（第26章）、《黜龙》司马正（第33章），必须在体制期确立镜像竞争关系。"
        )

    is_valid = len(critiques) == 0
    return is_valid, critiques, stats


def validate_clues_lifecycle(clues_ledger: List[Dict[str, Any]], current_chapter: int = 50) -> Tuple[bool, List[str], List[Dict[str, Any]]]:
    """Validates the lifecycle of Chekhov's guns in clues_ledger.json."""
    critiques = []
    report_items = []

    for c in clues_ledger:
        cid = c.get("id", "UNKNOWN")
        name = c.get("name", "未命名线索")
        planted = c.get("planted_chapter", 1)
        watered = c.get("watered_chapters", [])
        status = c.get("status", "planted")
        harvest_target = c.get("target_harvest_chapter", planted + 150)

        item = {
            "id": cid,
            "name": name,
            "planted": planted,
            "watered_count": len(watered),
            "status": status,
            "last_touch": watered[-1] if watered else planted,
            "distance_since_touch": current_chapter - (watered[-1] if watered else planted)
        }
        report_items.append(item)

        # Check: dormant clue (no water for > 70 chapters)
        if status == "active" or status == "planted":
            gap = current_chapter - item["last_touch"]
            if gap > 70 and current_chapter > planted:
                critiques.append(
                    f"【契诃夫之枪休眠告警】伏笔【{name} ({cid})】已超过 {gap} 章未被滋养唤醒（上次出现于第 {item['last_touch']} 章）。"
                    "白金法则：伏笔每隔 30~60 章需借次要道具、闲聊或背景物价进行一次微弱回响，避免读者彻底遗忘。"
                )

        # Check: premature harvest
        if status == "harvested":
            harvest_ch = c.get("harvested_chapter", current_chapter)
            if harvest_ch - planted < 20 and len(watered) == 0:
                critiques.append(
                    f"【伏笔速爆告警】伏笔【{name} ({cid})】在埋入后仅 {harvest_ch - planted} 章即被兑现，且无滋养过渡。"
                    "属于短线包袱而非大纲级伏笔，建议将其降级为本章小节微梗。"
                )

    is_valid = len(critiques) == 0
    return is_valid, critiques, report_items
