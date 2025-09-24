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

    self.root.bind("<Configure>", self._enforce_aspect)

  def _enforce_aspect(self, event=None):
    total_width = self.root.winfo_width()
    total_height = self.root.winfo_height()


    board_ratio = 0.8
    target_ratio = (1 / board_ratio)

    # compute what width *should* be for this height
    expected_width = int(total_height * target_ratio)
    expected_height = int(total_width / target_ratio)

    # pick whichever is closer
    if abs(expected_width - total_width) < abs(expected_height - total_height):
      new_width, new_height = expected_width, total_height
    else:
      new_width, new_height = total_width, expected_height

    # enforce corrected geometry
    if abs(new_width - total_width) > 2 or abs(new_height - total_height) > 2:
      self.root.geometry(f"{new_width}x{new_height}")

    board_width = int(new_width * board_ratio)
    sidebar_width = new_width - board_width
    self.sidebar_frame.config(width=sidebar_width)

    cell_size = int(min(board_width, new_height) // 8)
    for i in range(8):
      self.board_frame.grid_rowconfigure(i, minsize=cell_size)
      self.board_frame.grid_columnconfigure(i, minsize=cell_size)
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

    if not hasattr(self, "base_piece_images"):
      # Cache the base piece images once
      self.base_piece_images = {}
      for name, colours in self.piece_images.items():
        self.base_piece_images[name] = {}
        for colour in colours:
          path = f"Pieces/{colour}-{name.lower()}.png"
          self.base_piece_images[name][colour] = Image.open(path).convert("RGBA")

    img = self.base_piece_images[piece.name][piece.colour].resize((size, size), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img)

    self.squares[row][col].config(image=photo, bg=self.original_colors[row][col])
    self.squares[row][col].image = photo