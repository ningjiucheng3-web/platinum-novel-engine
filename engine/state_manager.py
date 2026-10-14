"""Universal Novel Engine - State Manager v2.1
Manages project state, outline beats, clues ledger, character registry, and text archives.
"""

import os
import shutil
import json
from typing import Dict, Any, List

class StateManager:
    def __init__(self, workspace_dir="."):
        self.workspace_dir = os.path.abspath(workspace_dir)
        self.state_dir = os.path.join(self.workspace_dir, "state")
        self.chapters_dir = os.path.join(self.state_dir, "chapters")

    def init_project(self, genre="history", title="新小说"):
        os.makedirs(self.chapters_dir, exist_ok=True)
        preset_src = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "presets", genre)
        if not os.path.exists(preset_src):
            raise ValueError(f"Unknown genre preset: {genre}. Available: history, xuanhuan, xianxia, western_fantasy")

        for fname in os.listdir(preset_src):
            if fname.endswith(".json"):
                shutil.copy(os.path.join(preset_src, fname), os.path.join(self.state_dir, fname))

        print(f"[OK] Novel workspace initialized at: {self.workspace_dir}")
        print(f"[OK] Loaded genre preset: {genre}")
        print(f"[OK] Created database in {self.state_dir}")

    def get_character_registry(self) -> Dict[str, Any]:
        p = os.path.join(self.state_dir, "character_registry.json")
        if not os.path.exists(p):
            return {}
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_character_registry(self, data: Dict[str, Any]):
        os.makedirs(self.state_dir, exist_ok=True)
        with open(os.path.join(self.state_dir, "character_registry.json"), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_clues_ledger(self) -> List[Dict[str, Any]]:
        p = os.path.join(self.state_dir, "clues_ledger.json")
        if not os.path.exists(p):
            return []
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_clues_ledger(self, data: List[Dict[str, Any]]):
        os.makedirs(self.state_dir, exist_ok=True)
        with open(os.path.join(self.state_dir, "clues_ledger.json"), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_imagery_cooldown(self) -> Dict[str, Any]:
        p = os.path.join(self.state_dir, "imagery_cooldown.json")
        if not os.path.exists(p):
            return {"active_cooldowns": {}}
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_volume_outline(self) -> Dict[str, Any]:
        p = os.path.join(self.state_dir, "volume_outline.json")
        if not os.path.exists(p):
            return {"chapter_beats": {}}
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_volume_outline(self, data: Dict[str, Any]):
        os.makedirs(self.state_dir, exist_ok=True)
        with open(os.path.join(self.state_dir, "volume_outline.json"), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def save_chapter_beat(self, chapter_idx: int, beat_dict: Dict[str, Any]):
        outline = self.get_volume_outline()
        beats = outline.setdefault("chapter_beats", {})
        beats[str(chapter_idx)] = beat_dict
        self.save_volume_outline(outline)

    def get_chapter_tail(self, chapter_idx: int) -> str:
        if chapter_idx <= 0:
            return ""
        ch_path = os.path.join(self.chapters_dir, f"chapter_{chapter_idx:03d}.txt")
        if os.path.exists(ch_path):
            with open(ch_path, "r", encoding="utf-8") as f:
                text = f.read().strip()
                return text[-600:] if len(text) > 600 else text
        return ""
