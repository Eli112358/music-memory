from __future__ import annotations

from io import StringIO
from logging import INFO, basicConfig
from os import PathLike

from eyed3.mp3 import Mp3AudioFile

EXCLUDE = [
    '??',
]
Tracks = list[Mp3AudioFile]


class Playlist:
    lines: list[str]
    tracks: Tracks

    def __init__(self, path: str | PathLike[str]):
        self.path = path
        self.lines = []
        self.tracks = []
        self.log_stream = StringIO()
        basicConfig(stream=self.log_stream, level=INFO)

    def __len__(self):
        return len(self.lines)

    def load(self):
        with open(self.path) as file:
            self.lines = [
                line
                for line in file.read().split('\n')
                if not any(e in line for e in EXCLUDE)
            ]
        if self.lines[-1] == '':
            self.lines.pop(-1)
        self.tracks = [Mp3AudioFile(path) for path in self.lines]
        log = self.log_stream.getvalue()
        if log:
            self.log_stream.truncate(0)
