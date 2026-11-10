import customtkinter as ctk
import os
from dotenv import load_dotenv
import sys
import tkinter as tk
from tkinter import messagebox

load_dotenv()

print("Current working directory:", os.getcwd())
print("Environment variables:")
for key, value in os.environ.items():
    if 'SUPABASE' in key:
        print(f"{key}: {value}")
print(".env file exists:", os.path.exists(".env"))
print("Python version:", sys.version)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

try:
    
    from ui.app import StarkLogApp
except ModuleNotFoundError as e:
    # Si matplotlib est manquant, afficher une boîte d'erreur claire et quitter proprement.
    msg = str(e)
    if "matplotlib" in msg:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Défaut de dépendance",
            "Le paquet requis 'matplotlib' n'est pas installé.\n\nInstallez-le avec :\n\npip install matplotlib\n\npuis relancez l'application."
        )
        sys.exit(1)
    else:
        # Pour toute autre erreur, la remonter afin de ne pas masquer le problème.
        raise

if __name__ == "__main__":
    try:
        app = StarkLogApp()
        app.mainloop()
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
