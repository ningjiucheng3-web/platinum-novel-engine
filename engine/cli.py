import argparse
import sys
import os
import json

from .state_manager import StateManager
from .context_compiler import compile_chapter_prompt
from .qa_inspector import inspect_chapter

def main():
    parser = argparse.ArgumentParser(
        prog="novel",
        description="Universal Novel Engine CLI - 工业级长篇网文外骨骼生成管线"
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # init
    p_init = subparsers.add_parser("init", help="初始化新小说工作区")
    p_init.add_argument("--genre", default="history", choices=["history", "xuanhuan", "xianxia", "western_fantasy"], help="预设题材模式")
    p_init.add_argument("--dir", default=".", help="工作区目录")

    # prompt
    p_prompt = subparsers.add_parser("prompt", help="编译指定章节的生产级 Prompt")
    p_prompt.add_argument("chapter", type=int, help="目标章节序号")
    p_prompt.add_argument("--mode", default="history", help="题材模式 (history/xuanhuan/xianxia/western_fantasy/hybrid)")
    p_prompt.add_argument("--dir", default=".", help="工作区目录")

    # qa
    p_qa = subparsers.add_parser("qa", help="质检指定章节文本并更新状态机")
    p_qa.add_argument("chapter", type=int, help="章节序号")
    p_qa.add_argument("--file", help="正文文件路径 (若不指定则从 stdin 读取)")
    p_qa.add_argument("--dir", default=".", help="工作区目录")

    # status
    p_status = subparsers.add_parser("status", help="查看当前小说大纲进度与状态机")
    p_status.add_argument("--dir", default=".", help="工作区目录")

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

    elif args.command == "qa":
        if args.file:
            with open(args.file, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            print("请输入或粘贴章节正文 (输入完成后按 Ctrl+D 结束):")
            content = sys.stdin.read()

        report = inspect_chapter(args.chapter, content, workspace_dir=args.dir)
        print("\n=== 质检报告 ===")
        print(f"通过状态: {'✅ 通过 (PASSED)' if report['passed'] else '❌ 未通过 (FAILED)'}")
        print(f"字数: {report['word_count']} 字 | 段落均长: {report['mean_para_len']} 字")
        print(f"短段落率: {round(report['short_para_ratio']*100, 1)}% | 动作交织率: {round(report['interleave_ratio']*100, 1)}%")
        print(f"具象物理词: {report['found_phys_cues']}")
        if report['critiques']:
            print("扣分项提示:")
            for c in report['critiques']:
                print(f"  - {c}")

    elif args.command == "status":
        sm = StateManager(args.dir)
        outline = sm.get_volume_outline()
        clues = sm.get_clues_ledger()
        chars = sm.get_character_registry()
        print(f"\n【书卷名称】: {outline.get('volume_title', '未知')}")
        print(f"【宏观冲突】: {outline.get('macro_conflict', '未知')}")
        print(f"【主角姓名】: {chars.get('protagonist', {}).get('name', '未知')}")
        print("\n【章节进度】:")
        for ch_idx, beat in outline.get("chapter_beats", {}).items():
            st = beat.get("status", "pending")
            icon = "✅" if st == "completed" else "⏳"
            print(f"  第 {ch_idx:>2} 章: [{icon} {st:<9}] {beat.get('title', '无题')}")
        print("\n【伏笔监控】:")
        for c in clues:
            print(f"  [{c['id']}] {c['name']} (埋入:第{c['planted_chapter']}章 | 滋养:{c['watered_chapters']} | 状态:{c['status']})")

if __name__ == "__main__":
    main()
