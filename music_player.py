import os
import tkinter as tk
from tkinter import filedialog, Menu, Listbox, Frame, Button, PhotoImage, END, messagebox
from pygame import mixer


class MusicPlayer:
    def __init__(self):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("500x300")

        mixer.init()

        self.songs = []
        self.current_song = ""
        self.paused = False
        self.current_track_index = 0

        # Menu bar
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        organise_menu = Menu(menubar, tearoff=False)
        organise_menu.add_command(label='Select Folder', command=self.load_music)
        menubar.add_cascade(label='Organise', menu=organise_menu)

        # Song list
        self.songlist = Listbox(self.root, bg="black", fg="white", width="100", height="15")
        self.songlist.pack()

        # Load control button images with absolute paths
        image_folder = 'C:/Users/Hamza Waheed/music player/'  # Replace with your actual image folder path
        try:
            self.play_btn_image = PhotoImage(file=os.path.join(image_folder, 'play.png'))
            self.pause_btn_image = PhotoImage(file=os.path.join(image_folder, 'pause.png'))
            self.next_btn_image = PhotoImage(file=os.path.join(image_folder, 'next.png'))
            self.previous_btn_image = PhotoImage(file=os.path.join(image_folder, 'previous.png'))
            # self.stop_btn_image = PhotoImage(file=os.path.join(image_folder, 'stop.png'))  # Added stop button image
        except tk.TclError as e:
            messagebox.showerror("Image Error", f"Error loading image files: {e}")
            self.root.destroy()
            return

        # Control frame
        control_frame = Frame(self.root)
        control_frame.pack()

        # Control buttons
        self.previous_btn = Button(control_frame, image=self.previous_btn_image, borderwidth=0, command=self.prev_track)
        self.play_btn = Button(control_frame, image=self.play_btn_image, borderwidth=0, command=self.play_music)
        self.pause_btn = Button(control_frame, image=self.pause_btn_image, borderwidth=0, command=self.pause_music)
        self.next_btn = Button(control_frame, image=self.next_btn_image, borderwidth=0, command=self.next_track)
        # self.stop_btn = Button(control_frame, image=self.stop_btn_image, borderwidth=0, command=self.stop_music,
        #                        width=50, height=50)  # Set width and height

        # Grid placement for control buttons
        self.previous_btn.grid(row=0, column=0, padx=7, pady=10)
        self.play_btn.grid(row=0, column=1, padx=7, pady=10)
        self.pause_btn.grid(row=0, column=2, padx=7, pady=10)
        # self.stop_btn.grid(row=0, column=3, padx=7, pady=10)
        self.next_btn.grid(row=0, column=4, padx=7, pady=10)

    def load_music(self):
        self.root.directory = filedialog.askdirectory()
        if self.root.directory:
            for song in os.listdir(self.root.directory):
                name, ext = os.path.splitext(song)
                if ext == '.mp3':
                    self.songs.append(song)

            for song in self.songs:
                self.songlist.insert("end", song)
            self.songlist.selection_set(0)
            self.current_song = self.songs[self.songlist.curselection()[0]]

    def play_music(self):
        if self.current_song:
            mixer.music.load(os.path.join(self.root.directory, self.current_song))
            mixer.music.play()
        elif self.songs:
            self.current_song = self.songs[0]
            self.play_music()

    def pause_music(self):
        if mixer.music.get_busy():
            mixer.music.pause()
            self.paused = True

    def stop_music(self):
        if mixer.music.get_busy():
            mixer.music.stop()
            self.current_song = ""
            self.paused = False

    def next_track(self):
        if self.songs:
            self.songlist.selection_clear(0, END)
            self.current_track_index = (self.current_track_index + 1) % len(self.songs)
            self.songlist.selection_set(self.current_track_index)
            self.current_song = self.songs[self.songlist.curselection()[0]]
            self.play_music()

    def prev_track(self):
        if self.songs:
            self.songlist.selection_clear(0, END)
            self.current_track_index = (self.current_track_index - 1) % len(self.songs)
            self.songlist.selection_set(self.current_track_index)
            self.current_song = self.songs[self.songlist.curselection()[0]]
            self.play_music()


if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer()
    root.mainloop()
