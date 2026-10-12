import os
import shutil
import json

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

    def get_character_registry(self):
        with open(os.path.join(self.state_dir, "character_registry.json"), "r", encoding="utf-8") as f:
            return json.load(f)

    def get_clues_ledger(self):
        with open(os.path.join(self.state_dir, "clues_ledger.json"), "r", encoding="utf-8") as f:
            return json.load(f)

    def get_imagery_cooldown(self):
        with open(os.path.join(self.state_dir, "imagery_cooldown.json"), "r", encoding="utf-8") as f:
            return json.load(f)

    def get_volume_outline(self):
        with open(os.path.join(self.state_dir, "volume_outline.json"), "r", encoding="utf-8") as f:
            return json.load(f)

    def get_chapter_tail(self, chapter_idx):
        if chapter_idx <= 0:
            return ""
        ch_path = os.path.join(self.chapters_dir, f"chapter_{chapter_idx:03d}.txt")
        if os.path.exists(ch_path):
            with open(ch_path, "r", encoding="utf-8") as f:
                text = f.read().strip()
                return text[-600:] if len(text) > 600 else text
        return ""
