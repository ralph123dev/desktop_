import customtkinter as ctk
from config.settings import settings
from services.network_info import get_ip_addresses
from services.cloudinary_service import CloudinaryService
from tkinter import filedialog
import threading
import time
import os
from ui.widgets.upload_progress import UploadProgressWindow

class SettingsFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=("#ffffff", "#0f0f0f"))
        self.app = app
        self.cloudinary = CloudinaryService()

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.create_header()
        self.create_settings()

    def create_header(self):
        header = ctk.CTkFrame(self, fg_color=("#f0f0f0", "#1a1a1a"), height=80)
        header.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header.grid_propagate(False)

        title = ctk.CTkLabel(
            header,
            text="⚙️ Paramètres",
            font=("Arial", 24, "bold"),
            text_color="#00d9ff"
        )
        title.pack(side="left", padx=30, pady=20)

    def create_settings(self):
        content = ctk.CTkScrollableFrame(self, fg_color=("#ffffff", "#0f0f0f"))
        content.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        theme_frame = ctk.CTkFrame(content, fg_color=("#f0f0f0", "#1a1a1a"), corner_radius=10)
        theme_frame.pack(fill="x", pady=20)

        theme_title = ctk.CTkLabel(
            theme_frame,
            text="🌙 Thème",
            font=("Arial", 14, "bold"),
            text_color="#00d9ff"
        )
        theme_title.pack(anchor="w", padx=20, pady=(15, 10))

        theme_desc = ctk.CTkLabel(
            theme_frame,
            text="Choisissez le mode d'affichage de l'application",
            font=("Arial", 11),
            text_color="#888888"
        )
        theme_desc.pack(anchor="w", padx=20, pady=(0, 15))

        theme_var = ctk.StringVar(value=settings.get("theme", "dark"))

        for theme in ["dark", "light"]:
            btn = ctk.CTkRadioButton(
                theme_frame,
                text="Mode " + ("Sombre" if theme == "dark" else "Clair"),
                variable=theme_var,
                value=theme,
                font=("Arial", 12),
                command=lambda: self.change_theme(theme_var.get())
            )
            btn.pack(anchor="w", padx=40, pady=5)

        chart_frame = ctk.CTkFrame(content, fg_color=("#f0f0f0", "#1a1a1a"), corner_radius=10)
        chart_frame.pack(fill="x", pady=20)

        chart_title = ctk.CTkLabel(
            chart_frame,
            text="📊 Style des Courbes",
            font=("Arial", 14, "bold"),
            text_color="#00d9ff"
        )
        chart_title.pack(anchor="w", padx=20, pady=(15, 10))

        chart_desc = ctk.CTkLabel(
            chart_frame,
            text="Choisissez le style d'affichage des graphiques",
            font=("Arial", 11),
            text_color="#888888"
        )
        chart_desc.pack(anchor="w", padx=20, pady=(0, 15))

        chart_var = ctk.StringVar(value=settings.get("chart_style", "curve"))

        for chart in ["curve", "circle"]:
            btn = ctk.CTkRadioButton(
                chart_frame,
                text="Style " + ("Courbe" if chart == "curve" else "Cercle"),
                variable=chart_var,
                value=chart,
                font=("Arial", 12),
                command=lambda: self.change_chart_style(chart_var.get())
            )
            btn.pack(anchor="w", padx=40, pady=5)

        ip_frame = ctk.CTkFrame(content, fg_color=("#f0f0f0", "#1a1a1a"), corner_radius=10)
        ip_frame.pack(fill="x", pady=20)

        ip_title = ctk.CTkLabel(
            ip_frame,
            text="🌐 Informations Réseau",
            font=("Arial", 14, "bold"),
            text_color="#00d9ff"
        )
        ip_title.pack(anchor="w", padx=20, pady=(15, 10))

        self.ipv4_label = ctk.CTkLabel(
            ip_frame,
            text="IPv4: Chargement...",
            font=("Arial", 11),
            text_color="#888888"
        )
        self.ipv4_label.pack(anchor="w", padx=20, pady=2)

        self.ipv6_label = ctk.CTkLabel(
            ip_frame,
            text="IPv6: Chargement...",
            font=("Arial", 11),
            text_color="#888888"
        )
        self.ipv6_label.pack(anchor="w", padx=20, pady=2)

        self.public_ip_label = ctk.CTkLabel(
            ip_frame,
            text="IP Publique: Chargement...",
            font=("Arial", 11),
            text_color="#888888"
        )
        self.public_ip_label.pack(anchor="w", padx=20, pady=(2, 15))

        refresh_btn = ctk.CTkButton(
            ip_frame,
            text="🔄 Actualiser",
            command=self.update_ip_info,
            font=("Arial", 12),
            fg_color="#00d9ff",
            hover_color="#00b3ff"
        )
        refresh_btn.pack(anchor="w", padx=20, pady=(0, 15))

        status_frame = ctk.CTkFrame(content, fg_color=("#f0f0f0", "#1a1a1a"), corner_radius=10)
        status_frame.pack(fill="x", pady=20)

        status_label = ctk.CTkLabel(
            status_frame,
            text="✅ Toutes les fonctionnalités sont activées",
            font=("Arial", 12),
            text_color="#00d9ff"
        )
        status_label.pack(anchor="w", padx=20, pady=15)

        # Démarrer la mise à jour des informations IP
        self.update_ip_info()

        # Ajouter la section de transfert
        transfer_frame = ctk.CTkFrame(content, fg_color=("#f0f0f0", "#1a1a1a"), corner_radius=10)
        transfer_frame.pack(fill="x", pady=20)

        transfer_title = ctk.CTkLabel(
            transfer_frame,
            text="📤 Transfert de Fichiers",
            font=("Arial", 14, "bold"),
            text_color="#00d9ff"
        )
        transfer_title.pack(anchor="w", padx=20, pady=(15, 10))

        # Bouton Envoyer
        send_btn = ctk.CTkButton(
            transfer_frame,
            text="📤 Envoyer à...",
            command=self.show_upload_dialog,
            font=("Arial", 12),
            fg_color="#00d9ff",
            hover_color="#00b3ff"
        )
        send_btn.pack(anchor="w", padx=20, pady=5)

        # Bouton Recevoir
        receive_btn = ctk.CTkButton(
            transfer_frame,
            text="📥 Recevoir de...",
            command=self.show_download_dialog,
            font=("Arial", 12),
            fg_color="#00d9ff",
            hover_color="#00b3ff"
        )
        receive_btn.pack(anchor="w", padx=20, pady=(5, 15))

    def change_theme(self, theme):
        settings.set("theme", theme)
        if theme == "dark":
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def change_chart_style(self, style):
        settings.set("chart_style", style)

    def update_ip_info(self):
        def update():
            ip_info = get_ip_addresses()
            self.ipv4_label.configure(text=f"IPv4: {ip_info['ipv4']}")
            self.ipv6_label.configure(text=f"IPv6: {ip_info['ipv6']}")
            self.public_ip_label.configure(text=f"IP Publique: {ip_info['public']}")

        # Exécuter dans un thread pour ne pas bloquer l'interface
        thread = threading.Thread(target=update)
        thread.daemon = True
        thread.start()

    def show_upload_dialog(self):
        # 1. Demander l'ID d'envoi
        dialog_send = ctk.CTkInputDialog(
            text="Entrez votre ID d'envoi (expéditeur) :",
            title="Envoyer un fichier - Étape 1"
        )
        send_id = dialog_send.get_input()
        if not send_id:
            return

        # 2. Choisir le fichier
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        # 3. Demander l'ID de réception
        dialog_recv = ctk.CTkInputDialog(
            text="Entrez l'ID de réception (destinataire) :",
            title="Envoyer un fichier - Étape 3"
        )
        receive_id = dialog_recv.get_input()
        if not receive_id:
            return

        # Créer la fenêtre de progression
        progress_window = UploadProgressWindow(self)
        
        def progress_callback(value, filename):
            if not progress_window.winfo_exists():
                return
                
            # Mettre à jour la barre de progression
            progress_window.after(0, lambda: progress_window.update_progress(value, filename))
            
            if value >= 1.0:
                # Fermer la fenêtre de progression après un petit délai
                progress_window.after(500, progress_window.done)
                # Afficher le message de succès dans le thread principal
                progress_window.after(600, lambda: messagebox.showinfo(
                    "Upload réussi", 
                    f"Fichier '{filename}' envoyé avec succès!\n\n"
                    f"ID d'envoi : {send_id}\n"
                    f"ID de réception : {receive_id}\n\n"
                    f"Note: Le destinataire devra utiliser l'ID de RÉCEPTION pour télécharger le fichier."
                ))

        # Lancer l'upload en utilisant l'ID de réception pour le stockage Cloudinary
        threading.Thread(target=self._run_upload, args=(file_path, receive_id, progress_callback), daemon=True).start()

    def _run_upload(self, file_path, user_id, progress_callback):
        try:
            self.cloudinary.upload_file(
                file_path, 
                user_id, 
                progress_callback
            )
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Erreur d'envoi", str(e)))

    def show_download_dialog(self):
        dialog = ctk.CTkInputDialog(
            text="Entrez VOTRE identifiant (ID de réception) :",
            title="Recevoir un fichier"
        )
        receive_id = dialog.get_input()
        if not receive_id:
            return

        dialog = ctk.CTkInputDialog(
            text="Entrez le nom exact du fichier à recevoir :",
            title="Recevoir un fichier"
        )
        file_name = dialog.get_input()
        if not file_name:
            return

        try:
            url = self.cloudinary.get_file_url(file_name, receive_id)
            if url:
                save_path = filedialog.asksaveasfilename(
                    defaultextension=os.path.splitext(file_name)[1],
                    initialfile=file_name
                )
                if save_path:
                    # Télécharger et sauvegarder le fichier
                    import requests
                    response = requests.get(url)
                    with open(save_path, 'wb') as f:
                        f.write(response.content)
                    self.show_info("Succès", "Fichier téléchargé avec succès!")
            else:
                self.show_error("Erreur", "Fichier non trouvé ou lien expiré.")
        except Exception as e:
            self.show_error("Erreur", str(e))

    def show_info(self, title, message):
        messagebox.showinfo(title, message)

    def show_error(self, title, message):
        messagebox.showerror(title, message)

    def destroy(self):
        # Nettoyer les ressources avant la destruction
        super().destroy()
