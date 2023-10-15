
from tkinter import *
import math
import random
import pygame
from tkinter import filedialog
import os

GREY = "#9EA1D4"
PURPLE = "#A8D1D1"
RED = "#FF8787"
GREEN = "#F1F7B5"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None

pygame.mixer.init()

# ---------------------------- MUSIC PLAYER ------------------------------- #
music_folder = ""  # Initialize the music folder variable

def select_music_folder():
    global music_folder
    music_folder = filedialog.askdirectory()  # Open a dialog to select the music folder
    if music_folder:
        print("Selected Music Folder:", music_folder)

current_song_index = 0

def play_music(next_song=False, previous_song=False):
    global current_song_index

    if not music_folder:
        print("Please select a music folder first.")
        return

    # List the music files in the selected folder
    music_files = [f for f in os.listdir(music_folder) if f.endswith(".mp3")]
    if not music_files:
        print("No music files found in the selected folder.")
        return

    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()

    if next_song:
        current_song_index += 1
        if current_song_index >= len(music_files):
            current_song_index = 0
    elif previous_song:
        current_song_index -= 1
        if current_song_index < 0:
            current_song_index = len(music_files) - 1

    music_file = os.path.join(music_folder, music_files[current_song_index])
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play()

# ---------------------------- QUOTES PLAYER ------------------------------- #

# Sample motivational quotes
quotes = [
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill",
    "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
    "Success is not in what you have, but who you are. - Bo Bennett",
    "The only thing we have to fear is fear itself. -Franklin D. Roosevelt",
    "Well done is better than well said. -Benjamin Franklin",
    "Be yourself; everyone else is already taken. -Oscar Wilde",
    "Life is a succession of lessons which must be lived to be understood. -Ralph Waldo Emerson",
    "You will face many defeats in life, but never let yourself be defeated. -Maya Angelou",
    "Many of life's failures are people who did not realize how close they were to success when they gave up. -Thomas A. Edison",
    "I find that the harder I work, the more luck I seem to have. -Thomas Jefferson",
    "Don't be distracted by criticism. Remember — the only taste of success some people get is to take a bite out of you. - Zig Ziglar",
    "The only place where success comes before work is in the dictionary. -Vidal Sassoon",
    "Before anything else, preparation is the key to success. - Alexander Graham Bell",
    # Add more quotes here
]

def display_quote():
    random_quote = random.choice(quotes)
    quote_label.config(text=random_quote)


# ---------------------------- TIMER RESET ------------------------------- #

def reset_timer():
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer")
    check_marks.config(text="")
    global reps
    reps = 0


# ---------------------------- TIMER MECHANISM ------------------------------- #

def start_timer():
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_sec)
        title_label.config(text="Break", fg=PURPLE)
    elif reps % 2 == 0:
        count_down(short_break_sec)
        title_label.config(text="Break", fg=GREY)
    else:
        count_down(work_sec)
        title_label.config(text="Work", fg=RED)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):

    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        work_sessions = math.floor(reps/2)
        for _ in range(work_sessions):
            marks += "✔"
        check_marks.config(text=marks)

# Create a Tkinter UI
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=GREEN)


title_label = Label(text="Timer", fg=RED, bg=GREEN, font=(FONT_NAME, 50))
title_label.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, bg=GREEN, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

# Buttons

start_button = Button(text="Start", highlightthickness=0, command=start_timer, bg="#A8DF8E")
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer, bg="#A8DF8E")
reset_button.grid(column=2, row=2)

check_marks = Label(fg=RED, bg=GREEN)
check_marks.grid(column=1, row=3)

# Quotes Player
quote_label = Label(fg=RED, bg=GREEN, wraplength=200, justify="center", font=(FONT_NAME, 10, "italic"))
quote_label.grid(column=1, row=4)

quote_button = Button(text="Show Quote", highlightthickness=0, command=display_quote, bg="#A8DF8E")
quote_button.grid(column=1, row=5)

select_music_folder_button = Button(text="Select Music Folder", highlightthickness=0, command=select_music_folder, bg="#A8DF8E")
select_music_folder_button.grid(column=1, row=6)

play_music_button = Button(text="Play Music", highlightthickness=0, command=play_music, bg="#A8DF8E")
play_music_button.grid(column=1, row=8)

next_button = Button(text="Next", highlightthickness=0, command=lambda: play_music(next_song=True), bg="#A8DF8E")
next_button.grid(column=2, row=8)

previous_button = Button(text="Previous", highlightthickness=0, command=lambda: play_music(previous_song=True), bg="#A8DF8E")
previous_button.grid(column=0, row=8)

window.mainloop()