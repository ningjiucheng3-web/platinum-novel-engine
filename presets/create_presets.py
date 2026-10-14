import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. 历史权谋预设 (覆汉/黜龙向)
history_preset = {
    "character_registry.json": {
        "protagonist": {
            "name": "沈淮",
            "role": "protagonist",
            "debut_chapter": 1,
            "voice_tone": "沉稳端方，言辞合乎汉晋仪轨，内心极度理智，精算天下账目",
            "habitual_gestures": ["按刀四顾", "整理长袍袖口", "指尖轻扣案几"],
            "forbidden_behaviors": ["严禁狂笑咆哮", "严禁无脑发表热血演讲", "严禁冲动当堂顶撞大员"],
            "current_status": {
                "location": "京畿督邮曹官廨",
                "health": "精气神饱满，左臂有旧年骑射拉伤",
                "equipment": ["半旧青绢长衫", "佩刀一柄", "户部度支旧账册一本"]
            }
        },
        "characters": [
            {
                "name": "沈淮",
                "role": "protagonist",
                "debut_chapter": 1,
                "archetype": "理智寒门度支吏"
            },
            {
                "name": "老韩头",
                "role": "guide",
                "debut_chapter": 1,
                "archetype": "引路老吏/前代度支案幸存者",
                "exit_mechanism": "第24章因查获私盐亏空被豪强灭口，临终前将京畿暗账残册托付主角，达成代谢交接"
            },
            {
                "name": "铁柱",
                "role": "loyal_escort",
                "debut_chapter": 1,
                "archetype": "忠勇伴行/军伍退役刀手"
            },
            {
                "name": "崔景纯",
                "role": "peer_rival",
                "debut_chapter": 26,
                "archetype": "世族门阀宿敌/同年入仕竞争者，行事狠辣有制度法度"
            },
            {
                "name": "薛大郎",
                "role": "rebel_comrade",
                "debut_chapter": 88,
                "archetype": "大乱期反贼头领/结义生死兄弟"
            },
            {
                "name": "陈文和",
                "role": "institutional_strategist",
                "debut_chapter": 255,
                "archetype": "深谋远虑的制度型军师/阴鸷策士"
            }
        ]
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
                                "name": "沈淮",
                                "action_objective": "核查淮南盐铁使虚报之折色粮米，找出五万石亏空差额",
                                "hidden_motivation": "试探老吏老韩头是否已收了城西门阀炭敬，预备锁定第一份罪证",
                                "sensory_micro_gesture": "指肚轻擦受潮发脆的粗黄账纸边缘，按压算筹发出轻微顿挫声"
                            },
                            {
                                "name": "老韩头",
                                "action_objective": "催促沈淮按旧例在销账公文上押字画押",
                                "hidden_motivation": "暗中收过豪强炭敬，恐惧引火烧身，欲拉沈淮分担罪责",
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
                    "tail_physical_state": "沈淮手中狼毫笔尖悬停在泛黄旧账末尾，屋顶瓦片忽传来一声极轻微的踩雪脆响",
                    "unresolved_friction": "佩刀挂在三步外横桁上，来人已至屋檐，刀与墨不可兼得"
                }
            }
        }
    },
    "clues_ledger.json": [
        {
            "id": "CLUE-001",
            "name": "旧年辽东军粮账册残卷",
            "planted_chapter": 1,
            "surface_mask": "垫桌角的一本旧账簿，字迹模糊，边角受潮发霉",
            "secret_core": "记录了当朝首辅通敌倒卖军械与虚报五万石军饷的铁证",
            "watered_chapters": [1],
            "target_harvest_chapter": 120,
            "status": "active"
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

# 2. 玄幻变法预设 (牧神记向)
xuanhuan_preset = {
    "character_registry.json": {
        "protagonist": {
            "name": "陆玄",
            "role": "protagonist",
            "debut_chapter": 1,
            "voice_tone": "笑眯眯，自称大荒老实山民，言语温和纯朴，下手绝不容情",
            "habitual_gestures": ["纯真微笑", "摸后脑勺", "藏在袖中的断空短刃微振"],
            "forbidden_behaviors": ["严禁邪魅装逼", "严禁视凡人为蝼蚁", "严禁无脑叫嚣"],
            "current_status": {
                "location": "大荒边关破落驿站",
                "health": "元气如江河充盈，神藏初辟",
                "equipment": ["粗布麻衣", "杀猪短刃", "行囊里的苞谷面饼"]
            }
        },
        "characters": [
            {
                "name": "陆玄",
                "role": "protagonist",
                "debut_chapter": 1,
                "archetype": "纯良外表下的道法革命者"
            },
            {
                "name": "瞎眼跛足老村长",
                "role": "guide",
                "debut_chapter": 1,
                "archetype": "引路老人/残老村守护者",
                "exit_mechanism": "第18章将人皇祖印交予主角后封村闭关，隔绝大荒与人世，主角独自入延康求学"
            },
            {
                "name": "哑巴铁匠",
                "role": "loyal_escort",
                "debut_chapter": 1,
                "archetype": "护道者/神兵锻造哑仆"
            },
            {
                "name": "卫天元",
                "role": "peer_rival",
                "debut_chapter": 30,
                "archetype": "太学院第一国士/算学神通天骄镜像"
            },
            {
                "name": "白狐妖帅",
                "role": "rebel_comrade",
                "debut_chapter": 92,
                "archetype": "乱世起义异族统领"
            },
            {
                "name": "天圣教主",
                "role": "institutional_strategist",
                "debut_chapter": 260,
                "archetype": "暗中掌控半壁帝国的改革总舵手"
            }
        ]
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
                "chapter_id": 1,
                "volume_id": "VOL-01",
                "title": "大漠风沙，老实少年",
                "word_budget": 3500,
                "paragraph_budget": {
                    "total_target": 65,
                    "short_paragraphs_target_pct": 52,
                    "max_paragraph_length": 110
                },
                "narrative_four_dimensions": {
                    "action_and_physical_friction_pct": 52.0,
                    "interleaved_dialogue_pct": 40.0,
                    "environment_and_logistics_pct": 7.0,
                    "pure_monologue_pct": 1.0
                },
                "scene_beats": [
                    {
                        "scene_id": 1,
                        "location": "大荒边关断壁残垣（黑夜狂风夹带骨殖、腐朽木雕神像、残存篝火）",
                        "characters_present": [
                            {
                                "name": "陆玄",
                                "action_objective": "削断神庙执法使的飞剑索命符，割下异种鹿皮充饥",
                                "hidden_motivation": "暗中验算村长所授几何算学轨迹，寻找神庙功法的破绽死角",
                                "sensory_micro_gesture": "指尖拂过杀猪短刃锋刃，听金属嗡鸣声计算风阻"
                            }
                        ],
                        "physical_friction_point": "飞剑寒气冻裂掌心皮肉，短刃切入青铜剑脊遭遇反震剧痛",
                        "spoken_subtext": "自称无害山民，每问一句老实问题便前踏一步拉近必杀距离",
                        "clue_action": {
                            "clue_id": "CLUE-001",
                            "action_type": "WATER",
                            "concrete_detail": "怀中木烟杆在神庙黑光照耀下隐隐泛起微弱青金色光晕"
                        }
                    }
                ],
                "chapter_tail_hook": {
                    "tail_physical_state": "陆玄拔出染血短刃在草靴上擦拭血沫，地平线尽头三道神庙巡界流光骤然停滞转向",
                    "unresolved_friction": "大荒黑夜暴雪封路，追兵已嗅到异血气息"
                }
            }
        }
    },
    "clues_ledger.json": [
        {
            "id": "CLUE-001",
            "name": "村长丢弃的断柄木烟杆",
            "planted_chapter": 1,
            "surface_mask": "老人抽劣质旱烟用的普通枯木管",
            "secret_core": "前代人皇断裂的人道祖神器残片",
            "watered_chapters": [1],
            "target_harvest_chapter": 150,
            "status": "active"
        }
    ],
    "imagery_cooldown.json": {
        "active_cooldowns": {
            "深吸一口气": {"last_used_chapter": 0, "cooldown_until": 5},
            "冷笑一声": {"last_used_chapter": 0, "cooldown_until": 8}
        }
    }
}

# 3. 仙侠古典预设
xianxia_preset = {
    "character_registry.json": {
        "protagonist": {
            "name": "陈青",
            "role": "protagonist",
            "debut_chapter": 1,
            "voice_tone": "淡漠寡言，敬畏因果天道，剑出必见血",
            "habitual_gestures": ["拂尘整袖", "按剑而立", "静默闭目"],
            "forbidden_behaviors": ["严禁盲目越级狂虐全场", "严禁废话连篇"],
            "current_status": {
                "location": "九华剑宗外门杂役竹林",
                "health": "炼气三层，经脉有火毒郁结",
                "equipment": ["青竹剑一柄", "残缺度厄经一卷"]
            }
        },
        "characters": [
            {
                "name": "陈青",
                "role": "protagonist",
                "debut_chapter": 1,
                "archetype": "苦修求道剑修"
            },
            {
                "name": "吴执事",
                "role": "guide",
                "debut_chapter": 1,
                "archetype": "引路外门执事",
                "exit_mechanism": "第21章因筑基失败大限将至坐化，将外门信物与残缺剑经留与主角"
            },
            {
                "name": "赵真传",
                "role": "peer_rival",
                "debut_chapter": 28,
                "archetype": "内门天骄宿敌镜像"
            }
        ]
    },
    "volume_outline.json": {
        "volume_id": "VOL-01",
        "volume_title": "第一卷：外门洗剑",
        "macro_conflict": "宗门气运枯竭，外门资源被豪族把持，主角以微末杂役之躯借古剑经破局。",
        "protagonist_dual_persona": {
            "surface": "任劳任怨的外门杂役弟子",
            "shadow": "暗修失传斩仙古剑诀的逆天求道者"
        },
        "chapter_beats": {
            "1": {
                "chapter_id": 1,
                "volume_id": "VOL-01",
                "title": "寒泉试剑，浊浊风尘",
                "word_budget": 3200,
                "paragraph_budget": {
                    "total_target": 60,
                    "short_paragraphs_target_pct": 50,
                    "max_paragraph_length": 115
                },
                "narrative_four_dimensions": {
                    "action_and_physical_friction_pct": 50.0,
                    "interleaved_dialogue_pct": 41.0,
                    "environment_and_logistics_pct": 8.0,
                    "pure_monologue_pct": 1.0
                },
                "scene_beats": [
                    {
                        "scene_id": 1,
                        "location": "洗剑池畔（寒水刺骨、青苔滑腻、残损顽石）",
                        "characters_present": [
                            {
                                "name": "陈青",
                                "action_objective": "在寒泉中磨砺钝剑，排出体内火毒",
                                "hidden_motivation": "试探吴执事暗中布下的眼线",
                                "sensory_micro_gesture": "粗粝麻布拭过青竹剑锋，指尖因寒冷发紫轻颤"
                            }
                        ],
                        "physical_friction_point": "顽石坚硬崩裂竹木剑胎，火毒顺经脉上涌引发剧烈喘息",
                        "spoken_subtext": "谨守尊卑规矩，言辞无懈可击",
                        "clue_action": {
                            "clue_id": "CLUE-001",
                            "action_type": "WATER",
                            "concrete_detail": "池底淤泥中显露半截锈蚀青铜剑柄"
                        }
                    }
                ],
                "chapter_tail_hook": {
                    "tail_physical_state": "陈青挽剑入鞘，身后竹林骤起杀意破空风声",
                    "unresolved_friction": "足下青苔湿滑难以发力，飞剑已临三尺门前"
                }
            }
        }
    },
    "clues_ledger.json": [
        {
            "id": "CLUE-001",
            "name": "洗剑池底断裂古剑",
            "planted_chapter": 1,
            "surface_mask": "池底烂泥中的无名锈铁",
            "secret_core": "初代祖师斩妖所断之佩剑本命灵魄",
            "watered_chapters": [1],
            "target_harvest_chapter": 110,
            "status": "active"
        }
    ],
    "imagery_cooldown.json": {
        "active_cooldowns": {}
    }
}

# 4. 西幻奇幻预设
western_preset = {
    "character_registry.json": {
        "protagonist": {
            "name": "罗恩",
            "role": "protagonist",
            "debut_chapter": 1,
            "voice_tone": "冷静克制，恪守佣兵生存信条，精通算计与火器装填",
            "habitual_gestures": ["检查转轮机括", "用指腹摩挲火药残渣", "拉低风衣帽檐"],
            "forbidden_behaviors": ["严禁盲信正义荣耀", "严禁冲动当英雄"],
            "current_status": {
                "location": "雾港下城区黑水巷酒馆",
                "health": "良好，右耳轻微耳鸣（近距离枪击后遗症）",
                "equipment": ["改良式短管转轮枪", "铅弹十二枚", "怀表"]
            }
        },
        "characters": [
            {
                "name": "罗恩",
                "role": "protagonist",
                "debut_chapter": 1,
                "archetype": "蒸汽与火枪时代的实用主义赏金猎人"
            },
            {
                "name": "老瘸子鲍恩",
                "role": "guide",
                "debut_chapter": 1,
                "archetype": "引路老兵/枪械改造师",
                "exit_mechanism": "第22章为掩护主角撤离被蒸汽教会逮捕流放黑牢，临行前交付密室钥匙"
            },
            {
                "name": "维克托中尉",
                "role": "peer_rival",
                "debut_chapter": 27,
                "archetype": "帝国调查局年轻新贵/猎魔宿敌镜像"
            }
        ]
    },
    "volume_outline.json": {
        "volume_id": "VOL-01",
        "volume_title": "第一卷：雾港低语",
        "macro_conflict": "蒸汽工业与旧日邪神崇拜剧烈碰撞，教会垄断灵能，主角以无名赏金猎人身份探查连环异化案。",
        "protagonist_dual_persona": {
            "surface": "为金磅奔波的二流枪手",
            "shadow": "掌控上古禁忌炼金法典的阴影清算人"
        },
        "chapter_beats": {
            "1": {
                "chapter_id": 1,
                "volume_id": "VOL-01",
                "title": "浓雾转轮，煤灰深巷",
                "word_budget": 3400,
                "paragraph_budget": {
                    "total_target": 65,
                    "short_paragraphs_target_pct": 55,
                    "max_paragraph_length": 110
                },
                "narrative_four_dimensions": {
                    "action_and_physical_friction_pct": 49.0,
                    "interleaved_dialogue_pct": 41.0,
                    "environment_and_logistics_pct": 9.0,
                    "pure_monologue_pct": 1.0
                },
                "scene_beats": [
                    {
                        "scene_id": 1,
                        "location": "黑水巷泥泞石子路（燃气路灯摇曳、煤灰烟雾刺鼻、阴冷雨水）",
                        "characters_present": [
                            {
                                "name": "罗恩",
                                "action_objective": "装填特制银粉铅弹，截停走私异化器官的马车",
                                "hidden_motivation": "寻找杀死搭档的畸变教会信徒线索",
                                "sensory_micro_gesture": "指尖感知击锤回弹阻力，黄铜转轮发出清脆咔哒声"
                            }
                        ],
                        "physical_friction_point": "受潮黑火药引燃滞涩，后坐力剧烈震麻虎口与腕骨",
                        "spoken_subtext": "短促冰冷的黑帮切口问询",
                        "clue_action": {
                            "clue_id": "CLUE-001",
                            "action_type": "WATER",
                            "concrete_detail": "马车残骸中掉出一枚印有三眼乌鸦徽记的染血铜怀表"
                        }
                    }
                ],
                "chapter_tail_hook": {
                    "tail_physical_state": "罗恩将发烫的枪管抵在奄奄一息的驭手额头，浓雾深处骤然响起沉重蒸汽机甲践踏声",
                    "unresolved_friction": "弹仓仅余一枚子弹，蒸汽护卫已封死巷口两端"
                }
            }
        }
    },
    "clues_ledger.json": [
        {
            "id": "CLUE-001",
            "name": "三眼乌鸦染血怀表",
            "planted_chapter": 1,
            "surface_mask": "停走的普通黄铜机械怀表",
            "secret_core": "记录帝国皇家炼金学会暗中祭祀邪神的加密坐标齿轮",
            "watered_chapters": [1],
            "target_harvest_chapter": 130,
            "status": "active"
        }
    ],
    "imagery_cooldown.json": {
        "active_cooldowns": {}
    }
}

presets = {
    "history": history_preset,
    "xuanhuan": xuanhuan_preset,
    "xianxia": xianxia_preset,
    "western_fantasy": western_preset
}

for name, files in presets.items():
    pdir = os.path.join(BASE_DIR, name)
    os.makedirs(pdir, exist_ok=True)
    for fname, data in files.items():
        with open(os.path.join(pdir, fname), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[OK] Generated presets for: {name}")

print("All presets updated successfully.")
