import tkinter as tk
from tkinter import messagebox
from EDMBank_register import EDMBankRegister
from EDMBank_keyboard import AlphaNumericKeyboard
from services.bank_service import BankService
from ui_utils import UIHelper
from PIL import Image, ImageTk
import os

class EDMBankLogin:
    def __init__(self, main, on_success_callback, bank_service: BankService):
        self.main = main
        self.main.title("EDM Bank - Login")
        self.on_success_callback = on_success_callback
        self.bank_service = bank_service

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

        self.ui = UIHelper(initial_width, initial_height)

        # password and field state
        self.active_field = 'username'
        
        # Store a reference to the image to prevent it from being garbage collected
        self.logo_image = None 

        # main container
        self.main_container = tk.Frame(self.main, bg="#354f52")
        self.main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Keypad container (will hold either numeric or alphanumeric keyboard)
        self.keyboard_container = tk.Frame(self.main_container, bg="#354f52")
        
        self.alphanum_frame = tk.Frame(self.keyboard_container, bg="#354f52")
        
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
            # Build a reliable path to the image file
            script_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(script_dir, "logoo.png")
            
            # load and resize the image
            original_image = Image.open(image_path)
            
            # using a proportional width for the logo (50% of screen width)
            target_width = self.ui.w_pct(50)
            aspect_ratio = original_image.height / original_image.width
            target_height = int(target_width * aspect_ratio)

            # use Image.LANCZOS (high quality resampling)
            resized_image = original_image.resize((target_width, target_height), Image.LANCZOS)
            
            # keep a reference to prevent garbage collection
            self.logo_image = ImageTk.PhotoImage(resized_image)

            # create a Label to display the image
            logo_label = tk.Label(self.main_container, image=self.logo_image, bg="#354f52")
            logo_label.pack(pady=(self.ui.h_pct(2), self.ui.h_pct(2)))

        except FileNotFoundError:
            # fallback in case the image is not found
            logo_label = tk.Label(self.main_container, text="EDM Bank", 
                                 font=self.ui.get_font('Arial', 40, 'bold'), bg="#354f52", fg="white")
            logo_label.pack(pady=(self.ui.h_pct(5), self.ui.h_pct(3)))
            messagebox.showwarning("Warning", "Logo image 'logoo.png' not found. Using text fallback.", parent=self.main)
        except Exception as e:
            # fallback for other errors (e.g., PIL not installed)
            logo_label = tk.Label(self.main_container, text="EDM Bank", 
                                 font=self.ui.get_font('Arial', 40, 'bold'), bg="#354f52", fg="white")
            logo_label.pack(pady=(self.ui.h_pct(5), self.ui.h_pct(3)))
            messagebox.showwarning("Warning", f"Could not load logo: {e}. Using text fallback.", parent=self.main)

        # username frame
        username_frame = tk.Frame(self.main_container, bg="#354f52")
        username_frame.pack(pady=self.ui.h_pct(2), fill='x', padx=self.ui.w_pct(9))
        tk.Label(username_frame, text="Username:", font=self.ui.get_font('Tex Gyre Chorus', 40), 
                 bg="#354f52", fg="white").pack(anchor='w')
        
        # type username box
        self.username_entry = tk.Entry(username_frame, font=self.ui.get_font('Courier', 25), 
                                       bg='#2f3e46', fg='white', relief='flat')
        self.username_entry.pack(fill='x', pady=(self.ui.h_pct(1), 0), ipady=self.ui.h_pct(0.8))
        
        # bind FocusIn to show alphanumeric keyboard
        self.username_entry.bind("<FocusIn>", lambda e: self.set_active_field('username'))
        
        # Enter Password for the box
        password_display_frame = tk.Frame(self.main_container, bg="#354f52")
        password_display_frame.pack(pady=self.ui.h_pct(2), fill='x', padx=self.ui.w_pct(9))
        tk.Label(password_display_frame, text="Enter Password:", font=self.ui.get_font('Tex Gyre Chorus', 40), 
                 bg="#354f52", fg="white").pack(anchor='w')
        # password entry
        self.password_entry = tk.Entry(password_display_frame, font=self.ui.get_font('Courier', 25), 
                                       bg='#2f3e46', fg='white', relief='flat', show="*")
        self.password_entry.pack(fill='x', pady=(self.ui.h_pct(1), 0), ipady=self.ui.h_pct(0.8))
        
        # bind FocusIn to show alphanumeric keyboard
        self.password_entry.bind("<FocusIn>", lambda e: self.set_active_field('password'))
        self.password_entry.bind("<Return>", lambda e: self.check_password())
        
        # initialize alphanumeric keyboard (must be done after username_entry is created)
        self.alphanum_keyboard = AlphaNumericKeyboard(self.alphanum_frame, self.username_entry, self.ui)
        
        # register button added BEFORE the keypad frame
        register_btn = tk.Button(self.main_container, text="Don't have an account? Register here", 
                                 font=self.ui.get_font('Courier', 20, 'bold'), bg="#354f52", fg="white", 
                                 relief='flat', command=self.open_register_window)
        register_btn.pack(pady=(self.ui.h_pct(2), self.ui.h_pct(5)))

    # --------------------------------------------------------------------------
 
    # manage keyboard visibility
    def set_active_field(self, field_name):
        self.active_field = field_name
        
        # hide both frames first
        self.alphanum_frame.pack_forget()
        
        # reset visual state
        if hasattr(self, 'password_entry'):
            self.password_entry.config(relief='flat')
        self.username_entry.config(relief='flat') 
        
        target_entry = None
        if field_name == 'password':
            target_entry = self.password_entry
        elif field_name == 'username':
            target_entry = self.username_entry
            
        if target_entry:
            self.alphanum_keyboard.target_entry = target_entry
            self.alphanum_frame.pack(fill='both', expand=True)
            target_entry.focus_set()
            target_entry.config(relief='sunken')
            
    # hides all keyboards
    def hide_keyboards(self):
        self.alphanum_frame.pack_forget()
        self.password_entry.config(relief='flat')
        self.username_entry.config(relief='flat')
        self.active_field = None # no field is active
    
    # --------------------------------------------------------------------------

    def check_password(self):
        self.hide_keyboards() # hide keyboards on login attempt
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username:
            messagebox.showerror("Error", "Please enter a username!", parent=self.main)
            self.set_active_field('username')
            return
        
        if self.bank_service.checkUserLogin(username, password):
            self.main.withdraw()
            user = self.bank_service.get_user(username)
            self.on_success_callback(user, self.main, self.bank_service)
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password!", parent=self.main)
            self.password_entry.delete(0, tk.END)
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
        
        EDMBankRegister(register_root, self.main, self.on_success_callback, self.bank_service)