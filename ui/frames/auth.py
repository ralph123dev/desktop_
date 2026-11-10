import customtkinter as ctk
from services.auth_service import AuthService

class AuthFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=("#ffffff", "#0f0f0f"))
        self.app = app
        self.auth_service = AuthService()
        self.is_register = False

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.create_login_frame()

    def create_login_frame(self):
        main_frame = ctk.CTkFrame(self, fg_color=("#f0f0f0", "#1a1a1a"), corner_radius=15)
        main_frame.grid(row=0, column=0, padx=20, pady=20)

        title = ctk.CTkLabel(
            main_frame,
            text="⚡ STARK LOG",
            font=("Arial", 40, "bold"),
            text_color="#00d9ff"
        )
        title.grid(row=0, column=0, columnspan=2, pady=30, padx=40)

        subtitle = ctk.CTkLabel(
            main_frame,
            text="Système de Monitoring Avancé",
            font=("Arial", 14),
            text_color="#888888"
        )
        subtitle.grid(row=1, column=0, columnspan=2, pady=10, padx=40)

        email_label = ctk.CTkLabel(
            main_frame,
            text="Email:",
            font=("Arial", 14, "bold"),
            text_color=("black", "white")
        )
        email_label.grid(row=2, column=0, columnspan=2, sticky="w", padx=40, pady=(30, 5))

        self.email_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="votre@email.com",
            font=("Arial", 14),
            width=300,
            height=40
        )
        self.email_entry.grid(row=3, column=0, columnspan=2, padx=40, pady=5)

        password_label = ctk.CTkLabel(
            main_frame,
            text="Mot de passe:",
            font=("Arial", 14, "bold"),
            text_color=("black", "white")
        )
        password_label.grid(row=4, column=0, columnspan=2, sticky="w", padx=40, pady=(20, 5))

        self.password_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="••••••••",
            font=("Arial", 14),
            width=300,
            height=40,
            show="*"
        )
        self.password_entry.grid(row=5, column=0, columnspan=2, padx=40, pady=5)

        self.username_label = ctk.CTkLabel(
            main_frame,
            text="Nom d'utilisateur:",
            font=("Arial", 14, "bold"),
            text_color=("black", "white")
        )

        self.username_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="votre_nom",
            font=("Arial", 14),
            width=300,
            height=40
        )

        self.message_label = ctk.CTkLabel(
            main_frame,
            text="",
            font=("Arial", 12),
            text_color="#ff3333"
        )
        self.message_label.grid(row=7, column=0, columnspan=2, pady=10, padx=40)

        self.login_btn = ctk.CTkButton(
            main_frame,
            text="Connexion",
            font=("Arial", 16, "bold"),
            fg_color="#00d9ff",
            text_color=("white", "black"),
            height=40,
            command=self.handle_login
        )
        self.login_btn.grid(row=8, column=0, columnspan=2, padx=40, pady=10)

        self.toggle_btn = ctk.CTkButton(
            main_frame,
            text="Créer un compte",
            font=("Arial", 14),
            fg_color="transparent",
            text_color="#00d9ff",
            hover_color="#1a3a3a",
            command=self.toggle_mode
        )
        self.toggle_btn.grid(row=9, column=0, columnspan=2, padx=40, pady=10)

    def toggle_mode(self):
        self.is_register = not self.is_register

        if self.is_register:
            self.username_label.grid(row=6, column=0, columnspan=2, sticky="w", padx=40, pady=(20, 5))
            self.username_entry.grid(row=7, column=0, columnspan=2, padx=40, pady=5)
            self.message_label.grid(row=8, column=0, columnspan=2, pady=10, padx=40)
            self.login_btn.grid(row=9, column=0, columnspan=2, padx=40, pady=10)
            self.toggle_btn.grid(row=10, column=0, columnspan=2, padx=40, pady=10)

            self.login_btn.configure(text="S'inscrire")
            self.toggle_btn.configure(text="Déjà inscrit?")
        else:
            self.username_label.grid_forget()
            self.username_entry.grid_forget()
            self.message_label.grid(row=7, column=0, columnspan=2, pady=10, padx=40)
            self.login_btn.grid(row=8, column=0, columnspan=2, padx=40, pady=10)
            self.toggle_btn.grid(row=9, column=0, columnspan=2, padx=40, pady=10)

            self.login_btn.configure(text="Connexion")
            self.toggle_btn.configure(text="Créer un compte")

    def handle_login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get()

        if not email or not password:
            self.message_label.configure(text="Veuillez remplir tous les champs", text_color="#ff3333")
            return

        if self.is_register:
            username = self.username_entry.get().strip()
            if not username:
                self.message_label.configure(text="Veuillez entrer un nom d'utilisateur", text_color="#ff3333")
                return

            success, message = self.auth_service.register(email, password, username)
            self.message_label.configure(text=message, text_color="#00d9ff" if success else "#ff3333")

            if success:
                self.is_register = False
                self.username_entry.delete(0, "end")
                self.toggle_mode()
        else:
            success, message, user_data = self.auth_service.login(email, password)
            self.message_label.configure(text=message, text_color="#00d9ff" if success else "#ff3333")

            if success:
                self.app.login_success(user_data.get("id"), user_data.get("username"))
