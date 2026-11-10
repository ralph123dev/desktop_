import customtkinter as ctk
from services.system_monitor import SystemMonitor
import threading
import time

class CleanupPopup(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Optimiser la RAM")
        self.geometry("400x300")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.monitor = SystemMonitor()
        
        # Centrer la fenêtre
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        self.create_widgets()

    def create_widgets(self):
        # Header Icon/Text
        header = ctk.CTkLabel(
            self,
            text="🚀 Optimisation RAM",
            font=("Arial", 20, "bold"),
            text_color="#00d9ff"
        )
        header.pack(pady=(30, 10))

        # Warning/Info Text
        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.pack(fill="x", padx=30, pady=10)
        
        info_text = (
            "Êtes-vous sûr de vouloir optimiser la mémoire ?\n\n"
            "Cette action va :\n"
            "• Fermer tous les logiciels en cours\n"
            "• Vider tous les caches RAM\n"
            "• Actualiser la machine"
        )
        
        info_label = ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=("Arial", 12),
            text_color="#cccccc",
            justify="center"
        )
        info_label.pack()

        # Action Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=30, pady=30)

        confirm_btn = ctk.CTkButton(
            btn_frame,
            text="OUI, Optimiser",
            font=("Arial", 13, "bold"),
            fg_color="#00d9ff",
            text_color="#000000",
            hover_color="#00b8d4",
            command=self.run_optimization
        )
        confirm_btn.pack(side="right", expand=True, fill="x", padx=(10, 0))

        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Annuler",
            font=("Arial", 13),
            fg_color="#333333",
            hover_color="#444444",
            command=self.destroy
        )
        cancel_btn.pack(side="left", expand=True, fill="x", padx=(0, 10))

        self.status_label = ctk.CTkLabel(
            self,
            text="",
            font=("Arial", 11),
            text_color="#00d9ff"
        )
        self.status_label.pack(side="bottom", pady=10)

    def run_optimization(self):
        # Disable buttons to prevent double click
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                for child in widget.winfo_children():
                    if isinstance(child, ctk.CTkButton):
                        child.configure(state="disabled")

        self.status_label.configure(text="Optimisation en cours...")
        threading.Thread(target=self._optimize_process, daemon=True).start()

    def _optimize_process(self):
        try:
            # 1. Fermer les logiciels
            self.monitor.kill_all_processes()
            time.sleep(1) # Pause pour laisser le système respirer
            
            # 2. Vider les caches
            self.monitor.clear_cache()
            
            # 3. Actualiser (Simulation visual)
            self.status_label.configure(text="Actualisation du système...")
            time.sleep(1)
            
            self.after(0, self.optimization_complete)
        except Exception as e:
            self.after(0, lambda: self.status_label.configure(text=f"Erreur: {str(e)}", text_color="#ff3333"))

    def optimization_complete(self):
        self.status_label.configure(text="Optimisation terminée!", text_color="#4ade80")
        self.after(2000, self.destroy)
