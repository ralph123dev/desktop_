import customtkinter as ctk

class UploadProgressWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("Upload en cours...")
        self.geometry("300x150")
        self.resizable(False, False)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.label = ctk.CTkLabel(
            self,
            text="Envoi du fichier en cours...",
            font=("Arial", 12)
        )
        self.label.grid(row=0, column=0, pady=10, padx=20)
        
        self.progress = ctk.CTkProgressBar(self)
        self.progress.grid(row=1, column=0, pady=10, padx=20, sticky="ew")
        self.progress.set(0)
        
        self.file_name_label = ctk.CTkLabel(
            self,
            text="",
            font=("Arial", 10)
        )
        self.file_name_label.grid(row=2, column=0, pady=10, padx=20)

    def update_progress(self, value, filename=None):
        self.progress.set(value)
        if filename:
            self.file_name_label.configure(text=filename)

    def done(self):
        self.destroy()
