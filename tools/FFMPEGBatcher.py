import tkinter as tk
from tkinter import filedialog
import glob
import subprocess

"""
useful flags
convert all to 10fps: -filter:v fps=10
add frame number overlay: -vf drawtext=fontfile=Arial.ttf:text=%{frame_num}:start_number=1:fontcolor=black:fontsize=32:box=1:boxcolor=white:boxborderw=10 -c:a copy
save as jpgs: -r 1/1 
(modified from https://stackoverflow.com/questions/15364861/frame-number-overlay-with-ffmpeg)
ffmpeg -r 1 -i file.mp4 -r 1 "$filename%03d.png
"""

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.pack()
		self.create_widgets()

	def create_widgets(self):
		
		self.flagsLabel = tk.Label(self, text="flags")
		self.flagsLabel.pack(side="top"); 
		self.flagsInput = tk.Entry(self, bd =5, width =100)
		self.flagsInput.insert(0, "-filter:v fps=10"); 
		self.flagsInput.pack(side="top"); 
		
		self.extLabel = tk.Label(self, text="input file ext")
		self.extLabel.pack(side="top"); 
		self.extInput = tk.Entry(self, bd =5)
		self.extInput.insert(0, ".mp4"); 
		self.extInput.pack(side="top"); 

		self.oprefLabel = tk.Label(self, text="output file prefix")
		self.oprefLabel.pack(side="top"); 
		self.oprefInput = tk.Entry(self, bd =5)
		self.oprefInput.insert(0, ""); 
		self.oprefInput.pack(side="top"); 		

		self.oextLabel = tk.Label(self, text="output file ext")
		self.oextLabel.pack(side="top"); 
		self.oextInput = tk.Entry(self, bd =5)
		self.oextInput.insert(0, ".mp4"); 
		self.oextInput.pack(side="top"); 
		
		self.selectButton = tk.Button(self)
		self.selectButton["text"] = "Select a folder"
		self.selectButton["command"] = self.SelectFolder
		self.selectButton.pack(side="top")
		
		self.runButton = tk.Button(self)
		self.runButton["text"] = "Run"
		self.runButton["command"] = self.RunProcess
		self.runButton.pack(side="top")
		
	def SelectFolder(self):
		self.folderSelected = filedialog.askdirectory()
		
		self.mp4files = []
		for file_ in glob.glob(self.folderSelected + "/*" + self.extInput.get() ):
			self.mp4files.append(file_)
		print(self.folderSelected) 
		for file_ in self.mp4files:
			print(file_)
			
	def RunProcess(self):
		print("Running process")
		for file_ in self.mp4files:
			print(file_)
			file_ =  file_.replace("\\","/")
			flags = self.flagsInput.get().split(" "); 
			fileNames = file_.split(".")
			
			commands = [
				"ffmpeg", 
				"-i",
				file_, 
			]+ flags + [
				self.oprefInput.get() + fileNames[0] + self.oextInput.get()
			]
			if subprocess.run(commands).returncode == 0:
				print ("FFmpeg Script Ran Successfully")
			else:
				print ("There was an error running your FFmpeg script")
			
		

root = tk.Tk()
root.title("FFMPEG Batcher"); 
app = Application(master=root)
app.mainloop()