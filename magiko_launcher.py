import subprocess
import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk


def resolve_project_root() -> Path:
    if getattr(sys, "frozen", False):
        exe_dir = Path(sys.executable).resolve().parent
        candidates = [exe_dir, exe_dir.parent]
    else:
        candidates = [Path(__file__).resolve().parent]

    for candidate in candidates:
        if (candidate / ".venv" / "Scripts" / "python.exe").exists():
            return candidate
    return candidates[0]


PROJECT_ROOT = resolve_project_root()

VENV_PYTHON = PROJECT_ROOT / ".venv" / "Scripts" / "python.exe"
ICON_PATH = PROJECT_ROOT / "magiko_launcher_icon.ico"
SPRITE_PREVIEW = PROJECT_ROOT / "img" / "characters" / "orange_superhero" / "idle" / "pixil-frame-0.png"

LAUNCH_TARGETS = {
    "Play Magiko": PROJECT_ROOT / "src" / "main.py",
    "Pixel Editor": PROJECT_ROOT / "pixel_editor.py",
    "Level Creator": PROJECT_ROOT / "src" / "level_creator.py",
}


class MagikoLauncher:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Magiko Launcher")
        self.root.geometry("420x340")
        self.root.resizable(False, False)
        self.root.configure(bg="#1c1c24")
        if ICON_PATH.exists():
            try:
                self.root.iconbitmap(ICON_PATH)
            except Exception:
                pass

        self.preview_image = None
        self._build_ui()

    def _build_ui(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Dark.TFrame", background="#1c1c24")
        style.configure("Dark.TLabel", background="#1c1c24", foreground="#f3f3f6")
        style.configure("Title.TLabel", background="#1c1c24", foreground="#f3f3f6", font=("Segoe UI", 17, "bold"))
        style.configure("Hint.TLabel", background="#1c1c24", foreground="#cfcfe6", font=("Segoe UI", 10))
        style.configure("Launch.TButton", background="#d96c06", foreground="#ffffff", padding=10, font=("Segoe UI", 11, "bold"))
        style.map("Launch.TButton", background=[("active", "#f28c18")])
        style.configure("Ghost.TButton", background="#343447", foreground="#f3f3f6", padding=8)
        style.map("Ghost.TButton", background=[("active", "#46465f")])

        container = ttk.Frame(self.root, style="Dark.TFrame", padding=18)
        container.pack(fill="both", expand=True)

        header = ttk.Frame(container, style="Dark.TFrame")
        header.pack(fill="x", pady=(0, 18))

        preview = self._load_preview_image()
        if preview is not None:
            preview_label = tk.Label(header, image=preview, bg="#1c1c24", bd=0, highlightthickness=0)
            preview_label.pack(side="left", padx=(0, 14))

        text_block = ttk.Frame(header, style="Dark.TFrame")
        text_block.pack(side="left", fill="y")
        ttk.Label(text_block, text="Magiko", style="Title.TLabel").pack(anchor="w")
        ttk.Label(text_block, text="Choose what you want to open", style="Hint.TLabel").pack(anchor="w", pady=(4, 0))

        for label, target in LAUNCH_TARGETS.items():
            ttk.Button(
                container,
                text=label,
                style="Launch.TButton",
                command=lambda path=target, name=label: self.launch(path, name),
            ).pack(fill="x", pady=6)

        footer = ttk.Frame(container, style="Dark.TFrame")
        footer.pack(fill="x", side="bottom", pady=(18, 0))

        ttk.Label(
            footer,
            text="Uses the Magiko virtual environment automatically.",
            style="Hint.TLabel",
        ).pack(anchor="w", pady=(0, 10))

        ttk.Button(footer, text="Open Project Folder", style="Ghost.TButton", command=self.open_project_folder).pack(fill="x")
        ttk.Button(footer, text="Close", style="Ghost.TButton", command=self.root.destroy).pack(fill="x", pady=(8, 0))

    def _load_preview_image(self):
        if not SPRITE_PREVIEW.exists():
            return None
        try:
            image = tk.PhotoImage(file=str(SPRITE_PREVIEW))
            self.preview_image = image.zoom(4, 4)
            return self.preview_image
        except Exception:
            return None

    def launch(self, target: Path, label: str) -> None:
        if not VENV_PYTHON.exists():
            messagebox.showerror(
                "Python not found",
                f"Magiko virtual environment was not found:\n{VENV_PYTHON}",
            )
            return
        if not target.exists():
            messagebox.showerror("File not found", f"Could not find:\n{target}")
            return

        try:
            subprocess.Popen(
                [str(VENV_PYTHON), str(target)],
                cwd=str(PROJECT_ROOT),
            )
            self.root.destroy()
        except Exception as exc:
            messagebox.showerror("Launch failed", f"Could not open {label}:\n{exc}")

    def open_project_folder(self) -> None:
        try:
            subprocess.Popen(["explorer.exe", str(PROJECT_ROOT)])
        except Exception as exc:
            messagebox.showerror("Open folder failed", str(exc))


def main() -> None:
    root = tk.Tk()
    MagikoLauncher(root)
    root.mainloop()


if __name__ == "__main__":
    main()
