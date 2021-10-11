import tkinter as tk

class Scrollbar_Example:
    def CurSelet(self, evt):
        value=str((self.listbox.get(self.listbox.curselection())))
        print(value)

    def __init__(self):
        self.window = tk.Tk()

        self.scrollbar = tk.Scrollbar(self.window)
        self.scrollbar.pack(side="right", fill="y")

        self.listbox = tk.Listbox(self.window, yscrollcommand=self.scrollbar.set)
        self.listbox.bind('<<ListboxSelect>>',self.CurSelet)
        for i in range(100):
            self.listbox.insert("end", str(i))
        self.listbox.pack(side="left", fill="both")

        self.scrollbar.config(command=self.listbox.yview)

        self.window.mainloop()

if __name__ == '__main__':
    app = Scrollbar_Example()