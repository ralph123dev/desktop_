import customtkinter as ctk
import threading
import time
from services.chat_service import ChatService
from config.settings import settings

class ChatFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=("#ffffff", "#0f0f0f"))
        self.app = app
        self.chat_service = ChatService()
        self.username = settings.get("username")
        self.user_id = settings.get("user_id")
        self.running = True

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.create_header()
        self.create_chat_area()

        self.update_thread = threading.Thread(target=self.update_messages_loop, daemon=True)
        self.update_thread.start()

    def create_header(self):
        header = ctk.CTkFrame(self, fg_color=("#f0f0f0", "#1a1a1a"), height=80)
        header.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header.grid_propagate(False)

        title = ctk.CTkLabel(
            header,
            text="💬 Communauté Stark Log",
            font=("Arial", 24, "bold"),
            text_color="#00d9ff"
        )
        title.pack(side="left", padx=30, pady=20)

        user_info = ctk.CTkLabel(
            header,
            text=f"Connecté en tant que: {self.username}",
            font=("Arial", 12),
            text_color="#888888"
        )
        user_info.pack(side="right", padx=30, pady=20)

    def create_chat_area(self):
        container = ctk.CTkFrame(self, fg_color=("#ffffff", "#0f0f0f"))
        container.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(1, weight=0)
        container.grid_columnconfigure(0, weight=1)

        self.messages_frame = ctk.CTkScrollableFrame(
            container,
            fg_color=("#f0f0f0", "#1a1a1a"),
            corner_radius=10
        )
        self.messages_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 20))

        input_frame = ctk.CTkFrame(container, fg_color=("#f0f0f0", "#1a1a1a"), corner_radius=10, height=80)
        input_frame.grid(row=1, column=0, sticky="ew")
        input_frame.grid_propagate(False)

        self.message_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="Écrivez votre message...",
            font=("Arial", 12),
            height=40
        )
        self.message_input.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        self.message_input.bind("<Return>", lambda e: self.send_message())

        send_btn = ctk.CTkButton(
            input_frame,
            text="📤 Envoyer",
            font=("Arial", 12, "bold"),
            fg_color="#00d9ff",
            text_color="#000000",
            width=100,
            command=self.send_message
        )
        send_btn.pack(side="right", padx=15, pady=15)

        self.load_initial_messages()

    def load_initial_messages(self):
        threading.Thread(target=self._load_messages, daemon=True).start()

    def _load_messages(self):
        messages = self.chat_service.get_messages(50)
        self.after(0, self._display_messages, messages)

    def _display_messages(self, messages):
        for widget in self.messages_frame.winfo_children():
            widget.destroy()

        for msg in messages:
            self._create_message_widget(msg)

    def _create_message_widget(self, msg):
        is_own = msg.get("username") == self.username

        msg_frame = ctk.CTkFrame(
            self.messages_frame,
            fg_color=("#e0e0e0", "#2a2a2a") if is_own else ("#ffffff", "#0f0f0f"),
            corner_radius=10
        )
        msg_frame.pack(fill="x", pady=8, padx=10)

        header_frame = ctk.CTkFrame(msg_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(10, 5))

        username = ctk.CTkLabel(
            header_frame,
            text=msg.get("username", "Unknown"),
            font=("Arial", 12, "bold"),
            text_color="#00d9ff" if is_own else ("black", "white")
        )
        username.pack(side="left")

        time_str = msg.get("created_at", "")[:16]
        time_label = ctk.CTkLabel(
            header_frame,
            text=time_str,
            font=("Arial", 10),
            text_color="#666666"
        )
        time_label.pack(side="right")

        content = ctk.CTkLabel(
            msg_frame,
            text=msg.get("content", ""),
            font=("Arial", 11),
            text_color="#888888",
            wraplength=400,
            justify="left"
        )
        content.pack(anchor="w", padx=15, pady=(0, 10))

    def send_message(self):
        message = self.message_input.get().strip()
        if not message:
            return

        if self.chat_service.send_message(self.user_id, self.username, message):
            self.message_input.delete(0, "end")
            self.load_initial_messages()

    def update_messages_loop(self):
        while self.running:
            try:
                time.sleep(3)
                self.after(0, self.load_initial_messages)
            except Exception as e:
                print(f"Update error: {e}")
                time.sleep(3)

    def destroy(self):
        self.running = False
        super().destroy()
