from tkinter import filedialog, Tk
from os import environ


class Filedialog:
    def __init__(self):
        self.file = None
        self.root = Tk()
        # embedding window ids
        # this is important to link both tkinter and pygame to the same window and prevent crashes
        environ['SDL_WINDOWID'] = str(self.root.winfo_id())
        # hiding window
        self.root.withdraw()

    def launch(self) -> str:
        # asking for file
        self.file = filedialog.askopenfile().name
        return self.file
