import customtkinter as ctk
import threading

class ProcessListPopup(ctk.CTkToplevel):
    def __init__(self, parent, monitor):
        super().__init__(parent)
        self.title("Gestion des Processus")
        self.geometry("600x700")
        self.monitor = monitor
        self.selected_pids = set()

        self.create_widgets()
        self.load_processes()

    def create_widgets(self):
        header = ctk.CTkFrame(self, fg_color="#1a1a1a", height=70)
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)

        title = ctk.CTkLabel(
            header,
            text="⚙️ Processus Actifs",
            font=("Arial", 18, "bold"),
            text_color="#00d9ff"
        )
        title.pack(side="left", padx=20, pady=20)

        button_frame = ctk.CTkFrame(header, fg_color="transparent")
        button_frame.pack(side="right", padx=20, pady=20)

        kill_btn = ctk.CTkButton(
            button_frame,
            text="🛑 Arrêter Sélectionnés",
            font=("Arial", 12, "bold"),
            fg_color="#ff3333",
            hover_color="#cc0000",
            command=self.kill_selected
        )
        kill_btn.pack()

        self.process_container = ctk.CTkScrollableFrame(self, fg_color="#0f0f0f")
        self.process_container.pack(fill="both", expand=True, padx=20, pady=20)

        self.status_label = ctk.CTkLabel(
            self,
            text="Chargement...",
            font=("Arial", 11),
            text_color="#888888"
        )
        self.status_label.pack(pady=10)

    def load_processes(self):
        threading.Thread(target=self._load, daemon=True).start()

    def _load(self):
        processes = self.monitor.get_running_processes()
        self.after(0, self._display_processes, processes)

    def _display_processes(self, processes):
        for widget in self.process_container.winfo_children():
            widget.destroy()

        for proc in processes:
            proc_frame = ctk.CTkFrame(self.process_container, fg_color="#1a1a1a", corner_radius=8)
            proc_frame.pack(fill="x", pady=8)

            checkbox = ctk.CTkCheckBox(
                proc_frame,
                text="",
                command=lambda pid=proc['pid']: self.toggle_selection(pid)
            )
            checkbox.pack(side="left", padx=10, pady=10)

            info_frame = ctk.CTkFrame(proc_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True, padx=10, pady=10)

            name = ctk.CTkLabel(
                info_frame,
                text=proc['name'],
                font=("Arial", 12, "bold"),
                text_color="#ffffff"
            )
            name.pack(anchor="w")

            memory = ctk.CTkLabel(
                info_frame,
                text=f"PID: {proc['pid']} | Memory: {proc['memory_mb']:.1f}MB ({proc['memory_percent']:.1f}%)",
                font=("Arial", 10),
                text_color="#888888"
            )
            memory.pack(anchor="w")

        self.status_label.configure(text=f"{len(processes)} processus actifs")

    def toggle_selection(self, pid):
        if pid in self.selected_pids:
            self.selected_pids.remove(pid)
        else:
            self.selected_pids.add(pid)

    def kill_selected(self):
        if not self.selected_pids:
            self.status_label.configure(text="Sélectionnez au moins un processus", text_color="#ff3333")
            return

        self.status_label.configure(text="Arrêt en cours...")
        threading.Thread(target=self._kill, daemon=True).start()

    def _kill(self):
        killed = 0
        for pid in self.selected_pids:
            if self.monitor.kill_process(pid):
                killed += 1

        self.after(0, self.status_label.configure, {"text": f"{killed} processus arrêtés", "text_color": "#00d9ff"})
        self.after(1000, self.load_processes)
