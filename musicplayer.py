import tkinter as tk
from tkinter import filedialog
import pygame
from threading import Thread
import time
import os

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Playlist")
        self.root.geometry("400x400")

        self.playlist = []
        self.current_song_index = 0
        self.is_playing = False
        self.is_paused = False

        pygame.mixer.init()

        self.create_widgets()
        self.load_songs_from_directory(r'C:\Users\V I C T U S\Desktop\test\music')

    def create_widgets(self):
        self.playlist_box = tk.Listbox(self.root, bg="black", fg="white", width=50, height=15)
        self.playlist_box.pack(pady=20)

        controls_frame = tk.Frame(self.root)
        controls_frame.pack()

        self.play_button = tk.Button(controls_frame, text="Play", command=self.play_music)
        self.play_button.grid(row=0, column=0, padx=10)

        self.pause_button = tk.Button(controls_frame, text="Pause", command=self.pause_music)
        self.pause_button.grid(row=0, column=1, padx=10)

        self.stop_button = tk.Button(controls_frame, text="Stop", command=self.stop_music)
        self.stop_button.grid(row=0, column=2, padx=10)

        self.next_button = tk.Button(controls_frame, text="Next", command=self.next_music)
        self.next_button.grid(row=0, column=3, padx=10)

        self.prev_button = tk.Button(controls_frame, text="Previous", command=self.previous_music)
        self.prev_button.grid(row=0, column=4, padx=10)

        self.add_button = tk.Button(self.root, text="Add Songs", command=self.add_songs)
        self.add_button.pack(pady=20)

        self.progress = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, length=360)
        self.progress.pack(pady=20)

       # Volume control slider
        self.volume_slider = tk.Scale(self.root, from_=0, to=1, orient=tk.HORIZONTAL, resolution=0.01, label="Volume")
        self.volume_slider.set(0.5)  # Set default volume to 50%
        self.volume_slider.pack(pady=20)
        self.volume_slider.bind("<Motion>", self.change_volume)

    def change_volume(self, event=None):
        volume = self.volume_slider.get()
        pygame.mixer.music.set_volume(volume)


    def load_songs_from_directory(self, directory):
        for file in os.listdir(directory):
            if file.endswith(".mp3"):
                full_path = os.path.join(directory, file)
                self.playlist.append(full_path)
                self.playlist_box.insert(tk.END, file)

    def add_songs(self):
        songs = filedialog.askopenfilenames(initialdir="music/", title="Choose A Song",
                                            filetypes=(("mp3 Files", "*.mp3"),))
        for song in songs:
            self.playlist.append(song)
            self.playlist_box.insert(tk.END, song.split("/")[-1])

    def play_music(self):
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
        else:
            if not self.is_playing:
                self.load_and_play_song()
            else:
                self.stop_music()
                self.load_and_play_song()

    def load_and_play_song(self):
        song = self.playlist[self.current_song_index]
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        self.is_playing = True
        self.is_paused = False
        Thread(target=self.update_progress_bar).start()

    def update_progress_bar(self):
        total_length = pygame.mixer.Sound(self.playlist[self.current_song_index]).get_length()
        while pygame.mixer.music.get_busy() or self.is_paused:
            if not self.is_paused:
                current_pos = pygame.mixer.music.get_pos() / 1000
                progress_percentage = (current_pos / total_length) * 100
                self.progress.set(progress_percentage)
            time.sleep(0.5)
        self.next_music()

    def pause_music(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_paused = True

    def stop_music(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        self.progress.set(0)

    def next_music(self):
        self.stop_music()
        self.current_song_index += 1
        if self.current_song_index >= len(self.playlist):
            self.current_song_index = 0
        self.load_and_play_song()

    def previous_music(self):
        self.stop_music()
        self.current_song_index -= 1
        if self.current_song_index < 0:
            self.current_song_index = len(self.playlist) - 1
        self.load_and_play_song()

    def volume(self, value):
        pygame.mixer.music.set_volume(float(value))

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()