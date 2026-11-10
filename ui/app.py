import customtkinter as ctk
from ui.frames.dashboard import DashboardFrame
from ui.frames.storage import StorageFrame
from ui.frames.settings import SettingsFrame
from ui.frames.auth import AuthFrame
from ui.frames.data import DataFrame
from ui.frames.network import NetworkFrame
from config.settings import settings
import threading
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

class StarkLogApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Undescord - System Monitor")
        try:
            self.iconbitmap("logo.ico")
        except:
            pass
        self.geometry("1400x800")
        self.resizable(True, True)

        # Initialiser l'utilisateur
        self.current_user = {"id": None, "username": "Guest"}
        
        # Créer d'abord le layout
        self.create_layout()
        
        # Puis afficher le dashboard
        self.switch_frame("Dashboard")

        # Ajouter la gestion de la fermeture de la fenêtre
        self.protocol("WM_DELETE_WINDOW", self.quit_app)

    def create_layout(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=200, fg_color=("#f0f0f0", "#1a1a1a"))
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.sidebar.grid_propagate(False)

        self.content_frame = ctk.CTkFrame(self, fg_color=("#ffffff", "#0f0f0f"))
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)

        self.create_sidebar()

    def create_sidebar(self):
        logo_label = ctk.CTkLabel(
            self.sidebar,
            text="⚡ Undescord",
            font=("Arial", 20, "bold"),
            text_color="#00d9ff"
        )
        logo_label.pack(pady=20, padx=10)

        separator = ctk.CTkFrame(self.sidebar, height=2, fg_color="#333333")
        separator.pack(fill="x", padx=10, pady=10)

        self.nav_buttons = {}

        nav_items = [
            ("Dashboard", "📊"),
            ("Data", "🌐"),
            ("Réseau", "📡"),
            ("Stockage", "💾"),
            ("Ultre Clean", "🛡️"),
            ("Paramètres", "⚙️"),
            ("Quitter", "❌"),
        ]

        for name, icon in nav_items:
            btn = ctk.CTkButton(
                self.sidebar,
                text=f"{icon} {name}",
                font=("Arial", 14, "bold"),
                fg_color="transparent",
                hover_color="#00d9ff",
                text_color=("black", "white"),
                command=lambda n=name: self.switch_frame(n)
            )
            btn.pack(fill="x", padx=10, pady=8)
            self.nav_buttons[name] = btn

        separator2 = ctk.CTkFrame(self.sidebar, height=2, fg_color="#333333")
        separator2.pack(fill="x", padx=10, pady=20)

        logout_btn = ctk.CTkButton(
            self.sidebar,
            text="🚪 Déconnexion",
            font=("Arial", 12, "bold"),
            fg_color="#ff3333",
            hover_color="#cc0000",
            command=self.logout
        )
        logout_btn.pack(fill="x", padx=10, pady=8)

        # Admin status indicator
        admin_status = "Mode Administrateur" if is_admin() else "Mode Utilisateur"
        admin_color = "#00ff00" if is_admin() else "#ffcc00"
        
        admin_label = ctk.CTkLabel(
            self.sidebar,
            text=f"🛡️ {admin_status}",
            font=("Arial", 10),
            text_color=admin_color
        )
        admin_label.pack(side="bottom", pady=20)

    def switch_frame(self, frame_name):
        if frame_name == "Quitter":
            self.quit_app()
            return

        for widget in self.content_frame.winfo_children():
            widget.destroy()

        for btn in self.nav_buttons.values():
            btn.configure(fg_color="transparent")

        if frame_name in self.nav_buttons:
            self.nav_buttons[frame_name].configure(fg_color="#00d9ff")

        if frame_name == "Dashboard":
            frame = DashboardFrame(self.content_frame, self)
        elif frame_name == "Data":
            frame = DataFrame(self.content_frame, self)
        elif frame_name == "Stockage":
            frame = StorageFrame(self.content_frame, self)
        elif frame_name == "Ultre Clean":
            from ui.frames.ultre_clean import UltreCleanFrame
            frame = UltreCleanFrame(self.content_frame, self)
        elif frame_name == "Réseau":
            frame = NetworkFrame(self.content_frame, self)
        elif frame_name == "Paramètres":
            frame = SettingsFrame(self.content_frame, self)

        frame.pack(fill="both", expand=True, padx=0, pady=0)

    def show_dashboard(self):
        self.switch_frame("Dashboard")

    def show_auth_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

        auth_frame = AuthFrame(self, self)
        auth_frame.pack(fill="both", expand=True)

    def clear_frames(self):
        # Nettoyer tous les widgets du content_frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def login_success(self, user_id, username):
        settings.set("user_id", user_id)
        settings.set("username", username)
        self.current_user = user_id

        for widget in self.winfo_children():
            widget.destroy()

        self.create_layout()
        self.show_dashboard()

    def logout(self):
        settings.set("user_id", None)
        settings.set("username", None)
        self.current_user = None
        
        for widget in self.winfo_children():
            widget.destroy()
            
        self.create_layout()
        self.show_auth_frame()

    def quit_app(self):
        # Arrêter proprement tous les timers et threads
        for widget in self.winfo_children():
            if hasattr(widget, 'destroy'):
                try:
                    widget.destroy()
                except:
                    pass
        
        # Forcé la fermeture de l'application
        self.quit()
        self.destroy()
        import sys
        sys.exit(0)
