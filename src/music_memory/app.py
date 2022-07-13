from tkinter import Tk, StringVar, Menu, filedialog
from tkinter.font import Font
from tkinter.ttk import Button, Entry, Treeview, Scrollbar, Frame

from music_memory.loader import Loader
from music_memory.player import Player

WIN_TITLE = 'Music Memory'
DELETE_WINDOW = 'WM_DELETE_WINDOW'
HEADER = [
    'title',
    'artist',
    'album',
]


class NamedDict(dict):

    def __init__(self):
        super().__init__()

    def __getattr__(self, item):
        return self.get(item)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)


class Application(Tk, Loader):

    def __init__(self):
        Tk.__init__(self)
        Loader.__init__(self)
        self.title(WIN_TITLE)
        self.geometry('350x300')
        self.protocol(DELETE_WINDOW, self.closing)
        self.player = Player()
        self.__init_ui__()

    def __init_ui__(self):
        # menu
        self.menus = NamedDict()
        self.menus.main = Menu(self, tearoff=False)
        self.configure(menu=self.menus.main)
        self.menus.file = Menu(self.menus.main, tearoff=False)
        self.menus.load = Menu(self.menus.file, tearoff=False)
        self.menus.main.add_cascade(label='File', menu=self.menus.file)
        self.menus.file.add_cascade(label='Load', menu=self.menus.load)
        self.menus.load.add_command(label='Playlist', command=self.load_playlist)

        # player
        self.player_frame = Frame(self)
        self.buttons = dict()
        self.buttons['play'] = Button(self.player_frame, text='Play', command=self.player.play)
        self.buttons['pause'] = Button(self.player_frame, text='Pause', command=self.player.toggle_paused)
        self.buttons['next'] = Button(self.player_frame, text='Next', command=self.player.next_track)
        self.buttons['stop'] = Button(self.player_frame, text='Stop', command=self.player.stop)
        for i, (_, button) in enumerate(self.buttons.items()):
            button: Button
            button.grid(row=0, column=i)
        self.player_frame.grid(row=0, column=0)

        # library searching
        self.search_frame = Frame(self)
        self.query = StringVar(self)
        run_search = self.register(self.search)
        self.search_box = Entry(
            self.search_frame,
            textvariable=self.query,
            width=50,
            validate='key',
            validatecommand=(run_search, '%P'),
        )
        self.search_box.grid(column=0, row=1, columnspan=2)
        self.track_listing = Treeview(self.search_frame, columns=HEADER, show='headings')
        vsb = Scrollbar(self.search_frame, orient='vertical', command=self.track_listing.yview)
        hsb = Scrollbar(self.search_frame, orient='horizontal', command=self.track_listing.xview)
        self.track_listing.configure(
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )
        self.track_listing.grid(row=2, column=0, sticky='nsew')
        vsb.grid(row=2, column=1, sticky='ns')
        hsb.grid(row=3, column=0, sticky='ew')
        self.search_frame.grid(row=1, column=0)
        for col in HEADER:
            self.track_listing.heading(col, text=col.title(), command=lambda c=col: self.sort_by(c, False))
            self.track_listing.column(col, width=Font().measure(col.title()))
        self.search_frame.grid_columnconfigure(0, weight=1)
        self.search_frame.grid_rowconfigure(0, weight=1)

    def __post_load__(self):
        self.player.tracks = self.tracks
        self.player.loaded = True
        self.update_track_listing()

    def closing(self):
        self.player.stop()
        self.destroy()

    def search(self, query):
        print(query)
        self.update_track_listing()
        return True

    def sort_by(self, col: int, descending: bool):
        """sort tree contents when a column header is clicked on"""
        data = [(self.track_listing.set(child, col), child) for child in self.track_listing.get_children('')]
        data.sort(reverse=descending)
        for ix, item in enumerate(data):
            self.track_listing.move(item[1], '', ix)
        self.track_listing.heading(col, command=lambda c=col: self.sort_by(c, not descending))

    def load_playlist(self):
        file_types = (
            ('playlist files', '*.m3u *.m3u8'),
            ('All files', '*.*')
        )
        path = filedialog.askopenfilename(
            title='Load a playlist',
            initialdir='/',
            filetypes=file_types
        )
        self.load({'playlist': path})

    def update_track_listing(self):
        self.track_listing.delete(*self.track_listing.get_children())
        for track in self.tracks:
            if not track.tag:
                continue
            self.track_listing.insert('', 'end', values=[
                track.tag.title,
                track.tag.artist,
                track.tag.album
            ])
            for ix, val in enumerate([track]):
                col_w = Font().measure(val.tag.title)
                if self.track_listing.column(HEADER[ix], width=None) < col_w:
                    self.track_listing.column(HEADER[ix], width=col_w)
        self.track_listing.grid()


def main():
    app = Application()
    app.mainloop()


if __name__ == '__main__':
    main()
