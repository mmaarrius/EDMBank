import tkinter as tk
from tkinter import messagebox
from EDMBank_register import EDMBankRegister
from EDMBank_keyboard import AlphaNumericKeyboard
from PIL import Image, ImageTk

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

        # password and field state
        self.correct_password = "000000"
        self.entered_password = ""
        self.active_field = 'username'
        
        # Store a reference to the image to prevent it from being garbage collected
        self.logo_image = None 

        # main container
        self.main_container = tk.Frame(self.main, bg="#354f52")
        self.main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Keypad container (will hold either numeric or alphanumeric keyboard)
        self.keyboard_container = tk.Frame(self.main_container, bg="#354f52")
        
        # Separate frames for each keyboard type
        self.numeric_frame = tk.Frame(self.keyboard_container, bg="#354f52")
        self.alphanum_frame = tk.Frame(self.keyboard_container, bg="#354f52")
        
        self.create_numeric_keypad(self.numeric_frame)
        
        # create login interface
        self.create_login_interface()
        
        # pack the main keyboard container at the bottom
        self.keyboard_container.pack(fill='both', expand=True, padx=50)
        
        # set initial focus and show the corresponding keyboard
        self.username_entry.focus_set()
        self.set_active_field('username')
    
    # --------------------------------------------------------------------------
    
    def create_login_interface(self):
        # EDM Bank title (REPLACED WITH IMAGE LOGO)
        try:
            # load and resize the image
            original_image = Image.open('logoo.png')
            
            # using a fixed width of 400px for the logo
            target_width = 400 
            aspect_ratio = original_image.height / original_image.width
            target_height = int(target_width * aspect_ratio)

            # use Image.LANCZOS (high quality resampling)
            resized_image = original_image.resize((target_width, target_height), Image.LANCZOS)
            
            # keep a reference to prevent garbage collection
            self.logo_image = ImageTk.PhotoImage(resized_image)

            # create a Label to display the image
            logo_label = tk.Label(self.main_container, image=self.logo_image, bg="#354f52")
            logo_label.pack(pady=(50, 30))

        except FileNotFoundError:
            # fallback in case the image is not found
            logo_label = tk.Label(self.main_container, text="EDM Bank", 
                                 font=('Arial', 40, 'bold'), bg="#354f52", fg="white")
            logo_label.pack(pady=(50, 30))
            messagebox.showwarning("Warning", "Logo image 'edm_bank_logo.gif' not found. Using text fallback.", parent=self.main)
        except Exception as e:
            # fallback for other errors (e.g., PIL not installed)
            logo_label = tk.Label(self.main_container, text="EDM Bank", 
                                 font=('Arial', 40, 'bold'), bg="#354f52", fg="white")
            logo_label.pack(pady=(50, 30))
            messagebox.showwarning("Warning", f"Could not load logo: {e}. Using text fallback.", parent=self.main)

        # username frame
        username_frame = tk.Frame(self.main_container, bg="#354f52")
        username_frame.pack(pady=40, fill='x', padx=50)
        tk.Label(username_frame, text="Username:", font=('Tex Gyre Chorus', 40), 
                 bg="#354f52", fg="white").pack(anchor='w')
        
        # type username box
        self.username_entry = tk.Entry(username_frame, font=('Courier', 25), 
                                       bg='#2f3e46', fg='white', relief='flat')
        self.username_entry.pack(fill='x', pady=(10, 0), ipady=8)
        # default username for testing
        self.username_entry.insert(0, "POPESCU IRIS-MARIA")
        
        # bind FocusIn to show alphanumeric keyboard
        self.username_entry.bind("<FocusIn>", lambda e: self.set_active_field('username'))
        
        # Enter Password for the box
        password_display_frame = tk.Frame(self.main_container, bg="#354f52")
        password_display_frame.pack(pady=30, fill='x', padx=50)
        tk.Label(password_display_frame, text="Enter Password:", font=('Tex Gyre Chorus', 40), 
                 bg="#354f52", fg="white").pack(anchor='w')
        # password display (shows • for each entered digit)
        self.password_display = tk.Label(password_display_frame, text="", 
                                         font=('Arial', 24, 'bold'), bg="#2f3e46", 
                                         fg="#cad2c5", width=15, height=2)
        self.password_display.pack(fill='x', pady=(10, 0))
        
        # bind click to show numeric keypad
        self.password_display.bind("<Button-1>", lambda e: self.set_active_field('password'))
        
        # initialize alphanumeric keyboard (must be done after username_entry is created)
        self.alphanum_keyboard = AlphaNumericKeyboard(self.alphanum_frame, self.username_entry)
        
        # register button added BEFORE the keypad frame
        register_btn = tk.Button(self.main_container, text="Don't have an account? Register here", 
                                 font=('Courier', 20, 'bold'), bg="#354f52", fg="white", 
                                 relief='flat', command=self.open_register_window)
        register_btn.pack(pady=(20,200))

    # --------------------------------------------------------------------------
 
    # manage keyboard visibility
    def set_active_field(self, field_name):
        self.active_field = field_name
        
        # hide both frames first
        self.numeric_frame.pack_forget()
        self.alphanum_frame.pack_forget()
        
        # reset visual state
        self.password_display.config(relief='flat', bg='#2f3e46')
        self.username_entry.config(relief='flat') 
        
        if field_name == 'password':
            # highlight active field and show numeric keypad
            self.password_display.config(relief='sunken', bg='#2f3e46')
            self.numeric_frame.pack(fill='both', expand=True)
            self.main_container.focus_set() # Remove focus from entry widget
            
        elif field_name == 'username':
            # set target entry for alphanumeric keyboard and show it
            self.alphanum_keyboard.target_entry = self.username_entry
            self.alphanum_frame.pack(fill='both', expand=True)
            self.username_entry.focus_set() # Keep focus on entry widget
            self.username_entry.config(relief='sunken')
            
    # hides all keyboards
    def hide_keyboards(self):
        self.numeric_frame.pack_forget()
        self.alphanum_frame.pack_forget()
        self.password_display.config(relief='flat')
        self.username_entry.config(relief='flat')
        self.active_field = None # no field is active
    
    # numeric keypad creation moved to a method
    def create_numeric_keypad(self, parent):
        # create 4x3 grid for keypad
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_columnconfigure(2, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)
        parent.grid_rowconfigure(2, weight=1)
        parent.grid_rowconfigure(3, weight=1)
        
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
                font_style = ('Courier', 27, 'bold')
            elif text == '⌫':
                bg_color = '#6f1d1b'
                fg_color = '#cad2c5'
                command = self.clear_password
                font_style = ('Courier', 27, 'bold')
            else:
                bg_color = '#84a98c'
                fg_color = '#2f3e46'
                command = lambda x=text: self.add_digit(x)
                font_style = ('Courier', 27, 'bold')
            
            btn = tk.Button(parent, text=text, font=font_style,
                            bg=bg_color, fg=fg_color, relief='flat',
                            command=command)
            btn.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
    
    # --------------------------------------------------------------------------

    # add digit to entered password (max 6 digits)
    def add_digit(self, digit):
        # only allow digit entry if password field is active
        if self.active_field == 'password':
            if len(self.entered_password) < 6:
                self.entered_password = self.entered_password + digit
                self.update_password_display()
        else:
            messagebox.showwarning("Input Error", "Please click the Password field to enter your PIN.", parent=self.main)

    # backspace functionality
    def backspace_password(self):
        if self.active_field == 'password':
            self.entered_password = self.entered_password[:-1]
            self.update_password_display()
        
    # clear the entered password (used for total clear, renamed for clarity)
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
        self.hide_keyboards() # hide keyboards on login attempt
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
                # If error, re-show username keyboard
                self.set_active_field('username')
        else:
            messagebox.showerror("Login Failed", "Incorrect password or username! Please try again.", parent=self.main)
            self.clear_password()
            # If error, re-show password keyboard
            self.set_active_field('password')
 
    # --------------------------------------------------------------------------

    def open_register_window(self):
        self.hide_keyboards() # hide keyboards before switching window
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