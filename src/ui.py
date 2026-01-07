import tkinter as tk
from tkinter import ttk

class ExamAIGUI:
    """
    Main GUI class for the Exam AI application.

    This class creates a GUI with three buttons:
    generate, history, and options.
    """

    def __init__(self, root):
        """
        Initialize the Exam AI GUI.

        Args:
            root (tk.Tk): The root window of the tkinter application.
        """
        self.root = root
        self.root.title("Exam AI")
        
        # set window size and center it
        window_width = 500
        window_height = 500
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # configure theme colors
        self.bg_color = "#1e1e1e"  # dark gray
        self.button_bg = "ghostwhite"
        self.button_fg = "black"
        self.text_color = "white"
        
        # set background color
        root.configure(bg=self.bg_color)
        
        # create the UI widgets
        self._create_widgets()
    
    def _create_widgets(self):
        """
        Create all GUI widgets.
        """
        # main title label
        title_label = tk.Label(
            self.root,
            text="Exam AI",
            font=("Roboto", 24, "bold"),
            fg=self.text_color,
            bg=self.bg_color
        )
        title_label.pack(pady=(40,10))
        
        # description label
        description_label = tk.Label(
            self.root,
            text="Turn notes into practice.",
            font=("Roboto", 14),
            fg=self.text_color,
            bg=self.bg_color
        )
        description_label.pack()
        
        # frame to hold history and options buttons side by side
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(pady=(10,50), side="bottom")
        
        # history button
        history_button = tk.Button(
            button_frame,
            text="History",
            command=lambda: print("history"),
            bg=self.button_bg,
            fg=self.button_fg,
            font=("Roboto", 12, "bold"),
            width=10,
            height=2
        )
        history_button.pack(side="left", padx=5)
        
        # options button
        options_button = tk.Button(
            button_frame,
            text="Options",
            command=lambda: print("options"),
            bg=self.button_bg,
            fg=self.button_fg,
            font=("Roboto", 12, "bold"),
            width=10,
            height=2
        )
        options_button.pack(side="right", padx=5)
        
        # add some bottom padding
        tk.Frame(self.root, height=20, bg=self.bg_color).pack()
        
        # generate button
        generate_button = tk.Button(
            self.root,
            text="Generate",
            command=lambda: print("generate"),
            bg=self.button_bg,
            fg=self.button_fg,
            font=("Roboto", 12, "bold"),
            width=15,
            height=2
        )
        generate_button.pack(pady=10, side="bottom")

def main():
    root = tk.Tk()
    app = ExamAIGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()