import tkinter as tk
from tkinter import ttk, filedialog

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
        
        # track uploaded files
        self.uploaded_files = []
        self.temp_uploaded_files = []  # track files during upload session
        
        # set window size and center it
        window_width = 500
        window_height = 550
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
        
        # uploaded files display area (main screen)
        upload_display_frame = tk.Frame(self.root, bg=self.bg_color)
        upload_display_frame.pack(pady=(20, 10), fill=tk.BOTH, expand=True)
        
        # create a canvas and scrollbar for uploaded files in main screen
        self.main_canvas = tk.Canvas(upload_display_frame, bg=self.bg_color, highlightthickness=0, height=150)
        main_scrollbar = tk.Scrollbar(upload_display_frame, orient="vertical", command=self.main_canvas.yview)
        self.main_scrollable_frame = tk.Frame(self.main_canvas, bg=self.bg_color)
        
        self.main_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )
        
        self.main_canvas.create_window((0, 0), window=self.main_scrollable_frame, anchor="nw")
        self.main_canvas.configure(yscrollcommand=main_scrollbar.set)
        
        # frame to hold uploaded files in main screen
        self.main_files_frame = tk.Frame(self.main_scrollable_frame, bg=self.bg_color)
        self.main_files_frame.pack(fill=tk.BOTH, expand=True)
        
        self.main_canvas.pack(side="left", fill=tk.BOTH, expand=True)
        main_scrollbar.pack(side="right", fill="y")
        
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
        
        # frame to hold generate, options, and upload buttons side by side
        generate_frame = tk.Frame(self.root, bg=self.bg_color)
        generate_frame.pack(side="bottom")
        
        # options button (⚙︎)
        options_button = tk.Button(
            generate_frame,
            text="⚙︎",
            command=lambda: print("options"),
            bg=self.button_bg,
            fg=self.button_fg,
            font=("Roboto", 12),
            width=2,
            height=1
        )
        options_button.pack(side="left", padx=5)
        
        # generate button (initially disabled)
        self.generate_button = tk.Button(
            generate_frame,
            text="Generate",
            command=lambda: print("generate"),
            bg="#cccccc",   # gray when disabled
            fg=self.button_fg,
            font=("Roboto", 12, "bold"),
            width=15,
            height=2,
            state="disabled"
        )
        self.generate_button.pack(side="left", padx=5)
        
        # upload button (+)
        upload_button = tk.Button(
            generate_frame,
            text="+",
            command=lambda: self._open_upload_window(),
            bg=self.button_bg,
            fg=self.button_fg,
            font=("Roboto", 12, "bold"),
            width=2,
            height=1
        )
        upload_button.pack(side="right", padx=5)
        
        # upload status label
        self.upload_status_label = tk.Label(
            self.root,
            text="No files uploaded.\nClick the '+' button to upload a file.",
            font=("Roboto", 10),
            fg=self.text_color,
            bg=self.bg_color
        )
        self.upload_status_label.pack(side="bottom", pady=(40, 10))

    def _open_upload_window(self):
        """
        Open a new window for file upload functionality.
        
        This window allows users to upload multiple files, displays them
        in a scrollable area, and provides delete functionality for each file.
        """
        upload_window = tk.Toplevel(self.root)
        upload_window.title("Upload Files")
        upload_window.configure(bg=self.bg_color)
        
        # set window size and position
        upload_width = 500
        upload_height = 600
        upload_window.geometry(f'{upload_width}x{upload_height}')
        
        # title label for upload window
        upload_title = tk.Label(
            upload_window,
            text="Upload Files for Text Extraction",
            font=("Roboto", 16, "bold"),
            fg=self.text_color,
            bg=self.bg_color
        )
        upload_title.pack(pady=20)
        
        # upload button
        upload_button = tk.Button(
            upload_window,
            text="Browse Files",
            command=lambda: self._upload_files(upload_window, file_display_frame, files_frame, clear_button),
            bg=self.button_bg,
            fg=self.button_fg,
            font=("Roboto", 11, "bold"),
            width=15,
            height=2
        )
        upload_button.pack(pady=10)
        
        # file display area
        file_display_frame = tk.Frame(upload_window, bg=self.bg_color)
        file_display_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # create a canvas and scrollbar for multiple files
        canvas = tk.Canvas(file_display_frame, bg=self.bg_color, highlightthickness=0)
        scrollbar = tk.Scrollbar(file_display_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # frame to hold uploaded files
        files_frame = tk.Frame(scrollable_frame, bg=self.bg_color)
        files_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas.pack(side="left", fill=tk.BOTH, expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # initialize temp_uploaded_files with current uploaded files
        self.temp_uploaded_files = self.uploaded_files.copy()
        
        # display existing uploaded files
        for file_path in self.temp_uploaded_files:
            self._display_uploaded_file(files_frame, file_path)
        
        # clear button
        clear_button = tk.Button(
            upload_window,
            text="Clear",
            command=lambda: self._clear_uploaded_files(files_frame, clear_button),
            bg="#ff6b6b",   # red background
            fg="white",
            font=("Roboto", 11, "bold"),
            width=7,
            height=1,
            state="disabled" if len(self.temp_uploaded_files) == 0 else "normal"
        )
        clear_button.pack(pady=(10, 5))
        
        # done button
        done_button = tk.Button(
            upload_window,
            text="Done",
            command=lambda: self._close_upload_window(upload_window),
            bg=self.button_bg,
            fg=self.button_fg,
            font=("Roboto", 11, "bold"),
            width=10,
            height=2
        )
        done_button.pack(pady=(0, 20))
    
    def _upload_files(self, upload_window, file_display_frame, files_frame, clear_button):
        """
        Handle file upload and display uploaded files.
        
        Args:
            upload_window (tk.Toplevel): The upload window instance.
            file_display_frame (tk.Frame): The frame containing the file display area.
            files_frame (tk.Frame): The frame where uploaded files will be displayed.
            clear_button (tk.Button): The clear button to update its state.
        """
        # open file dialog for multiple file selection
        file_paths = filedialog.askopenfilenames(
            title="Select files for text extraction",
            filetypes=[
                ("Text files", "*.txt"),
                ("PDF files", "*.pdf"),
                ("Word documents", "*.docx *.doc"),
                ("All files", "*.*")
            ]
        )
        
        if file_paths:
            # clear any existing files in the display
            for widget in files_frame.winfo_children():
                widget.destroy()
            
            # reset and populate temp list
            self.temp_uploaded_files = []
            for file_path in file_paths:
                self.temp_uploaded_files.append(file_path)
                self._display_uploaded_file(files_frame, file_path)
                
            # update clear button state
            self._update_clear_button_state(clear_button)
    
    def _display_uploaded_file(self, parent_frame, file_path):
        """
        Display a single uploaded file with delete button.
        
        Args:
            parent_frame (tk.Frame): The parent frame to display the file in.
            file_path (str): The path of the uploaded file.
        """
        file_frame = tk.Frame(parent_frame, bg=self.bg_color)
        file_frame.pack(fill=tk.X, pady=5, padx=10)
        
        # get just the filename from the path
        file_name = file_path.split("/")[-1]
        
        # file name label
        file_label = tk.Label(
            file_frame,
            text=file_name,
            font=("Roboto", 10),
            fg=self.text_color,
            bg=self.bg_color,
            anchor="w"
        )
        file_label.pack(side="left", padx=(0, 10))
        
        # delete button
        delete_button = tk.Button(
            file_frame,
            text="Delete",
            command=lambda f=file_path, frame=file_frame: self._delete_file(f, frame),
            bg="#ff6b6b",   # light red
            fg="white",
            font=("Roboto", 9),
            width=6
        )
        delete_button.pack(side="right")
        
        # success indicator (green dot)
        success_indicator = tk.Label(
            file_frame,
            text="●",
            font=("Roboto", 12),
            fg="#4CAF50",   # green
            bg=self.bg_color
        )
        success_indicator.pack(side="right", padx=(0, 10))
        
    def _delete_temp_file(self, file_path, file_frame):
        """
        Delete a file from the temp uploaded files list and remove its display.
        
        Args:
            file_path (str): The path of the file to delete.
            file_frame (tk.Frame): The frame containing the file display.
        """
        if file_path in self.temp_uploaded_files:
            self.temp_uploaded_files.remove(file_path)
            file_frame.destroy()
            
    def _clear_uploaded_files(self, files_frame, clear_button):
        """
        Clear all uploaded files from the upload window.
        
        Args:
            files_frame (tk.Frame): The frame containing the uploaded files.
            clear_button (tk.Button): The clear button to update its state.
        """
        # Clear the temp uploaded files list
        self.temp_uploaded_files = []
        
        # Remove all file display widgets
        for widget in files_frame.winfo_children():
            widget.destroy()
        
        # Update clear button state
        self._update_clear_button_state(clear_button)
    
    def _update_clear_button_state(self, clear_button):
        """
        Update the state of the clear button based on uploaded files.
        
        Args:
            clear_button (tk.Button): The clear button to update.
        """
        if len(self.temp_uploaded_files) == 0:
            clear_button.config(state="disabled")
        else:
            clear_button.config(state="normal")
            
    def _update_upload_status(self):
        """
        Update the upload status label in the main window.
        Also update the state of the generate button and the main display.
        """
        # clear existing files in main display
        for widget in self.main_files_frame.winfo_children():
            widget.destroy()
        
        if len(self.uploaded_files) == 0:
            self.upload_status_label.config(text="No files uploaded.\nClick the '+' button to upload a file.")
            # disable generate button
            self.generate_button.config(
                state="disabled",
                bg="#cccccc",
                fg="gray"
            )
        else:
            file_count = len(self.uploaded_files)
            plural = "s" if file_count > 1 else ""
            self.upload_status_label.config(text=f"{file_count} file{plural} uploaded.")
            # enable generate button
            self.generate_button.config(
                state="normal",
                bg=self.button_bg,
                fg=self.button_fg
            )
            
            # display uploaded files in main screen
            for file_path in self.uploaded_files:
                self._display_uploaded_file_main(self.main_files_frame, file_path)
                
    def _display_uploaded_file_main(self, parent_frame, file_path):
        """
        Display a single uploaded file with delete button in main screen.
        
        Args:
            parent_frame (tk.Frame): The parent frame to display the file in.
            file_path (str): The path of the uploaded file.
        """
        file_frame = tk.Frame(parent_frame, bg=self.bg_color)
        file_frame.pack(fill=tk.X, pady=2, padx=10)
        
        # get just the filename from the path
        file_name = file_path.split("/")[-1]
        
        # file name label
        file_label = tk.Label(
            file_frame,
            text=file_name,
            font=("Roboto", 9),
            fg=self.text_color,
            bg=self.bg_color,
            anchor="w"
        )
        file_label.pack(side="left", padx=(0, 10))
        
        # delete button
        delete_button = tk.Button(
            file_frame,
            text="Delete",
            command=lambda f=file_path, frame=file_frame: self._delete_file_main(f, frame),
            bg="#ff6b6b",   # light red
            fg="white",
            font=("Roboto", 8),
            width=5
        )
        delete_button.pack(side="right")
        
        # success indicator (green dot)
        success_indicator = tk.Label(
            file_frame,
            text="●",
            font=("Roboto", 10),
            fg="#4CAF50",   # green
            bg=self.bg_color
        )
        success_indicator.pack(side="right", padx=(0, 10))
                
    def _delete_file_main(self, file_path, file_frame):
        """
        Delete a file from the main uploaded files list and remove its display.
        
        Args:
            file_path (str): The path of the file to delete.
            file_frame (tk.Frame): The frame containing the file display.
        """
        if file_path in self.uploaded_files:
            self.uploaded_files.remove(file_path)
            file_frame.destroy()
            self._update_upload_status()
    
    def _close_upload_window(self, upload_window):
        """
        Close the upload window and update the main window status.
        
        Args:
            upload_window (tk.Toplevel): The upload window to close.
        """
        # update main uploaded_files with temp files
        self.uploaded_files = self.temp_uploaded_files.copy()
        upload_window.destroy()
        self._update_upload_status()

def main():
    root = tk.Tk()
    app = ExamAIGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()