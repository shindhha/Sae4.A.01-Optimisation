import tkinter as tk
from tkinter import filedialog

class TextEditor:
    def __init__(self, master,menubar):
        self.master = master

        # Créer un widget de texte
        self.text = tk.Text(self.master, undo=True)
        self.text.pack(fill=tk.BOTH, expand=True)
        # Créer un menu Fichier
        file_menu = tk.Menu(menubar)
        menubar.add_cascade(label="Fichier", menu=file_menu)
        file_menu.add_command(label="Nouveau", command=self.new_file)
        file_menu.add_command(label="Ouvrir", command=self.open_file)
        file_menu.add_command(label="Enregistrer", command=self.save_file)

        # Ajouter une barre d'état
        self.statusbar = tk.Label(self.master, text="Prêt", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

    def new_file(self):
        self.text.delete("1.0", tk.END)

    def open_file(self):
        file = filedialog.askopenfile(mode="r")
        if file is not None:
            content = file.read()
            self.text.insert(tk.END, content)
            file.close()

    def save_file(self):
        file = filedialog.asksaveasfile(mode="w")
        if file is not None:
            content = self.text.get("1.0", tk.END)
            file.write(content)
            file.close()
            self.statusbar.config(text="Fichier enregistré")
