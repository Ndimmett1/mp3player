import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
from tkinter import ttk
import os
import sys
import subprocess

playlist = []
current_index = 0

current_process = None

def add_songs():
    files = filedialog.askopenfilenames(
        title="Select MP3 Files",
        filetypes=[("MP3 Files", "*.mp3")]
    )

    if not files:
        return

    for file in files:
        playlist.append(file)
        playlist_box.insert(tk.END, os.path.basename(file))


def remove_song():
    try:
        index = playlist_box.curselection()[0]
        playlist_box.delete(index)
        playlist.pop(index)
    except IndexError:
        messagebox.showerror("Error", "No song selected to remove.")


def clear_playlist():
    playlist_box.delete(0, tk.END)
    playlist.clear()


def open_with_default_player(path):
    global current_process

    if current_process and current_process.poll() is None:
        try:
            current_process.terminate()
        except Exception:
            pass

    if sys.platform.startswith("win"):
        os.startfile(path)
        current_process = None 
    elif sys.platform == "darwin":
        current_process = subprocess.Popen(["open", path])
    else:
        current_process = subprocess.Popen(["xdg-open", path])


def play_song():
    global current_index

    try:
        index = playlist_box.curselection()[0]
        current_index = index
    except IndexError:
        messagebox.showerror("Error", "Please select a song to play.")
        return

    song_path = playlist[current_index]
    open_with_default_player(song_path)
    update_labels(os.path.basename(song_path), "Playing (external player)")

def pause_song():
    update_labels(None, "Pause requested (not supported)")

def resume_song():
    update_labels(None, "Resume requested (not supported)")

def stop_song():
    global current_process

    if current_process and current_process.poll() is None:
        try:
            current_process.terminate()
        except Exception:
            pass

    update_labels(None, "Stopped")

def next_song():
    global current_index

    if current_index < len(playlist) - 1:
        current_index += 1
        playlist_box.select_clear(0, tk.END)
        playlist_box.select_set(current_index)
        play_song()
    else:
        messagebox.showinfo("End", "Reached end of playlist.")

def previous_song():
    global current_index

    if current_index > 0:
        current_index -= 1
        playlist_box.select_clear(0, tk.END)
        playlist_box.select_set(current_index)
        play_song()
    else:
        messagebox.showinfo("Start", "This is the first song.")

def set_volume(val):
    update_labels(None, f"Volume slider: {int(float(val))}% (no effect on external player)")

def update_labels(track, status):
    if track:
        current_track_label.config(text=f"Current Track: {track}")
    status_label.config(text=f"Status: {status}")

def open_help_window():
    help_win = Toplevel(root)
    help_win.title("Help - MP3 Maestro Player")
    help_win.geometry("400x300")

    tk.Label(help_win, text="MP3 Maestro Player - Help Guide",
             font=("Arial", 14, "bold")).pack(pady=10)

    help_text = (
        "• Add Song: Load MP3 files into the playlist.\n"
        "• Play: Opens the selected song in your system's default media player.\n"
        "• Pause/Resume: Only updates status text (cannot control external player).\n"
        "• Next/Previous: Navigate playlist and open songs.\n"
        "• Volume Slider: Cosmetic only (no effect on external player).\n"
        "• Clear Playlist: Remove all songs.\n"
        "• Exit: Close the application."
    )

    tk.Label(help_win, text=help_text, justify="left").pack(pady=10)
    tk.Button(help_win, text="Close", command=help_win.destroy).pack(pady=10)

root = tk.Tk()
root.title("MP3 Maestro Player")
root.geometry("700x500")

top_frame = tk.Frame(root)
top_frame.pack(pady=10)

current_track_label = tk.Label(top_frame, text="Current Track: None", font=("Arial", 12))
current_track_label.pack()

status_label = tk.Label(top_frame, text="Status: Stopped", font=("Arial", 12))
status_label.pack()

playlist_frame = tk.Frame(root)
playlist_frame.pack(pady=10)

playlist_box = tk.Listbox(playlist_frame, width=50, height=12)
playlist_box.pack(side=tk.LEFT)

scrollbar = tk.Scrollbar(playlist_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

playlist_box.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=playlist_box.yview)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add Song", width=12, command=add_songs).grid(row=0, column=0)
tk.Button(button_frame, text="Remove Song", width=12, command=remove_song).grid(row=0, column=1)
tk.Button(button_frame, text="Clear Playlist", width=12, command=clear_playlist).grid(row=0, column=2)

tk.Button(button_frame, text="Play", width=12, command=play_song).grid(row=1, column=0)
tk.Button(button_frame, text="Pause", width=12, command=pause_song).grid(row=1, column=1)
tk.Button(button_frame, text="Resume", width=12, command=resume_song).grid(row=1, column=2)

tk.Button(button_frame, text="Previous", width=12, command=previous_song).grid(row=2, column=0)
tk.Button(button_frame, text="Stop", width=12, command=stop_song).grid(row=2, column=1)
tk.Button(button_frame, text="Next", width=12, command=next_song).grid(row=2, column=2)

volume_slider = ttk.Scale(root, from_=0, to=100, orient="horizontal", command=set_volume)
volume_slider.set(70)
volume_slider.pack(pady=10)

bottom_frame = tk.Frame(root)
bottom_frame.pack(pady=10)

tk.Button(bottom_frame, text="Help", width=12, command=open_help_window).grid(row=0, column=0)
tk.Button(bottom_frame, text="Exit", width=12, command=root.destroy).grid(row=0, column=1)

root.mainloop()
