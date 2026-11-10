import customtkinter as ctk
import threading
from pathlib import Path
from services.system_monitor import SystemMonitor
import os
import subprocess
import platform

class StorageFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=("#ffffff", "#0f0f0f"))
        self.app = app
        self.monitor = SystemMonitor()
        self.current_path = Path.home()
        self.selected_file = None

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.create_header()
        self.create_content()

    def create_header(self):
        header = ctk.CTkFrame(self, fg_color=("#f0f0f0", "#1a1a1a"), height=80)
        header.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header.grid_propagate(False)

        title = ctk.CTkLabel(
            header,
            text="💾 Gestionnaire de Fichiers",
            font=("Arial", 24, "bold"),
            text_color="#00d9ff"
        )
        title.pack(side="left", padx=30, pady=20)

    def create_content(self):
        container = ctk.CTkFrame(self, fg_color=("#ffffff", "#0f0f0f"))
        container.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        container.grid_rowconfigure(0, weight=0)
        container.grid_rowconfigure(1, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=0)

        nav_frame = ctk.CTkFrame(container, fg_color=("#f0f0f0", "#1a1a1a"), corner_radius=10, height=60)
        nav_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        nav_frame.grid_propagate(False)

        self.path_label = ctk.CTkLabel(
            nav_frame,
            text=str(self.current_path),
            font=("Arial", 12),
            text_color="#00d9ff"
        )
        self.path_label.pack(side="left", padx=15, pady=15)

        back_btn = ctk.CTkButton(
            nav_frame,
            text="← Retour",
            font=("Arial", 11, "bold"),
            width=80,
            command=self.go_back
        )
        back_btn.pack(side="right", padx=15, pady=15)

        home_btn = ctk.CTkButton(
            nav_frame,
            text="🏠 Accueil",
            font=("Arial", 11, "bold"),
            width=80,
            command=self.go_home
        )
        home_btn.pack(side="right", padx=5, pady=15)

        main_content = ctk.CTkFrame(container, fg_color="transparent")
        main_content.grid(row=1, column=0, columnspan=2, sticky="nsew")
        main_content.grid_rowconfigure(0, weight=1)
        main_content.grid_columnconfigure(0, weight=1)
        main_content.grid_columnconfigure(1, weight=0)

        file_list_frame = ctk.CTkFrame(main_content, fg_color="transparent")
        file_list_frame.grid(row=0, column=0, sticky="nsew")
        file_list_frame.grid_rowconfigure(0, weight=1)
        file_list_frame.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            file_list_frame,
            text="Fichiers et Dossiers",
            font=("Arial", 13, "bold"),
            text_color=("black", "white")
        )
        title.grid(row=0, column=0, sticky="w", pady=(0, 10))

        self.file_list = ctk.CTkScrollableFrame(file_list_frame, fg_color=("#f0f0f0", "#1a1a1a"), corner_radius=10)
        self.file_list.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        file_list_frame.grid_rowconfigure(1, weight=1)

        preview_frame = ctk.CTkFrame(main_content, fg_color=("#f0f0f0", "#1a1a1a"), corner_radius=10, width=300)
        preview_frame.grid(row=0, column=1, sticky="nsew", padx=(20, 0))
        preview_frame.grid_propagate(False)

        preview_title = ctk.CTkLabel(
            preview_frame,
            text="📋 Aperçu",
            font=("Arial", 13, "bold"),
            text_color="#00d9ff"
        )
        preview_title.pack(padx=15, pady=(15, 10))

        self.preview_text = ctk.CTkTextbox(preview_frame, fg_color=("#ffffff", "#0f0f0f"), text_color="#888888")
        self.preview_text.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self.refresh_files()

    def refresh_files(self):
        threading.Thread(target=self._load_files, daemon=True).start()

    def _load_files(self):
        try:
            items = sorted(self.current_path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
            self.after(0, self._display_files, items)
        except PermissionError:
            self.after(0, lambda: ctk.CTkMessagebox.show_error("Erreur", "Accès refusé au dossier"))

    def _display_files(self, items):
        for widget in self.file_list.winfo_children():
            widget.destroy()

        for item in items[:100]:
            self._create_file_item(item)

    def _create_file_item(self, item):
        frame = ctk.CTkFrame(self.file_list, fg_color=("#e0e0e0", "#2a2a2a"), corner_radius=8)
        frame.pack(fill="x", pady=5, padx=10)

        icon = "📁" if item.is_dir() else self._get_file_icon(item)

        label_text = f"{icon} {item.name}"
        if item.is_file():
            try:
                size = item.stat().st_size / 1024
                if size > 1024:
                    size_str = f" ({size/1024:.1f}MB)"
                else:
                    size_str = f" ({size:.1f}KB)"
                label_text += size_str
            except:
                pass

        btn = ctk.CTkButton(
            frame,
            text=label_text,
            font=("Arial", 11),
            fg_color="transparent",
            hover_color="#333333",
            text_color=("black", "white"),
            anchor="w",
            command=lambda i=item: self.select_item(i)
        )
        btn.pack(fill="both", expand=True, padx=10, pady=8)

    def _get_file_icon(self, path):
        ext = path.suffix.lower()
        icons = {
            ".pdf": "📄", ".doc": "📄", ".docx": "📄", ".txt": "📝",
            ".mp3": "🎵", ".wav": "🎵", ".flac": "🎵",
            ".mp4": "🎬", ".avi": "🎬", ".mkv": "🎬",
            ".jpg": "🖼️", ".png": "🖼️", ".gif": "🖼️",
            ".zip": "📦", ".rar": "📦", ".7z": "📦",
            ".exe": "⚙️", ".app": "⚙️"
        }
        return icons.get(ext, "📄")

    def select_item(self, item):
        self.selected_file = item

        if item.is_dir():
            try:
                self.current_path = item
                self.path_label.configure(text=str(self.current_path))
                self.refresh_files()
            except PermissionError:
                pass
        else:
            self.show_preview(item)

    def show_preview(self, item):
        self.preview_text.configure(state="normal")
        self.preview_text.delete("1.0", "end")

        try:
            size = item.stat().st_size
            size_mb = size / (1024 * 1024)
            created = item.stat().st_mtime

            info = f"Fichier: {item.name}\n\n"
            info += f"Chemin: {item.absolute()}\n"
            info += f"Taille: {size_mb:.2f}MB ({size} bytes)\n"
            info += f"Extension: {item.suffix}\n"

            self.preview_text.insert("1.0", info)

            ext = item.suffix.lower()
            if ext in [".txt", ".md", ".py", ".js", ".html", ".css"]:
                try:
                    with open(item, "r", encoding="utf-8") as f:
                        content = f.read()[:1000]
                    self.preview_text.insert("end", f"\n\n--- Contenu (premiers 1000 caractères) ---\n\n{content}")
                except:
                    pass

            open_btn_frame = ctk.CTkFrame(self.preview_text, fg_color="transparent", height=40)
            self.preview_text.window_create("end", window=open_btn_frame)

        except Exception as e:
            self.preview_text.insert("1.0", f"Erreur: {str(e)}")

        self.preview_text.configure(state="disabled")

    def go_back(self):
        if self.current_path.parent != self.current_path:
            self.current_path = self.current_path.parent
            self.path_label.configure(text=str(self.current_path))
            self.refresh_files()

    def go_home(self):
        self.current_path = Path.home()
        self.path_label.configure(text=str(self.current_path))
        self.refresh_files()
