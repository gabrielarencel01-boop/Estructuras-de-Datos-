import tkinter as tk
from interfaz_grafica import EditorGrafosGUI

def main():
    root = tk.Tk()
    app = EditorGrafosGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()