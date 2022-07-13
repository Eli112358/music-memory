from random import choice
from typing import Optional

from eyed3.mp3 import Mp3AudioFile
from pygame import mixer

from music_memory.loader import Loader


class Player(Loader):
    track: Optional[Mp3AudioFile]

    def __init__(self):
        Loader.__init__(self)
        mixer.init()
        self.music = mixer.music
        self.paused = False
        self.playing = False
        self.track = None

    def play(self):
        if not self.loaded:
            return
        self.track = choice(self.tracks)
        self.music.load(self.track.path)
        self.music.play()
        self.playing = True

    def toggle_paused(self):
        if not self.playing:
            return
        if self.music.get_busy():
            self.music.pause()
        else:
            self.music.unpause()

    def stop(self):
        self.music.stop()
        self.playing = False

    def next_track(self):
        if not self.loaded:
            return
        self.music.fadeout(1000)
        if 'elimination' in self.config:
            if self.config['elimination']:
                self.tracks.remove(self.track)
        self.play()
