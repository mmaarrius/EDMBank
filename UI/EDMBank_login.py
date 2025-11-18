import tkinter as tk
from tkinter import messagebox
from EDMBank_register import EDMBankRegister # Import the register class

class EDMBankLogin:
    def __init__(self, main, on_success_callback):
        self.main = main
        self.main.title("EDM Bank - Login")
        self.on_success_callback = on_success_callback
        
        # initial dimensions for mobile: FORMAT 9 X 16 - RESPONSIVE
        screen_width = main.winfo_screenwidth()
        screen_height = main.winfo_screenheight()
        
        # START WITH SMALLER SIZE THAT FITS ON SCREEN BUT KEEP 9:16 ASPECT RATIO
        max_width = min(990, screen_width)
        max_height = min(1760, screen_height - 100)

        # Calculate proportional size maintaining 9:16 aspect ratio
        if max_width / max_height > 9/16:
            initial_width = int(max_height * 9/16)
            initial_height = max_height
        else:
            initial_width = max_width
            initial_height = int(max_width * 16/9)
            
        # Center the window
        x = (screen_width - initial_width) // 2
        y = (screen_height - initial_height) // 2
        self.main.geometry(f"{initial_width}x{initial_height}+{x}+{y}")
        self.main.minsize(300, 500)
        self.main.configure(bg="#354f52")

        # password
        self.correct_password = "000000"
        self.entered_password = ""

        # main container
        self.main_container = tk.Frame(self.main, bg="#354f52")
        self.main_container.pack(fill='both', expand=True, padx=20, pady=20)
        # create login interface
        self.create_login_interface()
    
    # --------------------------------------------------------------------------
    
    def create_login_interface(self):
        # EDM Bank title
        title_label = tk.Label(self.main_container, text="EDM Bank", 
                              font=('Arial', 40, 'bold'), bg="#354f52", fg="white")
        title_label.pack(pady=(50, 30))

        # Secure Banking subtitle
        subtitle_label = tk.Label(self.main_container, text="Secure Banking",
                                 font=('Arial', 20), bg="#354f52", fg="#cad2c5")
        subtitle_label.pack(pady=(0, 50))

        # username frame
        username_frame = tk.Frame(self.main_container, bg="#354f52")
        username_frame.pack(pady=20, fill='x', padx=50)
        tk.Label(username_frame, text="Username:", font=('Arial', 16), 
                bg="#354f52", fg="white").pack(anchor='w')
        
        # type username box
        self.username_entry = tk.Entry(username_frame, font=('Arial', 16), 
                                      bg='white', fg='#2f3e46', relief='flat')
        self.username_entry.pack(fill='x', pady=(10, 0), ipady=8)
        # default username for testing
        self.username_entry.insert(0, "POPESCU IRIS-MARIA")
        self.username_entry.focus_set()
        
        # Enter Password for the box
        password_display_frame = tk.Frame(self.main_container, bg="#354f52")
        password_display_frame.pack(pady=30, fill='x', padx=50)
        tk.Label(password_display_frame, text="Enter Password:", font=('Arial', 16), 
                bg="#354f52", fg="white").pack(anchor='w')
        # password display (shows • for each entered digit)
        self.password_display = tk.Label(password_display_frame, text="", 
                                        font=('Arial', 24, 'bold'), bg="#2f3e46", 
                                        fg="white", width=15, height=2)
        self.password_display.pack(fill='x', pady=(10, 0))
        
        # register button added BEFORE the keypad frame
        register_btn = tk.Button(self.main_container, text="Don't have an account? Register here", 
                                font=('Arial', 12), bg="#354f52", fg="white", 
                                relief='flat', command=self.open_register_window)
        register_btn.pack(pady=(0, 20))

        # numeric keypad frame
        keypad_frame = tk.Frame(self.main_container, bg="#354f52")
        keypad_frame.pack(pady=30, fill='both', expand=True)

        # create 4x3 grid for keypad
        keypad_frame.grid_columnconfigure(0, weight=1)
        keypad_frame.grid_columnconfigure(1, weight=1)
        keypad_frame.grid_columnconfigure(2, weight=1)
        keypad_frame.grid_rowconfigure(0, weight=1)
        keypad_frame.grid_rowconfigure(1, weight=1)
        keypad_frame.grid_rowconfigure(2, weight=1)
        keypad_frame.grid_rowconfigure(3, weight=1)
        
        # keypad buttons (0-9, Clear, Enter)
        buttons = [
            ('1', 0, 0), ('2', 0, 1), ('3', 0, 2), # the other indices are row, column
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
            ('⌫', 3, 0), ('0', 3, 1), ('↵', 3, 2)
        ]
        
        for text, row, col in buttons:
            if text == '↵':
                bg_color = '#588157'
                fg_color = '#cad2c5'
                command = self.check_password
            elif text == '⌫':
                bg_color = '#6f1d1b'
                fg_color = '#cad2c5'
                command = self.clear_password
            else:
                bg_color = '#84a98c'
                fg_color = '#2f3e46'
                command = lambda x=text: self.add_digit(x)
            
            btn = tk.Button(keypad_frame, text=text, font=('Arial', 27, 'bold'),
                           bg=bg_color, fg=fg_color, relief='flat',
                           command=command)
            btn.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
    
    # add digit to entered password (max 6 digits)
    def add_digit(self, digit):
        if len(self.entered_password) < 6:
            self.entered_password = self.entered_password + digit
            self.update_password_display()

    # clear the entered password
    def clear_password(self):
        self.entered_password = ""
        self.update_password_display()
    
    # when digit pressed • appears
    def update_password_display(self):
        # show dots for entered digits
        display_text = "•" * len(self.entered_password)
        self.password_display.config(text=display_text)
    
    # --------------------------------------------------------------------------

    def check_password(self):
        # if password is correct call the success callback
        if self.entered_password == self.correct_password:
            # get username in uppercase without leading/trailing spaces
            username = self.username_entry.get().strip().upper()
            # if username written
            if username:
                self.main.withdraw()  # hide login window
                self.on_success_callback(username, self.main)
            else:
                messagebox.showerror("Error", "Please enter a username!", parent=self.main)
        else:
            messagebox.showerror("Login Failed", "Incorrect password or username! Please try again.", parent=self.main)
            self.clear_password()
  
    # --------------------------------------------------------------------------

    def open_register_window(self):
        # hide the login window
        self.main.withdraw() 
        
        # create a new top-level window for registration
        register_root = tk.Toplevel(self.main)
        
        # calculate size and position to match the login window
        self.main.update_idletasks()
        x = self.main.winfo_x()
        y = self.main.winfo_y()
        width = self.main.winfo_width()
        height = self.main.winfo_height()
        register_root.geometry(f"{width}x{height}+{x}+{y}")
        register_root.minsize(300, 500)
        
        EDMBankRegister(register_root, self.main, self.on_success_callback)