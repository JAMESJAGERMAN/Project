import requests
import spacy
import random
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from tkinter import Tk, Canvas, Entry, scrolledtext, PhotoImage, messagebox, font

# ... (keep all the existing functions)

# This part is modified to match the new GUI layout
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Rakaputu Banardi A\Documents\AI class\AI Project\GUI\build\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()
window.geometry("1282x740")
window.configure(bg = "#FFFFFF")

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 740,
    width = 1282,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)

canvas.create_text(
    53.0,
    55.0,
    anchor="nw",
    text="AI-Powered Recipe",
    fill="#000000",
    font=("BonaNova Regular", 30 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    640.5,
    136.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFF3DB",
    fg="#000716",
    highlightthickness=0,
    font=("Bonheur Royale", 16)
)
entry_1.place(
    x=202.0,
    y=104.0,
    width=877.0,
    height=62.0
)

entry_1.bind("<Return>", search_recipe)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    1064.0,
    605.9999625682831,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    105.00000911821735,
    632.5798950195312,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    131.0,
    643.5835206052861,
    image=image_image_3
)

canvas.create_text(
    176.0,
    188.0,
    anchor="nw",
    text="Text View",
    fill="#000000",
    font=("BonheurRoyale Regular", 30 * -1)
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    1176.0,
    107.0,
    image=image_image_4
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    104.0,
    103.0,
    image=image_image_5
)

canvas.create_text(
    158.0,
    607.0,
    anchor="nw",
    text="When everything you want is in your hands",
    fill="#000000",
    font=("BonheurRoyale Regular", 48 * -1)
)

results_text = scrolledtext.ScrolledText(window, width=80, height=20, wrap="word", font=("Bonheur Royale", 14))
results_text.place(x=202.0, y=230.0, width=877.0, height=350.0)

window.resizable(False, False)
window.mainloop()