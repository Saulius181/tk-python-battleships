#!/usr/bin/env python

__author__ = "Saulius Bartkus"
__copyright__ = "Copyright 2017"

__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Saulius Bartkus"
__email__ = "saulius181@yahoo.com"
__status__ = "Production"

from tkinter import *
import random
EMPTY_COLOR = "white"

class game_controller(object):
	def start(self):
		if self.canvas.data["play"] == None:
			self.canvas.data["play"] = True
			self.currentDeploy = self.canvas.data["shipTypes"]["typeList"][0]
			self.deploy_state()
			
		elif self.canvas.data["play"] == False:
			pass
		else:
			pass

	def deploy_state(self):
		if self.canvas.data["shipTypes"][self.currentDeploy]["count"] != 0:
			self.canvas.data["stage"] = "deploy"
		else:
			nextIndex = self.canvas.data["shipTypes"]["typeList"].index(self.currentDeploy) + 1
			if nextIndex < len(self.canvas.data["shipTypes"]["typeList"]):
				self.currentDeploy = self.canvas.data["shipTypes"]["typeList"][nextIndex]
			else:
				self.canvas.data["stage"] = "play"
			
	
	def quit(self):
		self.root.destroy()
		
	def on_click1(self, event=None):
		if self.canvas.data["play"]:
			deploy_list = self.get_deploy_list()
			if self.canvas.data["stage"] == "deploy" and deploy_list["valid"]:
				_y = int( self.canvas.gettags(CURRENT)[2] )
				_x = int( self.canvas.gettags(CURRENT)[3] )
				
		
				if self.canvas.data["deployDir"] == "horizontal":
					for x in range(_x, _x + self.canvas.data["shipTypes"][self.currentDeploy]["size"]):

						self.canvas.itemconfig(self.canvas.data["playerBoard"][_y][x]["ref"], fill="#0000FF")
						self.canvas.data["playerBoard"][_y][x]["presence"] = self.currentDeploy
					self.canvas.data["shipTypes"][self.currentDeploy]["count"] -=1
					self.deploy_state()

				else:
					for y in range(_y, _y + self.canvas.data["shipTypes"][self.currentDeploy]["size"]):
						self.canvas.itemconfig(self.canvas.data["playerBoard"][y][_x]["ref"], fill="#0000FF")		
						self.canvas.data["playerBoard"][y][_x]["presence"] = self.currentDeploy				
					self.canvas.data["shipTypes"][self.currentDeploy]["count"] -=1
					self.deploy_state()
						
	def on_click3(self, event=None):
		if self.canvas.data["play"]:
			if self.canvas.data["deployDir"] == "horizontal":
				self.canvas.data["deployDir"] = "vertical"
			else:
				self.canvas.data["deployDir"] = "horizontal"
			self.redraw_board()

			
	def on_release(self, event=None):
		pass
		
	def on_enter(self, event=None):
		if self.canvas.data["play"]:
			if self.canvas.data["stage"] == "deploy" and "block" in self.canvas.gettags(CURRENT) and "player" in self.canvas.gettags(CURRENT):
				self.currentId = self.canvas.find_withtag(CURRENT)[0]
				self.redraw_board()

	def get_deploy_list(self):
		deploy_list = {}
		_y = int( self.canvas.gettags(CURRENT)[2] )
		_x = int( self.canvas.gettags(CURRENT)[3] )
		deploy_list["valid"] = True
		if self.canvas.data["deployDir"] == "horizontal":
			deploy_list[_y] = {}
			for x in range(_x, _x + self.canvas.data["shipTypes"][self.currentDeploy]["size"]):
				if x in self.canvas.data["playerBoard"][_y]:
					if self.canvas.data["playerBoard"][_y][x]["presence"] in self.canvas.data["shipTypes"]["typeList"]: 
						deploy_list[_y][x] = False
						deploy_list["valid"] = False
					else:
						deploy_list[_y][x] = True
				else:
					break
		else:
			for y in range(_y, _y + self.canvas.data["shipTypes"][self.currentDeploy]["size"]):		
				if y in self.canvas.data["playerBoard"]:
					deploy_list[y] = {}
					if self.canvas.data["playerBoard"][y][_x]["presence"] in self.canvas.data["shipTypes"]["typeList"]: 
						deploy_list[y][_x] = False
						deploy_list["valid"] = False
					else:
						deploy_list[y][_x] = True
				else:
					break
		
		return deploy_list
		
	def redraw_board(self):
		deploy_list = self.get_deploy_list()
		for y in range(0,10):
			for x in range(0,10):
				
				if y in deploy_list and x in deploy_list[y] and deploy_list[y][x] == False:
					self.canvas.itemconfig(self.canvas.data["playerBoard"][y][x]["ref"], fill="#FF0000")		
				elif y in deploy_list and x in deploy_list[y] and deploy_list[y][x] == True:
					self.canvas.itemconfig(self.canvas.data["playerBoard"][y][x]["ref"], fill="#AAAAFF")				
				elif self.canvas.data["playerBoard"][y][x]["presence"] in self.canvas.data["shipTypes"]["typeList"]:
					self.canvas.itemconfig(self.canvas.data["playerBoard"][y][x]["ref"], fill="#0000FF")	
				else:
					self.canvas.itemconfig(self.canvas.data["playerBoard"][y][x]["ref"], fill=EMPTY_COLOR)
				
	def on_leave(self, event=None):
		if self.canvas.data["play"]:
			if self.canvas.data["stage"] == "deploy" and self.currentId:
				self.redraw_board()							
				self.currentId = None
	
	def __init__(self, root):
		self.root = root
		self.canvas = Canvas(root, width=850, height=350)

		self.canvas.pack()	
		self.button1 = Button(self.canvas, text = "New game", anchor = W, command = self.start)
		self.button1.place(x=720,y=25)
		self.button2 = Button(self.canvas, text = "Quit", anchor = W, command = self.quit)
		self.button2.place(x=790,y=25)		
	
		self.canvas.bind("<Button-1>", self.on_click1)
		self.canvas.bind("<Button-3>", self.on_click3)
		self.canvas.bind("<ButtonRelease-1>", self.on_release)
		self.canvas.data = { }
		self.canvas.data["play"] = None
		self.canvas.data["stage"] = None
		self.canvas.data["deployDir"] = "horizontal"
		
		self.canvas.data["playerBoard"] = {}
		self.canvas.data["aiBoard"] = {}
		
		self.canvas.data["shipTypes"] = {}
		self.canvas.data["shipTypes"]["typeList"] = ["AircraftCarrier", "Battleship", "Cruiser", "Destroyer", "Frigate"]
		self.canvas.data["shipTypes"]["AircraftCarrier"] = {"size": 5, "count": 1}
		self.canvas.data["shipTypes"]["Battleship"] = {"size": 4, "count": 2}
		self.canvas.data["shipTypes"]["Cruiser"] = {"size": 3, "count": 3}
		self.canvas.data["shipTypes"]["Destroyer"] = {"size": 2, "count": 4}
		self.canvas.data["shipTypes"]["Frigate"] = {"size": 1, "count": 5}
		
		self.currentId = None	
		
		for y in range(0,10):
			self.canvas.data["playerBoard"][y] = {}
			for x in range(0,10):
				self.canvas.data["playerBoard"][y][x] = {}
				self.canvas.data["playerBoard"][y][x]["ref"] = self.canvas.create_rectangle(30+x*30, 30+y*30, 30+30+ x*30, 30+30 +y*30, fill=EMPTY_COLOR, tags="block player {} {}".format(y,x))
				self.canvas.data["playerBoard"][y][x]["presence"] = None
				self.canvas.tag_bind(self.canvas.data["playerBoard"][y][x]["ref"], "<Enter>", self.on_enter)
				self.canvas.tag_bind(self.canvas.data["playerBoard"][y][x]["ref"], "<Leave>", self.on_leave)	
		
		for y in range(0,10):
			self.canvas.data["aiBoard"][y] = {}
			for x in range(0,10):
				self.canvas.data["aiBoard"][y][x] = {}
				self.canvas.data["aiBoard"][y][x]["ref"] = self.canvas.create_rectangle(20+x*30 + 350, 30+y*30, 20+30+ x*30 + 350, 30+30 +y*30, fill=EMPTY_COLOR, tags="block ai {} {}".format(y,x))
				self.canvas.data["aiBoard"][y][x]["presence"] = None
				self.canvas.tag_bind(self.canvas.data["aiBoard"][y][x], "<Enter>", self.on_enter)
				self.canvas.tag_bind(self.canvas.data["aiBoard"][y][x], "<Leave>", self.on_leave)	

		self.text = self.canvas.create_text(740,10, text="Battleships", anchor='w')
				
if __name__ == "__main__":
	root = Tk()
	root.title("Battleships Tk")
	root.resizable(0,0)
	game = game_controller(root);
	root.mainloop()
