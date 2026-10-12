import os
import json

BASE_DIR = "/Users/haiwaizhushou/.gemini/antigravity/scratch/universal-novel-engine/presets"

# 1. 历史权谋预设 (覆汉/庆余年向)
history_preset = {
    "character_registry.json": {
        "protagonist": {
            "name": "沈淮",
            "voice_tone": "沉稳端方，言辞合乎汉晋仪轨，内心极度理智，精算天下账目",
            "habitual_gestures": ["按刀四顾", "整理长袍袖口", "指尖轻扣案几"],
            "forbidden_behaviors": ["严禁狂笑咆哮", "严禁无脑发表热血演讲", "严禁冲动当堂顶撞大员"],
            "current_status": {
                "location": "京畿督邮曹官廨",
                "health": "精气神饱满，左臂有旧年骑射拉伤",
                "equipment": ["半旧青绢长衫", "佩刀一柄", "户部度支旧账册一本"]
            }
        }
    },
    "volume_outline.json": {
        "volume_id": "VOL-01",
        "volume_title": "第一卷：白简如霜",
        "macro_conflict": "朝廷三饷摊派，江南豪强匿户抗粮，京畿官场风声鹤唳，主角以户曹书吏身份入局算账破局。",
        "protagonist_dual_persona": {
            "surface": "谨小慎微、按规矩行文的督邮曹书吏",
            "shadow": "手握账目漏洞、暗中重构地盘的寒门执棋者"
        },
        "chapter_beats": {
            "1": {
                "title": "落雪按刀，度支疑云",
                "conflict_pivot": "查验各县私盐账目，发现豪强瞒报数千顷官田",
                "combat_motif": "衙署暗杀与狭窄回廊冷兵器搏杀",
                "active_clue_to_water": "CLUE-001"
            }
        }
    },
    "clues_ledger.json": [
        {
            "id": "CLUE-001",
            "name": "旧年辽东军粮账册残卷",
            "planted_chapter": 1,
            "surface_mask": "垫桌角的一本旧账簿，字迹模糊",
            "secret_core": "记录了当朝首辅通敌倒卖军械的唯一铁证",
            "watered_chapters": [],
            "target_payoff_arc": "第一卷末朝堂大清算",
            "status": "planted"
        }
    ],
    "imagery_cooldown.json": {
        "active_cooldowns": {
            "深吸一口气": {"last_used_chapter": 0, "cooldown_until": 5},
            "嘴角勾起一抹冷笑": {"last_used_chapter": 0, "cooldown_until": 10},
            "夕阳如血": {"last_used_chapter": 0, "cooldown_until": 6}
        }
    }
}

# 2. 高武变法预设 (牧神记向)
xuanhuan_preset = {
    "character_registry.json": {
        "protagonist": {
            "name": "陆玄",
            "voice_tone": "笑眯眯，自称大荒老实山民，言语温和纯朴，下手绝不容情",
            "habitual_gestures": ["纯真微笑", "摸后脑勺", "藏在袖中的断空刀微振"],
            "forbidden_behaviors": ["严禁邪魅装逼", "严禁视凡人为蝼蚁", "严禁无脑叫嚣"],
            "current_status": {
                "location": "大荒边关破落驿站",
                "health": "元气如江河充盈，神藏初辟",
                "equipment": ["粗布麻衣", "杀猪短刃", "行囊里的苞谷面饼"]
            }
        }
    },
    "volume_outline.json": {
        "volume_id": "VOL-01",
        "volume_title": "第一卷：大荒出牧",
        "macro_conflict": "神魔视下界凡人为口粮血祭，人族帝国开启太学变法，推行算学改制法宝，主角走出大荒踏入人世。",
        "protagonist_dual_persona": {
            "surface": "懵懂无害、初入江湖的乡下放牛少年",
            "shadow": "精通古道法禁忌、肉身战力恐怖的变法破壁者"
        },
        "chapter_beats": {
            "1": {
                "title": "大漠风沙，老实少年",
                "conflict_pivot": "斩杀企图血祭村落的神庙执法使，夺取神符",
                "combat_motif": "几何算学角度的元气丝线切割与骨裂沉重反馈",
                "active_clue_to_water": "CLUE-001"
            }
        }
    },
    "clues_ledger.json": [
        {
            "id": "CLUE-001",
            "name": "村长丢弃的断柄木烟杆",
            "planted_chapter": 1,
            "surface_mask": "老人抽劣质旱烟用的普通木管",
            "secret_core": "前代人皇断裂的人道祖神器残片",
            "watered_chapters": [],
            "target_payoff_arc": "人皇殿诸神黄昏",
            "status": "planted"
        }
    ],
    "imagery_cooldown.json": {
        "active_cooldowns": {
            "倒吸一口凉气": {"last_used_chapter": 0, "cooldown_until": 999},
            "恐怖如斯": {"last_used_chapter": 0, "cooldown_until": 999}
        }
    }
}

# 3. 凡人仙侠预设 (凡人修仙/赤心巡天向)
xianxia_preset = {
    "character_registry.json": {
        "protagonist": {
            "name": "李沉舟",
            "voice_tone": "相貌平平，言语寡淡木讷，行事极度低调隐忍，遇杀局断腕果决",
            "habitual_gestures": ["退后半步", "双手拢入袖口", "指腹摩挲储物袋"],
            "forbidden_behaviors": ["严禁出风头", "严禁为虚名争斗", "严禁妇人之仁放虎归山"],
            "current_status": {
                "location": "青云宗外门矿山小棚",
                "health": "炼气四层，经脉略显干涩",
                "equipment": ["粗糙灰布道袍", "下品精铁飞剑", "三块下品灵石"]
            }
        }
    },
    "volume_outline.json": {
        "volume_id": "VOL-01",
        "volume_title": "第一卷：微末散修",
        "macro_conflict": "修仙界灵气日渐稀薄，各大宗门垄断筑基丹药，底层外门矿修命如草芥，主角在夹缝中谋求长生资粮。",
        "protagonist_dual_persona": {
            "surface": "资质平庸、按部就班挖矿的外门杂役",
            "shadow": "暗中掌握催熟灵草玄宝、冷血夺宝的求道孤狼"
        },
        "chapter_beats": {
            "1": {
                "title": "废矿暗影，铁剑初鸣",
                "conflict_pivot": "矿洞遭遇同门劫杀，反杀灭口并搜刮储物袋",
                "combat_motif": "飞剑对撞灵光黯淡与近身符箓偷袭",
                "active_clue_to_water": "CLUE-001"
            }
        }
    },
    "clues_ledger.json": [
        {
            "id": "CLUE-001",
            "name": "生锈的无铭青铜小药铲",
            "planted_chapter": 1,
            "surface_mask": "杂役堂配发的生锈采药废铁",
            "secret_core": "可吸纳草木精魄、逆转药材年份的上古仙府遗珍",
            "watered_chapters": [],
            "target_payoff_arc": "筑基秘境夺丹战",
            "status": "planted"
        }
    ],
    "imagery_cooldown.json": {
        "active_cooldowns": {
            "冷哼一声跳将出来": {"last_used_chapter": 0, "cooldown_until": 999}
        }
    }
}

# 4. 诡秘西幻预设 (诡秘之主向)
western_preset = {
    "character_registry.json": {
        "protagonist": {
            "name": "安东尼·莫兰",
            "voice_tone": "维多利亚绅士礼仪，表面温和客气，内心理性缜密，时刻谨防理智失控",
            "habitual_gestures": ["轻正单片眼镜或礼帽", "右手探入风衣口袋握紧左轮", "默默计数心跳"],
            "forbidden_behaviors": ["严禁冲动无脑莽撞", "严禁忽视理智失控征兆"],
            "current_status": {
                "location": "贝克兰德桥区廉价公寓",
                "health": "灵性平稳，序列9【占卜家】初阶",
                "equipment": ["旧双排扣厚呢风衣", "转轮手枪一柄及六枚猎魔子弹", "黄铜怀表"]
            }
        }
    },
    "volume_outline.json": {
        "volume_id": "VOL-01",
        "volume_title": "第一卷：雾夜占卜家",
        "macro_conflict": "工业革命蒸汽车间下的贫困工人与黑死病阴影，非凡者官方教会与隐秘邪神教派的暗中绞杀，主角为了求生与寻找回家之路探索序列之秘。",
        "protagonist_dual_persona": {
            "surface": "为中产阶级寻找失踪宠物的平民侦探",
            "shadow": "灰雾神殿之上统御隐秘聚会的神秘执掌者"
        },
        "chapter_beats": {
            "1": {
                "title": "煤气灯下，铅弹与灵摆",
                "conflict_pivot": "调查一起富商暴毙案，遭遇畸变怪物袭击，开枪反击",
                "combat_motif": "左轮后坐力与硝烟味，精神受到轻微污染的幻听针扎感",
                "active_clue_to_water": "CLUE-001"
            }
        }
    },
    "clues_ledger.json": [
        {
            "id": "CLUE-001",
            "name": "表面磨损的古典黄铜怀表",
            "planted_chapter": 1,
            "surface_mask": "典当行五便士淘来的旧怀表，秒针偶尔倒转",
            "secret_core": "源自第四纪图铎王朝的【时空窥镜】核心齿轮",
            "watered_chapters": [],
            "target_payoff_arc": "第一卷末特里尔大雾霾浩劫",
            "status": "planted"
        }
    ],
    "imagery_cooldown.json": {
        "active_cooldowns": {
            "桀桀怪笑": {"last_used_chapter": 0, "cooldown_until": 999}
        }
    }
}

presets = {
    "history": history_preset,
    "xuanhuan": xuanhuan_preset,
    "xianxia": xianxia_preset,
    "western_fantasy": western_preset
}

for genre, files in presets.items():
    g_dir = os.path.join(BASE_DIR, genre)
    os.makedirs(g_dir, exist_ok=True)
    for fname, content in files.items():
        with open(os.path.join(g_dir, fname), "w", encoding="utf-8") as f:
            json.dump(content, f, ensure_ascii=False, indent=2)
    print(f"Created preset: {genre}")
