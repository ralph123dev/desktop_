import customtkinter as ctk
from services.system_monitor import SystemMonitor
import threading

class DNSPopup(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Cache DNS")
        self.geometry("700x600")
        self.monitor = SystemMonitor()

        self.create_widgets()
        self.load_dns_cache()

    def create_widgets(self):
        header = ctk.CTkFrame(self, fg_color="#1a1a1a", height=70)
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)

        title = ctk.CTkLabel(
            header,
            text="🔍 Cache DNS",
            font=("Arial", 18, "bold"),
            text_color="#00d9ff"
        )
        title.pack(side="left", padx=20, pady=20)

        clear_btn = ctk.CTkButton(
            header,
            text="🗑️ Vider le Cache",
            font=("Arial", 12, "bold"),
            fg_color="#ff3333",
            hover_color="#cc0000",
            command=self.clear_dns_cache
        )
        clear_btn.pack(side="right", padx=20, pady=20)

        self.text_widget = ctk.CTkTextbox(self, fg_color="#1a1a1a", text_color="#00d9ff")
        self.text_widget.pack(fill="both", expand=True, padx=20, pady=20)

        self.status_label = ctk.CTkLabel(
            self,
            text="Chargement...",
            font=("Arial", 11),
            text_color="#888888"
        )
        self.status_label.pack(pady=10)

    def load_dns_cache(self):
        threading.Thread(target=self._load_dns, daemon=True).start()

    def _load_dns(self):
        dns_records = self.monitor.get_dns_cache()
        content = "\n".join(dns_records)
        self.after(0, self.text_widget.insert, "1.0", content)
        self.after(0, self.status_label.configure, {"text": f"Cache DNS: {len(dns_records)} entrées"})

    def clear_dns_cache(self):
        self.status_label.configure(text="Nettoyage en cours...")
        threading.Thread(target=self._clear, daemon=True).start()

    def _clear(self):
        if self.monitor.clear_dns_cache():
            self.after(0, self.status_label.configure, {"text": "Cache DNS vidé avec succès", "text_color": "#00d9ff"})
            self.after(0, self.text_widget.delete, "1.0", "end")
        else:
            self.after(0, self.status_label.configure, {"text": "Erreur lors du nettoyage", "text_color": "#ff3333"})
