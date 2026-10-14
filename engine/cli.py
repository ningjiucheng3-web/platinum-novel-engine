"""Universal Novel Engine CLI v2.1
Industrial-grade web novel generation pipeline CLI grounded in the Platinum Reverse Engineering Whitepaper.
"""

import argparse
import sys
import os
import json

from .state_manager import StateManager
from .context_compiler import compile_chapter_prompt
from .qa_inspector import inspect_chapter
from .schema import get_default_beat_template, validate_beat_schema
from .wave_validator import validate_character_waves, validate_clues_lifecycle

def main():
    parser = argparse.ArgumentParser(
        prog="novel",
        description="Universal Novel Engine CLI v2.1 - 工业级白金网文生成外骨骼管线"
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # init
    p_init = subparsers.add_parser("init", help="初始化新小说工作区")
    p_init.add_argument("--genre", default="history", choices=["history", "xuanhuan", "xianxia", "western_fantasy"], help="预设题材模式")
    p_init.add_argument("--dir", default=".", help="工作区目录")

    # prompt
    p_prompt = subparsers.add_parser("prompt", help="编译指定章节的生产级 Prompt (支持细纲分镜与四维配比)")
    p_prompt.add_argument("chapter", type=int, help="目标章节序号")
    p_prompt.add_argument("--mode", default="history", help="题材模式 (history/xuanhuan/xianxia/western_fantasy/hybrid)")
    p_prompt.add_argument("--dir", default=".", help="工作区目录")

    # qa
    p_qa = subparsers.add_parser("qa", help="四维质检指定章节文本并更新状态机")
    p_qa.add_argument("chapter", type=int, help="章节序号")
    p_qa.add_argument("--file", help="正文文件路径 (若不指定则从 stdin 读取)")
    p_qa.add_argument("--dir", default=".", help="工作区目录")

    # status
    p_status = subparsers.add_parser("status", help="查看小说大纲进度、四波次人物与状态机")
    p_status.add_argument("--dir", default=".", help="工作区目录")

    # beat-template
    p_beat = subparsers.add_parser("beat-template", help="生成指定章节的超微颗粒度细纲模板 (UniversalChapterBeatSchema)")
    p_beat.add_argument("chapter", type=int, help="目标章节序号")
    p_beat.add_argument("--apply", action="store_true", help="直接写入 volume_outline.json")
    p_beat.add_argument("--dir", default=".", help="工作区目录")

    # validate
    p_val = subparsers.add_parser("validate", help="校验大纲细纲合规性、四波次人物脉冲与伏笔生命周期")
    p_val.add_argument("target", choices=["all", "outline", "characters", "clues"], default="all", nargs="?", help="校验目标")
    p_val.add_argument("--dir", default=".", help="工作区目录")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "init":
        sm = StateManager(args.dir)
        sm.init_project(genre=args.genre)

    elif args.command == "prompt":
        prompt = compile_chapter_prompt(args.chapter, mode=args.mode, workspace_dir=args.dir)
        print(prompt)

    elif args.command == "beat-template":
        sm = StateManager(args.dir)
        outline = sm.get_volume_outline()
        vol_id = outline.get("volume_id", "VOL-01")
        tpl = get_default_beat_template(args.chapter, volume_id=vol_id)
        if args.apply:
            sm.save_chapter_beat(args.chapter, tpl)
            print(f"[OK] 第 {args.chapter} 章细纲模板已写入 {os.path.join(sm.state_dir, 'volume_outline.json')}")
        else:
            print(json.dumps(tpl, ensure_ascii=False, indent=2))

    elif args.command == "qa":
        if args.file:
            with open(args.file, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            print("请输入或粘贴章节正文 (输入完成后按 Ctrl+D 结束):")
            content = sys.stdin.read()

        report = inspect_chapter(args.chapter, content, workspace_dir=args.dir)
        print("\n" + "="*50)
        print(f"  第 {args.chapter} 章 四维叙事质检报告")
        print("="*50)
        print(f"通过状态: {'✅ 通过 (PASSED)' if report['passed'] else '❌ 未通过 (FAILED)'}")
        print(f"总 字 数: {report['word_count']} 字 | 总自然段: {report['total_paragraphs']} 段 | 段均长: {report['mean_para_len']} 字")
        print(f"短段落率: {round(report['short_para_ratio']*100, 1)}% (目标>40%) | 对话字数比: {round(report['dialogue_char_ratio']*100, 1)}%")
        print(f"对白穿插率: {round(report['interleave_ratio']*100, 1)}% (目标>65%) | 估算独立场景: {report['estimated_scene_count']} 个 (白金标准1.2-1.8)")
        
        dims = report.get("four_dimensional_composition", {})
        print("\n【四维叙事结构配比】:")
        print(f"  - 动作与物理受阻: {dims.get('action_friction_pct', 0)}% (白金均值 ~48%)")
        print(f"  - 动作交织对白:   {dims.get('interleaved_dialogue_pct', 0)}% (白金均值 ~42%)")
        print(f"  - 环境与度支风物: {dims.get('environment_logistics_pct', 0)}% (白金均值 ~9%)")
        print(f"  - 纯内心独白:     {dims.get('pure_monologue_pct', 0)}% (白金严控 <1.5%)")

        print(f"\n【捕捉具象物理词】: {', '.join(report['found_phys_cues']) if report['found_phys_cues'] else '无'}")
        if report['critiques']:
            print("\n【扣分项与违规提示】:")
            for c in report['critiques']:
                print(f"  ⚠️  {c}")
        print("="*50 + "\n")

    elif args.command == "status":
        sm = StateManager(args.dir)
        outline = sm.get_volume_outline()
        clues = sm.get_clues_ledger()
        chars = sm.get_character_registry()
        
        protagonist_name = chars.get('protagonist', {}).get('name', '主角')
        if not protagonist_name and "characters" in chars:
            for ch in chars["characters"]:
                if ch.get("role") == "protagonist":
                    protagonist_name = ch.get("name")
                    break

        print("\n" + "="*50)
        print(f"【书卷信息】: {outline.get('volume_title', '未知')} ({outline.get('volume_id', 'VOL-01')})")
        print(f"【宏观冲突】: {outline.get('macro_conflict', '未知')}")
        print(f"【核 心 主角】: {protagonist_name}")
        print("="*50)

        print("\n【章节细纲进度】:")
        beats = outline.get("chapter_beats", {})
        if not beats:
            print("  （暂无已规划章节，可用 'novel beat-template <ch> --apply' 生成）")
        for ch_idx, beat in sorted(beats.items(), key=lambda x: int(x[0]) if x[0].isdigit() else 0):
            st = beat.get("status", "pending")
            icon = "✅" if st == "completed" else "⏳"
            sc_count = len(beat.get("scene_beats", [])) if "scene_beats" in beat else 1
            print(f"  第 {ch_idx:>2} 章: [{icon} {st:<9}] {beat.get('title', '无题')} (微场景: {sc_count}个)")

        print("\n【四波次人物登场总览】:")
        _, _, char_stats = validate_character_waves(chars)
        for wave_id, cnt in char_stats["wave_counts"].items():
            print(f"  - {wave_id}: {cnt} 位登场")
        if char_stats["guide_npcs"]:
            print(f"  * 重点引路人: {', '.join(char_stats['guide_npcs'])} (需严格执行杜盟代谢律)")

        print("\n【契诃夫之枪 (伏笔监控)】:")
        for c in clues:
            w_count = len(c.get("watered_chapters", []))
            print(f"  [{c['id']}] {c['name']} (埋入:第{c.get('planted_chapter', 1)}章 | 滋养:{w_count}次 | 状态:{c.get('status', 'active')})")
        print()

    elif args.command == "validate":
        sm = StateManager(args.dir)
        target = args.target
        all_passed = True

        print("\n" + "="*50)
        print("  Universal Novel Engine 工程合规性审查")
        print("="*50)

        # 1. Outline Beat Schema Check
        if target in ["all", "outline"]:
            outline = sm.get_volume_outline()
            beats = outline.get("chapter_beats", {})
            print(f"\n[1/3] 检查章节细纲规范 (共 {len(beats)} 章)...")
            outline_passed = True
            for ch_idx, beat in beats.items():
                if "scene_beats" in beat:
                    valid, critiques = validate_beat_schema(beat)
                    if not valid:
                        outline_passed = False
                        all_passed = False
                        print(f"  ❌ 第 {ch_idx} 章细纲未完全合规:")
                        for c in critiques:
                            print(f"     - {c}")
                    else:
                        print(f"  ✅ 第 {ch_idx} 章细纲合规: {beat.get('title', '')}")
                else:
                    print(f"  ⚠️  第 {ch_idx} 章为简易细纲，建议升级至 UniversalChapterBeatSchema")
            if outline_passed and beats:
                print("  => 章节细纲校验全部合规！")

        # 2. Four-Wave Character Check
        if target in ["all", "characters"]:
            chars = sm.get_character_registry()
            print(f"\n[2/3] 检查四波次人物脉冲与杜盟律...")
            char_valid, char_critiques, char_stats = validate_character_waves(chars)
            if not char_valid:
                all_passed = False
                print("  ❌ 人物谱系规划存在违规:")
                for c in char_critiques:
                    print(f"     - {c}")
            else:
                print("  ✅ 四波次人物脉冲节奏合规！引路人代谢机制已就绪。")

        # 3. Clues Lifecycle Check
        if target in ["all", "clues"]:
            clues = sm.get_clues_ledger()
            print(f"\n[3/3] 检查契诃夫之枪 (伏笔生命周期)...")
            clue_valid, clue_critiques, _ = validate_clues_lifecycle(clues)
            if not clue_valid:
                all_passed = False
                print("  ❌ 伏笔布局存在断层或速爆:")
                for c in clue_critiques:
                    print(f"     - {c}")
            else:
                print("  ✅ 伏笔生命周期监控正常，无遗忘之枪！")

        print("\n" + "="*50)
        if all_passed:
            print("  🏆 审查结果: 全部模块符合白金级工程规范 (PASSED)")
        else:
            print("  ⚠️  审查结果: 存在待优化或违规项，请根据提示调整")
        print("="*50 + "\n")

if __name__ == "__main__":
    main()
