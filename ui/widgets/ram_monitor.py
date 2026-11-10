import customtkinter as ctk
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import collections
from config.settings import settings

class RAMMonitor(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.running = True
        self.history_size = 60
        self.data = collections.deque([0] * self.history_size, maxlen=self.history_size)
        self.current_style = settings.get("chart_style", "curve")
        
        # Determine background colors based on system theme or fallback
        # Ideally we want transparent or matching the parent. "transparent" is best for monitors usually.
        # But matplotlib needs a concrete color.
        self.bg_color = kwargs.get("fg_color", "#0f0f0f") # fallback
        if isinstance(self.bg_color, tuple):
             # Just pick one for now or handle complexity. Matplotlib doesn't support dual themes easily dynamically without redraw.
             # We will handle colors in update mostly.
             pass

        self.setup_ui()
        self.start_monitoring()

    def setup_ui(self):
        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=10, pady=5)
        
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="📊 Utilisation RAM",
            font=("Arial", 16, "bold"),
            text_color="#00d9ff"
        )
        self.title_label.pack(side="left")

        self.percent_label = ctk.CTkLabel(
            self.header_frame,
            text="0%",
            font=("Arial", 16, "bold"),
            text_color="#00d9ff"
        )
        self.percent_label.pack(side="right")

        self.setup_chart()

    def setup_chart(self):
        # Clean up existing canvas if any
        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().destroy()
            plt.close(self.fig)

        # Style & Colors
        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(figsize=(5, 3), dpi=100)
        
        # We need to detect actual display mode often, but matplotlib 'dark_background' is good for dark mode.
        # For light mode we might want 'default'. 
        
        mode = ctk.get_appearance_mode()
        if mode == "Light":
             bg_color = "#ffffff"
             plot_bg = "#f0f0f0"
             text_color = "black"
             plt.style.use('default')
        else:
             bg_color = "#1a1a1a" # Matching frame bg
             plot_bg = "#0f0f0f"
             text_color = "white"
             plt.style.use('dark_background')

        self.fig.patch.set_facecolor(bg_color)
        self.ax.set_facecolor(plot_bg)
        
        if self.current_style == "curve":
            self.setup_curve(text_color)
        else:
            self.setup_circle(text_color)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)

    def setup_curve(self, text_color):
        self.line, = self.ax.plot(range(self.history_size), self.data, color='#00d9ff')
        self.ax.set_ylim(0, 100)
        self.ax.set_xlim(0, self.history_size - 1)
        self.ax.grid(True, color='#333333', linestyle='--', alpha=0.5)
        self.ax.tick_params(colors='#888888', labelsize=8)
        # Hide standard spines
        for spine in self.ax.spines.values():
            spine.set_edgecolor('#333333')

    def setup_circle(self, text_color):
        self.ax.clear()
        self.ax.axis('equal')
        # We will draw it in update
        pass

    def update_stats(self):
        if not self.running:
            return
            
        try:
            # Check for style change
            new_style = settings.get("chart_style", "curve")
            current_mode = ctk.get_appearance_mode()
            
            # Simple check for mode change might be needed too, but checking every second is okay
            # For now I rely on update_stats to refresh data. 
            # If style changed, rebuild.
            if new_style != self.current_style:
                self.current_style = new_style
                self.setup_chart()
                
            # Get Data
            percent = psutil.virtual_memory().percent
            self.data.append(percent)
            
            # Update Label
            self.percent_label.configure(text=f"{percent}%")
            
            if self.current_style == "curve":
                self.update_curve(percent)
            else:
                self.update_circle(percent)

            self.canvas.draw_idle()
            
            self.after(1000, self.update_stats)
        except Exception as e:
            print(f"RAM Monitor Update Error: {e}")
            self.running = False

    def update_curve(self, percent):
        self.line.set_ydata(self.data)
        if percent > 80:
            self.line.set_color('#ff3333')
            self.percent_label.configure(text_color="#ff3333")
        else:
            self.line.set_color('#00d9ff')
            self.percent_label.configure(text_color="#00d9ff")

    def update_circle(self, percent):
        self.ax.clear()
        
        # Colors: Green(unused), Red(used)
        # Unused = 100 - percent
        sizes = [percent, 100 - percent]
        colors = ['#ff3333', '#00ff00'] # Red used, Green unused
        
        wedges, texts = self.ax.pie(
            sizes, 
            colors=colors, 
            startangle=90, 
            counterclock=False,
            wedgeprops=dict(width=0.3) # Donut style looks better usually, but circle was asked. 
            # "sous forme de cercle... au centre du cercle on va avoir le poucentage"
            # Donut is essentially what fits best for "center text".
        )
        
        # Add text in center
        # Since ax.clear removes text, we add it again
        mode = ctk.get_appearance_mode()
        text_color = "white" if mode == "Dark" else "black"
        
        self.ax.text(0, 0, f"{percent}%", ha='center', va='center', fontsize=12, fontweight='bold', color=text_color)

    def start_monitoring(self):
        self.running = True
        self.update_stats()

    def stop_monitoring(self):
        self.running = False

    def destroy(self):
        self.stop_monitoring()
        plt.close(self.fig)
        super().destroy()
