import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import threading
import youtube_dl
import os

class Downloader:
    def __init__(self, url, resolution, format, bitrate, output_path, progress_var, status_label):
        self.url = url
        self.resolution = resolution
        self.format = format
        self.bitrate = bitrate
        self.output_path = output_path
        self.progress_var = progress_var
        self.status_label = status_label

    def download(self):
        try:
            if self.format == "Video":
                ydl_opts = {
                    'format': 'bestvideo+bestaudio/best[height<={}]'.format(self.resolution),
                    'outtmpl': os.path.join(self.output_path, 'video.mp4'),
                    'progress_hooks': [self.progress_hook],
                }
            else:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': os.path.join(self.output_path, 'audio.%(ext)s'),
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': self.bitrate,
                    }],
                    'progress_hooks': [self.progress_hook],
                }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])

            self.status_label.config(text="Download completed!")
        except Exception as e:
            self.status_label.config(text=f"Error during download: {e}")

    def progress_hook(self, d):
        if d['status'] == 'finished':
            self.progress_var.set(100)
        elif d['status'] == 'downloading':
            self.progress_var.set(d['_percent_str'])

def choose_output_path():
    chosen_path = filedialog.askdirectory()
    if chosen_path:
        output_path_var.set(chosen_path)

def open_download_folder():
    os.startfile(output_path_var.get())

def download():
    url = url_entry.get()
    resolution = res_var.get()
    format = format_var.get()
    bitrate = bitrate_var.get()
    output_path = output_path_var.get()

    progress_var.set(0)
    status_label.config(text="Downloading...")

    downloader = Downloader(url, resolution, format, bitrate, output_path, progress_var, status_label)
    download_thread = threading.Thread(target=downloader.download)
    download_thread.start()

root = tk.Tk()
root.title("YouTube Downloader")

input_frame = ttk.LabelFrame(root, text="Input", padding=(10, 5))
input_frame.pack(padx=10, pady=10, fill="both")

url_label = ttk.Label(input_frame, text="YouTube URL:")
url_label.grid(row=0, column=0, sticky="W", padx=5, pady=5)
url_entry = ttk.Entry(input_frame, width=40)
url_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

res_label = ttk.Label(input_frame, text="Resolution:")
res_label.grid(row=1, column=0, sticky="W", padx=5, pady=5)
res_var = tk.StringVar(root)
res_var.set("720")
res_menu = ttk.Combobox(input_frame, textvariable=res_var, values=["240", "360", "480", "720", "1080"])
res_menu.grid(row=1, column=1, padx=5, pady=5)

bitrate_label = ttk.Label(input_frame, text="Bitrate:")
bitrate_label.grid(row=2, column=0, sticky="W", padx=5, pady=5)
bitrate_var = tk.StringVar(root)
bitrate_var.set("128")
bitrate_menu = ttk.Combobox(input_frame, textvariable=bitrate_var, values=["64", "128", "192", "256", "320"])
bitrate_menu.grid(row=2, column=1, padx=5, pady=5)

format_label = ttk.Label(input_frame, text="Format:")
format_label.grid(row=3, column=0, sticky="W", padx=5, pady=5)
format_var = tk.StringVar(root)
format_var.set("Video")
format_menu = ttk.Combobox(input_frame, textvariable=format_var, values=["Video", "Audio"])
format_menu.grid(row=3, column=1, padx=5, pady=5)

output_frame = ttk.LabelFrame(root, text="Output", padding=(10, 5))
output_frame.pack(padx=10, pady=10, fill="both")

output_path_var = tk.StringVar(root, os.getcwd())
output_label = ttk.Label(output_frame, text="Output Path:")
output_label.grid(row=0, column=0, sticky="W", padx=5, pady=5)
output_entry = ttk.Entry(output_frame, textvariable=output_path_var, width=30)
output_entry.grid(row=0, column=1, padx=5, pady=5)
output_button = ttk.Button(output_frame, text="Choose", command=choose_output_path)
output_button.grid(row=0, column=2, padx=5, pady=5)

download_frame = ttk.LabelFrame(root, padding=(10, 5))
download_frame.pack(padx=10, pady=10, fill="both")

download_button = ttk.Button(download_frame, text="Download", command=download)
download_button.grid(row=0, column=0, padx=5, pady=5)

progress_var = tk.StringVar(root)
progress_bar = ttk.Progressbar(download_frame, orient="horizontal", length=250, mode="determinate", variable=progress_var)
progress_bar.grid(row=0, column=1, padx=5, pady=5)

status_label = ttk.Label(download_frame, text="")
status_label.grid(row=1, column=0, columnspan=2, pady=5)

open_folder_button = ttk.Button(root, text="Open Download Folder", command=open_download_folder)
open_folder_button.pack(pady=10)

root.mainloop()
