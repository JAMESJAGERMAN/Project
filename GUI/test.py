import tkinter as tk
from PIL import Image, ImageTk

def open_book():
    book_label.config(image=open_book_image)

def close_book():
    book_label.config(image=closed_book_image)

root = tk.Tk()
root.title("Book Open/Close Example")

# Load and resize images
closed_book_image_raw = Image.open("book1.png").resize((150, 200), Image.ANTIALIAS)
open_book_image_raw = Image.open("Book2.png").resize((150, 200), Image.ANTIALIAS)

closed_book_image = ImageTk.PhotoImage(closed_book_image_raw)
open_book_image = ImageTk.PhotoImage(open_book_image_raw)

# Create a label to display the book image
book_label = tk.Label(root, image=closed_book_image)
book_label.pack()

# Create a Text widget
text_widget = tk.Text(root, height=10, width=40)
text_widget.pack()

# Frame to hold the buttons
button_frame = tk.Frame(root)
button_frame.pack()

# Add buttons to open and close the book
open_button = tk.Button(button_frame, text="Open Book", command=open_book)
open_button.pack(side=tk.LEFT, padx=5)

close_button = tk.Button(button_frame, text="Close Book", command=close_book)
close_button.pack(side=tk.LEFT, padx=5)

root.mainloop()
