import tkinter as tk
import customtkinter as ctk
from board import Board
from chessgui import chessGUI

class StartScreen(ctk.CTkFrame):
  def __init__(self,parent,controller):
    super().__init__(parent, fg_color="#2b2b2b")
    self.controller = controller

    ctk.CTkLabel(self, text="Welcome to Chess!", text_color="white", font=("Arial", 24)).pack(pady=40)

    ctk.CTkButton(self, text="Play", command=lambda: controller.show_frame("Game")).pack(pady=10)
    ctk.CTkButton(self, text="Settings", command=lambda: controller.show_frame("Settings")).pack(pady=10)
    ctk.CTkButton(self, text="Exit", command=controller.root.quit).pack(pady=10)

class SettingsScreen(ctk.CTkFrame):
  def __init__(self,parent,controller):
    super().__init__(parent, fg_color="#2b2b2b")
    self.controller = controller
    ctk.CTkLabel(self, text="Settings (WIP)", text_color="white", font=("Arial", 20)).pack(pady=20)
    ctk.CTkButton(self, text="Back", command=self.go_back).pack(pady=20)

  def go_back(self):
      if self.controller.previous_screen:
          self.controller.show_frame(self.controller.previous_screen)
      else:
          self.controller.show_frame("Start")

class ChessApp:
  def __init__(self,root):
    self.root = root
    self.root.title("Chess")
    self.root.geometry("1000x700")
    self.previous_screen = None
    self.container = ctk.CTkFrame(root)
    self.container.pack(fill="both", expand=True)

    self.frames = {}

    self.frames["Start"] = StartScreen(self.container, self)
    self.frames["Start"].pack(fill="both", expand=True)

    self.frames["Settings"] = SettingsScreen(self.container, self)

    game = Board()
    self.frames["Game"] = chessGUI(self.container, game, controller = self)
  

    self.show_frame("Start")

  def show_frame(self,name):
    if name == "Settings":
      if self.previous_screen != "Settings":
        self.previous_screen = self.current_screen
    self.current_screen = name

    for frame in self.frames.values():
      frame.pack_forget()
    frame = self.frames[name]
    frame.pack(fill="both", expand=True)

if __name__ == "__main__":
  root = ctk.CTk()
  app = ChessApp(root)
  root.mainloop()