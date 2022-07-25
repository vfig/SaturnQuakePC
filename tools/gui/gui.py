import tkinter
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import messagebox
from os import listdir
from os.path import isfile, join

class main_display:

	#
	# funcs
	#

	def label(parent, text, font, justify, row, column, padx, pady, sticky, fgcolor, bgcolor):
		label = tkinter.Label(parent=parent, text=text, font=font, justify=justify, fg=fgcolor, bg=bgcolor)
		label.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)

	def choice_dialog(prompt, options):
		root = Tk()

		if prompt:
			Label(root, text=prompt).pack()

		v = IntVar()

		for i, option in enumerate(options):
			Radiobutton(root, text=option, variable=v, value=i).pack(anchor="w")

		Button(text="Submit", command=root.destroy).pack()

		root.mainloop()

		if v.get() == 0:
			return None
		else:
			return options[v.get()]

	#
	# main loop
	#

	def __init__(self, window, window_title, window_resolution):

		#
		# window setup
		#
		
		self.window = window
		self.window.title(window_title)
		self.window.geometry(window_resolution)
		self.window.resizable(False, False)
		self.window["background"] = "#171717"
		
		#
		# defs
		#
		
		# text styling
		self.font_header = "Arial 20 bold"
		self.font_subheader = "Arial 16 bold"
		self.font_body = "Arial 12"
		self.font_body_bold = "Arial 12 bold"
		self.font_small = "Arial 9"
		self.font_small_bold = "Arial 9 bold"

		#
		# main window
		#

		self.file_listbox = tkinter.Listbox(self.window, selectmode="single", width=35)
		self.file_listbox.grid(row=0, column=0, sticky="W, E, N, S")

		gameedir = filedialog.askdirectory(title="Select Game Directory")
		
		game = self.choice_dialog(prompt="Select Game", options=["Quake", "PowerSlave", "Duke Nukem 3D"])

		print("User's response was: {}".format(repr(game)))

		for f in listdir(gameedir):
			if isfile(join(gameedir, f)):
				self.file_listbox.insert(tkinter.END, f)

		#
		# window init
		#
		
		self.window.mainloop()


main_display(window=tkinter.Tk(), window_title="Lobotomy Software Suite", window_resolution="800x600")