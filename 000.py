from tkinter import *
from tkinter import ttk
import os
import threading
import tkinter.messagebox
import time
import glob
from mutagen.mp3 import MP3
from pygame import mixer

mixer.init()


def format_songs(song):
    song_name = song.split("\\")[-1]
    return song_name


def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)


class Mp3Player:
    root = Tk()
    root.minsize(650, 560)
    root.title('Psarris\' Mp3 player')

    def __init__(self):
        self.master = Mp3Player.root

        self.playlist = []
        self.current = ''
        self.paused = False

        frame_ = Frame(self.master)

        self.list_main = Listbox(frame_, height=10, exportselection=False, relief=SOLID)
        self.list_scroll = ttk.Scrollbar(frame_, orient=VERTICAL, command=self.list_main.yview)
        self.list_main.config(yscrollcommand=self.list_scroll.set)
        self.list_scroll.pack(side=RIGHT, fill=Y)
        self.list_main.pack(fill=BOTH, expand=True, pady=1)

        frame_.pack(fill=BOTH, expand=True)

        frames_ = Frame(self.master, height=70)

        frame_1 = Frame(frames_, height=70)
        frame_2 = Frame(frames_, height=70)
        frame_3 = Frame(frames_, height=70)

        prev = Button(frame_2, text='Prev', command=self.prev)
        next_ = Button(frame_2, text='Next', command=self.next)

        pause = Button(frame_2, text='Pause', command=self.pause)
        play = Button(frame_2, text='Play', command=self.play)
        stop = Button(frame_2, text='Stop', command=self.stop)
        prev.pack(side=LEFT)
        next_.pack(side=RIGHT)

        pause.pack(padx=10, side=LEFT)
        play.pack(padx=10, side=LEFT)
        stop.pack(padx=10, side=RIGHT)

        self.scale = ttk.Scale(frame_3, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
        self.scale.set(70)  # implement the default value of scale when music player starts
        mixer.music.set_volume(0.7)
        self.scale.pack()

        self.name = ttk.Label(frame_1, text='title of the song', width=25, relief=SOLID)
        self.label = ttk.Label(frame_1, text='--:--')
        self.label_ = ttk.Label(frame_1, text='--:--')

        self.name.pack(side=LEFT, padx=10)
        self.label.pack(pady=20, side=LEFT)
        self.label_.pack(pady=20, padx=10, side=LEFT)

        frame_1.pack(side=LEFT)
        frame_2.pack(side=LEFT)
        frame_3.pack(side=LEFT, fill=X, expand=True)

        frames_.pack(fill=X)

        t1 = threading.Thread(target=self.get_songs)
        t1.start()

        self.master.mainloop()

    def get_songs(self):
        for file_path in glob.glob('C:\\Users\\Dr Steve\\Music\\**\\*.mp3', recursive=True):
            self.playlist.append(file_path)
            file_name = format_songs(file_path)
            self.list_main.insert(END, file_name)

    def play(self):
        try:
            x = self.list_main.curselection()
            x = self.list_main.get(x)
            for i in self.playlist:
                j = i.split("\\")[-1]
                if j == x:
                    self.name.config(text=j)
                    if self.paused:
                        mixer.music.unpause()
                        self.paused = False
                    else:
                        self.stop()
                        mixer.music.load(i)
                        mixer.music.play()
                        self.show_details(i)
        except (RuntimeError, TclError):
            pass

    def next(self):
        try:
            x = self.list_main.curselection()
            p = list(x)
            p = p[0] + 1
            if p > -1:
                self.list_main.selection_clear(0, END)
                self.list_main.selection_set(p)
                self.list_main.event_generate("<<ListboxSelect>>")
                self.play()
        except (RuntimeError, TclError):
            pass
        except IndexError:
            self.list_main.selection_set(END)

    def prev(self):
        try:
            x = self.list_main.curselection()
            p = list(x)
            p = p[0] - 1
            if p > -1:
                self.list_main.selection_clear(0, END)
                self.list_main.selection_set(p)
                self.list_main.event_generate("<<ListboxSelect>>")
                self.play()
        except (RuntimeError, TclError):
            pass
        except IndexError:
            self.list_main.selection_set(END)

    def pause(self):
        self.paused = True
        mixer.music.pause()

    def stop(self):
        mixer.music.stop()
        time.sleep(1)
        self.paused = False

    def start_count(self, t):
        current_time = 0
        while current_time <= t and mixer.music.get_busy():
            if self.paused:
                continue
            else:
                mins, secs = divmod(current_time, 60)
                mins = round(mins)
                secs = round(secs)
                time_format = '{:02d}:{:02d}'.format(mins, secs)
                self.label.config(text=time_format)
                time.sleep(1)
                current_time += 1

    def show_details(self, play_song):
        file_data = os.path.splitext(play_song)

        if file_data[1] == '.mp3':
            audio = MP3(play_song)
            total_length = audio.info.length
        else:
            a = mixer.Sound(play_song)
            total_length = a.get_length()

        mins, secs = divmod(total_length, 60)
        mins = round(mins)
        secs = round(secs)
        time_format = '{:02d}:{:02d}'.format(mins, secs)
        self.label_.config(text=time_format)

        t1 = threading.Thread(target=self.start_count, args=(total_length,))
        t1.start()


if __name__ == "__main__":
    try:
        Mp3Player()
    except Exception as e:
        tkinter.messagebox.showerror('An Error Occurred', str(e))
