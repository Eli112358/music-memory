from music_memory.playlist import Playlist, Tracks


class Loader:

    def __init__(self):
        self.config = dict()
        self.loaded = False
        self.tracks: Tracks = list()

    def load(self, config: dict):
        self.config = config
        playlist = Playlist(self.config['playlist'])
        playlist.load()
        self.tracks = playlist.tracks.copy()
        self.loaded = True
        self.__post_load__()

    def __post_load__(self):
        pass
