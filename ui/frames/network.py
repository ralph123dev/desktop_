import customtkinter as ctk
import subprocess
import ctypes
import threading
import time
import socket
import re
from tkinter import messagebox

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

class NetworkFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=("white", "#0f0f0f"))
        self.controller = controller

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.create_header()
        self.create_content()
        
        self.running_monitor = False
        self.monitor_thread = None

    def create_header(self):
        header = ctk.CTkFrame(self, fg_color=("#f0f0f0", "#1a1a1a"), height=80)
        header.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header.grid_propagate(False)

        title = ctk.CTkLabel(
            header,
            text="📡 Réseau",
            font=("Arial", 24, "bold"),
            text_color="#00d9ff"
        )
        title.pack(side="left", padx=30, pady=20)

    def create_content(self):
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        # Container for form
        form_frame = ctk.CTkFrame(content, fg_color=("#f0f0f0", "#1a1a1a"), corner_radius=10)
        form_frame.pack(fill="x", pady=20, padx=20)

        # SSID
        ssid_label = ctk.CTkLabel(form_frame, text="Nom du réseau (SSID)", font=("Arial", 14, "bold"))
        ssid_label.pack(anchor="w", padx=20, pady=(20, 5))
        
        self.ssid_entry = ctk.CTkEntry(form_frame, placeholder_text="Entrez le nom du réseau", width=300)
        self.ssid_entry.pack(anchor="w", padx=20, pady=(0, 15))

        # Password
        pass_label = ctk.CTkLabel(form_frame, text="Mot de passe", font=("Arial", 14, "bold"))
        pass_label.pack(anchor="w", padx=20, pady=(0, 5))
        
        self.pass_entry = ctk.CTkEntry(form_frame, placeholder_text="Entrez le mot de passe (min 8 car.)", width=300, show="*")
        self.pass_entry.pack(anchor="w", padx=20, pady=(0, 20))

        # Buttons
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))

        start_btn = ctk.CTkButton(
            btn_frame,
            text="Démarrer le réseau",
            command=self.start_network,
            fg_color="#00d9ff",
            hover_color="#00b3ff"
        )
        start_btn.pack(side="left", padx=(0, 10))

        stop_btn = ctk.CTkButton(
            btn_frame,
            text="Arrêter le réseau",
            command=self.stop_network,
            fg_color="#ff3333",
            hover_color="#cc0000"
        )
        stop_btn.pack(side="left")

        # Status output
        self.status_label = ctk.CTkLabel(content, text="", font=("Arial", 12))
        self.status_label.pack(pady=5)

        # Connected devices section
        devices_frame = ctk.CTkFrame(content, fg_color=("#f0f0f0", "#1a1a1a"), corner_radius=10)
        devices_frame.pack(fill="both", expand=True, padx=20, pady=10)

        ctk.CTkLabel(devices_frame, text="📱 Équipements connectés", font=("Arial", 14, "bold")).pack(pady=10)
        
        self.devices_list = ctk.CTkScrollableFrame(devices_frame, fg_color="transparent", height=200)
        self.devices_list.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.no_devices_label = ctk.CTkLabel(self.devices_list, text="Aucun équipement connecté", text_color="#888888")
        self.no_devices_label.pack(pady=20)

    def start_network(self):
        if not is_admin():
            messagebox.showwarning("Privilèges requis", "Cette opération nécessite des droits d'administrateur.\nVeuillez relancer l'application en tant qu'administrateur pour activer le hotspot.")
            self.status_label.configure(text="Relancez en tant qu'administrateur", text_color="orange")
            return

        ssid = self.ssid_entry.get()
        password = self.pass_entry.get()

        if not ssid or len(password) < 8:
            messagebox.showerror("Erreur", "Veuillez entrer un SSID et un mot de passe d'au moins 8 caractères.")
            return

        try:
            self.status_label.configure(text="Configuration en cours...", text_color="#00d9ff")
            self.update_idletasks()

            # 1. Configure hosted network
            cmd_config = f'netsh wlan set hostednetwork mode=allow ssid="{ssid}" key="{password}"'
            result_config = subprocess.run(cmd_config, shell=True, capture_output=True, text=True)
            
            if result_config.returncode != 0:
                error_msg = result_config.stderr or result_config.stdout
                raise Exception(f"Erreur de configuration : {error_msg}")

            # 2. Start hosted network
            cmd_start = "netsh wlan start hostednetwork"
            result_start = subprocess.run(cmd_start, shell=True, capture_output=True, text=True)

            if result_start.returncode == 0:
                 self.status_label.configure(text="Réseau hébergé avec succès", text_color="green")
                 messagebox.showinfo("Succès", "Le réseau Wi-Fi a été activé avec succès.")
                 self.start_device_monitor()
            else:
                 error_msg = result_start.stderr or result_start.stdout
                 self.status_label.configure(text="Échec de l'activation", text_color="red")
                 
                 friendly_error = "Votre PC ne semble pas supporter le mode réseau hébergé ou la carte Wi-Fi est désactivée."
                 if "elevation" in error_msg.lower() or "administrateur" in error_msg.lower() or "privilège" in error_msg.lower():
                     friendly_error = "Droits d'administrateur insuffisants pour démarrer le réseau."
                 
                 messagebox.showerror("Erreur", f"{friendly_error}\n\nDétails techniques :\n{error_msg}")

        except Exception as e:
            self.status_label.configure(text="Erreur", text_color="red")
            messagebox.showerror("Erreur", str(e))

    def stop_network(self):
        try:
            cmd_stop = "netsh wlan stop hostednetwork"
            subprocess.run(cmd_stop, shell=True)
            self.status_label.configure(text="Réseau arrêté", text_color="orange")
            self.stop_device_monitor()
        except Exception as e:
             messagebox.showerror("Erreur", str(e))
    def start_device_monitor(self):
        if not self.running_monitor:
            self.running_monitor = True
            self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
            self.monitor_thread.start()

    def stop_device_monitor(self):
        self.running_monitor = False
        self.clear_devices_list()

    def monitor_loop(self):
        while self.running_monitor:
            try:
                clients = self.get_connected_clients()
                self.after(0, self.update_devices_ui, clients)
            except Exception as e:
                print(f"Monitor error: {e}")
            time.sleep(5)

    def get_connected_clients(self):
        clients = []
        try:
            # Get MAC addresses from netsh
            result = subprocess.run("netsh wlan show hostednetwork", shell=True, capture_output=True, text=True)
            mac_regex = re.compile(r'([0-9a-fA-F]{2}[:-]){5}([0-9a-fA-F]{2})')
            macs = mac_regex.findall(result.stdout)
            # Find the section "Authenticated clients"
            if "Number of clients" in result.stdout:
                # get just the macs (regex findall returns tuples if there are groups, mac_regex has two)
                # Let's use a simpler regex or just take the full matches
                raw_macs = [m.group(0) for m in mac_regex.finditer(result.stdout)]
                
                # Get ARP table for IP matching
                arp_result = subprocess.run("arp -a", shell=True, capture_output=True, text=True)
                
                for mac in raw_macs:
                    ip = "Inconnu"
                    name = "Équipement"
                    # Match MAC in ARP (arp -a output format: 192.168.x.x  aa-bb-cc-dd-ee-ff  dynamic)
                    # We normalize mac format (netsh uses lowercase colon/dash, arp uses dash)
                    norm_mac = mac.lower().replace(":", "-")
                    
                    for line in arp_result.stdout.splitlines():
                        if norm_mac in line.lower():
                            parts = line.split()
                            if parts:
                                ip = parts[0]
                                try:
                                    # Try to get hostname
                                    name = socket.gethostbyaddr(ip)[0]
                                except:
                                    name = f"Appareil ({ip})"
                                break
                    
                    clients.append({"mac": mac, "ip": ip, "name": name})
        except:
            pass
        return clients

    def update_devices_ui(self, clients):
        if not self.winfo_exists(): return
        self.clear_devices_list()
        
        if not clients:
            self.no_devices_label = ctk.CTkLabel(self.devices_list, text="Aucun équipement connecté", text_color="#888888")
            self.no_devices_label.pack(pady=20)
            return

        for client in clients:
            client_frame = ctk.CTkFrame(self.devices_list, fg_color=("#e0e0e0", "#2a2a2a"), corner_radius=8)
            client_frame.pack(fill="x", pady=5, padx=10)
            
            icon_label = ctk.CTkLabel(client_frame, text="💻", font=("Arial", 20))
            icon_label.pack(side="left", padx=15, pady=10)
            
            info_frame = ctk.CTkFrame(client_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True)
            
            name_label = ctk.CTkLabel(info_frame, text=client['name'], font=("Arial", 12, "bold"), anchor="w")
            name_label.pack(fill="x", pady=(5, 0))
            
            details_label = ctk.CTkLabel(info_frame, text=f"IP: {client['ip']} | MAC: {client['mac']}", font=("Arial", 10), text_color="#888888", anchor="w")
            details_label.pack(fill="x", pady=(0, 5))

    def clear_devices_list(self):
        for widget in self.devices_list.winfo_children():
            widget.destroy()

    def destroy(self):
        self.stop_device_monitor()
        super().destroy()
