"""Universal Novel Engine - Chapter Beat & Architecture Schema Definitions
Based on the Platinum Novel Outline Reverse Engineering Whitepaper.
"""

from typing import Dict, Any, List, Tuple

UNIVERSAL_BEAT_TEMPLATE = {
    "chapter_id": 1,
    "volume_id": "VOL-01",
    "title": "落雪按刀，度支疑云",
    "word_budget": 3500,
    "paragraph_budget": {
        "total_target": 65,
        "short_paragraphs_target_pct": 52,
        "max_paragraph_length": 110
    },
    "narrative_four_dimensions": {
        "action_and_physical_friction_pct": 48.0,
        "interleaved_dialogue_pct": 42.0,
        "environment_and_logistics_pct": 9.0,
        "pure_monologue_pct": 1.0
    },
    "scene_beats": [
        {
            "scene_id": 1,
            "location": "督邮曹东厢书案（炭盆将熄、窗缝灌入带雪冷风、积年受潮账册）",
            "characters_present": [
                {
                    "name": "主角",
                    "action_objective": "翻查各县虚报之官田荒赋，找出亏空差额",
                    "hidden_motivation": "试探户曹主簿是否与城西豪强同流合污，预备扣押首批证据",
                    "sensory_micro_gesture": "指肚轻擦受潮发脆的粗黄账纸边缘，按压算筹发出轻微顿挫声"
                },
                {
                    "name": "引路老吏",
                    "action_objective": "催促主角封账签字，按旧例结案",
                    "hidden_motivation": "暗中收过豪强炭敬，恐惧引火烧身，欲拉主角下水分担罪责",
                    "sensory_micro_gesture": "拢袖缩颈，咳嗽两声后用茶盖撇去泛黄茶沫"
                }
            ],
            "physical_friction_point": "砚台冻结无法着墨，需呵热气化墨；老吏故意碰翻茶盏湿污关键页账目",
            "spoken_subtext": "表面商量按公文旧例行事，实则在查验底线与问罪杀机间暗流涌动",
            "clue_action": {
                "clue_id": "CLUE-001",
                "action_type": "WATER",
                "concrete_detail": "老吏腰间挂着一枚磨损严重的青铜鱼形旧牌，与十年前案卷印泥缺口完全吻合"
            }
        }
    ],
    "chapter_tail_hook": {
        "tail_physical_state": "主角手中狼毫笔尖悬停在泛黄旧账末尾，屋顶瓦片忽传来一声极轻微的踩雪脆响",
        "unresolved_friction": "佩刀挂在三步外横桁上，来人已至屋檐，刀与墨不可兼得"
    }
}

def get_default_beat_template(chapter_idx: int, volume_id: str = "VOL-01") -> Dict[str, Any]:
    """Generates an ultra-fine granular chapter beat template conforming to UniversalChapterBeatSchema."""
    beat = dict(UNIVERSAL_BEAT_TEMPLATE)
    beat["chapter_id"] = chapter_idx
    beat["volume_id"] = volume_id
    beat["title"] = f"第{chapter_idx}章待定标题（动词+名词）"
    return beat

def validate_beat_schema(beat: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validates a chapter beat dictionary against the UniversalChapterBeatSchema standard.
    
    Returns (is_valid, critiques).
    """
    critiques = []

    # Required top-level keys
    required_keys = ["chapter_id", "volume_id", "title", "word_budget", "paragraph_budget", 
                     "narrative_four_dimensions", "scene_beats", "chapter_tail_hook"]
    for k in required_keys:
        if k not in beat:
            critiques.append(f"缺失顶级必需字段: '{k}'")

    if critiques:
        return False, critiques

    # Check title structure
    title = str(beat.get("title", "")).strip()
    if not title or title.startswith("第") and "待定" in title:
        critiques.append("章节标题未正式设定，需采用具象动宾或双音节微观题眼（如'落雪按刀'）")

    # Check word budget
    wb = beat.get("word_budget", 0)
    if not isinstance(wb, (int, float)) or wb < 2000 or wb > 6000:
        critiques.append(f"字数预算异常 ({wb} 字)，白金单章工业化预算应在 2500~4500 字之间")

    # Check paragraph budget
    pb = beat.get("paragraph_budget", {})
    if pb.get("max_paragraph_length", 0) > 130:
        critiques.append(f"最大段落预算超过安全阈值 ({pb.get('max_paragraph_length')} > 130字)，易引发网文臃肿感")
    if pb.get("short_paragraphs_target_pct", 0) < 40:
        critiques.append(f"短段落占比目标过低 ({pb.get('short_paragraphs_target_pct')}% < 40%)，违背白金快节奏律动")

    # Check narrative four dimensions
    dims = beat.get("narrative_four_dimensions", {})
    act_pct = dims.get("action_and_physical_friction_pct", 0)
    dia_pct = dims.get("interleaved_dialogue_pct", 0)
    env_pct = dims.get("environment_and_logistics_pct", 0)
    mono_pct = dims.get("pure_monologue_pct", 0)

    total_dim = act_pct + dia_pct + env_pct + mono_pct
    if abs(total_dim - 100.0) > 1.0:
        critiques.append(f"四维叙事配比总和不为 100% (当前合计: {round(total_dim, 1)}%)")

    if mono_pct > 2.5:
        critiques.append(f"纯心理独白配比超标 ({mono_pct}% > 2.5%)，顶级白金严禁大段内心独白，必须外化为肢体动作与言语交锋")
    if act_pct < 40.0:
        critiques.append(f"动作与物理受阻配比偏低 ({act_pct}% < 40%)，缺乏现场物理压迫感")

    # Check scene beats density
    scenes = beat.get("scene_beats", [])
    if not isinstance(scenes, list) or len(scenes) == 0:
        critiques.append("细纲中未定义任何微观场景 (scene_beats 为空)")
    elif len(scenes) > 3:
        critiques.append(f"单章微场景过多 ({len(scenes)} 个 > 3 个)，白金单章平均密度为 1.2~1.8 个，场景过多易导致流水账")

    for idx, sc in enumerate(scenes, 1):
        if not sc.get("location"):
            critiques.append(f"场景 {idx} 缺失具象空间/环境阻碍 (location)")
        if not sc.get("physical_friction_point"):
            critiques.append(f"场景 {idx} 缺失核心物理受阻点 (physical_friction_point)")
        chars = sc.get("characters_present", [])
        if not chars:
            critiques.append(f"场景 {idx} 无在场人物定义")
        for ch in chars:
            if not ch.get("action_objective"):
                critiques.append(f"场景 {idx} 人物【{ch.get('name', '未知')}】缺失明确行动目标 (action_objective)")
            if not ch.get("hidden_motivation"):
                critiques.append(f"场景 {idx} 人物【{ch.get('name', '未知')}】缺失隐秘动机/底牌 (hidden_motivation)")
            if not ch.get("sensory_micro_gesture"):
                critiques.append(f"场景 {idx} 人物【{ch.get('name', '未知')}】缺失感官微动作 (sensory_micro_gesture)")

    # Check tail hook
    tail = beat.get("chapter_tail_hook", {})
    if not tail.get("tail_physical_state"):
        critiques.append("缺失章末具象物理定格动作 (tail_physical_state)")
    if not tail.get("unresolved_friction"):
        critiques.append("缺失章末未决悬念与物理危机 (unresolved_friction)")

    is_valid = len(critiques) == 0
    return is_valid, critiques
