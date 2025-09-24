from PIL import Image, ImageTk

class ResizeManager:
  def __init__(self, root, board_frame, sidebar_frame, squares, original_colors, piece_images, update_callback, board_ratio=0.8):
    self.root = root
    self.board_frame = board_frame
    self.sidebar_frame = sidebar_frame
    self.squares = squares
    self.original_colors = original_colors
    self.piece_images = piece_images
    self.update_callback = update_callback
    self.board_ratio = board_ratio
    self._last_cell_size = None
    self._resize_job = None
    # Whenever the window is resized tkinter sends a <Configure> event, which calls the enforce_aspect method, this allows enforce aspect to run constantly when resizing a window
    self.root.bind("<Configure>", self._enforce_aspect)

  def _enforce_aspect(self, event=None):
    total_width = self.root.winfo_width()
    total_height = self.root.winfo_height()

    #Calculating aspect ratio
    board_ratio = 0.8
    target_ratio = (1 / board_ratio)

    # compute what width should be for the current height, then picks whichever adjustment is closer to the actual size to the target ratio
    expected_width = int(total_height * target_ratio)
    expected_height = int(total_width / target_ratio)

    
    if abs(expected_width - total_width) < abs(expected_height - total_height):
      new_width, new_height = expected_width, total_height
    else:
      new_width, new_height = total_width, expected_height

    # if the size is off by more than 2 pixels, it corrects by setting the new geometry
    if abs(new_width - total_width) > 2 or abs(new_height - total_height) > 2:
      self.root.geometry(f"{new_width}x{new_height}")


    #Board gets 80% of the window, sidebar gets the rest (20%)
    board_width = int(new_width * board_ratio)
    sidebar_width = new_width - board_width
    self.sidebar_frame.config(width=sidebar_width)

    #Calculates cell sizes and configures the rows and columns to have this size
    cell_size = int(min(board_width, new_height) // 8)
    for i in range(8):
      self.board_frame.grid_rowconfigure(i, minsize=cell_size)
      self.board_frame.grid_columnconfigure(i, minsize=cell_size)

    #cancels any pending resize updates to prevent spam and schedules an update after 50ms
    if self._resize_job is not None:
      self.root.after_cancel(self._resize_job)
    if getattr(self, "initialized", False):
        self._resize_job = self.root.after(
            50, lambda: self.update_callback(preserve_highlights=True)
        )

  
  def resize_piece(self, row, col, piece, size):
    """Resize a piece image and apply it to the correct square"""
    if not piece or size <= 0:
      self.squares[row][col].config(image="", bg=self.original_colors[row][col])
      self.squares[row][col].image = None
      return

    #First time you resize, it loads the original images for all pieces and caches them, means you dont need to reload from the disk every time
    if not hasattr(self, "base_piece_images"):
      self.base_piece_images = {}
      for name, colours in self.piece_images.items():
        self.base_piece_images[name] = {}
        for colour in colours:
          path = f"Pieces/{colour}-{name.lower()}.png"
          self.base_piece_images[name][colour] = Image.open(path).convert("RGBA")

    #Takes the cached image and resizes for all current cell sizes, wraps in imagetk.photoimage so it can be used by tkinter
    img = self.base_piece_images[piece.name][piece.colour].resize((size, size), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img)
    self.squares[row][col].config(image=photo, bg=self.original_colors[row][col])
    self.squares[row][col].image = photo