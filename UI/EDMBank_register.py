import random
import tkinter as tk
from tkinter import messagebox
from EDMBank_keyboard import AlphaNumericKeyboard 
from services.bank_service import BankService
from user_management.user import User, UserCredentials, PaymentsHistory, Card
from ui_utils import UIHelper

class EDMBankRegister:


    def __init__(self, main, login_window, on_success_callback, bank_service: BankService):
        self.main = main
        self.main.title("EDM Bank - Register")
        self.login_window = login_window 
        self.on_success_callback = on_success_callback # Store the success callback
        self.bank_service = bank_service
        
        # Initialize UI Helper
        self.main.update_idletasks() # Ensure geometry is applied
        self.ui = UIHelper(self.main.winfo_width(), self.main.winfo_height())

        # variables for password management
        self.active_field = None 
        
        # main container
        self.main_container = tk.Frame(self.main, bg="#354f52")
        self.main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Keypad container (will hold either numeric or alphanumeric keyboard)
        self.keyboard_container = tk.Frame(self.main_container, bg="#354f52")
        
        # Separate frames for each keyboard type
        self.alphanum_frame = tk.Frame(self.keyboard_container, bg="#354f52")
        
        self.create_register_interface()

    # --------------------------------------------------------------------------

    # helper function to create standard text/email input field
    def create_entry_field(self, parent, label_text, field_name, label_font=('Arial', 14)):
        frame = tk.Frame(parent, bg="#354f52")
        frame.pack(pady=self.ui.h_pct(0.2), fill='x')
        
        # uses the passed label_font
        tk.Label(frame, text=label_text, font=label_font, 
                bg="#354f52", fg="white").pack(anchor='w')
        
        entry = tk.Entry(frame, font=self.ui.get_font('Courier', 16), 
                         bg='#2f3e46', fg='white', relief='flat')
        entry.pack(fill='x', pady=(self.ui.h_pct(0.2), 0), ipady=self.ui.h_pct(0.5))
        # Bind FocusIn to set active field and show alphanumeric keyboard
        entry.bind("<FocusIn>", lambda e, name=field_name: self.set_active_field(name))
        return entry
    
    # --------------------------------------------------------------------------

    # helper function to create password fields
    def create_password_field(self, parent, label_text, field_name, label_font=('Arial', 14)):
        container = tk.Frame(parent, bg="#354f52")
        container.pack(pady=self.ui.h_pct(0.2), fill='x')
        
        # uses the passed label_font
        tk.Label(container, text=label_text, font=label_font, 
                bg="#354f52", fg="white").pack(anchor='w')
        
        entry = tk.Entry(container, font=self.ui.get_font('Courier', 20), 
                         bg='#2f3e46', fg='white', relief='flat', show="*")
        entry.pack(fill='x', pady=(self.ui.h_pct(0.2), self.ui.h_pct(0.5)), ipady=self.ui.h_pct(0.5))
        
        # Bind FocusIn to select this field and show the alphanumeric keyboard
        entry.bind("<FocusIn>", lambda e, name=field_name: self.set_active_field(name))
        entry.bind("<Return>", lambda e: self.attempt_register())
        return entry, container
    
    # --------------------------------------------------------------------------
        
    def create_register_interface(self):
        # EDM Bank title
        title_label = tk.Label(self.main_container, text="Register Account", 
                              font=self.ui.get_font('Arial', 40, 'bold'), bg="#354f52", fg="white")
        title_label.pack(pady=(self.ui.h_pct(1), self.ui.h_pct(1)))
        
        # container for form elements
        self.form_frame = tk.Frame(self.main_container, bg="#354f52")
        self.form_frame.pack(fill='x', padx=self.ui.w_pct(5))

        # username input
        self.username_entry = self.create_entry_field(
            self.form_frame, 
            "Username:", 
            'username', 
            label_font=self.ui.get_font('Tex Gyre Chorus', 25)
        )

        # email input
        self.email_entry = self.create_entry_field(
            self.form_frame, 
            "Email:", 
            'email',
            label_font=self.ui.get_font('Tex Gyre Chorus', 25)
        )
        
        # password displays
        self.password_entry, self.password_container = self.create_password_field(
            self.form_frame, 
            "Password:", 
            'password',
            label_font=self.ui.get_font('Tex Gyre Chorus', 25)
        )

        self.confirm_password_entry, self.confirm_password_container = self.create_password_field(
            self.form_frame, 
            "Confirm Password:", 
            'confirm_password',
            label_font=self.ui.get_font('Tex Gyre Chorus', 25)
        )

        # initialize alphanumeric keyboard (must be done after entry widgets are created)
        self.alphanum_keyboard = AlphaNumericKeyboard(self.alphanum_frame, self.username_entry, self.ui)
        
        # Back to Login Button (positioned above the dynamic keyboard area)
        back_btn = tk.Button(self.main_container, text="← Back to Login", 
                             font=self.ui.get_font('Courier', 16, 'bold'), bg="#354f52", fg="#cad2c5", 
                             relief='flat', command=self.back_to_login)
        back_btn.pack(pady=(self.ui.h_pct(1), self.ui.h_pct(1)))
        
        # Pack the main keyboard container at the bottom
        self.keyboard_container.pack(fill='both', expand=True, padx=self.ui.w_pct(5))
        
        # Set initial focus to username and show alphanumeric keyboard
        self.username_entry.focus_set()
        self.set_active_field('username') 
        
    
    # --------------------------------------------------------------------------

    def set_active_field(self, field_name):
        self.active_field = field_name
        
        # hide both frames first
        self.alphanum_frame.pack_forget()
        
        # reset visual state of password fields
        if hasattr(self, 'password_entry'):
            self.password_entry.config(relief='flat')
            self.confirm_password_entry.config(relief='flat')
        
        # Reset visual state of entry fields
        self.username_entry.config(relief='flat')
        self.email_entry.config(relief='flat')
        
        target_entry = None
        if field_name == 'password':
            target_entry = self.password_entry
        elif field_name == 'confirm_password':
            target_entry = self.confirm_password_entry
        elif field_name == 'username':
            target_entry = self.username_entry
        elif field_name == 'email':
            target_entry = self.email_entry
            
        if target_entry:
            target_entry.config(relief='sunken')
            self.alphanum_keyboard.target_entry = target_entry
            self.alphanum_frame.pack(fill='both', expand=True)
            target_entry.focus_set()

    # ----------------------------------------------------------------------

    def attempt_register(self):
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

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
            self.password_entry.delete(0, tk.END)
            self.confirm_password_entry.delete(0, tk.END)
            self.set_active_field('password')
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
        
        # Refresh user from DB to ensure we have the hashed password
        # This prevents overwriting the hash with plain text if modify_user is called later
        user = self.bank_service.get_user(username)

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
        self.on_success_callback(user, self.login_window, self.bank_service)

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