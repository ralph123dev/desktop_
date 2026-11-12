import customtkinter as ctk
import threading
import ctypes
import tkinter as tk
from tkinter import messagebox
from services.usb_antivirus import USBAntivirusService

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

class UltreCleanFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.checking = False
        self.target_usb_name = ""
        self.closing = False
        self.usb_refreshing = False
        self.usb_refresh_after_id = None

        self.setup_ui()
        self.refresh_usb_list()
        self.schedule_usb_refresh()

    def setup_ui(self):
        # Titre
        self.title = ctk.CTkLabel(
            self, 
            text="🛡️ ULTRE CLEAN - SUPPRESSION VIRUS", 
            font=("Arial", 24, "bold"),
            text_color="#00d9ff"
        )
        self.title.pack(pady=30)

        self.usb_frame = ctk.CTkFrame(self, fg_color=("#f0f0f0", "#1a1a1a"))
        self.usb_frame.pack(pady=(0, 15), padx=40, fill="x")

        usb_header = ctk.CTkFrame(self.usb_frame, fg_color="transparent")
        usb_header.pack(fill="x", padx=15, pady=(12, 4))

        ctk.CTkLabel(
            usb_header,
            text="CLÉS USB CONNECTÉES",
            font=("Arial", 16, "bold"),
            text_color="#00d9ff",
        ).pack(side="left")

        self.usb_refresh_button = ctk.CTkButton(
            usb_header,
            text="Actualiser",
            width=100,
            command=self.refresh_usb_list,
        )
        self.usb_refresh_button.pack(side="right")

        self.usb_list = ctk.CTkScrollableFrame(
            self.usb_frame,
            fg_color="transparent",
            height=110,
        )
        self.usb_list.pack(fill="x", padx=10, pady=(0, 10))
        self.usb_status_label = ctk.CTkLabel(
            self.usb_list,
            text="Recherche des clés USB...",
            text_color="#888888",
        )
        self.usb_status_label.pack(pady=12)

        # Zone de status et log
        self.status_label = ctk.CTkLabel(
            self,
            text="En attente d'action...",
            font=("Arial", 14),
            text_color="#cccccc"
        )
        self.status_label.pack(pady=10)

        # Card principale
        self.process_frame = ctk.CTkFrame(self, fg_color=("#f0f0f0", "#1a1a1a"))
        self.process_frame.pack(pady=20, padx=40, fill="x")

        # Input Nom Clé
        self.info_label = ctk.CTkLabel(
            self.process_frame,
            text="Entrez le NOM (Label) de la clé USB infectée :",
            font=("Arial", 14, "bold")
        )
        self.info_label.pack(pady=(20, 10))

        self.entry_name = ctk.CTkEntry(
            self.process_frame,
            width=300,
            placeholder_text="Ex: MA_CLE_USB"
        )
        self.entry_name.pack(pady=10)

        # Bouton Valider
        self.btn_validate = ctk.CTkButton(
            self.process_frame,
            text="VALIDER ET ATTENDRE L'INSERTION",
            font=("Arial", 14, "bold"),
            fg_color="#00d9ff",
            text_color="#000000",
            hover_color="#00b8d4",
            command=self.start_detection_process
        )
        self.btn_validate.pack(pady=20)

        # Indicateur de chargement (caché par défaut)
        self.loader = ctk.CTkProgressBar(self.process_frame, width=400)
        self.loader.set(0)
        # self.loader.pack(pady=10) # On le packera quand nécessaire

        # Section Deep Scan
        self.scan_frame = ctk.CTkFrame(self, fg_color=("#f0f0f0", "#1a1a1a"))
        self.scan_frame.pack(pady=20, padx=40, fill="x")

        self.scan_title = ctk.CTkLabel(
            self.scan_frame,
            text="SCAN EN PROFONDEUR",
            font=("Arial", 16, "bold"),
            text_color="#ffcc00"
        )
        self.scan_title.pack(pady=(20, 10))

        self.scan_desc = ctk.CTkLabel(
            self.scan_frame,
            text="Scanner une clé spécifiquement pour trouver les petits fichiers cachés et les supprimer.",
            font=("Arial", 12)
        )
        self.scan_desc.pack(pady=5)

        # Pour le scan manuel, on peut demander la lettre ou le nom aussi
        # Simplification: bouton qui scanne la clé active ou demande une lettre
        self.btn_scan = ctk.CTkButton(
            self.scan_frame,
            text="SCANNER UNE CLÉ (MANUEL)",
            font=("Arial", 12, "bold"),
            fg_color="#333333",
            hover_color="#444444",
            command=self.manual_scan_prompt
        )
        self.btn_scan.pack(pady=20)

    def refresh_usb_list(self):
        if self.closing or self.usb_refreshing:
            return

        self.usb_refreshing = True
        self.usb_refresh_button.configure(state="disabled")
        threading.Thread(target=self.load_usb_list, daemon=True).start()

    def load_usb_list(self):
        try:
            drives = USBAntivirusService.get_removable_drives()
        except Exception as error:
            try:
                self.after(0, self.show_usb_error, error)
            except tk.TclError:
                pass
            return

        try:
            self.after(0, self.display_usb_list, drives)
        except tk.TclError:
            pass

    def display_usb_list(self, drives):
        self.usb_refreshing = False
        if self.closing:
            return

        self.usb_refresh_button.configure(state="normal")
        for widget in self.usb_list.winfo_children():
            widget.destroy()

        if not drives:
            self.usb_status_label = ctk.CTkLabel(
                self.usb_list,
                text="Aucune clé USB détectée.",
                text_color="#888888",
            )
            self.usb_status_label.pack(pady=12)
            return

        for drive in drives:
            total = self.format_storage_size(drive["total_size"])
            used = self.format_storage_size(drive["used_size"])
            free = self.format_storage_size(drive["free_size"])
            details = (
                f"{drive['mountpoint']}  •  "
                f"Utilisé : {used} / {total} ({drive['percent']:.1f} %)  •  "
                f"Libre : {free}"
            )
            drive_row = ctk.CTkFrame(
                self.usb_list,
                fg_color=("#e0e0e0", "#2a2a2a"),
                corner_radius=8,
            )
            drive_row.pack(fill="x", padx=4, pady=4)
            ctk.CTkLabel(
                drive_row,
                text=drive["name"],
                font=("Arial", 13, "bold"),
                anchor="w",
            ).pack(fill="x", padx=12, pady=(8, 0))
            ctk.CTkLabel(
                drive_row,
                text=details,
                font=("Arial", 11),
                text_color="#888888",
                anchor="w",
            ).pack(fill="x", padx=12, pady=(2, 8))

    def show_usb_error(self, error):
        self.usb_refreshing = False
        if self.closing:
            return

        self.usb_refresh_button.configure(state="normal")
        for widget in self.usb_list.winfo_children():
            widget.destroy()
        ctk.CTkLabel(
            self.usb_list,
            text=f"Erreur lors de la détection des clés USB : {error}",
            text_color="#ff3333",
            wraplength=500,
        ).pack(pady=12)

    def schedule_usb_refresh(self):
        if not self.closing:
            self.usb_refresh_after_id = self.after(5000, self.run_scheduled_usb_refresh)

    def run_scheduled_usb_refresh(self):
        self.usb_refresh_after_id = None
        self.refresh_usb_list()
        self.schedule_usb_refresh()

    @staticmethod
    def format_storage_size(size):
        value = float(size)
        for unit in ("o", "Ko", "Mo", "Go", "To"):
            if value < 1024 or unit == "To":
                return f"{value:.1f} {unit}"
            value /= 1024

    def update_status(self, text, color="#cccccc"):
        self.after(0, lambda: self.status_label.configure(text=text, text_color=color))

    def start_detection_process(self):
        if not is_admin():
            messagebox.showwarning("Privilèges requis", "Cette opération nécessite des droits d'administrateur pour manipuler les fichiers système et formater les disques.\nVeuillez relancer l'application en tant qu'administrateur.")
            self.update_status("Relancez en tant qu'administrateur", "#ff3333")
            return

        name = self.entry_name.get().strip()
        if not name:
            messagebox.showerror("Erreur", "Veuillez entrer le nom de la clé.")
            return

        self.target_usb_name = name
        self.entry_name.configure(state="disabled")
        self.btn_validate.configure(state="disabled")
        self.loader.pack(pady=10)
        self.loader.start()
        
        self.update_status(f"Veuillez insérer la clé nommée '{name}'...", "#00d9ff")
        
        # Lancer le thread d'écoute
        threading.Thread(target=self.wait_for_usb_thread, daemon=True).start()

    def wait_for_usb_thread(self):
        USBAntivirusService.wait_for_usb(self.target_usb_name, self.on_usb_detected)

    def on_usb_detected(self, drive_info, label):
        self.after(0, self.loader.stop)
        self.update_status(f"Clé détectée : {label} ({drive_info['mountpoint']})", "#00ff00")
        
        # Lancer le nettoyage/formatage
        self.process_cleaning(drive_info)

    def process_cleaning(self, drive_info):
        self.update_status("Analyse du contenu et sécurité...", "#ffff00")
        self.after(0, self.loader.start)
        
        def run_clean():
            # Pass a thread-safe callback
            safe_callback = lambda msg: self.update_status(msg)
            result = USBAntivirusService.clean_and_format(drive_info, safe_callback)
            
            # Post-process UI updates
            self.after(0, lambda: self.finish_processing(result))

        threading.Thread(target=run_clean, daemon=True).start()

    def finish_processing(self, result_msg):
        self.loader.stop()
        self.loader.pack_forget()
        self.entry_name.configure(state="normal")
        self.btn_validate.configure(state="normal")

        if "SUCCESS" in result_msg:
            self.update_status("VIRUS ÉLIMINÉ ! Clé formatée et sécurisée.", "#00ff00")
            messagebox.showinfo("Succès", result_msg)
        else:
            self.update_status("Opération terminée avec avertissements.", "#ff3333")
            messagebox.showwarning("Attention", result_msg)

    def manual_scan_prompt(self):
        # Simple input dialog for drive letter
        dialog = ctk.CTkInputDialog(text="Entrez la lettre du lecteur à scanner (ex: E:):", title="Scan Manuel")
        # Note: dialog.get_input() blocks, so this should ideally be done before thread or is fine in main thread
        letter = dialog.get_input()
        if letter:
            formatted_letter = letter if ":" in letter else f"{letter}:"
            formatted_path = f"{formatted_letter}\\"
            
            self.scan_loader = ctk.CTkProgressBar(self.scan_frame)
            self.scan_loader.pack(pady=10)
            self.scan_loader.start()
            
            def run_deep_scan():
                # Thread-safe logging
                safe_callback = lambda msg: self.update_status(msg)
                res = USBAntivirusService.deep_scan(formatted_path, safe_callback)
                self.after(0, lambda: self.scan_finished(res))
            
            threading.Thread(target=run_deep_scan, daemon=True).start()

    def scan_finished(self, msg):
        self.scan_loader.stop()
        self.scan_loader.pack_forget()
        messagebox.showinfo("Scan Terminé", msg)
        self.update_status("Scan terminé.", "#ffffff")

    def destroy(self):
        self.closing = True
        if self.usb_refresh_after_id is not None:
            self.after_cancel(self.usb_refresh_after_id)
        super().destroy()
