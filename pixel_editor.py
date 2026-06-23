import json
import math
import tkinter as tk
from copy import deepcopy
from pathlib import Path
from tkinter import colorchooser, filedialog, messagebox, simpledialog, ttk

from PIL import Image, ImageDraw, ImageTk


DEFAULT_PALETTE = [
    "#000000",
    "#ffffff",
    "#d7263d",
    "#f46036",
    "#2e294e",
    "#1b998b",
    "#c5d86d",
    "#f6bd60",
    "#6d597a",
    "#355070",
    "#43aa8b",
    "#577590",
]

TOOL_LABELS = {
    "pencil": "Pencil",
    "eraser": "Eraser",
    "fill": "Fill",
    "picker": "Picker",
    "select": "Select",
}


class PixelEditor:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Magiko Pixel Editor")
        self.root.geometry("1360x820")
        self.root.minsize(1180, 720)
        self.root.configure(bg="#1c1c24")

        self.project_root = Path(__file__).resolve().parent
        self.img_dir = self.project_root / "img"
        self.characters_dir = self.img_dir / "characters"
        self.project_dir = self.img_dir / "pixel_editor_exports"
        self.project_dir.mkdir(parents=True, exist_ok=True)

        self.grid_size = 16
        self.pixel_size = 24
        self.preview_scale = 8
        self.selected_color = DEFAULT_PALETTE[0]
        self.previous_color = DEFAULT_PALETTE[1]
        self.current_tool = "pencil"
        self.current_frame_index = 0
        self.frames = [self.new_blank_frame()]
        self.frame_names = ["frame_01.png"]
        self.project_path = None
        self.loaded_sprite_dir = None
        self.drawing = False
        self.last_cell = None
        self.last_hover_cell = None
        self.stroke_snapshot = None
        self.undo_stack = []
        self.max_undo = 80
        self.onion_skin_enabled = tk.BooleanVar(value=True)
        self.icon_images = {}
        self.tool_buttons = {}
        self.character_sprite_dirs = []
        self.selection_start = None
        self.selection_bounds = None
        self.clipboard_cells = None
        self.pending_paste = False
        self.selection_drag_snapshot = None
        self.selection_drag_origin = None
        self.selection_drag_base = None
        self.selection_dragging = False

        self.canvas_signature = None
        self.preview_signature = None
        self.canvas_cells = []
        self.preview_cells = []
        self.selection_rect = None
        self.preview_border = None

        self._build_layout()
        self._bind_shortcuts()
        self.refresh_sprite_sources()
        self.refresh_everything()

    def new_blank_frame(self):
        return [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]

    def resized_blank_frame(self, old_frame):
        new_frame = self.new_blank_frame()
        copy_size = min(self.grid_size, len(old_frame))
        for y in range(copy_size):
            for x in range(copy_size):
                new_frame[y][x] = old_frame[y][x]
        return new_frame

    def current_state_snapshot(self):
        return {
            "frames": deepcopy(self.frames),
            "frame_names": list(self.frame_names),
            "current_frame_index": self.current_frame_index,
            "grid_size": self.grid_size,
            "selected_color": self.selected_color,
            "selection_bounds": self.selection_bounds,
            "clipboard_cells": deepcopy(self.clipboard_cells),
        }

    def restore_state_snapshot(self, snapshot):
        self.frames = deepcopy(snapshot["frames"])
        self.frame_names = list(snapshot["frame_names"])
        self.current_frame_index = snapshot["current_frame_index"]
        self.grid_size = snapshot["grid_size"]
        self.selected_color = snapshot["selected_color"]
        self.selection_bounds = snapshot.get("selection_bounds")
        self.clipboard_cells = deepcopy(snapshot.get("clipboard_cells"))
        self.pending_paste = False
        self.selection_drag_snapshot = None
        self.selection_drag_origin = None
        self.selection_drag_base = None
        self.selection_dragging = False
        self.refresh_everything()

    def push_undo_snapshot(self, snapshot=None):
        self.undo_stack.append(snapshot or self.current_state_snapshot())
        if len(self.undo_stack) > self.max_undo:
            self.undo_stack.pop(0)

    def undo(self):
        if not self.undo_stack:
            self.update_status(extra_message="Nothing to undo")
            return
        snapshot = self.undo_stack.pop()
        self.restore_state_snapshot(snapshot)
        self.update_status(extra_message="Undo applied")

    def _build_layout(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Dark.TFrame", background="#1c1c24")
        style.configure("Dark.TLabelframe", background="#1c1c24", foreground="#f3f3f6")
        style.configure("Dark.TLabelframe.Label", background="#1c1c24", foreground="#f3f3f6")
        style.configure("Dark.TLabel", background="#1c1c24", foreground="#f3f3f6")
        style.configure("Dark.TButton", background="#343447", foreground="#f3f3f6", padding=6)
        style.map("Dark.TButton", background=[("active", "#46465f")])
        style.configure("Dark.TCheckbutton", background="#1c1c24", foreground="#f3f3f6")

        main = ttk.Frame(self.root, style="Dark.TFrame", padding=12)
        main.pack(fill="both", expand=True)
        main.columnconfigure(0, weight=0)
        main.columnconfigure(1, weight=1)
        main.rowconfigure(0, weight=1)

        sidebar = ttk.Frame(main, style="Dark.TFrame")
        sidebar.grid(row=0, column=0, sticky="nsw", padx=(0, 12))

        workspace = ttk.Frame(main, style="Dark.TFrame")
        workspace.grid(row=0, column=1, sticky="nsew")
        workspace.columnconfigure(0, weight=1)
        workspace.columnconfigure(1, weight=0)
        workspace.rowconfigure(1, weight=1)

        self._build_sidebar(sidebar)
        self._build_workspace(workspace)

    def _build_sidebar(self, parent: ttk.Frame) -> None:
        parent.configure(width=330)
        parent.grid_propagate(False)

        notebook = ttk.Notebook(parent)
        notebook.pack(fill="both", expand=True)

        assets_tab = ttk.Frame(notebook, style="Dark.TFrame", padding=8)
        paint_tab = ttk.Frame(notebook, style="Dark.TFrame", padding=8)
        notebook.add(assets_tab, text="Assets")
        notebook.add(paint_tab, text="Paint")

        project_box = ttk.LabelFrame(assets_tab, text="Project", style="Dark.TLabelframe", padding=8)
        project_box.pack(fill="x", pady=(0, 8))

        project_grid = ttk.Frame(project_box, style="Dark.TFrame")
        project_grid.pack(fill="x")
        project_grid.columnconfigure(0, weight=1)
        project_grid.columnconfigure(1, weight=1)
        ttk.Button(project_grid, text="New", style="Dark.TButton", command=self.new_project).grid(row=0, column=0, sticky="ew", padx=(0, 4), pady=2)
        ttk.Button(project_grid, text="Open Project", style="Dark.TButton", command=self.open_project).grid(row=0, column=1, sticky="ew", padx=(4, 0), pady=2)
        ttk.Button(project_grid, text="Save Project", style="Dark.TButton", command=self.save_project).grid(row=1, column=0, sticky="ew", padx=(0, 4), pady=2)
        ttk.Button(project_grid, text="Save As", style="Dark.TButton", command=lambda: self.save_project(save_as=True)).grid(row=1, column=1, sticky="ew", padx=(4, 0), pady=2)
        ttk.Button(project_grid, text="Open Folder", style="Dark.TButton", command=self.open_sprite_folder_dialog).grid(row=2, column=0, sticky="ew", padx=(0, 4), pady=2)
        ttk.Button(project_grid, text="Save To Folder", style="Dark.TButton", command=self.save_to_loaded_sprite_folder).grid(row=2, column=1, sticky="ew", padx=(4, 0), pady=2)

        sprite_box = ttk.LabelFrame(assets_tab, text="Character Sprites", style="Dark.TLabelframe", padding=8)
        sprite_box.pack(fill="both", expand=True, pady=(0, 8))

        sprite_list_wrap = ttk.Frame(sprite_box, style="Dark.TFrame")
        sprite_list_wrap.pack(fill="both", expand=True)

        self.sprite_list = tk.Listbox(
            sprite_list_wrap,
            width=34,
            height=12,
            bg="#111117",
            fg="#f3f3f6",
            selectbackground="#355070",
            activestyle="none",
            highlightthickness=0,
            bd=0,
        )
        sprite_scroll = tk.Scrollbar(sprite_list_wrap, command=self.sprite_list.yview)
        self.sprite_list.configure(yscrollcommand=sprite_scroll.set)
        self.sprite_list.pack(side="left", fill="both", expand=True)
        sprite_scroll.pack(side="right", fill="y")
        self.sprite_list.bind("<Double-Button-1>", self.open_selected_sprite_folder)

        ttk.Button(sprite_box, text="Refresh List", style="Dark.TButton", command=self.refresh_sprite_sources).pack(fill="x", pady=(8, 2))
        ttk.Button(sprite_box, text="Load Selected", style="Dark.TButton", command=self.open_selected_sprite_folder).pack(fill="x", pady=2)

        canvas_box = ttk.LabelFrame(paint_tab, text="Canvas", style="Dark.TLabelframe", padding=8)
        canvas_box.pack(fill="x", pady=(0, 8))

        canvas_grid = ttk.Frame(canvas_box, style="Dark.TFrame")
        canvas_grid.pack(fill="x")
        canvas_grid.columnconfigure(0, weight=1)
        canvas_grid.columnconfigure(1, weight=1)
        ttk.Button(canvas_grid, text="16 x 16", style="Dark.TButton", command=lambda: self.set_grid_size(16)).grid(row=0, column=0, sticky="ew", padx=(0, 4), pady=2)
        ttk.Button(canvas_grid, text="32 x 32", style="Dark.TButton", command=lambda: self.set_grid_size(32)).grid(row=0, column=1, sticky="ew", padx=(4, 0), pady=2)
        ttk.Button(canvas_grid, text="Clear Frame", style="Dark.TButton", command=self.clear_current_frame).grid(row=1, column=0, sticky="ew", padx=(0, 4), pady=2)
        ttk.Button(canvas_grid, text="Flip Horizontal", style="Dark.TButton", command=self.flip_current_frame).grid(row=1, column=1, sticky="ew", padx=(4, 0), pady=2)
        ttk.Button(canvas_grid, text="Import To 32x32", style="Dark.TButton", command=self.import_image_to_32x32).grid(row=2, column=0, columnspan=2, sticky="ew", pady=(2, 0))
        ttk.Checkbutton(
            canvas_box,
            text="Onion Skin Previous Frame",
            variable=self.onion_skin_enabled,
            style="Dark.TCheckbutton",
            command=self.refresh_everything,
        ).pack(anchor="w", pady=(8, 2))

        ttk.Label(canvas_box, text="Zoom", style="Dark.TLabel").pack(anchor="w", pady=(10, 2))
        self.zoom_label = ttk.Label(canvas_box, text="", style="Dark.TLabel")
        self.zoom_label.pack(anchor="w")

        self.zoom_scale = tk.Scale(
            canvas_box,
            from_=4,
            to=36,
            orient="horizontal",
            bg="#1c1c24",
            fg="#f3f3f6",
            troughcolor="#343447",
            highlightthickness=0,
            command=self.on_zoom_change,
        )
        self.zoom_scale.set(self.pixel_size)
        self.zoom_scale.pack(fill="x")

        tools_box = ttk.LabelFrame(paint_tab, text="Tools", style="Dark.TLabelframe", padding=8)
        tools_box.pack(fill="x", pady=(0, 8))

        self.tool_bar = ttk.Frame(tools_box, style="Dark.TFrame")
        self.tool_bar.pack(fill="x")
        for column, tool_name in enumerate(("pencil", "eraser", "fill", "picker", "select")):
            button = tk.Button(
                self.tool_bar,
                bg="#2b2b39",
                activebackground="#46465f",
                relief="raised",
                bd=2,
                fg="#f3f3f6",
                font=("Segoe UI", 8, "bold"),
                compound="top",
                padx=4,
                pady=4,
                command=lambda value=tool_name: self.set_tool(value),
            )
            button.grid(row=0, column=column, padx=4, pady=4, sticky="ew")
            self.tool_buttons[tool_name] = button
        for column in range(5):
            self.tool_bar.columnconfigure(column, weight=1)
        ttk.Label(tools_box, text="B pencil, E eraser, G fill, I picker, M select", style="Dark.TLabel").pack(anchor="w", pady=(2, 0))

        palette_box = ttk.LabelFrame(paint_tab, text="Palette", style="Dark.TLabelframe", padding=8)
        palette_box.pack(fill="x", pady=(0, 8))

        swatch_header = ttk.Frame(palette_box, style="Dark.TFrame")
        swatch_header.pack(fill="x", pady=(0, 8))
        self.current_color_display = tk.Label(swatch_header, width=8, height=2, bg=self.selected_color, relief="ridge", bd=2)
        self.current_color_display.pack(side="left", padx=(0, 8))
        self.previous_color_display = tk.Label(swatch_header, width=4, height=2, bg=self.previous_color, relief="ridge", bd=2)
        self.previous_color_display.pack(side="left")

        ttk.Button(palette_box, text="Custom Color", style="Dark.TButton", command=self.pick_custom_color).pack(fill="x", pady=(0, 8))

        self.palette_grid = ttk.Frame(palette_box, style="Dark.TFrame")
        self.palette_grid.pack(fill="x")

        status_box = ttk.LabelFrame(paint_tab, text="Status", style="Dark.TLabelframe", padding=8)
        status_box.pack(fill="both", expand=True)
        self.status_label = ttk.Label(status_box, text="", style="Dark.TLabel", wraplength=260, justify="left")
        self.status_label.pack(anchor="w")

    def _build_workspace(self, parent: ttk.Frame) -> None:
        toolbar = ttk.Frame(parent, style="Dark.TFrame")
        toolbar.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        toolbar.columnconfigure(0, weight=1)

        self.project_title = ttk.Label(toolbar, text="Untitled Project", style="Dark.TLabel", font=("Segoe UI", 15, "bold"))
        self.project_title.grid(row=0, column=0, sticky="w")

        hint = ttk.Label(
            toolbar,
            text="Ctrl+Z undo, Ctrl+C copy, Ctrl+V paste, Ctrl+Shift+S save to sprite folder",
            style="Dark.TLabel",
        )
        hint.grid(row=1, column=0, sticky="w", pady=(4, 0))

        grid_box = ttk.LabelFrame(parent, text="Canvas", style="Dark.TLabelframe", padding=10)
        grid_box.grid(row=1, column=0, sticky="nsew", padx=(0, 12))
        grid_box.rowconfigure(0, weight=1)
        grid_box.columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(grid_box, bg="#111117", highlightthickness=0, cursor="tcross")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.bind("<Button-1>", self.on_canvas_press)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.canvas.bind("<Motion>", self.on_canvas_motion)

        right_panel = ttk.Frame(parent, style="Dark.TFrame", width=290)
        right_panel.grid(row=1, column=1, sticky="ns")
        right_panel.grid_propagate(False)

        preview_box = ttk.LabelFrame(right_panel, text="Preview", style="Dark.TLabelframe", padding=10)
        preview_box.pack(fill="x", pady=(0, 10))
        self.preview_canvas = tk.Canvas(preview_box, width=256, height=256, bg="#111117", highlightthickness=0)
        self.preview_canvas.pack()

        animation_box = ttk.LabelFrame(right_panel, text="Frames", style="Dark.TLabelframe", padding=10)
        animation_box.pack(fill="both", expand=True, pady=(0, 10))

        frame_actions = ttk.Frame(animation_box, style="Dark.TFrame")
        frame_actions.pack(fill="x", pady=(0, 8))
        ttk.Button(frame_actions, text="+ Frame", style="Dark.TButton", command=self.add_frame).pack(fill="x", pady=2)
        ttk.Button(frame_actions, text="Duplicate", style="Dark.TButton", command=self.duplicate_frame).pack(fill="x", pady=2)
        ttk.Button(frame_actions, text="Rename", style="Dark.TButton", command=self.rename_current_frame).pack(fill="x", pady=2)
        ttk.Button(frame_actions, text="Delete", style="Dark.TButton", command=self.delete_frame).pack(fill="x", pady=2)

        nav = ttk.Frame(animation_box, style="Dark.TFrame")
        nav.pack(fill="x", pady=(0, 8))
        ttk.Button(nav, text="Prev", style="Dark.TButton", command=lambda: self.select_frame(self.current_frame_index - 1)).pack(side="left", fill="x", expand=True, padx=(0, 4))
        ttk.Button(nav, text="Next", style="Dark.TButton", command=lambda: self.select_frame(self.current_frame_index + 1)).pack(side="left", fill="x", expand=True, padx=(4, 0))

        frame_list_wrap = ttk.Frame(animation_box, style="Dark.TFrame")
        frame_list_wrap.pack(fill="both", expand=True)
        self.frame_list = tk.Listbox(
            frame_list_wrap,
            height=14,
            bg="#111117",
            fg="#f3f3f6",
            selectbackground="#355070",
            activestyle="none",
            highlightthickness=0,
            bd=0,
        )
        frame_scroll = tk.Scrollbar(frame_list_wrap, command=self.frame_list.yview)
        self.frame_list.configure(yscrollcommand=frame_scroll.set)
        self.frame_list.pack(side="left", fill="both", expand=True)
        frame_scroll.pack(side="right", fill="y")
        self.frame_list.bind("<<ListboxSelect>>", self.on_frame_list_select)
        self.frame_list.bind("<Double-Button-1>", self.rename_current_frame)

        export_box = ttk.LabelFrame(right_panel, text="Export", style="Dark.TLabelframe", padding=10)
        export_box.pack(fill="x")
        ttk.Button(export_box, text="Export Current PNG", style="Dark.TButton", command=self.export_current_frame).pack(fill="x", pady=2)
        ttk.Button(export_box, text="Export Frames PNG", style="Dark.TButton", command=self.export_all_frames).pack(fill="x", pady=2)
        ttk.Button(export_box, text="Export Sprite Sheet", style="Dark.TButton", command=self.export_sprite_sheet).pack(fill="x", pady=2)

    def _bind_shortcuts(self) -> None:
        self.root.bind("<Control-s>", lambda event: self.save_project())
        self.root.bind("<Control-S>", lambda event: self.save_project())
        self.root.bind("<Control-e>", lambda event: self.export_sprite_sheet())
        self.root.bind("<Control-E>", lambda event: self.export_sprite_sheet())
        self.root.bind("<Control-z>", lambda event: self.undo())
        self.root.bind("<Control-Z>", lambda event: self.undo())
        self.root.bind("<Control-c>", lambda event: self.copy_selection())
        self.root.bind("<Control-C>", lambda event: self.copy_selection())
        self.root.bind("<Control-v>", lambda event: self.prepare_paste())
        self.root.bind("<Control-V>", lambda event: self.prepare_paste())
        self.root.bind("<Control-Shift-S>", lambda event: self.save_to_loaded_sprite_folder())
        self.root.bind("<Key-b>", lambda event: self.set_tool("pencil"))
        self.root.bind("<Key-e>", lambda event: self.set_tool("eraser"))
        self.root.bind("<Key-g>", lambda event: self.set_tool("fill"))
        self.root.bind("<Key-i>", lambda event: self.set_tool("picker"))
        self.root.bind("<Key-m>", lambda event: self.set_tool("select"))
        self.root.bind("<Key-n>", lambda event: self.add_frame())
        self.root.bind("<F2>", self.rename_current_frame)
        self.root.bind("<Delete>", lambda event: self.delete_frame())

    def recommended_pixel_size(self):
        if self.grid_size <= 16:
            return 24
        if self.grid_size <= 32:
            return 14
        if self.grid_size <= 64:
            return 8
        return 4

    def sync_view_scales(self):
        self.pixel_size = max(4, min(self.pixel_size, 36))
        self.preview_scale = max(2, min(8, 256 // max(1, self.grid_size)))
        self.zoom_scale.set(self.pixel_size)
        self.zoom_label.config(text=f"{self.pixel_size}px per cell")

    def refresh_everything(self) -> None:
        self.sync_view_scales()
        self.redraw_canvas()
        self.redraw_preview()
        self.refresh_frame_list()
        self.refresh_palette()
        self.refresh_tool_icons()
        self.update_title()
        self.update_status()

    def update_title(self) -> None:
        if self.loaded_sprite_dir:
            name = self.loaded_sprite_dir.relative_to(self.project_root).as_posix()
        elif self.project_path:
            name = Path(self.project_path).name
        else:
            name = "Untitled Project"
        self.project_title.config(text=f"{name}  |  {self.grid_size}x{self.grid_size}  |  {len(self.frames)} frame(s)")
        self.root.title(f"Magiko Pixel Editor - {name}")

    def update_status(self, extra_message: str | None = None) -> None:
        location = self.loaded_sprite_dir or self.project_dir
        details = [
            f"Tool: {TOOL_LABELS[self.current_tool]}",
            f"Color: {self.selected_color}",
            f"Frame: {self.current_frame_index + 1}/{len(self.frames)}",
            f"Target: {location}",
            f"Undo states: {len(self.undo_stack)}",
        ]
        if self.selection_bounds:
            left, top, right, bottom = self.selection_bounds
            details.append(f"Selection: {right - left + 1}x{bottom - top + 1}")
        if self.clipboard_cells:
            details.append(f"Clipboard: {len(self.clipboard_cells[0])}x{len(self.clipboard_cells)}")
        if extra_message:
            details.append(extra_message)
        self.status_label.config(text="\n".join(str(detail) for detail in details))

    def refresh_sprite_sources(self):
        self.sprite_list.delete(0, tk.END)
        self.character_sprite_dirs = []
        for directory in sorted(self.characters_dir.rglob("*")):
            if directory.is_dir() and any(directory.glob("*.png")):
                self.character_sprite_dirs.append(directory)
                self.sprite_list.insert(tk.END, directory.relative_to(self.project_root).as_posix())

    def open_selected_sprite_folder(self, _event=None):
        selection = self.sprite_list.curselection()
        if selection:
            self.load_sprite_folder(self.character_sprite_dirs[selection[0]])

    def open_sprite_folder_dialog(self):
        selected = filedialog.askdirectory(title="Open sprite folder", initialdir=self.characters_dir, mustexist=True)
        if selected:
            self.load_sprite_folder(Path(selected))

    def infer_grid_size_from_images(self, images):
        for image in images:
            if image.width == image.height and image.width <= 128:
                return image.width
        return 16

    def image_to_frame(self, image: Image.Image):
        rgba = image.convert("RGBA")
        frame = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for y in range(min(self.grid_size, rgba.height)):
            for x in range(min(self.grid_size, rgba.width)):
                red, green, blue, alpha = rgba.getpixel((x, y))
                if alpha:
                    frame[y][x] = f"#{red:02x}{green:02x}{blue:02x}"
        return frame

    def normalize_image_to_square(self, image: Image.Image, target_size: int):
        rgba = image.convert("RGBA")
        bbox = rgba.getbbox()
        if bbox:
            rgba = rgba.crop(bbox)

        if rgba.width == 0 or rgba.height == 0:
            return Image.new("RGBA", (target_size, target_size), (0, 0, 0, 0))

        scale = min(target_size / rgba.width, target_size / rgba.height)
        resized_width = max(1, int(round(rgba.width * scale)))
        resized_height = max(1, int(round(rgba.height * scale)))
        resized = rgba.resize((resized_width, resized_height), Image.Resampling.NEAREST)

        canvas = Image.new("RGBA", (target_size, target_size), (0, 0, 0, 0))
        offset_x = (target_size - resized_width) // 2
        offset_y = (target_size - resized_height) // 2
        canvas.paste(resized, (offset_x, offset_y), resized)
        return canvas

    def import_image_to_32x32(self):
        selected = filedialog.askopenfilename(
            title="Import image and fit to 32x32",
            initialdir=self.img_dir,
            filetypes=[
                ("Image files", "*.png *.bmp *.gif *.jpg *.jpeg *.webp"),
                ("All files", "*.*"),
            ],
        )
        if not selected:
            return

        try:
            with Image.open(selected) as source:
                normalized = self.normalize_image_to_square(source, 32)
            self.push_undo_snapshot()
            self.grid_size = 32
            self.pixel_size = self.recommended_pixel_size()
            self.frames[self.current_frame_index] = self.image_to_frame(normalized)
            self.frame_names[self.current_frame_index] = Path(selected).with_suffix(".png").name
            self.canvas_signature = None
            self.preview_signature = None
            self.selection_bounds = None
            self.pending_paste = False
            palette = self.collect_palette_from_frames()
            self.selected_color = palette[0]
            self.previous_color = palette[1] if len(palette) > 1 else palette[0]
            self.refresh_everything()
            self.update_status(extra_message=f"Imported {Path(selected).name} as centered 32x32 pixel art")
        except Exception as exc:
            messagebox.showerror("Import failed", f"Could not convert image to 32x32:\n{exc}")

    def collect_palette_from_frames(self):
        palette = []
        for frame in self.frames:
            for row in frame:
                for color in row:
                    if color and color not in palette:
                        palette.append(color)
        for color in DEFAULT_PALETTE:
            if color not in palette:
                palette.append(color)
        return palette[:20]

    def load_sprite_folder(self, folder: Path):
        png_files = sorted(folder.glob("*.png"))
        if not png_files:
            messagebox.showerror("Open failed", "The selected folder contains no PNG files.")
            return

        images = [Image.open(path) for path in png_files]
        self.push_undo_snapshot()
        self.grid_size = self.infer_grid_size_from_images(images)
        self.pixel_size = self.recommended_pixel_size()
        self.frames = [self.image_to_frame(image) for image in images]
        self.frame_names = [path.name for path in png_files]
        self.current_frame_index = 0
        self.loaded_sprite_dir = folder
        self.project_path = None
        self.selection_bounds = None
        self.pending_paste = False
        palette = self.collect_palette_from_frames()
        self.selected_color = palette[0]
        self.previous_color = palette[1] if len(palette) > 1 else palette[0]
        self.refresh_everything()
        self.update_status(extra_message=f"Loaded {folder.relative_to(self.project_root).as_posix()}")

    def create_tool_icon(self, tool_name: str):
        icon = Image.new("RGBA", (36, 36), (0, 0, 0, 0))
        draw = ImageDraw.Draw(icon)
        if tool_name == "pencil":
            draw.line((10, 27, 26, 11), fill="#f6bd60", width=6)
            draw.line((12, 29, 28, 13), fill="#7f5539", width=2)
            draw.polygon([(24, 9), (29, 4), (32, 7), (27, 12)], fill="#f3f3f6", outline="#141414")
            draw.polygon([(9, 28), (13, 32), (7, 33)], fill="#f28482", outline="#141414")
        elif tool_name == "eraser":
            draw.polygon([(8, 23), (18, 11), (29, 21), (19, 32)], fill="#f46036", outline="#f3f3f6")
            draw.polygon([(18, 11), (22, 7), (33, 17), (29, 21)], fill="#ffcab1", outline="#f3f3f6")
            draw.rectangle((17, 23, 29, 27), fill="#fff1e6", outline="#f3f3f6")
        elif tool_name == "fill":
            draw.polygon([(10, 13), (18, 7), (28, 17), (20, 23)], fill="#577590", outline="#f3f3f6")
            draw.rectangle((9, 22, 23, 26), fill="#1b998b", outline="#f3f3f6")
            draw.ellipse((22, 21, 31, 31), fill="#43aa8b", outline="#d8f3dc")
            draw.line((15, 10, 25, 20), fill="#dce6f2", width=2)
        elif tool_name == "picker":
            draw.line((11, 24, 25, 10), fill="#f3f3f6", width=5)
            draw.ellipse((22, 7, 32, 17), outline="#f3f3f6", width=3)
            draw.ellipse((6, 20, 13, 27), fill="#355070", outline="#dce6f2")
            draw.line((8, 26, 4, 32), fill="#7bdff2", width=3)
        elif tool_name == "select":
            draw.rectangle((7, 7, 28, 28), outline="#f3f3f6", width=2)
            draw.line((7, 13, 7, 7), fill="#f3f3f6", width=3)
            draw.line((13, 7, 7, 7), fill="#f3f3f6", width=3)
            draw.line((22, 28, 28, 28), fill="#f3f3f6", width=3)
            draw.line((28, 22, 28, 28), fill="#f3f3f6", width=3)
        return ImageTk.PhotoImage(icon)

    def refresh_tool_icons(self):
        for tool_name, button in self.tool_buttons.items():
            if tool_name not in self.icon_images:
                self.icon_images[tool_name] = self.create_tool_icon(tool_name)
            button.configure(
                image=self.icon_images[tool_name],
                text=TOOL_LABELS[tool_name],
                compound="top",
                relief="sunken" if tool_name == self.current_tool else "raised",
                bg="#3f526f" if tool_name == self.current_tool else "#2b2b39",
                activeforeground="#f3f3f6",
                width=58,
                height=52,
            )

    def refresh_palette(self):
        palette = self.collect_palette_from_frames()
        for child in self.palette_grid.winfo_children():
            child.destroy()
        for index, color in enumerate(palette):
            button = tk.Button(
                self.palette_grid,
                bg=color,
                activebackground=color,
                width=4,
                height=2,
                relief="sunken" if color == self.selected_color else "raised",
                bd=2,
                highlightbackground="#53536b",
                highlightthickness=1,
                command=lambda hex_color=color: self.set_color(hex_color),
            )
            row = index // 4
            column = index % 4
            button.grid(row=row, column=column, padx=3, pady=3, sticky="nsew")
        for column in range(4):
            self.palette_grid.columnconfigure(column, weight=1)
        self.current_color_display.config(bg=self.selected_color)
        self.previous_color_display.config(bg=self.previous_color)

    def refresh_frame_list(self):
        self.frame_list.delete(0, tk.END)
        for index, name in enumerate(self.frame_names):
            marker = " <" if index == self.current_frame_index else ""
            self.frame_list.insert(tk.END, f"{index + 1:02d} {name}{marker}")
        self.frame_list.selection_clear(0, tk.END)
        self.frame_list.selection_set(self.current_frame_index)
        self.frame_list.activate(self.current_frame_index)

    def onion_skin_frame(self):
        if not self.onion_skin_enabled.get() or self.current_frame_index == 0:
            return None
        return self.frames[self.current_frame_index - 1]

    def ensure_canvas_grid(self):
        signature = (self.grid_size, self.pixel_size)
        if self.canvas_signature == signature:
            return
        self.canvas_signature = signature
        canvas_size = self.grid_size * self.pixel_size
        self.canvas.config(width=canvas_size, height=canvas_size)
        self.canvas.delete("all")
        self.canvas_cells = []
        for y in range(self.grid_size):
            row = []
            for x in range(self.grid_size):
                x1 = x * self.pixel_size
                y1 = y * self.pixel_size
                x2 = x1 + self.pixel_size
                y2 = y1 + self.pixel_size
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill="#0e0e13", outline="#2d2d39")
                cross_a = self.canvas.create_line(x1, y1, x2, y2, fill="#1d1d28")
                cross_b = self.canvas.create_line(x1, y2, x2, y1, fill="#1d1d28")
                row.append((rect, cross_a, cross_b))
            self.canvas_cells.append(row)
        self.selection_rect = self.canvas.create_rectangle(0, 0, 0, 0, outline="#f6bd60", width=2, dash=(6, 3), state="hidden")

    def ensure_preview_grid(self):
        signature = (self.grid_size, self.preview_scale)
        if self.preview_signature == signature:
            return
        self.preview_signature = signature
        self.preview_canvas.delete("all")
        self.preview_cells = []
        preview_size = self.grid_size * self.preview_scale
        offset_x = max(0, (256 - preview_size) // 2)
        offset_y = max(0, (256 - preview_size) // 2)
        for y in range(self.grid_size):
            row = []
            for x in range(self.grid_size):
                x1 = offset_x + x * self.preview_scale
                y1 = offset_y + y * self.preview_scale
                x2 = x1 + self.preview_scale
                y2 = y1 + self.preview_scale
                rect = self.preview_canvas.create_rectangle(x1, y1, x2, y2, fill="#111117", outline="#111117")
                row.append(rect)
            self.preview_cells.append(row)
        self.preview_border = self.preview_canvas.create_rectangle(
            offset_x - 1,
            offset_y - 1,
            offset_x + preview_size + 1,
            offset_y + preview_size + 1,
            outline="#4a4a61",
        )

    def get_canvas_cell_display(self, x: int, y: int):
        frame = self.frames[self.current_frame_index]
        shadow_frame = self.onion_skin_frame()
        shadow_color = shadow_frame[y][x] if shadow_frame else None
        color = frame[y][x]
        if color:
            return color, "#2d2d39", False
        if shadow_color:
            return self.mix_hex(shadow_color, "#111117", 0.25), "#353549", False
        return "#0e0e13", "#2d2d39", True

    def refresh_canvas_cell(self, x: int, y: int):
        rect, cross_a, cross_b = self.canvas_cells[y][x]
        fill, outline, show_cross = self.get_canvas_cell_display(x, y)
        self.canvas.itemconfig(rect, fill=fill, outline=outline)
        state = "normal" if show_cross else "hidden"
        self.canvas.itemconfig(cross_a, state=state)
        self.canvas.itemconfig(cross_b, state=state)

    def update_selection_overlay(self):
        if not self.selection_bounds:
            self.canvas.itemconfig(self.selection_rect, state="hidden")
            return
        left, top, right, bottom = self.selection_bounds
        self.canvas.coords(
            self.selection_rect,
            left * self.pixel_size,
            top * self.pixel_size,
            (right + 1) * self.pixel_size,
            (bottom + 1) * self.pixel_size,
        )
        self.canvas.itemconfig(self.selection_rect, state="normal")

    def redraw_canvas(self):
        self.ensure_canvas_grid()
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                self.refresh_canvas_cell(x, y)
        self.update_selection_overlay()

    def get_preview_cell_display(self, x: int, y: int):
        frame = self.frames[self.current_frame_index]
        shadow_frame = self.onion_skin_frame()
        color = frame[y][x]
        if color:
            return color
        if shadow_frame and shadow_frame[y][x]:
            return self.mix_hex(shadow_frame[y][x], "#111117", 0.18)
        return "#111117"

    def refresh_preview_cell(self, x: int, y: int):
        rect = self.preview_cells[y][x]
        color = self.get_preview_cell_display(x, y)
        self.preview_canvas.itemconfig(rect, fill=color, outline=color)

    def redraw_preview(self):
        self.ensure_preview_grid()
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                self.refresh_preview_cell(x, y)

    def mix_hex(self, source: str, target: str, ratio: float):
        source_rgb = tuple(int(source[i:i + 2], 16) for i in (1, 3, 5))
        target_rgb = tuple(int(target[i:i + 2], 16) for i in (1, 3, 5))
        mixed = tuple(int(source_rgb[i] * ratio + target_rgb[i] * (1 - ratio)) for i in range(3))
        return f"#{mixed[0]:02x}{mixed[1]:02x}{mixed[2]:02x}"

    def on_zoom_change(self, value: str):
        self.pixel_size = int(float(value))
        self.canvas_signature = None
        self.redraw_canvas()

    def set_tool(self, tool_name: str):
        self.current_tool = tool_name
        self.refresh_tool_icons()
        self.update_status()

    def set_color(self, color: str):
        if color != self.selected_color:
            self.previous_color = self.selected_color
        self.selected_color = color
        self.refresh_palette()
        self.update_status()

    def pick_custom_color(self):
        result = colorchooser.askcolor(color=self.selected_color, title="Choose pixel color")
        if result[1]:
            self.set_color(result[1])

    def get_cell_from_event(self, event):
        x = math.floor(event.x / self.pixel_size)
        y = math.floor(event.y / self.pixel_size)
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            return x, y
        return None

    def on_canvas_press(self, event):
        cell = self.get_cell_from_event(event)
        if cell is None:
            return
        if self.pending_paste and self.clipboard_cells:
            self.paste_at(*cell)
            return
        if self.current_tool == "select":
            if self.selection_bounds and self.is_cell_in_selection(*cell):
                self.selection_drag_snapshot = self.current_state_snapshot()
                self.selection_drag_origin = cell
                self.selection_drag_base = self.selection_bounds
                self.selection_dragging = True
                self.drawing = True
                self.last_cell = cell
                self.update_status(extra_message="Dragging selection")
                return
            self.selection_start = cell
            self.selection_bounds = (cell[0], cell[1], cell[0], cell[1])
            self.selection_dragging = False
            self.drawing = True
            self.update_selection_overlay()
            self.update_status()
            return
        if self.current_tool in {"pencil", "eraser", "fill"}:
            self.stroke_snapshot = self.current_state_snapshot()
        self.drawing = True
        self.last_cell = cell
        self.apply_tool(*cell)

    def on_canvas_drag(self, event):
        if not self.drawing:
            return
        cell = self.get_cell_from_event(event)
        if cell is None or cell == self.last_cell:
            return
        self.last_cell = cell
        if self.current_tool == "select":
            if self.selection_dragging and self.selection_drag_origin and self.selection_drag_base:
                dx = cell[0] - self.selection_drag_origin[0]
                dy = cell[1] - self.selection_drag_origin[1]
                self.move_selection_preview(dx, dy)
            elif self.selection_start:
                self.selection_bounds = self.normalize_selection(self.selection_start, cell)
                self.update_selection_overlay()
                self.update_status()
        elif self.current_tool in {"pencil", "eraser"}:
            self.apply_tool(*cell)

    def on_canvas_release(self, _event):
        self.drawing = False
        self.last_cell = None
        self.selection_start = None
        if self.selection_drag_snapshot:
            self.push_undo_snapshot(self.selection_drag_snapshot)
            self.refresh_palette()
        self.selection_drag_origin = None
        self.selection_drag_base = None
        self.selection_drag_snapshot = None
        self.selection_dragging = False
        if self.stroke_snapshot:
            self.push_undo_snapshot(self.stroke_snapshot)
            self.stroke_snapshot = None
            self.refresh_palette()

    def on_canvas_motion(self, event):
        cell = self.get_cell_from_event(event)
        if cell == self.last_hover_cell:
            return
        self.last_hover_cell = cell
        if cell is None:
            self.update_status()
        else:
            self.update_status(extra_message=f"Cursor: {cell[0]}, {cell[1]}")

    def apply_tool(self, x: int, y: int):
        frame = self.frames[self.current_frame_index]
        changed = False
        full_redraw = False
        if self.current_tool == "pencil":
            if frame[y][x] != self.selected_color:
                frame[y][x] = self.selected_color
                changed = True
        elif self.current_tool == "eraser":
            if frame[y][x] is not None:
                frame[y][x] = None
                changed = True
        elif self.current_tool == "picker":
            picked = frame[y][x]
            if picked:
                self.set_color(picked)
            return
        elif self.current_tool == "select":
            return
        elif self.current_tool == "fill":
            target = frame[y][x]
            replacement = self.selected_color
            if target == replacement:
                return
            changed = self.flood_fill(frame, x, y, target, replacement)
            full_redraw = True

        if not changed:
            return
        if full_redraw:
            self.redraw_canvas()
            self.redraw_preview()
            self.refresh_palette()
        else:
            self.refresh_canvas_cell(x, y)
            self.refresh_preview_cell(x, y)

    def flood_fill(self, frame, start_x: int, start_y: int, target, replacement):
        changed = False
        stack = [(start_x, start_y)]
        while stack:
            x, y = stack.pop()
            if x < 0 or y < 0 or x >= self.grid_size or y >= self.grid_size:
                continue
            if frame[y][x] != target:
                continue
            frame[y][x] = replacement
            changed = True
            stack.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])
        return changed

    def normalize_selection(self, start, end):
        return min(start[0], end[0]), min(start[1], end[1]), max(start[0], end[0]), max(start[1], end[1])

    def is_cell_in_selection(self, x: int, y: int):
        if not self.selection_bounds:
            return False
        left, top, right, bottom = self.selection_bounds
        return left <= x <= right and top <= y <= bottom

    def clear_area(self, frame, bounds):
        left, top, right, bottom = bounds
        for y in range(top, bottom + 1):
            for x in range(left, right + 1):
                frame[y][x] = None

    def copy_cells_from_bounds(self, frame, bounds):
        left, top, right, bottom = bounds
        return [[frame[y][x] for x in range(left, right + 1)] for y in range(top, bottom + 1)]

    def paste_cells(self, frame, cells, start_x: int, start_y: int):
        for row_index, row in enumerate(cells):
            y = start_y + row_index
            if y >= self.grid_size:
                break
            for col_index, color in enumerate(row):
                x = start_x + col_index
                if x >= self.grid_size:
                    break
                frame[y][x] = color

    def move_selection_preview(self, dx: int, dy: int):
        if not self.selection_drag_snapshot or not self.selection_drag_base:
            return
        base_frame = deepcopy(self.selection_drag_snapshot["frames"][self.current_frame_index])
        cells = self.copy_cells_from_bounds(base_frame, self.selection_drag_base)
        left, top, right, bottom = self.selection_drag_base
        width = right - left + 1
        height = bottom - top + 1
        target_left = min(max(0, left + dx), self.grid_size - width)
        target_top = min(max(0, top + dy), self.grid_size - height)
        self.clear_area(base_frame, self.selection_drag_base)
        self.paste_cells(base_frame, cells, target_left, target_top)
        self.frames[self.current_frame_index] = base_frame
        self.selection_bounds = (
            target_left,
            target_top,
            target_left + width - 1,
            target_top + height - 1,
        )
        self.redraw_canvas()
        self.redraw_preview()
        self.update_status(extra_message="Dragging selection")

    def copy_selection(self):
        if not self.selection_bounds:
            self.update_status(extra_message="No selection to copy")
            return
        left, top, right, bottom = self.selection_bounds
        frame = self.frames[self.current_frame_index]
        self.clipboard_cells = self.copy_cells_from_bounds(frame, self.selection_bounds)
        self.pending_paste = False
        self.update_status(extra_message="Selection copied")

    def prepare_paste(self):
        if not self.clipboard_cells:
            self.update_status(extra_message="Clipboard is empty")
            return
        self.pending_paste = True
        self.set_tool("select")
        self.update_status(extra_message="Click a cell to paste")

    def paste_at(self, start_x: int, start_y: int):
        if not self.clipboard_cells:
            return
        self.push_undo_snapshot()
        frame = self.frames[self.current_frame_index]
        self.paste_cells(frame, self.clipboard_cells, start_x, start_y)
        height = len(self.clipboard_cells)
        width = len(self.clipboard_cells[0]) if height else 0
        self.selection_bounds = (
            start_x,
            start_y,
            min(self.grid_size - 1, start_x + width - 1),
            min(self.grid_size - 1, start_y + height - 1),
        )
        self.pending_paste = False
        self.redraw_canvas()
        self.redraw_preview()
        self.refresh_palette()
        self.update_status(extra_message="Selection pasted")

    def set_grid_size(self, new_size: int):
        if new_size == self.grid_size:
            return
        if not messagebox.askyesno("Resize canvas", f"Switch all frames to {new_size}x{new_size}? Existing pixels outside the new size will be cropped."):
            return
        self.push_undo_snapshot()
        self.grid_size = new_size
        self.pixel_size = self.recommended_pixel_size()
        self.frames = [self.resized_blank_frame(frame) for frame in self.frames]
        self.canvas_signature = None
        self.preview_signature = None
        self.selection_bounds = None
        self.refresh_everything()

    def split_frame_name(self, name: str):
        path = Path(name)
        stem = path.stem
        suffix = path.suffix or ".png"
        digits = []
        index = len(stem) - 1
        while index >= 0 and stem[index].isdigit():
            digits.append(stem[index])
            index -= 1
        if not digits:
            return stem, None, 2, suffix
        digits.reverse()
        number_text = "".join(digits)
        prefix = stem[: index + 1]
        return prefix, int(number_text), len(number_text), suffix

    def format_frame_name(self, prefix: str, number: int, width: int, suffix: str):
        return f"{prefix}{number:0{width}d}{suffix}"

    def increment_name(self, name: str):
        prefix, number, width, suffix = self.split_frame_name(name)
        if number is None:
            return f"{prefix}_copy{suffix}"
        return self.format_frame_name(prefix, number + 1, width, suffix)

    def shift_names_forward_from(self, start_index: int):
        for index in range(len(self.frame_names) - 1, start_index - 1, -1):
            self.frame_names[index] = self.increment_name(self.frame_names[index])

    def default_new_frame_name(self):
        if self.frame_names:
            return self.increment_name(self.frame_names[-1])
        return "frame_01.png"

    def add_frame(self):
        self.push_undo_snapshot()
        self.frames.append(deepcopy(self.frames[self.current_frame_index]))
        self.frame_names.append(self.default_new_frame_name())
        self.select_frame(len(self.frames) - 1)

    def duplicate_frame(self):
        self.push_undo_snapshot()
        self.frames.insert(self.current_frame_index + 1, deepcopy(self.frames[self.current_frame_index]))
        self.frame_names.insert(self.current_frame_index + 1, self.frame_names[self.current_frame_index])
        self.shift_names_forward_from(self.current_frame_index + 1)
        self.select_frame(self.current_frame_index + 1)

    def sanitize_frame_name(self, name: str):
        safe = name.strip().replace("\\", "_").replace("/", "_")
        if not safe:
            return None
        if "." not in Path(safe).name:
            safe += ".png"
        return safe

    def rename_current_frame(self, _event=None):
        current_name = self.frame_names[self.current_frame_index]
        new_name = simpledialog.askstring(
            "Rename frame",
            "Frame filename",
            initialvalue=current_name,
            parent=self.root,
        )
        if new_name is None:
            return
        safe_name = self.sanitize_frame_name(new_name)
        if not safe_name:
            self.update_status(extra_message="Invalid frame name")
            return
        if safe_name != current_name and safe_name in self.frame_names:
            messagebox.showerror("Rename failed", "Another frame already uses that filename.")
            return
        self.push_undo_snapshot()
        self.frame_names[self.current_frame_index] = safe_name
        self.refresh_frame_list()
        self.update_status(extra_message=f"Renamed to {safe_name}")

    def delete_frame(self):
        self.push_undo_snapshot()
        if len(self.frames) == 1:
            self.frames[0] = self.new_blank_frame()
            self.frame_names[0] = "frame_01.png"
            self.current_frame_index = 0
        else:
            del self.frames[self.current_frame_index]
            del self.frame_names[self.current_frame_index]
            self.current_frame_index = max(0, self.current_frame_index - 1)
        self.refresh_everything()

    def select_frame(self, index: int):
        if 0 <= index < len(self.frames):
            self.current_frame_index = index
            self.refresh_everything()

    def on_frame_list_select(self, _event):
        selection = self.frame_list.curselection()
        if selection:
            self.select_frame(selection[0])

    def clear_current_frame(self):
        self.push_undo_snapshot()
        self.frames[self.current_frame_index] = self.new_blank_frame()
        self.refresh_everything()

    def flip_current_frame(self):
        self.push_undo_snapshot()
        self.frames[self.current_frame_index] = [list(reversed(row)) for row in self.frames[self.current_frame_index]]
        self.refresh_everything()

    def new_project(self):
        size = simpledialog.askinteger("New project", "Canvas size: 16 or 32", initialvalue=self.grid_size, minvalue=16, maxvalue=32, parent=self.root)
        if size not in {16, 32}:
            return
        self.push_undo_snapshot()
        self.grid_size = size
        self.pixel_size = self.recommended_pixel_size()
        self.frames = [self.new_blank_frame()]
        self.frame_names = ["frame_01.png"]
        self.current_frame_index = 0
        self.project_path = None
        self.loaded_sprite_dir = None
        self.canvas_signature = None
        self.preview_signature = None
        self.selection_bounds = None
        self.pending_paste = False
        self.refresh_everything()

    def save_project(self, save_as: bool = False):
        if save_as or not self.project_path:
            target = filedialog.asksaveasfilename(
                title="Save pixel project",
                defaultextension=".magiko-pixel.json",
                initialdir=self.project_dir,
                filetypes=[("Magiko Pixel Project", "*.magiko-pixel.json"), ("JSON", "*.json")],
            )
            if not target:
                return
            self.project_path = target

        data = {
            "grid_size": self.grid_size,
            "frames": self.frames,
            "frame_names": self.frame_names,
            "selected_color": self.selected_color,
            "loaded_sprite_dir": str(self.loaded_sprite_dir) if self.loaded_sprite_dir else None,
        }
        Path(self.project_path).write_text(json.dumps(data, indent=2), encoding="utf-8")
        self.update_title()
        self.update_status(extra_message=f"Saved project to {self.project_path}")

    def open_project(self):
        target = filedialog.askopenfilename(
            title="Open pixel project",
            initialdir=self.project_dir,
            filetypes=[("Magiko Pixel Project", "*.magiko-pixel.json"), ("JSON", "*.json")],
        )
        if not target:
            return
        try:
            data = json.loads(Path(target).read_text(encoding="utf-8"))
            grid_size = int(data["grid_size"])
            if grid_size < 1 or grid_size > 128:
                raise ValueError("Unsupported grid size")
            frames = data["frames"]
            if not frames:
                raise ValueError("Project contains no frames")
            self.push_undo_snapshot()
            self.grid_size = grid_size
            self.pixel_size = self.recommended_pixel_size()
            self.frames = []
            for frame in frames:
                normalized = self.new_blank_frame()
                for y in range(min(grid_size, len(frame))):
                    for x in range(min(grid_size, len(frame[y]))):
                        normalized[y][x] = frame[y][x]
                self.frames.append(normalized)
            self.frame_names = data.get("frame_names", [f"frame_{index + 1:02d}.png" for index in range(len(self.frames))])
            self.current_frame_index = 0
            self.project_path = target
            sprite_dir = data.get("loaded_sprite_dir")
            self.loaded_sprite_dir = Path(sprite_dir) if sprite_dir else None
            self.selected_color = data.get("selected_color", DEFAULT_PALETTE[0])
            self.canvas_signature = None
            self.preview_signature = None
            self.selection_bounds = None
            self.pending_paste = False
            self.refresh_everything()
            self.update_status(extra_message=f"Opened {target}")
        except Exception as exc:
            messagebox.showerror("Open failed", f"Could not open project:\n{exc}")

    def frame_to_image(self, frame):
        image = Image.new("RGBA", (self.grid_size, self.grid_size), (0, 0, 0, 0))
        pixels = image.load()
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                color = frame[y][x]
                if color:
                    color = color.lstrip("#")
                    pixels[x, y] = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4)) + (255,)
        return image

    def ask_export_basename(self, prompt: str):
        default_name = self.loaded_sprite_dir.name if self.loaded_sprite_dir else "magiko_sprite"
        base = simpledialog.askstring("Export name", prompt, initialvalue=default_name, parent=self.root)
        if not base:
            return None
        safe = "".join(char if char.isalnum() or char in {"_", "-"} else "_" for char in base.strip())
        return safe or None

    def export_current_frame(self):
        name = self.ask_export_basename("Base name for the current frame PNG")
        if not name:
            return
        path = self.project_dir / f"{name}.png"
        self.frame_to_image(self.frames[self.current_frame_index]).save(path)
        self.update_status(extra_message=f"Exported {path.name}")
        messagebox.showinfo("Export complete", f"Saved {path}")

    def export_all_frames(self):
        name = self.ask_export_basename("Base name for all frame PNGs")
        if not name:
            return
        for index, frame in enumerate(self.frames, start=1):
            self.frame_to_image(frame).save(self.project_dir / f"{name}_{index:02d}.png")
        self.update_status(extra_message=f"Exported {len(self.frames)} PNG frames")
        messagebox.showinfo("Export complete", f"Saved {len(self.frames)} PNG files in\n{self.project_dir}")

    def export_sprite_sheet(self):
        name = self.ask_export_basename("Base name for the sprite sheet")
        if not name:
            return
        sheet = Image.new("RGBA", (self.grid_size * len(self.frames), self.grid_size), (0, 0, 0, 0))
        for index, frame in enumerate(self.frames):
            sheet.paste(self.frame_to_image(frame), (index * self.grid_size, 0))
        path = self.project_dir / f"{name}_sheet.png"
        sheet.save(path)
        self.update_status(extra_message=f"Exported sprite sheet {path.name}")
        messagebox.showinfo("Export complete", f"Saved sprite sheet to\n{path}")

    def save_to_loaded_sprite_folder(self):
        target_dir = self.loaded_sprite_dir
        if not target_dir:
            selected = filedialog.askdirectory(title="Save frames to sprite folder", initialdir=self.characters_dir, mustexist=True)
            if not selected:
                return
            target_dir = Path(selected)
            self.loaded_sprite_dir = target_dir

        for index, frame in enumerate(self.frames):
            filename = self.frame_names[index] if index < len(self.frame_names) else f"frame_{index + 1:02d}.png"
            self.frame_to_image(frame).save(target_dir / filename)
        self.refresh_sprite_sources()
        self.update_title()
        self.update_status(extra_message=f"Saved {len(self.frames)} frame(s) to {target_dir.relative_to(self.project_root).as_posix()}")
        messagebox.showinfo("Save complete", f"Saved {len(self.frames)} frame(s) to\n{target_dir}")


def main():
    root = tk.Tk()
    PixelEditor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
