import customtkinter as ctk
import threading
import time
from services.system_monitor import SystemMonitor
from ui.widgets.ram_monitor import RAMMonitor
from ui.widgets.cleanup_popup import CleanupPopup
from ui.widgets.dns_popup import DNSPopup
from ui.widgets.process_list import ProcessListPopup

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=("#ffffff", "#0f0f0f"))
        self.controller = controller
        self.monitor = SystemMonitor()
        self.running = True
        self.monitors = []

        # Configuration de la grille
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=1)  # Content
        self.grid_columnconfigure(0, weight=1)

        self.create_header()
        self.create_content()

        self.update_thread = threading.Thread(target=self.update_loop, daemon=True)
        self.update_thread.start()

    def create_header(self):
        header = ctk.CTkFrame(self, fg_color=("#f0f0f0", "#1a1a1a"), height=80)
        header.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header.grid_propagate(False)

        title = ctk.CTkLabel(
            header,
            text="📊 Dashboard Système",
            font=("Arial", 24, "bold"),
            text_color="#00d9ff"
        )
        title.pack(side="left", padx=30, pady=20)

    def create_content(self):
        self.content = ctk.CTkScrollableFrame(self, fg_color=("#ffffff", "#0f0f0f"))
        self.content.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.content.grid_columnconfigure(0, weight=1)
        current_row = 0

        # RAM Monitor
        ram_monitor = RAMMonitor(self.content)
        ram_monitor.grid(row=current_row, column=0, sticky="ew", pady=10, padx=10)
        self.ram_monitor = ram_monitor
        self.monitors.append(ram_monitor)
        current_row += 1

        # Buttons frame
        button_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        button_frame.grid(row=current_row, column=0, sticky="ew", pady=10)
        button_frame.grid_columnconfigure((0,1,2), weight=1)

        cleanup_btn = ctk.CTkButton(
            button_frame,
            text="🧹 Nettoyer la RAM et Optimiser",
            font=("Arial", 14, "bold"),
            fg_color="#00d9ff",
            text_color=("white", "black"),
            height=40,
            command=self.show_cleanup_popup
        )
        cleanup_btn.grid(row=0, column=0, padx=10, sticky="ew")

        dns_btn = ctk.CTkButton(
            button_frame,
            text="🔍 Cache DNS",
            font=("Arial", 14, "bold"),
            fg_color="#9333ea",
            text_color="#ffffff",
            height=40,
            command=self.show_dns_popup
        )
        dns_btn.grid(row=0, column=1, padx=10, sticky="ew")

        process_btn = ctk.CTkButton(
            button_frame,
            text="⚙️ Processus",
            font=("Arial", 14, "bold"),
            fg_color="#3b82f6",
            text_color="#ffffff",
            height=40,
            command=self.show_process_list
        )
        process_btn.grid(row=0, column=2, padx=10, sticky="ew")
        current_row += 1

        # Disk frame
        disk_frame = ctk.CTkFrame(self.content, fg_color=("#f0f0f0", "#1a1a1a"), corner_radius=10)
        disk_frame.grid(row=current_row, column=0, sticky="ew", pady=20)
        disk_frame.grid_columnconfigure(0, weight=1)

        disk_title = ctk.CTkLabel(
            disk_frame,
            text="💾 Stockage",
            font=("Arial", 16, "bold"),
            text_color="#00d9ff"
        )
        disk_title.grid(row=0, column=0, sticky="w", padx=20, pady=(15, 10))

        self.disk_container = ctk.CTkFrame(disk_frame, fg_color="transparent")
        self.disk_container.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 15))
        self.disk_container.grid_columnconfigure(0, weight=1)
        current_row += 1

        # Login button for guest mode
        if self.controller.current_user["id"] is None:
            self.login_button = ctk.CTkButton(
                self.content,
                text="Se connecter / S'inscrire",
                command=self.show_auth
            )
            self.login_button.grid(row=current_row, column=0, pady=10, padx=10, sticky="e")

    def update_loop(self):
        while self.running:
            try:
                disks = self.monitor.get_disk_info()
                self.after(0, self.update_disk_display, disks)

                time.sleep(2)
            except Exception as e:
                print(f"Update error: {e}")
                time.sleep(2)

    def update_disk_display(self, disks):
        for widget in self.disk_container.winfo_children():
            widget.destroy()

        for disk in disks:
            disk_widget = ctk.CTkFrame(self.disk_container, fg_color=("#e0e0e0", "#2a2a2a"), corner_radius=8)
            disk_widget.pack(fill="x", pady=8)

            info_frame = ctk.CTkFrame(disk_widget, fg_color="transparent")
            info_frame.pack(fill="x", padx=15, pady=10)

            left = ctk.CTkFrame(info_frame, fg_color="transparent")
            left.pack(side="left", fill="x", expand=True)

            name = ctk.CTkLabel(
                left,
                text=f"{disk['device']} ({disk['mountpoint']})",
                font=("Arial", 12, "bold"),
                text_color=("black", "ffffff")
            )
            name.pack(anchor="w")

            size_text = f"{disk['used'] / (1024**3):.1f}GB / {disk['total'] / (1024**3):.1f}GB ({disk['percent']:.1f}%)"
            size = ctk.CTkLabel(
                left,
                text=size_text,
                font=("Arial", 11),
                text_color="#888888"
            )
            size.pack(anchor="w")

            progress = ctk.CTkProgressBar(disk_widget)
            progress.set(disk['percent']/100)  # Utiliser set() au lieu de value=

    def show_cleanup_popup(self):
        CleanupPopup(self.controller)

    def show_dns_popup(self):
        DNSPopup(self.controller)

    def show_process_list(self):
        ProcessListPopup(self.controller, self.monitor)

    def show_auth(self):
        self.controller.show_auth_frame()

    def destroy(self):
        # Arrêter proprement tous les moniteurs et la boucle d'uodate
        self.running = False
        for monitor in self.monitors:
            if hasattr(monitor, 'stop_monitoring'):
                try:
                    monitor.stop_monitoring()
                except:
                    pass
        super().destroy()
