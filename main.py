from tkinter import *
from tkinter import messagebox
from gtts import gTTS
from playsound import playsound
from pygame import mixer
import pandas as pd
import random
import os
from os.path import isfile, join


index = 0

MAIN_FONT = ("Ariel", 11, "bold")
SECONDARY_FONT = ("Ariel", 8, "bold")
BACKGROUND_COLOR = "black"
MUSIC_FOLDER = '/home/h78sh/Desktop/python/schöne/data/music'


window = Tk()
window.config(bg=BACKGROUND_COLOR, width=1000, height=700, padx=0, pady=0)
window.title("Schöne")
background = PhotoImage(file="data/images/background.png")
next_icon = PhotoImage(file="data/images/next.png")
previous_icon = PhotoImage(file="data/images/previous.png")
background_label = Label(window, image=background)
background_label.place(x=0, y=0, relwidth=1, relheight=1)


current_card = {}
words_dict = {}

# Databases

try:
    data = pd.read_csv("data/words_to_learn.csv")

except FileNotFoundError:
    original_data = pd.read_csv("data/german_words.csv")
    words_dict = original_data.to_dict(orient="records")

else:
    words_dict = data.to_dict(orient="records")

# Functions


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    try:
        current_card = random.choice(words_dict)
        language = 'de'
        audio_german = gTTS(text=current_card["German"], lang=language)
        audio_german.save("data/sounds/german.mp3")
        playsound("data/sounds/german.mp3", True)
        os.remove("data/sounds/german.mp3")
    except IndexError:
        messagebox.showinfo(title="Cards Finished", message="You have finished all your available cards "
                                                            "and your csv file has been deleted.")
        if (os.path.exists("data/words_to_learn.csv")) and os.path.isfile("data/words_to_learn.csv"):
            os.remove("data/words_to_learn.csv")

    canvas.itemconfig(text, text=f"{current_card['German']} ", fill="black")
    canvas.itemconfig(title, text="German", fill="black")
    canvas.itemconfig(canvas_image, image=card_front)

    flip_timer = window.after(3000, func=flip_card)


def delete_saved_words():
    try:
        os.remove("data/words_to_learn.csv")
    except FileNotFoundError:
        pass


def known_to_do():
    try:
        words_dict.remove(current_card)
        new_data = pd.DataFrame(words_dict)
        new_data.to_csv("data/words_to_learn.csv", index=False)
        next_card()
    except ValueError:
        pass


def unknown_to_do():
    new_data = pd.DataFrame(words_dict)
    new_data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


def next_song():
    global index
    for _ in range(len(mp3files)):
        index += 1
        mixer.music.stop()
        mixer.music.load(f"/home/h78sh/Desktop/python/schöne/data/music/{mp3files[index]}")
        name_of_song.config(text=(mp3files[index]))
        mixer.music.play()
        if index >= 13:
            index = 0
        mixer.music.queue(f"/home/h78sh/Desktop/python/schöne/data/music/{mp3files[index + 1]}")
        name_of_song.config(text=(mp3files[index]))


def previous_song():
    global index
    for _ in range(len(mp3files)):
        index -= 1
        mixer.music.stop()
        mixer.music.load(f"/home/h78sh/Desktop/python/schöne/data/music/{mp3files[index]}")
        name_of_song.config(text=(mp3files[index]))
        mixer.music.play()
        if index <= -14:
            index = -1
        mixer.music.queue(f"/home/h78sh/Desktop/python/schöne/data/music/{mp3files[index -1]}")
        name_of_song.config(text=(mp3files[index]))


# Flip and Timmer

def flip_card():
    try:
        canvas.itemconfig(text, text=current_card["English"], fill="black")
        canvas.itemconfig(title, text="English", fill="black")
        canvas.itemconfig(canvas_image, image=card_front)
    except KeyError:
        pass


flip_timer = window.after(3000, func=flip_card)
canvas = Canvas(window, bg="black", width=750, height=510, bd=3, highlightthickness=1)
canvas.grid(row=1, column=1, columnspan=2)

# Images
card_front = PhotoImage(file="data/images/card_front.png")


# Main Canvas
canvas_image = canvas.create_image(0, 0, image=card_front, anchor="nw")
text = canvas.create_text(400, 280, text="Willkommen", font=("Ariel", 30, "bold"), tags='text')
title = canvas.create_text(400, 150, text="Schöne!", font=("Ariel", 30, "italic"), tags='title')

# Main Buttons
known_button = Button(text="Ja!, I know this one",
                      command=known_to_do,  font=MAIN_FONT,
                      fg="white", bg=BACKGROUND_COLOR, bd=0, highlightthickness=0)
known_button.grid(row=2, column=2, pady=10, padx=0)

unknown_button = Button(text="Don't know this word...",
                        command=unknown_to_do, font=MAIN_FONT,
                        fg="white", bg=BACKGROUND_COLOR, bd=0, highlightthickness=0)
unknown_button.grid(row=2, column=1, pady=10, padx=0)

next_button = Button(image=next_icon, bd=0, highlightthickness=0, text="Next", compound="top",
                     font=("Ariel", 8, "bold"), command=next_song)
next_button.grid(row=0, column=3)

previous_button = Button(image=previous_icon, bd=0, highlightthickness=0, text="Previous", compound="top",
                         font=("Ariel", 8, "bold"), command=previous_song)
previous_button.grid(row=0, column=0)

# Music


def set_vol(val):
    volume = float(val)/10
    mixer.music.set_volume(volume)

# Iterate  through music folder


mp3files = [f for f in os.listdir(MUSIC_FOLDER) if isfile(join(MUSIC_FOLDER, f))]


name_of_song = Label(text=f"{mp3files[index]}", font=MAIN_FONT, fg="white", bg=BACKGROUND_COLOR)
name_of_song.grid(row=0, column=1, columnspan=2)

# Scale Widget (Volume)
scale = Scale(window, from_=0.0, to=10.0, fg="white", bg=BACKGROUND_COLOR, orient=HORIZONTAL, resolution=0.01,
              label="  Volume", font=MAIN_FONT, command=set_vol)
scale.grid(row=2, column=3)

mixer.init()
mixer.music.load(f"/home/h78sh/Desktop/python/schöne/data/music/{mp3files[index]}")
mixer.music.set_volume(0.05)
next_song()


# Secondary Buttons
unpause = Button(text="Unpause Music", command=mixer.music.unpause, font=MAIN_FONT,
                 fg="white", bg=BACKGROUND_COLOR, bd=0, highlightthickness=0)
unpause.grid(row=1, column=0, pady=0, padx=0)
delete_saved_data_button = Button(text="Delete Saved Words", command=delete_saved_words, font=SECONDARY_FONT,
                                  fg="red", bg="black", bd=0, highlightthickness=0)
delete_saved_data_button.grid(row=2, column=0, pady=0, padx=0)

pause = Button(text="Pause Music",
               command=mixer.music.pause, font=MAIN_FONT,
               fg="white", bg=BACKGROUND_COLOR, bd=0, highlightthickness=0)
pause.grid(row=1, column=3, pady=0, padx=20)

# Exit Button
exit_game = Button(text="Exit", command=lambda: [window.destroy(), mixer.music.stop()],
                   font=MAIN_FONT,
                   fg="white", bg=BACKGROUND_COLOR)
exit_game.grid(row=3, column=1, columnspan=2, pady=0, padx=0)


# Opening Message
messagebox.showinfo(title="Welcome to Schöne!",
                    message="'Schöne' help you learn German.\n\n"
                            "This program will show you a German word and after 3 seconds"
                            " it will show you its English translation.\n\n"
                            "When you select '''don't know this word''' The program will save that word in order"
                            " to show it to you again and again till you learn it, instead when you select"
                            " '''Ja!, I know this one''' it will remove"
                            " it from the list of words reducing thus the total number of words to memorize.\n\n"
                            "If you want to reset the flashcards"
                            " as to include the previous deleted ones, just click on '''Delete Saved Words'''.")
next_card()


window.mainloop()
