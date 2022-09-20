import tkinter as tk
import pandas as pd
import random
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

# ------------------------ Read From CSV -------------------------------- #
try:  # Check if exists a words_to_learn file
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:  # If not, then use the base data file (french_words.csv)
    original_data = pd.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:  # Ran without exceptions, our to_learn dict uses the words_to_learn file
    to_learn = data.to_dict(orient="records")


# -------------------------- Next Card ---------------------------------- #
def next_card():
    global current_card, flip_timer
    screen.after_cancel(flip_timer)  # Cancel the flip timer to restart on every new card

    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)

    flip_timer = screen.after(3000, func=flip_card)  # We start again the flip timer on every new card


# -------------------------- Flip Card ---------------------------------- #
def flip_card():
    canvas.itemconfig(card_background, image=card_back_img)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")


# --------------------------- Known Card ---------------------------------- #
def is_known():
    to_learn.remove(current_card)
    df = pd.DataFrame(to_learn)
    df.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# ---------------------------- UI --------------------------------------- #
screen = tk.Tk()
screen.title("Flashy")
screen.config(pady=50, padx=50, background=BACKGROUND_COLOR)

flip_timer = screen.after(3000, func=flip_card)

canvas = tk.Canvas(width=800, height=526)
card_front_img = tk.PhotoImage(file="images/card_front.png")
card_back_img = tk.PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
canvas.config(highlightthickness=0, background=BACKGROUND_COLOR)
canvas.grid(row=0, column=0, columnspan=2)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

right_image = tk.PhotoImage(file="images/right.png")
known_button = tk.Button(image=right_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

wrong_image = tk.PhotoImage(file="images/wrong.png")
unknown_button = tk.Button(image=wrong_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

next_card()

screen.mainloop()
