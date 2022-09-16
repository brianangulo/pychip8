from tkinter import filedialog

class Filedialog:
    def __init__(self):
        self.file = None
    def launch(self) -> str:
        self.file = filedialog.askopenfile().name
        return self.file
