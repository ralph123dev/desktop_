import customtkinter as ctk
import threading
import time
from services import network_info

class DataFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.running = True
        
        # State for Network Speed
        self.last_net_io = network_info.get_network_io()
        self.last_time = time.time()
        
        self.setup_ui()
        
        # Start Updates
        self.update_stats()
        
        # Load IP Info in Background
        threading.Thread(target=self.load_ip_info, daemon=True).start()

    def setup_ui(self):
        # Grid Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Title
        title = ctk.CTkLabel(
            self,
            text="🌐 Monitor Réseau & Données",
            font=("Arial", 24, "bold"),
            text_color="#00d9ff"
        )
        title.grid(row=0, column=0, columnspan=2, pady=20, sticky="w", padx=20)

        # Left Panel: Network Usage
        self.net_frame = ctk.CTkFrame(self, fg_color=("#f0f0f0", "#1a1a1a"), corner_radius=10)
        self.net_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(self.net_frame, text="Utilisation Bande Passante", font=("Arial", 16, "bold"), text_color="#00d9ff").pack(pady=15)
        
        self.speed_frame = ctk.CTkFrame(self.net_frame, fg_color="transparent")
        self.speed_frame.pack(fill="x", padx=20)
        
        self.down_label = ctk.CTkLabel(self.speed_frame, text="⬇️ Download: 0 KB/s", font=("Arial", 14))
        self.down_label.pack(anchor="w", pady=5)
        
        self.up_label = ctk.CTkLabel(self.speed_frame, text="⬆️ Upload: 0 KB/s", font=("Arial", 14))
        self.up_label.pack(anchor="w", pady=5)

        self.total_frame = ctk.CTkFrame(self.net_frame, fg_color="transparent")
        self.total_frame.pack(fill="x", padx=20, pady=20)
        
        self.total_sent_label = ctk.CTkLabel(self.total_frame, text="Total Envoyé: 0 MB", font=("Arial", 12), text_color="#888888")
        self.total_sent_label.pack(anchor="w")
        
        self.total_recv_label = ctk.CTkLabel(self.total_frame, text="Total Reçu: 0 MB", font=("Arial", 12), text_color="#888888")
        self.total_recv_label.pack(anchor="w")

        # Right Panel: IP Info & Ports
        self.right_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.right_panel.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        
        # IP Info Box
        self.ip_frame = ctk.CTkFrame(self.right_panel, fg_color=("#f0f0f0", "#1a1a1a"), corner_radius=10)
        self.ip_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(self.ip_frame, text="📍 Adresses IP", font=("Arial", 16, "bold"), text_color="#00d9ff").pack(pady=10)
        
        self.public_ip_label = ctk.CTkLabel(self.ip_frame, text="Public: Chargement...", font=("Arial", 13))
        self.public_ip_label.pack(pady=2)
        
        self.local_ip_label = ctk.CTkLabel(self.ip_frame, text="Local: Chargement...", font=("Arial", 13))
        self.local_ip_label.pack(pady=2)

        # Ports Box
        self.ports_frame = ctk.CTkFrame(self.right_panel, fg_color=("#f0f0f0", "#1a1a1a"), corner_radius=10)
        self.ports_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(self.ports_frame, text="🔓 Ports Ouverts (Top 50)", font=("Arial", 16, "bold"), text_color="#00d9ff").pack(pady=10)
        
        # Scrollable Output for Ports
        self.ports_textbox = ctk.CTkTextbox(self.ports_frame, font=("Consolas", 11))
        self.ports_textbox.pack(fill="both", expand=True, padx=10, pady=10)
        self.ports_textbox.configure(state="disabled")

    def load_ip_info(self):
        ips = network_info.get_ip_addresses()
        self.public_ip_label.configure(text=f"Public: {ips.get('public', 'N/A')}")
        self.local_ip_label.configure(text=f"Local: {ips.get('ipv4', 'N/A')}")
        
        # Load ports once initially
        self.update_ports()

    def update_ports(self):
        try:
            ports = network_info.get_open_ports()
            text = f"{'PORT':<8} {'TYPE':<6} {'PID':<8}\n"
            text += "-" * 30 + "\n"
            for p in ports:
                text += f"{p['port']:<8} {p['type']:<6} {p['pid'] or '?' :<8}\n"
            
            self.ports_textbox.configure(state="normal")
            self.ports_textbox.delete("0.0", "end")
            self.ports_textbox.insert("0.0", text)
            self.ports_textbox.configure(state="disabled")
        except:
            pass

    def update_stats(self):
        if not self.running:
            return

        try:
            current_net = network_info.get_network_io()
            current_time = time.time()
            
            # Calculate Speed (Bytes per second)
            time_diff = current_time - self.last_time
            if time_diff > 0:
                bytes_sent_diff = current_net['bytes_sent'] - self.last_net_io['bytes_sent']
                bytes_recv_diff = current_net['bytes_recv'] - self.last_net_io['bytes_recv']
                
                speed_up = bytes_sent_diff / time_diff
                speed_down = bytes_recv_diff / time_diff
                
                self.up_label.configure(text=f"⬆️ Upload: {self._format_bytes(speed_up)}/s")
                self.down_label.configure(text=f"⬇️ Download: {self._format_bytes(speed_down)}/s")
            
            # Update Totals
            self.total_sent_label.configure(text=f"Total Envoyé: {self._format_bytes(current_net['bytes_sent'])}")
            self.total_recv_label.configure(text=f"Total Reçu: {self._format_bytes(current_net['bytes_recv'])}")

            self.last_net_io = current_net
            self.last_time = current_time

            self.after(1000, self.update_stats)
        except Exception as e:
            print(f"Data Frame Update Error: {e}")

    def _format_bytes(self, size):
        power = 2**10
        n = 0
        power_labels = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
        while size > power:
            size /= power
            n += 1
        return f"{size:.1f} {power_labels[n]}B"

    def destroy(self):
        self.running = False
        super().destroy()
