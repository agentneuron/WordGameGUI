import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import random

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
LETTER_IMAGES = []
FINAL_IMAGES = []
NUMBER_IMAGES = []
HELPER_IMAGES = ['','','','']
SOLVABLE_BLOCKS = []
BUTTONS = []
LABELS = []
WORDLIST = []
WORDNUMPOS = []
THEWORD = ''
SOLVED = False
WORD_VERIFY = ''
ALPHABET_BUTTONS = []
ROW_COUNT = 0
ATTEMPTS_MAX = 5
ATTEMPTS = 0
ATTEMPT_COUNTER = []


class mainwindow:
	def __init__(self, master):
		global ROW_COUNT		
		self.load_resources()
		frame = Frame(master, padx=20,pady=20)
		frame.pack()
		self.display_alphabet(frame, ROW_COUNT)
		ROW_COUNT += 2
		self.add_spacers(frame, ROW_COUNT, 1)
		ROW_COUNT += 1
		self.add_word_row(frame, ROW_COUNT)
		ROW_COUNT += 1
		self.add_spacers(frame, ROW_COUNT, 1)
		ROW_COUNT += 1
		self.add_action_buttons(frame, master, ROW_COUNT)
		ROW_COUNT += 1


	def display_alphabet(self, w, ROW_COUNT):
		column = 0
		for x, y in enumerate(ALPHABET):
			alphabutton = Button(w, image=LETTER_IMAGES[x], command=lambda y=y: self.check_letter(y), bd=0)
			alphabutton.image = LETTER_IMAGES[x]
			ALPHABET_BUTTONS.append(alphabutton)
			ALPHABET_BUTTONS[x].grid(row=ROW_COUNT, column=column, padx=0, pady=0)
			column += 1
			if column >= 13:
				column = 0
				ROW_COUNT += 1


	def add_word_row(self, w, row_start):
		WORDNUMPOS.clear()
		SOLVABLE_BLOCKS.clear()
		wordspacelen = 12 - len(THEWORD)
		solve_blocks_start = wordspacelen/2
		solve_blocks_end   = 12 - wordspacelen/2
		for x in range(0 , 13):
			if (x >= solve_blocks_start) and (x < solve_blocks_end):
				slabel = Label(w, image=HELPER_IMAGES[1], bd=0)
				slabel.image=HELPER_IMAGES[1]
				SOLVABLE_BLOCKS.append(slabel)
				WORDNUMPOS.append(x)
			else:
				slabel = Label(w, image=HELPER_IMAGES[0],bd=0)
				slabel.image=HELPER_IMAGES[0]
				SOLVABLE_BLOCKS.append(slabel)
			SOLVABLE_BLOCKS[x].grid(row=row_start, column=x)


	def add_action_buttons(self, w, wm, row_start):
		attempt_counter = Label(w, image=NUMBER_IMAGES[ATTEMPTS_MAX-ATTEMPTS])
		attempt_counter.image=NUMBER_IMAGES[ATTEMPTS]
		ATTEMPT_COUNTER.append(attempt_counter)
		reset_game = Button(w, image=HELPER_IMAGES[2], bd=0, command=lambda: self.reset_game(w))
		reset_game.image = HELPER_IMAGES[2]
		exit_game = Button(w, image=HELPER_IMAGES[3], bd=0, command=wm.destroy)
		exit_game.image = HELPER_IMAGES[3]
		reset_game.grid(row=row_start, column=11, sticky=E)
		exit_game.grid(row=row_start, column=12, sticky=E)
		attempt_counter.grid(row=row_start, column=10, sticky=E)

	def add_spacers(self, w, row_start, count):
		for x in range(0, count):
			grid_spacer = Label(w, image=HELPER_IMAGES[0])
			grid_spacer.grid(row=row_start+x, column=1, columnspan=13)


	def load_resources(self):
		for x in ALPHABET:
			y_image = ImageTk.PhotoImage(Image.open(f"resources/alphabet/yellow/letter_{x}.png"))
			b_image = ImageTk.PhotoImage(Image.open(f"resources/alphabet/blue/letter_{x}.png"))
			LETTER_IMAGES.append(y_image)
			FINAL_IMAGES.append(b_image)
		for y in range(0,6):
			t_image = ImageTk.PhotoImage(Image.open(f"resources/numbers/{str(y)}.png"))
			NUMBER_IMAGES.append(t_image)
		HELPER_IMAGES[0] = ImageTk.PhotoImage(Image.open("resources/spacer.png"))
		HELPER_IMAGES[1] = ImageTk.PhotoImage(Image.open('resources/metal.png'))
		HELPER_IMAGES[2] = ImageTk.PhotoImage(Image.open('resources/reset.png'))
		HELPER_IMAGES[3] = ImageTk.PhotoImage(Image.open('resources/quit.png'))


	def reset_game(self, w):
		global THEWORD
		global WORD_VERIFY
		global ATTEMPTS
		for x, y in enumerate(ALPHABET_BUTTONS):
			ALPHABET_BUTTONS[x]['state']="normal"
		for x in range(0,13):
			SOLVABLE_BLOCKS[x].config(image=HELPER_IMAGES[0])
		THEWORD, WORD_VERIFY = choose_word()
		ATTEMPTS = 0
		ATTEMPT_COUNTER[0].config(image=NUMBER_IMAGES[5])
		self.add_word_row(w, 3)


	def check_letter(self, clicked):
		global WORD_VERIFY
		global ATTEMPTS
		tw = list(THEWORD)
		wv = list(WORD_VERIFY)
		if clicked in THEWORD:
			for x, y in enumerate(THEWORD):
				if y == clicked:
					wv[x] = clicked
					SOLVABLE_BLOCKS[WORDNUMPOS[x]].config(image=LETTER_IMAGES[ALPHABET.index(clicked)])
		else:
			ATTEMPTS += 1
			ATTEMPT_COUNTER[0].config(image=NUMBER_IMAGES[ATTEMPTS_MAX-ATTEMPTS])
		WORD_VERIFY = ''.join(wv)
		ALPHABET_BUTTONS[ALPHABET.index(clicked)]['state']="disabled"
		if ATTEMPTS == ATTEMPTS_MAX:
			self.game_complete(False)
		if THEWORD == WORD_VERIFY:
			self.game_complete(True)

	def game_complete(self, result):
		for x, y in enumerate(ALPHABET_BUTTONS):
			ALPHABET_BUTTONS[x]['state']="disabled"
		if not result:
			for x, y in enumerate(THEWORD):
				if WORD_VERIFY[x] == '#':
					t=THEWORD[x]
					SOLVABLE_BLOCKS[WORDNUMPOS[x]].config(image=FINAL_IMAGES[ALPHABET.index(t)])
					

def choose_word():
	wv = ''
	if len(WORDLIST) == 0:
	    wordfile = open("resources/words.txt", "r", encoding="utf-8")
	    lines = wordfile.readlines()
	    for count in range(0, len(lines) - 1):
	        x = lines[count]
	        wordlen = len(x)
	        a = x[:wordlen - 1]
	        if (wordlen <= 11) and (wordlen >= 6):
	            WORDLIST.append(a)
	    WORDLIST.append(lines[count + 1])
	    wordfile.close()
	new_word = random.choice(WORDLIST)
	for x in new_word:
		wv = wv + '#' 
	return new_word, wv


def main():	
	global THEWORD
	global WORD_VERIFY
	THEWORD, WORD_VERIFY = choose_word()
	THEWORD = 'wordgame'
	WORD_VERIFY = '########'
	root = Tk()
	root.title("Word Game")
	root.resizable(False, False)
	x = mainwindow(root)
	root.mainloop()


if __name__ == "__main__":
	main()