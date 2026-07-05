
from PIL import Image 
import customtkinter as ctk 
import tkinter as tk 
import pygame 
import random
import sqlite3
import os
import sys

def resource_path(relative_path):
    """Get to absolute path to resorce, works for development and PyInstaller."""
    
    try:
        base_path = sys._MEIPASS
        
    except Exception:
        base_path = os.path.abspath(".")
        
    return os.path.join(base_path, relative_path)



IMAGE_DIR = resource_path("images")
MUSIC_DIR = resource_path("music")
SAVE_DIR = resource_path("saves")

def img(name):
	return os.path.join(IMAGE_DIR, name)

def music(name):
	return os.path.join(MUSIC_DIR, name)

def save(name):
	return os.path.join(SAVE_DIR, name)




pygame.init()
pygame.mixer.init()

score = 0
high_score = 0
highest_streak = 0
rank = "Newbie"

app = ctk.CTk()
app.withdraw()
app.title("HANGY")
app.geometry("720x500")
#----------------------------------------------------MUSIC----------------------------------------------------------------------

pygame.mixer.music.load(resource_path(music("Music.mpeg")))
pygame.mixer.music.play(-1)

click_sound = pygame.mixer.Sound(resource_path(music("click.mp3")))
win_sound = pygame.mixer.Sound(resource_path(music("ywin.mp3")))
lost_sound = pygame.mixer.Sound(resource_path(music("ylost.mp3")))

def play_click():
	click_sound.play()

def play_win():
	win_sound.play()

def play_lost():
	lost_sound.play()

#-----------------------------------------------------words--------------------------------------------------------------------

with open(resource_path("words.txt"), "r") as file:
	all_words = [word.strip().lower() for word in file if word.strip()]


words_2 = [w for w in all_words if len(w) == 2]
words_3 = [w for w in all_words if len(w) == 3]
words_4 = [w for w in all_words if len(w) == 4]
words_5 = [w for w in all_words if len(w) == 5]
words_6 = [w for w in all_words if len(w) == 6]
words_7 = [w for w in all_words if len(w) == 7]
words_8 = [w for w in all_words if len(w) == 8]

words_5plus = words_5 + words_6 + words_7 + words_8
#------------------------------------------------------Database----------------------------------------------------------------

conn = sqlite3.connect(save("hangy.db"))
cursor = conn.cursor()

cursor.execute("""
	CREATE TABLE IF NOT EXISTS player(
		id INTEGER PRIMARY KEY,
		username TEXT,
		high_score REAL,
		highest_streak INTEGER,
		rank TEXT,
		total_score REAL)
""")

cursor.execute(""" 
	INSERT OR IGNORE INTO player
	(id, username, high_score, highest_streak, rank, total_score)
	VALUES(1,'' , 0,0,'NEWBIE',0)
""")

conn.commit()

cursor.execute("SELECT *FROM player")
player = cursor.fetchone()

#--------------------------------------------------register------------------------------------------------------------------

def register():
	cursor.execute("""
			SELECT username 
			FROM player
			WHERE id = 1
			""")

	username = cursor.fetchone()[0]

	if username == "":
		reg = ctk.CTkToplevel()
		reg.title("LET's BEGIN")
		reg.geometry("600x450")
		reg.resizable(False, False)

		reg_img = ctk.CTkImage(
			light_image = Image.open(resource_path(img("w.png"))),
			dark_image = Image.open(resource_path(img("w.png"))),
			size = (600,450))

		reg_label = ctk.CTkLabel(
			reg,
			image = reg_img,
			text = "")
		reg_label.place(x=0, y=0, relwidth=1, relheight=1)

		username_entry = ctk.CTkEntry(
			reg,
			width = 305,
			height = 45,
            justify = "center",

			fg_color = "black",
			border_color = "black",
			text_color = "white",

			corner_radius = 0
			)

		username_entry.place(relx = 0.5, rely = 0.68, anchor = "center")

		start_img = ctk.CTkImage(
			light_image = Image.open(resource_path(img("start.png"))),
			dark_image = Image.open(resource_path(img("start.png"))),
			size = (215,52))

		def save_username(event = None):
			play_click()
			username = username_entry.get().strip()

			if username == "":
				return

			cursor.execute("""
				UPDATE player
				SET username = ?
				WHERE id = 1
				""", (username,))

			conn.commit()
			reg.destroy()
			welcome_window(username)


		start_label = ctk.CTkLabel(
			reg,
			image = start_img,
			text = "")

		start_label.place(
			relx = 0.5,
			rely = 0.85,
			anchor = "center")

		start_label.image = start_img

		start_label.bind(
			"<Button-1>",
			save_username)


	else:
		welcome_window(username)





def welcome_window(username):

    wel = ctk.CTkToplevel()

    wel.title("Welcome")
    wel.geometry("600x450")
    wel.resizable(False, False)

    wel_img = ctk.CTkImage(
        light_image=Image.open(resource_path(img("wel.jpeg"))),
        dark_image=Image.open(resource_path(img("wel.jpeg"))),
        size=(600,450)
    )

    bg = ctk.CTkLabel(
        wel,
        image=wel_img,
        text=""
    )

    bg.place(
        x=0,
        y=0,
        relwidth=1,
        relheight=1
    )

    bg.image = wel_img

    welcome = ctk.CTkLabel(
        wel,
        text=f"{username}",
        font=("Cinzel",28,"bold"),
        text_color="#B08D57",
	bg_color="#090402",
    )

    welcome.place(
        relx=0.5,
        rely=0.65,
        anchor="center"
    )

    def fade(alpha = 1.0):
        alpha -= 0.05

        if alpha <=0:
            wel.destroy()
            app.deiconify()
            app.lift()
            return

        wel.attributes("-alpha",alpha)
        wel.after(40, lambda: fade(alpha))

    wel.after(2000, fade)

register()



#-------------------------------------------------------BG----------------------------------------------------------------------

bg_image = ctk.CTkImage(
 	light_image = Image.open(resource_path(img("bg.jpeg"))),
	dark_image = Image.open(resource_path(img("bg.jpeg"))),
	size = (720,500))

bg_label = ctk.CTkLabel(
	app,
	image = bg_image,
	text = "")
bg_label.place(x=0, y=0, relwidth=1, relheight=1)


#------------------------------------------------------PLAY----------------------------------------------------------------------

play_img = ctk.CTkImage(
	light_image = Image.open(resource_path(img("play.png"))),
	dark_image = Image.open(resource_path(img("play.png"))),
	size = (180,42))


play_label = ctk.CTkLabel(
	bg_label,
	image = play_img,
	text="")
play_label.place(relx=0.3, rely=0.5, anchor = "center")

set_win = None
game_win = None


diff_win = None
def diff(event):
	play_click()

	app.withdraw()

	global diff_win

	if diff_win is not None and diff_win.winfo_exists():
		diff_win.deiconify()
		diff_win.lift()
		diff_win.focus_force()
		return

	diff_win = ctk.CTkToplevel()
	diff_win.title("Choose Difficulty")
	diff_win.geometry("720x500")

	def close_diff():
		global diff_win
		diff_win.destroy()
		diff_win = None

		app.deiconify()
		app.lift()
		app.focus_force()

	diff_win.protocol("WM_DELETE_WINDOW", close_diff)

	diff_img = ctk.CTkImage(
		light_image = Image.open(resource_path(img("diff.png"))),
		dark_image = Image.open(resource_path(img("diff.png"))),
		size = (720,500))

	diff_label = ctk.CTkLabel(
		diff_win,
		image = diff_img,
		text = "")
	diff_label.place(x=0, y=0, relwidth = 1, relheight = 1)

	diff_label.image = diff_img 

	pf_img = ctk.CTkImage(
		light_image = Image.open(resource_path(img("pf.png"))),
		dark_image = Image.open(resource_path(img("pf.png"))),
		size = (180,60))

	xrank_label = ctk.CTkLabel(
		diff_win,
		image=pf_img,
		text=""
		)

	xrank_label.place(relx=0.865, rely=0.935, anchor="center")

	def show_profile(event = None):

		play_click()

		profile = ctk.CTkToplevel()
		profile.title("PLAYER PROFILE")
		profile.geometry("600x450")
		profile.resizable(False, False)

    # ---------------- Background ----------------

		profile_bg = ctk.CTkImage(
			light_image=Image.open(resource_path(img("pp.jpeg"))),
			dark_image=Image.open(resource_path(img("pp.jpeg"))),
			size=(600, 450)
		)

		profile_label = ctk.CTkLabel(
			profile,
			image=profile_bg,
			text=""
		)

		profile_label.place(x=0, y=0, relwidth=1, relheight=1)
		profile_label.image = profile_bg

    # ---------------- Read Database ----------------

		cursor.execute("""
		SELECT username,
		high_score,
		highest_streak,
		rank
		FROM player
		WHERE id = 1
		""")

		player = cursor.fetchone()

		high_score = player[1]
		username = player[0]
		highest_streak = player[2]
		rank = player[3]

		

		user_label = ctk.CTkLabel(
			profile,
			text = username,
			font = ("Cinzel", 28 , "bold"),
			text_color = "#B08D57",
			bg_color = "black")

		user_label.place(
				relx = 0.5,
				rely = 0.21,
				anchor = "center")

		sc_label = ctk.CTkLabel(
			profile,
			text = f"{high_score:.2f}",
			font = ("Cinzel", 15 , "bold"),
			text_color = "#B08D57",
			bg_color = "black",
            height = 15,
            corner_radius = 0)

		sc_label.place(
				relx = 0.21,
				rely = 0.91,
				anchor = "center")     


		str_label = ctk.CTkLabel(
			profile,
			text = highest_streak,
			font = ("Cinzel", 15 , "bold"),
			text_color = "#B08D57",
			bg_color = "black",
            height = 15,
            corner_radius = 0)

		str_label.place(
				relx = 0.5,
				rely = 0.91,
				anchor = "center")   

		r_label = ctk.CTkLabel(
			profile,
			text = rank,
			font = ("Cinzel", 15 , "bold"),
			text_color = "#B08D57",
			bg_color = "black",
            height = 15,
            corner_radius = 0)

		r_label.place(
				relx = 0.8,
				rely = 0.91,
				anchor = "center")   


		xrank_label.bind(
			"<Button-1>",
			lambda e: show_profile())


	word2_img = ctk.CTkImage(
		light_image=Image.open(resource_path(img("2.jpeg"))),
		dark_image=Image.open(resource_path(img("2.jpeg"))),
		size=(180, 42)
		)

	word3_img = ctk.CTkImage(
		light_image=Image.open(resource_path(img("3.jpeg"))),
		dark_image=Image.open(resource_path(img("3.jpeg"))),
		size=(180, 42)
		)

	word4_img = ctk.CTkImage(
		light_image=Image.open(resource_path(img("4.jpeg"))),
		dark_image=Image.open(resource_path(img("4.jpeg"))),
		size=(180, 42)
		)

	word5_img = ctk.CTkImage(
		light_image=Image.open(resource_path(img("5.jpeg"))),
		dark_image=Image.open(resource_path(img("5.jpeg"))),
		size=(180, 42)
		)

	word5plus_img = ctk.CTkImage(
		light_image=Image.open(resource_path(img("5a.jpeg"))),
		dark_image=Image.open(resource_path(img("5a.jpeg"))),
		size=(180, 42)
		)

	label2 = ctk.CTkLabel(diff_win, image=word2_img, text="")
	label2.place(relx=0.375, y=220, anchor="center")

	label3 = ctk.CTkLabel(diff_win, image=word3_img, text="")
	label3.place(relx=0.375, y=270, anchor="center")

	label4 = ctk.CTkLabel(diff_win, image=word4_img, text="")
	label4.place(relx=0.375, y=320, anchor="center")

	label5 = ctk.CTkLabel(diff_win, image=word5_img, text="")
	label5.place(relx=0.375, y=370, anchor="center")

	label5plus = ctk.CTkLabel(diff_win, image=word5plus_img, text="")
	label5plus.place(relx=0.375, y=420, anchor="center")


	xrank_label.bind(
				"<Button-1>",
				lambda e: show_profile())


#-------------------------------------------------GAME SCREEN --------------------------------------------------------------------

	def start_game(length):
		play_click()

		diff_win.withdraw()

		global game_win

		if game_win is not None and game_win.winfo_exists():
			game_win.focus_force()
			return

		game_win = ctk.CTkToplevel()
		game_win.title("HANGY")
		game_win.geometry("720x500")


		def close_game():
			global game_win

			game_win.destroy()
			game_win = None

			diff_win.deiconify()
			diff_win.lift()
			diff_win.focus_force()

		game_win.protocol("WM_DELETE_WINDOW", close_game)

		g_bg = ctk.CTkImage(
			light_image = Image.open(resource_path(img("gbg.jpeg"))),
			dark_image = Image.open(resource_path(img("gbg.jpeg"))),
			size = (720,500))

		g_bg_label = ctk.CTkLabel(
			game_win,
			image = g_bg,
			text="")

		g_bg_label.place(x = 0, y = 0, relwidth = 1, relheight = 1)


		used_words = []

		def get_random_word(word_list):
			nonlocal used_words
			available = [w for w in word_list if w not in used_words]

			if not available:
				used_words.clear()
				available = word_list.copy()

			word = random.choice(available)
			used_words.append(word)
			return word


		if length == 2:
			word = get_random_word(words_2)

		elif length == 3:
			word = get_random_word(words_3) 

		elif length == 4:
			word = get_random_word(words_4)

		elif length == 5:
			word =get_random_word(words_5)

		else:
			word = get_random_word(words_5plus)


		hidden_word = ["_"] * len(word)

		if len(word) <=3 :
			random_pos = random.randint(1, len(word)-1)
			hidden_word[random_pos] = word[random_pos].upper()

		else:
			pos1, pos2 = random.sample(
				range(len(word)),
				2
				)

			hidden_word[pos1] = word[pos1].upper()
			hidden_word[pos2] = word[pos2].upper()

		ywin_img  = ctk.CTkImage(
			light_image = Image.open(resource_path(img("ywin.png"))),
			dark_image = Image.open(resource_path(img("ywin.png"))),
			size = (360,84))

		ylost_img  = ctk.CTkImage(
			light_image = Image.open(resource_path(img("ylost.png"))),
			dark_image = Image.open(resource_path(img("ylost.png"))),
			size = (360,84))

		frame_img  = ctk.CTkImage(
			light_image = Image.open(resource_path(img("fr.png"))),
			dark_image = Image.open(resource_path(img("fr.png"))),
			size = (360,84))


		frame_label = ctk.CTkLabel(
			game_win,
			text="",
			image = frame_img
			)

		frame_label.place(relx = 0.5, rely = 0.35, anchor  ="center")


		word_label = ctk.CTkLabel(
			game_win,
			text = " ".join(hidden_word),
			font = ("Cinzel",32,"bold"),
			text_color = "#FFD700",
			bg_color = "#090402",
			height = 28,
			corner_radius = 0,
			padx = 20, pady = 10		)

		word_label.place(relx = 0.5, rely = 0.35, anchor  ="center")

		score = 0
		streak = 0



		score_img  = ctk.CTkImage(
			light_image = Image.open(resource_path(img("sc.png"))),
			dark_image = Image.open(resource_path(img("sc.png"))),
			size = (180,42))

		score_label = ctk.CTkLabel(
			game_win,
			text="",
			image = score_img
			)

		score_label.place(relx=0.2 , rely=0.1, anchor = "center")

		score_value = ctk.CTkLabel(
			game_win,
			text = "0",
			font = ("Cinzel",20,"bold"),
			text_color = '#B08D57',
			fg_color = "black")

		score_value.place(relx=0.25 , rely = 0.1, anchor = "center")

		streak_img = ctk.CTkImage(
			light_image = Image.open(resource_path(img("st.png"))),
			dark_image = Image.open(resource_path(img("st.png"))),
			size = (180,42))

		streak_label = ctk.CTkLabel(
			game_win,
			text="",
			image = streak_img
			)
		streak_label.place(relx=0.2,rely=0.175, anchor = "center")

		streak_value = ctk.CTkLabel(
			game_win,
			text = "0",
			font = ("Cinzel", 20, "bold"),
			text_color = '#B08D57',
			fg_color = "black")

		streak_value.place(relx = 0.25, rely = 0.175, anchor = "center")


		garea_img = ctk.CTkImage(
			light_image = Image.open(resource_path(img("garea.jpeg"))),
			dark_image = Image.open(resource_path(img("garea.jpeg"))),
			size = (260,90))

		garea_label = ctk.CTkLabel(
			game_win,
			text="",
			image = garea_img
			)
		garea_label.place(relx=0.5,rely=0.63, anchor = "center")

		guess_entry = ctk.CTkEntry(
						game_win,
						width = 240,
						height = 60,
						justify = "center",
						fg_color = "black",
						border_color = "black",
						font = ("Cinzel",18,"italic"),
						corner_radius = 0)

		guess_entry.place(relx = 0.5, rely = 0.65, anchor = "center")

		gus_img = ctk.CTkImage(
			light_image = Image.open(resource_path(img("guess.jpeg"))),
			dark_image = Image.open(resource_path(img("guess.jpeg"))),
			size = (180,42))

		gus_label = ctk.CTkLabel(
			game_win,
			text="",
			image = gus_img
			)
		gus_label.place(relx=0.5,rely=0.78, anchor = "center")

		l0_img = ctk.CTkImage(
			light_image=Image.open(resource_path(img("l0.png"))),
            		dark_image=Image.open(resource_path(img("l0.png"))),
            		size=(130, 40))

		l1_img = ctk.CTkImage(
            		light_image=Image.open(resource_path(img("l1.png"))),
			dark_image=Image.open(resource_path(img("l1.png"))),
			size=(130, 40))

		l2_img = ctk.CTkImage(
            		light_image=Image.open(resource_path(img("l2.png"))),
            		dark_image=Image.open(resource_path(img("l2.png"))),
            		size=(130, 40))

		l3_img = ctk.CTkImage(
            		light_image=Image.open(resource_path(img("l3.png"))),
            		dark_image=Image.open(resource_path(img("l3.png"))),
            		size=(130, 40))

		lives = 3

		lives_label = ctk.CTkLabel(
			game_win,
			text="",
            		image = l3_img)
		

		lives_label.place(relx = 0.8, rely = 0.1, anchor = "center")

		def update_lives():
            		if lives == 3:
                		lives_label.configure(image=l3_img)

            		elif lives == 2:
                		lives_label.configure(image=l2_img)

            		elif lives == 1:
                		lives_label.configure(image=l1_img)

            		else:
                		lives_label.configure(image=l0_img)

		restart_button = ctk.CTkButton(
			game_win,
			text = "RESTART",
			width = 140,
			height = 40,
			fg_color = "#B22222",
			hover_color = "#8B0000")

		res_img = ctk.CTkImage(
			light_image = Image.open(resource_path(img("res.jpeg"))),
			dark_image = Image.open(resource_path(img("res.jpeg"))),
			size = (180,42))

		res_label = ctk.CTkLabel(
			game_win,
			text="",
			image = res_img
			)


		def restart_game():
			nonlocal score, streak, lives, guessed_letters

			score = 0
			streak = 0
			lives = 3
			guessed_letters.clear()

			score_value.configure(
						text = "0" )
			streak_value.configure(
						text = "0")
			update_lives()

			res_label.place_forget()

			gus_label.place(relx = 0.5, rely = 0.78, anchor = "center")
			load_new_word()
			guess_entry.focus()

		restart_button.configure(command = restart_game)


		def get_word_score(word):
			length = len(word)

			if length == 2:
				return 0.5
			elif length == 3:
				return 0.75
			elif length == 4:
				return 1
			elif length == 5:
				return 1.25
			elif length == 6:
				return 1.5
			elif length == 7:
				return 1.75
			else:
				return 2

		def get_streak_bonus(streak):
			if streak >= 100:
				return 1.00

			elif streak >= 75:
				return 0.75

			elif streak >= 50:
				return 0.50

			elif streak >= 40:
				return 0.40

			elif streak >= 30:
				return 0.30

			elif streak >= 20:
				return 0.20

			elif streak >= 10:
				return 0.10
			else:
				return 0



		h2_img = ctk.CTkImage(
			light_image = Image.open(resource_path(img("h2.png"))),
			dark_image = Image.open(resource_path(img("h2.png"))),
			size = (220, 48))

		h1_img = ctk.CTkImage( 
                        light_image = Image.open(resource_path(img("h1.png"))),
                        dark_image = Image.open(resource_path(img("h1.png"))),
                        size = (220, 48))

		h0_img = ctk.CTkImage( 
                        light_image = Image.open(resource_path(img("h0.png"))),
                        dark_image = Image.open(resource_path(img("h0.png"))),
                        size = (220, 48))

		hint_label = ctk.CTkLabel(
			g_bg_label,
			width = 220,
			height = 48,

			image = h2_img,
			text = "")


		guessed_letters = []

		if length <=2:
			max_hints = 0
		elif length <=5:
			max_hints = 1
		else:
			max_hints = 2

		hints_used = 0

		def update_hint():
			remaining = max_hints - hints_used

			if remaining == 2:
				hint_label.configure(image = h2_img)

			elif remaining == 1:
				hint_label.configure(image = h1_img)

			else:
				hint_label.configure(image = h0_img)


		def show_popup(message):

			popup = ctk.CTkToplevel()
			popup.geometry("350x200")
			popup.title("HANGY")

			popup_img = ctk.CTkImage(
				light_image = Image.open(resource_path(img("pop.png"))),
				dark_image = Image.open(resource_path(img("pop.png"))),
				size = (350,200))

			bg = ctk.CTkLabel(
				popup,
				image = popup_img,
				text = "")
			bg.place(x=0, y=0, relwidth=1, relheight=1)

			msg = ctk.CTkLabel(
				popup,
				text = message,
				font = ("Cinzel", 20, "bold"),
				text_color = "#FFD700",
				bg_color = "#090402")
			msg.place(relx = 0.5, rely = 0.45, anchor = "center")

			ok = ctk.CTkButton(
				popup,
				text = "OK",
				fg_color = "#090402",
				hover_color = "black",
				command = popup.destroy)
			ok.place(relx=0.5, rely=0.8, anchor = "center")


		def use_hints(event = None):
			nonlocal hints_used, score
			if hints_used >= max_hints:
				return

			if score < 0.25:
				show_popup("you need at least 0.25 score")
				return


			hidden_indexes = [
				i for i in range(len(word))
				if hidden_word[i]== "_"
			]

			if not hidden_indexes:
				return

			pos = random.choice(hidden_indexes)

			hidden_word[pos] = word[pos].upper()

			word_label.configure(
				text = " ".join(hidden_word))

			hints_used += 1

			update_hint()

			score = max(0, score - 0.25)

			score_value.configure(
					text = f"{score:.2f}")


		hint_label.bind(
			"<Button-1>",
			use_hints)

		update_hint()

		hint_label.place(relx = 0.5, rely = 0.88, anchor = "center")


		def load_new_word():
			nonlocal word, hidden_word, lives, guessed_letters, score, streak, hints_used



			if length == 2:
				word = get_random_word(words_2)

			elif length == 3:
				word = get_random_word(words_3)

			elif length == 4:
				word = get_random_word(words_4)

			elif length == 5:
				word =get_random_word(words_5)

			else:
				word = get_random_word(words_5plus)



			hints_used = 0
			update_hint()

			lives = 3
			guessed_letters.clear()
			hidden_word = ["_"] * len(word)

			if len(word) <=3 :
				random_pos = random.randint(0, len(word)-1)
				hidden_word[random_pos] = word[random_pos].upper()

			else:
				pos1, pos2 = random.sample(
					range(len(word)),
                                    					2)
				hidden_word[pos1] = word[pos1].upper()
				hidden_word[pos2] = word[pos2].upper()

			guess_entry.configure(state = "normal")
			guess_entry.delete(0 , "end")
			guess_entry.configure(
						font = ("Cinzel" , 18, "italic"))

			gus_label.configure(state = "normal")

			word_label.configure(
				text=" ".join(hidden_word),
				image = "")

			update_lives()


		def check_guess(event = None):
			nonlocal lives, score, streak
			global high_score

			guess = guess_entry.get().lower()
			guess_entry.delete(0,"end")

			if len(guess) !=1:
				return

			if guess in guessed_letters:
				return

			guessed_letters.append(guess)

			if guess in word:
				for i in range(len(word)):
					if word[i] == guess:
						hidden_word[i] = guess.upper()

				word_label.configure(
					text = " ".join (hidden_word))

				if "_" not in hidden_word:

					play_win()
					word_label.configure(
					text = "",
					image = ywin_img)

					streak += 1

					base_score = get_word_score(word)
					bonus = base_score * get_streak_bonus(streak)
					score += base_score + bonus

					cursor.execute(""" 
							UPDATE player
							SET total_score = total_score + ?
							WHERE id = 1
							""", (base_score + bonus,))

					conn.commit()

					cursor.execute("""
							SELECT high_score
							FROM player
							WHERE id = 1
							""")

					high_score = cursor.fetchone()[0]

					if score > high_score:

						cursor.execute("""
							UPDATE player
							SET high_score = ?
							WHERE id = 1
							""", (score,))
						conn.commit()

						high_score = score


					if streak >  highest_streak:

						cursor.execute("""
							UPDATE player
							SET highest_streak = ?
							WHERE id = 1
							""", (streak,))
						conn.commit()


						update_rank()

					game_win.after(
						1000,
						load_new_word)


			else:
				lives -= 1

				update_lives()

				if lives == 0:
					play_lost()

					word_label.configure(
					text = (""),
					image = ylost_img)

					guess_entry.delete(0, "end")
					guess_entry.insert(0, word.upper())


					guess_entry.configure(state = "disabled",
								justify = "center")
					gus_label.configure(state = "disabled")

					gus_label.place_forget()
					res_label.place(relx = 0.5, rely = 0.78, anchor = "center")
					res_label.bind(
						"<Button-1>",
						lambda e: restart_game())


			score_value.configure(
				text = f" {score:.2f}")

			streak_value.configure(
				text = f" {streak}")

		gus_label.bind(
                        "<Button-1>",
                        lambda e: check_guess())

		game_win.bind(
                                "<Return>",
                                lambda e: check_guess())



	label2.bind("<Button-1>", lambda e: start_game(2))
	label3.bind("<Button-1>", lambda e: start_game(3))
	label4.bind("<Button-1>", lambda e: start_game(4))
	label5.bind("<Button-1>", lambda e: start_game(5))
	label5plus.bind("<Button-1>", lambda e: start_game(6))


play_label.bind(
	"<Button-1>",
	diff)

#-------------------------------------------------------SETTING--------------------------------------------------------------------

set_img = ctk.CTkImage(
        light_image = Image.open(resource_path(img("set.png"))),
        dark_image = Image.open(resource_path(img("set.png"))),
        size = (180,42))

set_label = ctk.CTkLabel(
        bg_label,
        image = set_img,
        text="")
set_label.place(relx=0.3, rely=0.65, anchor = "center")

music_enabled = True

def set_window():

	play_click()

	global set_win 

	if set_win is not None and set_win.winfo_exists():
		set_win.focus_force()
		set_win.lift()
		return

	set_win = ctk.CTkToplevel()
	set_win.title("SETTINGS")
	set_win.geometry("432x300")

	def close_set():
		global set_win
		set_win.destroy()
		set_win = None
	
	set_win.protocol("WM_DELETE_WINDOW", close_set)

	set_win_img = ctk.CTkImage(
        light_image = Image.open(resource_path(img("set.jpeg"))),
        dark_image = Image.open(resource_path(img("set.jpeg"))),
        size = (432,300)
	)

	set_win_label = ctk.CTkLabel(
		set_win,
		image = set_win_img,
		text="")

	set_win_label.place(x=0, y=0, relwidth=1, relheight=1)

	set_win_label.image = set_win_img

	vol_img = ctk.CTkImage(
        	light_image = Image.open(resource_path(img("vol.jpeg"))),
        	dark_image = Image.open(resource_path(img("vol.jpeg"))),
        	size = (128.4,30))


	vol_label = ctk.CTkLabel(
        	set_win_label,
        	image = vol_img,
        	text="")
	vol_label.place(relx=0.25, rely=0.55, anchor = "center")

	def update_vol(value):
                pygame.mixer.music.set_volume(float(value)/100)


	volume_slider = ctk.CTkSlider(
                set_win,
                from_=0,
                to = 100,
                command = update_vol)
	volume_slider.place(relx = 0.65, rely = 0.55, anchor = "center")


	music_img = ctk.CTkImage(
                light_image = Image.open(resource_path(img("mu.jpeg"))),
                dark_image = Image.open(resource_path(img("mu.jpeg"))),
                size = (128.4,30))

	music_label = ctk.CTkLabel(
                set_win_label,
                image = music_img,
                text="")
	music_label.place(relx=0.25, rely=0.65, anchor = "center")


	on_img = ctk.CTkImage(
                light_image = Image.open(resource_path(img("on.jpeg"))),
                dark_image = Image.open(resource_path(img("on.jpeg"))),
                size = (128.4,30))

	on_label = ctk.CTkLabel(
                set_win_label,
                image = on_img,
                text="")
	on_label.place(relx=0.65, rely=0.65, anchor = "center")

	off_img = ctk.CTkImage(
                light_image = Image.open(resource_path(img("off.jpeg"))),
                dark_image = Image.open(resource_path(img("off.jpeg"))),
                size = (128.4,30))

	def toggle_music(event):
		global music_enabled

		if music_enabled:
			pygame.mixer.music.pause()
			on_label.configure(
				image=off_img)
			music_enabled = False

		else:
			pygame.mixer.music.unpause()
			on_label.configure(
				image=on_img)
			music_enabled = True

	on_label.bind(
		"<Button-1>",
		toggle_music)

set_label.bind(
        "<Button-1>",
	lambda e: set_window())

#--------------------------------------------------------EXIT-----------------------------------------------------------------------

exit_img = ctk.CTkImage(
        light_image = Image.open(resource_path(img("exit.png"))),
        dark_image = Image.open(resource_path(img("exit.png"))),
        size = (180,42))

def exit_game(event):
	play_click()
	app.destroy()

exit_label = ctk.CTkLabel(
        bg_label,
        image = exit_img,
        text="")
exit_label.place(relx=0.3, rely=0.8, anchor = "center")

exit_label.bind(
        "<Button-1>",
        exit_game
)



def update_rank():

    global rank

    cursor.execute("""
    SELECT total_score
    FROM player
    WHERE id = 1
    """)

    total_score = cursor.fetchone()[0]


    if total_score < 25:
        rank = "NEWBIE"

    elif total_score < 100:
        rank = "EXPERIENCED"

    elif total_score < 300:
        rank = "MASTER"

    else:
        rank = "GRAND MASTER"


    cursor.execute("""
    UPDATE player
    SET rank = ?
    WHERE id = 1
    """, (rank,))

    conn.commit()


app.mainloop()
