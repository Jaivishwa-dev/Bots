import customtkinter as ctk
import psutil
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import numpy as np
import threading
import random

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def format_size(bytes):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024
    return f"{bytes:.2f} TB"


def get_network_usage():
    net_io = psutil.net_io_counters()
    return net_io.bytes_sent, net_io.bytes_recv


class SpeedMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Internet Speed Monitor")
        self.root.geometry("900x550")

        self.frame = ctk.CTkFrame(root, corner_radius=20, fg_color="#1a1d29")
        self.frame.pack(pady=20, padx=20, fill='both', expand=True)

        self.title_label = ctk.CTkLabel(self.frame, text="Internet Speed Monitor", font=("Helvetica", 24, "bold"))
        self.title_label.pack(pady=15)

        self.download_label = ctk.CTkLabel(self.frame, text="⬇ Download: 0.00 MB/s", font=("Helvetica", 18),
                                           text_color="lime")
        self.download_label.pack(pady=5)

        self.upload_label = ctk.CTkLabel(self.frame, text="⬆ Upload: 0.00 MB/s", font=("Helvetica", 18),
                                         text_color="cyan")
        self.upload_label.pack(pady=5)

        self.data_usage_label = ctk.CTkLabel(self.frame, text="📊 Data Used: 0.00 MB", font=("Helvetica", 16, "bold"),
                                             text_color="orange")
        self.data_usage_label.pack(pady=10)

        self.fig, self.ax = plt.subplots(figsize=(6, 3))
        self.ax.set_facecolor("#1a1d29")
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.ax.tick_params(colors='white')

        self.download_speeds = [0] * 30
        self.upload_speeds = [0] * 30
        self.time_intervals = np.linspace(-29, 0, 30)

        self.line1, = self.ax.plot(self.time_intervals, self.download_speeds, label='Download', color='lime',
                                   linewidth=2, animated=True)
        self.line2, = self.ax.plot(self.time_intervals, self.upload_speeds, label='Upload', color='cyan', linewidth=2,
                                   animated=True)
        self.ax.legend(facecolor="#1a1d29", edgecolor="white", fontsize=10)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(pady=10, padx=10, fill='both', expand=True)

        self.total_data_used = 0
        self.ani = animation.FuncAnimation(self.fig, self.animate_graph, interval=1000, blit=True)

        self.start_monitoring()

    def update_speed(self):
        initial_sent, initial_recv = get_network_usage()
        time.sleep(1)
        current_sent, current_recv = get_network_usage()

        download_speed = current_recv - initial_recv
        upload_speed = current_sent - initial_sent

        self.download_label.configure(text=f"⬇ Download: {format_size(download_speed)}/s")
        self.upload_label.configure(text=f"⬆ Upload: {format_size(upload_speed)}/s")

        data_used = (download_speed + upload_speed) / (1024 * 1024)
        self.total_data_used += data_used
        self.data_usage_label.configure(text=f"📊 Data Used: {format_size(self.total_data_used * 1024 * 1024)}")

        self.download_speeds.pop(0)
        self.download_speeds.append(download_speed / (1024 * 1024))
        self.upload_speeds.pop(0)
        self.upload_speeds.append(upload_speed / (1024 * 1024))

        self.root.after(1000, self.update_speed)

    def animate_graph(self, i):
        self.line1.set_ydata(self.download_speeds)
        self.line2.set_ydata(self.upload_speeds)
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()
        return self.line1, self.line2

    def start_monitoring(self):
        threading.Thread(target=self.update_speed, daemon=True).start()


if __name__ == "__main__":
    root = ctk.CTk()
    app = SpeedMonitorApp(root)
    root.mainloop()
