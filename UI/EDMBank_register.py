import random
import tkinter as tk
from tkinter import messagebox
from EDMBank_keyboard import AlphaNumericKeyboard 
from services.bank_service import BankService
from user_management.user import User, UserCredentials, PaymentsHistory, Card

class EDMBankRegister:


    def __init__(self, main, login_window, on_success_callback, bank_service: BankService):
        self.main = main
        self.main.title("EDM Bank - Register")
        self.login_window = login_window 
        self.on_success_callback = on_success_callback # Store the success callback
        self.bank_service = bank_service
        
        # variables for password management
        self.entered_password = ""
        self.entered_confirm_password = ""
        self.active_field = None 
        
        # main container
        self.main_container = tk.Frame(self.main, bg="#354f52")
        self.main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Keypad container (will hold either numeric or alphanumeric keyboard)
        self.keyboard_container = tk.Frame(self.main_container, bg="#354f52")
        
        # Separate frames for each keyboard type
        self.numeric_frame = tk.Frame(self.keyboard_container, bg="#354f52")
        self.alphanum_frame = tk.Frame(self.keyboard_container, bg="#354f52")
        
        self.create_numeric_keypad(self.numeric_frame)
        
        self.create_register_interface()

    # --------------------------------------------------------------------------

    # helper function to create standard text/email input field
    def create_entry_field(self, parent, label_text, field_name, label_font=('Arial', 14)):
        frame = tk.Frame(parent, bg="#354f52")
        frame.pack(pady=10, fill='x')
        
        # uses the passed label_font
        tk.Label(frame, text=label_text, font=label_font, 
                bg="#354f52", fg="white").pack(anchor='w')
        
        entry = tk.Entry(frame, font=('Courier', 20), 
                         bg='#2f3e46', fg='white', relief='flat')
        entry.pack(fill='x', pady=(5, 0), ipady=12)
        # Bind FocusIn to set active field and show alphanumeric keyboard
        entry.bind("<FocusIn>", lambda e, name=field_name: self.set_active_field(name))
        return entry
    
    # --------------------------------------------------------------------------

    # helper function to create password fields
    def create_password_field(self, parent, label_text, field_name, label_font=('Arial', 14)):
        container = tk.Frame(parent, bg="#354f52")
        container.pack(pady=10, fill='x')
        
        # uses the passed label_font
        tk.Label(container, text=label_text, font=label_font, 
                bg="#354f52", fg="white").pack(anchor='w')
        
        display = tk.Label(container, text="", 
                           font=('Courier', 27), bg="#2f3e46", 
                           fg="white", height=1, anchor='w', padx=10)
        display.pack(fill='x', pady=(10, 20), ipady=12)
        # Bind click to select this field and show the numeric keypad
        display.bind("<Button-1>", lambda e, name=field_name: self.set_active_field(name))
        return display, container
    
    # --------------------------------------------------------------------------
        
    def create_register_interface(self):
        # EDM Bank title
        title_label = tk.Label(self.main_container, text="Register Account", 
                              font=('Arial', 60, 'bold'), bg="#354f52", fg="white")
        title_label.pack(pady=(30, 20))
        
        # container for form elements
        self.form_frame = tk.Frame(self.main_container, bg="#354f52")
        self.form_frame.pack(fill='x', padx=50)

        # username input
        self.username_entry = self.create_entry_field(
            self.form_frame, 
            "Username:", 
            'username', 
            label_font=('Tex Gyre Chorus', 40)
        )

        # email input
        self.email_entry = self.create_entry_field(
            self.form_frame, 
            "Email:", 
            'email',
            label_font=('Tex Gyre Chorus', 40)
        )
        
        # password displays
        self.password_display, self.password_container = self.create_password_field(
            self.form_frame, 
            "Password (6 digits):", 
            'password',
            label_font=('Tex Gyre Chorus', 40)
        )

        self.confirm_password_display, self.confirm_password_container = self.create_password_field(
            self.form_frame, 
            "Confirm Password:", 
            'confirm_password',
            label_font=('Tex Gyre Chorus', 40)
        )

        # initialize alphanumeric keyboard (must be done after entry widgets are created)
        self.alphanum_keyboard = AlphaNumericKeyboard(self.alphanum_frame, self.username_entry)
        
        # Back to Login Button (positioned above the dynamic keyboard area)
        back_btn = tk.Button(self.main_container, text="← Back to Login", 
                             font=('Courier', 20, 'bold'), bg="#354f52", fg="#cad2c5", 
                             relief='flat', command=self.back_to_login)
        back_btn.pack(pady=(10, 60))
        
        # Pack the main keyboard container at the bottom
        self.keyboard_container.pack(fill='both', expand=True, padx=50)
        
        # Set initial focus to username and show alphanumeric keyboard
        self.username_entry.focus_set()
        self.set_active_field('username') 
    
    # --------------------------------------------------------------------------
        
    def create_numeric_keypad(self, parent):
        # Configure grid for 4x3 keypad
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_columnconfigure(2, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)
        parent.grid_rowconfigure(2, weight=1)
        parent.grid_rowconfigure(3, weight=1)
        
        buttons = [
            ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
            ('⌫', 3, 0), ('0', 3, 1), ('↵', 3, 2)
        ]
        
        for text, row, col in buttons:
            if text == '↵':
                bg_color = '#588157'
                fg_color = 'white'
                command = self.attempt_register
                font_style = ('Courier', 27, 'bold')
            elif text == '⌫':
                bg_color = '#6f1d1b'
                fg_color = 'white'
                command = self.clear_active_password
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
            
    # ----------------------------------------------------------------------

    def set_active_field(self, field_name):
        self.active_field = field_name
        
        # hide both frames first
        self.numeric_frame.pack_forget()
        self.alphanum_frame.pack_forget()
        
        # reset visual state of password fields
        self.password_display.config(relief='flat', bg='#2f3e46')
        self.confirm_password_display.config(relief='flat', bg='#2f3e46')
        
        # Reset visual state of entry fields
        self.username_entry.config(relief='flat')
        self.email_entry.config(relief='flat')
        
        if field_name in ['password', 'confirm_password']:
            # highlight active field and show numeric keypad
            display = self.password_display if field_name == 'password' else self.confirm_password_display
            display.config(relief='sunken', bg='#2f3e46')
            self.numeric_frame.pack(fill='both', expand=True)
            self.main_container.focus_set()

        elif field_name in ['username', 'email']:
            # set target entry for alphanumeric keyboard and show it
            target_entry = self.username_entry if field_name == 'username' else self.email_entry
            target_entry.config(relief='sunken')
            self.alphanum_keyboard.target_entry = target_entry
            self.alphanum_frame.pack(fill='both', expand=True)
            target_entry.focus_set()

    def add_digit(self, digit):
        if self.active_field == 'password':
            if len(self.entered_password) < 6:
                self.entered_password += digit
        elif self.active_field == 'confirm_password':
            if len(self.entered_confirm_password) < 6:
                self.entered_confirm_password += digit
        else:
            messagebox.showwarning("Input Error", "Please click a Password field to enter digits.", parent=self.main)
            
        self.update_password_displays()

    def clear_active_password(self):
        # Clears the active password field
        if self.active_field == 'password':
            self.entered_password = ""
        elif self.active_field == 'confirm_password':
            self.entered_confirm_password = ""
            
        self.update_password_displays()
    
    def update_password_displays(self):
        # show dots for entered digits
        pass_text = "•" * len(self.entered_password)
        self.password_display.config(text=pass_text)
        
        confirm_pass_text = "•" * len(self.entered_confirm_password)
        self.confirm_password_display.config(text=confirm_pass_text)

    # ----------------------------------------------------------------------

    def attempt_register(self):
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.entered_password
        confirm_password = self.entered_confirm_password

        # check if all fields are completed
        if not all([username, email, password, confirm_password]):
            messagebox.showerror("Registration Error", "You must complete all the requested fields", parent=self.main)
            return
        
        # check if the username is unique
        if not self.bank_service.is_username_unique(username):
            messagebox.showerror("Registration Error", "This username is already taken.", parent=self.main)
            self.username_entry.focus_set()
            return

        # password match
        if password != confirm_password:
            messagebox.showerror("Registration Error", "You entered 2 different passwords", parent=self.main)
            self.clear_active_password()
            self.set_active_field('password')
            return
            
        # password length (keeping this standard check)
        if len(password) != 6:
            messagebox.showerror("Registration Error", "Password must be exactly 6 digits.", parent=self.main)
            return
            
        # email format
        if '@' not in email or '.' not in email:
            messagebox.showerror("Registration Error", "The entered email is not valid", parent=self.main)
            return

        # if all validations pass, proceed with registration
        credentials = UserCredentials(username, password, email)
        pay_history = PaymentsHistory()
        user_card = Card.generateCard()

        while (self.bank_service.is_card_unique(user_card.number) == False):
            user_card = Card.generateCard()

        user = User(credentials, 0, pay_history, user_card)
        self.bank_service.add_user(user)
        messagebox.showinfo("Registration Successful", 
                            f"Account created for {username} ({email}). Proceeding to main app.", 
                            parent=self.main)
        
        # transfer geometry from register window (self.main) to the hidden login window (self.login_window) before destroying self.main.
        self.main.update_idletasks()
        x = self.main.winfo_x()
        y = self.main.winfo_y()
        width = self.main.winfo_width()
        height = self.main.winfo_height()
        
        self.login_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # destroy registration window 
        self.main.destroy() 
        # call the success callback (which is start_main_app from launcher)
        self.on_success_callback(username.upper(), self.login_window, self.bank_service)

    def back_to_login(self):
        # capture size/position of registration window
        self.main.update_idletasks()
        x = self.main.winfo_x()
        y = self.main.winfo_y()
        width = self.main.winfo_width()
        height = self.main.winfo_height()

        # apply size/position to the hidden login window
        self.login_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # destroy the register window
        self.main.destroy() 
        # un-hide the login window
        self.login_window.deiconify()