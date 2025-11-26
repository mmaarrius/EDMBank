import tkinter as tk
from tkinter import ttk, messagebox
import os
import random
from PIL import Image, ImageTk
from EDMBank_contact import EDMBankContact
import locale
from EDMBank_profile import EDMBankProfile 

class EDMBankApp:
    def __init__(self, main, relauch_login_callback=None): 
        self.main = main 
        self.main.title("EDM Bank")
        self.relauch_login_callback = relauch_login_callback 

        screen_width = main.winfo_screenwidth()
        screen_height = main.winfo_screenheight()
        
        max_width = min(990, screen_width)  
        max_height = min(1760, screen_height - 100)
        
        if max_width / max_height > 9/16:
            initial_width = int(max_height * 9/16)
            initial_height = max_height
        else:
            initial_width = max_width
            initial_height = int(max_width * 16/9)
            
        x = (screen_width - initial_width) // 2
        y = (screen_height - initial_height) // 2
        self.main.geometry(f"{initial_width}x{initial_height}+{x}+{y}")
        self.main.minsize(300, 500)
        self.main.configure(bg="#354f52")

        self.sold_visible = False
        self.card_data_visible = False
        self.sold_amount = "1.250,00 RON"
        self.is_large_screen = False
        self.logged_in_user = "POPESCU IRIS-MARIA"
        self.logged_in_user_email = f"{self.logged_in_user.lower().replace(' ', '').replace('-', '')}@edmbank.com"
        
        self.card_number = self.generate_card_number()
        self.card_cvv = f"{random.randint(0,999):03d}"
        self.card_expiry = "02/26"
        
        self.nav_images = []  
        self.top_logo_image = None
        self.card_background_image = None
        self.card_background_image_path = 'card.png' # Ensure this file exists
        self.card_image_item = None # Canvas item ID for the background image

        self.main_container = tk.Frame(self.main, bg="#354f52")
        self.main_container.pack(fill='both', expand=True, padx=10, pady=10)

        self.main_container.grid_rowconfigure(1, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        self.create_top_menu()
        self.create_main_content() 
        self.create_bottom_menu()

        self.main.bind('<Configure>', self.on_resize)

    # --------------------------------------------------------------------------

    def show_message(self, title, message, message_type="info"):
        self.main.update_idletasks()
        x = self.main.winfo_x() + self.main.winfo_width() // 2 - 150
        y = self.main.winfo_y() + self.main.winfo_height() // 2 - 75

        if message_type == "info":
            messagebox.showinfo(title, message, parent=self.main)
        elif message_type == "warning":
            messagebox.showwarning(title, message, parent=self.main)
        elif message_type == "error":
            messagebox.showerror(title, message, parent=self.main)

    # --------------------------------------------------------------------------

    def generate_card_number(self):
        digits = ''.join([str(random.randint(0, 9)) for _ in range(16)])
        return digits

    # --------------------------------------------------------------------------

    def format_card_number(self, number, show_full=False):
        if show_full:
            return ' '.join([number[i:i+4] for i in range(0, 16, 4)])
        else:
            return f"•••• •••• •••• {number[-4:]}"

    # --------------------------------------------------------------------------

    def on_resize(self, event):
        window_width = self.main.winfo_width()
        
        if str(event.widget) == '.':
            self.main.unbind('<Configure>')
        
        try:
            if hasattr(self, 'buttons_frame'):
                if hasattr(self, 'card_frame'):
                    if window_width > 600 and not self.is_large_screen:
                        self.switch_to_desktop_layout()
                        self.is_large_screen = True
                    elif window_width <= 600 and self.is_large_screen:
                        self.switch_to_mobile_layout()
                        self.is_large_screen = False
                    else:
                        self.update_card_background(rebind=False)
        finally:
             if str(event.widget) == '.':
                 self.main.bind('<Configure>', self.on_resize)

    # --------------------------------------------------------------------------

    def update_card_background(self, rebind=True):
        if rebind:
            self.main.unbind('<Configure>')

        if hasattr(self, 'card_background_image_path') and self.card_background_image_path:
             try:
                self.card_frame.update_idletasks() 
                card_width = self.card_frame.winfo_width()
                card_height = self.card_frame.winfo_height()

                if card_width <= 1: card_width = 400
                if card_height <= 1: card_height = 240

                original_card_image = Image.open(self.card_background_image_path)
                resized_card_image = original_card_image.resize((card_width, card_height), Image.LANCZOS)
                self.card_background_image = ImageTk.PhotoImage(resized_card_image)

                if self.card_image_item is None:
                    # Create the image item at the bottom of the stack (0,0)
                    self.card_image_item = self.card_frame.create_image(0, 0, image=self.card_background_image, anchor='nw')
                    self.card_frame.tag_lower(self.card_image_item) 
                else:
                    self.card_frame.itemconfig(self.card_image_item, image=self.card_background_image)
                
                padding = 20
                
                # Move text items to new coordinates
                self.card_frame.coords(self.text_bank, padding, padding)
                self.card_frame.coords(self.text_chip, card_width - padding, padding)
                self.card_frame.coords(self.text_number, card_width // 2, card_height // 2)
                self.card_frame.coords(self.text_holder, padding, card_height - padding)
                self.card_frame.coords(self.text_expiry, card_width - padding, card_height - padding)
                
             except Exception as e:
                 pass
        
        if rebind:
            self.main.bind('<Configure>', self.on_resize)

    # --------------------------------------------------------------------------

    def switch_to_desktop_layout(self):
        self.main.unbind('<Configure>')

        for widget in self.buttons_frame.winfo_children():
            widget.destroy()
        
        buttons_data = [
            ("$ TRANSFER", self.transfer),
            ("⇄ IBAN TRANSFER", self.transfer_iban),
            ("⎙ TRANSACTION HISTORY", self.transaction_history),
            ("⤾ ADD MONEY", self.add_money),
            ("ⓘ SHOW CARD DETAILS", self.toggle_card_data),
            ("✎ MAKE PAYMENT", self.make_payment),
            ("⚙︎ ACCOUNT SETTINGS", self.settings)
        ]
        
        for text, command in buttons_data:
            # use ttk.Button with the new 'MainAction.TButton' style
            btn = ttk.Button(self.buttons_frame, text=text, command=command, style='MainAction.TButton')
            btn.pack(fill='x', padx=10, pady=6)
        
        self.card_frame.configure(height=360, width=500)
        self.card_frame.grid_propagate(False)
        self.update_card_display()
        self.update_card_background() 
    
    # --------------------------------------------------------------------------

    def switch_to_mobile_layout(self):
        self.main.unbind('<Configure>')

        for widget in self.buttons_frame.winfo_children():
            widget.destroy()
        
        self.buttons_frame.grid_columnconfigure(0, weight=1)
        self.buttons_frame.grid_columnconfigure(1, weight=1)
        
        buttons_data = [
            ("$ TRANSFER", self.transfer, 0, 0),
            ("⇄ IBAN TRANSFER", self.transfer_iban, 0 , 1),
            ("⎙ TRANSACTION HISTORY", self.transaction_history, 1, 0),
            ("⤾ ADD MONEY", self.add_money, 1, 1),
            ("ⓘ SHOW CARD DETAILS", self.toggle_card_data, 2, 0),
            ("✎ MAKE PAYMENT", self.make_payment, 2, 1),
            ("⚙︎ ACCOUNT SETTINGS", self.settings, 3, 0)
        ]
        
        for text, command, row, col in buttons_data:
            # use ttk.Button with the new 'MainAction.TButton' style
            btn = ttk.Button(self.buttons_frame, text=text, command=command, style='MainAction.TButton')
            btn.grid(row=row, column=col, padx=6, pady=6, sticky='nsew')
        
        self.card_frame.configure(height=240, width=400)
        self.card_frame.grid_propagate(False)
        self.update_card_display()
        self.update_card_background() 

    # --------------------------------------------------------------------------

    def update_card_display(self):
        display_number = self.format_card_number(self.card_number, self.card_data_visible)
        self.card_frame.itemconfig(self.text_number, text=display_number)
        
        if self.card_data_visible:
            self.card_frame.itemconfig(self.text_holder, text=self.logged_in_user)
        else:
            self.card_frame.itemconfig(self.text_holder, text="POPESCU IRINA-MARIA")

    # --------------------------------------------------------------------------

    def create_top_menu(self):
        top_frame = tk.Frame(self.main_container, bg="#354f52", height=120)
        top_frame.grid(row=0, column=0, sticky='ew', padx=20, pady=10)
        top_frame.grid_propagate(False)
        top_frame.grid_columnconfigure(1, weight=1)

        style = ttk.Style()
        
        # configure style for main action buttons
        style.configure('MainAction.TButton',
                            font=('Courier', 20, 'bold'),
                            foreground='#2f3e46',
                            background='#52796f',
                            padding=20)
        style.map('MainAction.TButton',
                        background=[('active', '#84a98c')])
        
        style.theme_use('default') 
        style.configure("Green.TCombobox", 
                              fieldbackground="#ffffff",
                              background="#051f0b",
                              foreground='white',
                              selectbackground='#84a98c',
                              selectforeground='white',
                              font=('Courier', 26, 'bold'),
                              padding=10)

        style.map('Green.TCombobox', 
                      fieldbackground=[('readonly', '#52796f')],
                      background=[('readonly', '#84a98c')])
        
        self.main.option_add('*TCombobox*Listbox.font', ('Courier', 14))

        self.dropdown_var = tk.StringVar()
        self.dropdown_var.set("Menu")
        
        dropdown = ttk.Combobox(top_frame, textvariable=self.dropdown_var, 
                                     values=["Accounts", "Savings", "Settings", "Cards", "Payments"], 
                                     state="readonly", width=12, background='#52796f',
                                     style="Green.TCombobox")

        dropdown.grid(row=0, column=0, sticky='w', padx=(0, 10))
        dropdown.bind("<<ComboboxSelected>>", self.handle_dropdown_selection) 

        try:
            original_image = Image.open('logoo.png')
            target_height = 120
            aspect_ratio = original_image.width / original_image.height
            target_width = int(target_height * aspect_ratio)
            resized_image = original_image.resize((target_width, target_height), Image.LANCZOS)
            self.top_logo_image = ImageTk.PhotoImage(resized_image)
            title_label = tk.Label(top_frame, image=self.top_logo_image, bg="#354f52")
            title_label.grid(row=0, column=1, sticky='')
        except Exception:
            title_label = tk.Label(top_frame, text="EDM Bank", font=('Arial', 30, 'bold'),
                                     bg='#354f52', fg="#FFFFFF")
            title_label.grid(row=0, column=1, sticky='ew')

        login_btn = tk.Button(top_frame, text="LOGOUT", font=('Arial', 12, 'bold'), 
                              bg="#354f52", fg='white', relief='flat', padx=25,
                              height=2, command=self.logout_and_relaunch_login)
        login_btn.grid(row=0, column=2, sticky='e', padx=(10, 0))

    # --------------------------------------------------------------------------
    def handle_dropdown_selection(self, event):
        # this function handles the selection from the main top-left dropdown menu.
        selected = self.dropdown_var.get()

        if selected == "Accounts":
            self.logout_and_relaunch_login()
        elif selected == "Savings":
            self.show_message("Savings", "Manage your savings accounts", "info")
        elif selected == "Settings":
            self.settings()
        elif selected == "Cards":
            self.show_cards()
        elif selected == "Payments":
            self.make_payment()

        # reset the dropdown display text to 'Menu' after selection
        self.dropdown_var.set("Menu")

    # --------------------------------------------------------------------------

    def create_main_content(self):
        self.content_frame = tk.Frame(self.main_container, bg="#cad2c5")
        self.content_frame.grid(row=1, column=0, sticky='nsew', padx=20, pady=10)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.show_home_view()
        
    # --------------------------------------------------------------------------

    def show_home_view(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        self.content_frame.grid_rowconfigure(1, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        self.create_card(self.content_frame)

        sold_btn = tk.Button(self.content_frame, text="VIEW BALANCE", font=('Courier', 20, 'bold'),
                              bg='#52796f', fg='#ffffff', relief='flat',
                              height=3, command=self.toggle_sold)
        sold_btn.grid(row=1, column=0, sticky='ew', pady=15)

        self.sold_label = tk.Label(self.content_frame, text=self.sold_amount,
                                     font=('Arial', 20, 'bold'), bg='#cad2c5', fg='#2f3e46')
        self.sold_label.grid(row=2, column=0, pady=10)
        self.sold_label.grid_remove()
        
        self.buttons_frame = tk.Frame(self.content_frame, bg='#cad2c5')
        self.buttons_frame.grid(row=3, column=0, sticky='nsew', pady=20)
        
        current_width = self.main.winfo_width()
        if current_width > 600:
            self.switch_to_desktop_layout()
            self.is_large_screen = True
        else:
            self.switch_to_mobile_layout()
            self.is_large_screen = False
    
    # --------------------------------------------------------------------------

    def create_card(self, parent):
        self.card_frame = tk.Canvas(parent, bg="#2f3e46", highlightthickness=0)
        self.card_frame.grid(row=0, column=0, sticky='n', pady=20)
        
        self.card_background_image = None
        self.card_image_item = None 
        
        self.text_bank = self.card_frame.create_text(0, 0, text="EDM Bank", 
                                                     font=('Arial', 16, 'bold'), fill='white', anchor='nw')
        
        self.text_chip = self.card_frame.create_text(0, 0, text="◘ Chip", 
                                                     font=('Arial', 12), fill='white', anchor='ne')
        
        self.text_number = self.card_frame.create_text(0, 0, text=self.format_card_number(self.card_number), 
                                                         font=('Arial', 18, 'bold'), fill='white', anchor='center')
        
        self.text_holder = self.card_frame.create_text(0, 0, text="POPESCU IRINA-MARIA", 
                                                         font=('Arial', 12), fill='white', anchor='sw')
        
        self.text_expiry = self.card_frame.create_text(0, 0, text=self.card_expiry, 
                                                         font=('Arial', 12), fill='white', anchor='se')
        self.update_card_background(rebind=False)
        
    # --------------------------------------------------------------------------

    def switch_view(self, view_name):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if view_name == "home":
            self.show_home_view()
        elif view_name == "contact":
            self.content_frame.grid_rowconfigure(0, weight=1) # make the single row expand
            self.content_frame.grid_columnconfigure(0, weight=1)
            try:
                EDMBankContact(self.content_frame, 
                               self.logged_in_user, 
                               self.logged_in_user_email, 
                               self.switch_view)
            except Exception as e:
                self.show_message("Error", f"Could not load contact view: {e}", "error")
                lbl = tk.Label(self.content_frame, text=f"Error Loading Contact View: {e}", bg="#cad2c5", fg="red")
                lbl.pack(fill='both', expand=True)
        elif view_name == "profile": # handle profile view
            self.content_frame.grid_rowconfigure(0, weight=1) 
            self.content_frame.grid_columnconfigure(0, weight=1)
            try:
                # initialize EDMBankProfile
                EDMBankProfile(self.content_frame, 
                               self.logged_in_user, 
                               self.logged_in_user_email,
                               self.switch_view) # pass self.switch_view as the callback
            except Exception as e:
                self.show_message("Error", f"Could not load profile view: {e}", "error")
                lbl = tk.Label(self.content_frame, text=f"Error Loading Profile View: {e}", bg="#cad2c5", fg="red")
                lbl.pack(fill='both', expand=True)
        # handle special callbacks from EDMBankProfile (and others)
        elif view_name == "logout_relaunch":
            self.logout_and_relaunch_login()
        elif view_name == "get_card_snippet": # helper for EDMBankProfile to get data
            return self.card_number[-4:] 
        else:
            self.show_message("Navigation Error", f"View '{view_name}' is not yet implemented.", "warning")

    # --------------------------------------------------------------------------

    def create_bottom_menu(self):
        nav_frame = tk.Frame(self.main_container, bg="#7ecd9d", height=80)
        nav_frame.grid(row=2, column=0, sticky='ew', padx=0, pady=30)
        nav_frame.grid_propagate(False)
        
        nav_buttons_data = [
            ("HOME", "./icons/icon_home.png", self.go_home),
            ("CARD", "./icons/icon_card.png", self.show_cards),
            ("STATISTICS", "./icons/icon_stats.png", self.show_stats),
            ("PROFILE", "./icons/icon_profile.png", self.show_profile),
            ("CONTACT", "./icons/icon_contact.png", self.open_chat)
        ]
        
        self.nav_images = []
        
        for text, icon_filename, command in nav_buttons_data:
            btn_frame = tk.Frame(nav_frame, bg="#354f52")
            btn_frame.pack(side='left', expand=True, fill='both')
            try:
                original_image = Image.open(icon_filename)
                target_size = (80, 80)
                resized_image = original_image.resize(target_size, Image.LANCZOS)  
                photo_image = ImageTk.PhotoImage(resized_image)
                self.nav_images.append(photo_image)  
                icon_label = tk.Label(btn_frame, image=photo_image, bg="#354f52", cursor='hand2')
            except FileNotFoundError:
                icon_label = tk.Label(btn_frame, text=text[0], font=('FreeMono', 25, 'bold'), 
                                      bg="#84a98c", fg="#323A87", cursor='hand2')
            icon_label.pack(pady=(10, 2))

            text_label = tk.Label(btn_frame, text=text, font=('Courier', 16, 'bold'),
                                     bg="#354f52", fg='#ffffff', cursor='hand2')
            text_label.pack(pady=(0, 10))
            
            for widget in [btn_frame, icon_label, text_label]:
                widget.bind("<Button-1>", lambda e, cmd=command: cmd())

    def toggle_sold(self):
        if self.sold_visible:
            self.sold_label.grid_remove()
            self.sold_visible = False
        else:
            self.sold_label.grid()
            self.sold_visible = True

    def toggle_card_data(self):
        if not self.card_data_visible:
            self.card_data_visible = True
            self.update_card_display()
            self.show_message("Card Details", 
                              f"Card Number: {self.format_card_number(self.card_number, True)}\n"
                              f"Holder: {self.logged_in_user}\n"
                              f"Expiry Date: {self.card_expiry}\n"
                              f"CVV: {self.card_cvv}\n\n"
                              "⚠️ Keep this information safe!",
                              "info")
        else:
            self.card_data_visible = False
            self.update_card_display()
            self.show_message("Card Details", "Card details have been hidden", "info")

    def logout_and_relaunch_login(self):
        if self.relauch_login_callback:
            self.relauch_login_callback()
        else:
             self.show_in_app_login() 
            
    def show_in_app_login(self):
        login_window = tk.Toplevel(self.main)
        login_window.title("Login EDM Bank")
        login_window_width = min(300, self.main.winfo_width() - 100)
        login_window_height = min(200, self.main.winfo_height() - 100)
        login_window.geometry(f"{login_window_width}x{login_window_height}")
        login_window.configure(bg='#b0c4b1')
        login_window.transient(self.main) 
        login_window.grab_set() 

        self.main.update_idletasks()
        x = self.main.winfo_x() + self.main.winfo_width() // 2 - login_window_width // 2
        y = self.main.winfo_y() + self.main.winfo_height() // 2 - login_window_height // 2
        login_window.geometry(f"+{x}+{y}")
        login_window.resizable(False, False)

        tk.Label(login_window, text="Username:", font=('URW Gothic', 20),
                 bg='#b0c4b1').pack(pady=10)
        
        username_entry = tk.Entry(login_window, font=('Arial', 12))
        username_entry.pack(pady=5, padx=20, fill='x')
        username_entry.insert(0, self.logged_in_user)
        username_entry.focus_set() 
        
        def do_login():
            username = username_entry.get().strip().upper()
            if username:
                self.logged_in_user = username
                self.logged_in_user_email = f"{username.lower().replace(' ', '').replace('-', '')}@edmbank.com"
                self.update_card_display()
                login_window.destroy()
                self.show_message("Login", f"Welcome, {username}!", "info")
            else:
                self.show_message("Error", "Please enter a username!", "error")

        def on_enter(event):
            do_login()
            
        username_entry.bind('<Return>', on_enter)
        
        login_btn = tk.Button(login_window, text="LOGIN", font=('Arial', 12, 'bold'),
                              bg='#2f3e46', fg='white', command=do_login)
        login_btn.pack(pady=20)
        login_window.bind('<Escape>', lambda e: login_window.destroy())
    
    def go_home(self):
        self.switch_view("home")

    def open_chat(self):
        self.switch_view("contact") 
    
    def transfer(self):
        self.show_transfer_popup()
    
    def transfer_iban(self):
        self.show_iban_transfer_popup()

    def transaction_history(self):
        self.show_message("Transaction History", "Your transaction history", "info")

    def add_money(self):
        self.show_message("Add Money", "Deposit or transfer to account", "info")
    
    def make_payment(self):
        self.show_message("Payments", "Pay bills and services", "info")

    def settings(self):
        self.show_message("Settings", "Application settings", "info")
    
    def show_cards(self):
        self.show_message("Cards", "Manage your cards", "info")

    def show_stats(self):
        self.show_message("Statistics", "Spending statistics", "info")
    
    def show_profile(self):
        # MODIFIED: Navigate to the profile page
        self.switch_view("profile")
        
    def balance_to_float(self, balance_str):
        """Converts a balance string (e.g., '1.250,00 RON') to a float."""
        try:
            # Remove currency and thousand separator, replace decimal comma
            return float(balance_str.upper().replace(' RON', '').replace('.', '').replace(',', '.'))
        except ValueError:
            return 0.0

    def float_to_balance(self, amount_float):
        """Converts a float to a balance string (e.g., '1.250,00 RON')."""
        
        # Set locale for correct number formatting (assuming Romanian/European standard for the format)
        try:
            # Try to set Romanian locale for correct format
            locale.setlocale(locale.LC_ALL, 'ro_RO.UTF-8')
        except locale.Error:
            # Fallback for systems where 'ro_RO.UTF-8' is not available
            try:
                locale.setlocale(locale.LC_ALL, 'C')
            except locale.Error:
                pass
                
        # Manual format fallback (thousands dot, decimal comma):
        # Format to two decimal places, then handle custom separators
        formatted = "{:,.2f}".format(amount_float).replace(",", "X").replace(".", ",").replace("X", ".")
        return f"{formatted} RON"

    def update_balance_display(self):
        """Updates the label that shows the current balance."""
        if hasattr(self, 'sold_label'):
             self.sold_label.config(text=self.sold_amount)
    
# --------------------------------------------------------------------------
    def show_transfer_popup(self):
        transfer_window = tk.Toplevel(self.main)
        transfer_window.title("Fast Transfer")
        transfer_window.configure(bg='#cad2c5')
        
        # Calculate position to center the window relative to the main window
        self.main.update_idletasks()
        main_width = self.main.winfo_width()
        main_height = self.main.winfo_height()
        
        popup_width = 350
        popup_height = 250
        
        x = self.main.winfo_x() + (main_width // 2) - (popup_width // 2)
        y = self.main.winfo_y() + (main_height // 2) - (popup_height // 2)
        
        transfer_window.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        transfer_window.resizable(False, False)
        transfer_window.grab_set() # Modal window: forces focus on this window
        
        # --- Recipient Username Input ---
        tk.Label(transfer_window, text="Recipient Username:", font=('Tex Gyre Chorus', 20, 'bold'),
                 bg='#cad2c5', fg='#354f52').pack(pady=(15, 2), padx=10, anchor='w')
        
        username_entry = tk.Entry(transfer_window, font=('Arial', 12), relief='flat', bd=2, bg='white')
        username_entry.pack(pady=(0, 10), padx=20, fill='x')
        
        # --- Transfer Sum Input ---
        tk.Label(transfer_window, text="Sum you want to transfer:", font=('Tex Gyre Chorus', 20, 'bold'),
                 bg='#cad2c5', fg='#354f52').pack(pady=(5, 2), padx=10, anchor='w')
        
        sum_entry = tk.Entry(transfer_window, font=('Arial', 12), relief='flat', bd=2, bg='white')
        sum_entry.pack(pady=(0, 15), padx=20, fill='x')
        
        # --- Button Frame ---
        button_frame = tk.Frame(transfer_window, bg='#cad2c5')
        button_frame.pack(pady=10)
        
        def attempt_transfer():
            username = username_entry.get().strip()
            amount = sum_entry.get().strip()
            
            if not username or not amount:
                self.show_message("Error", "Please fill in both fields.", "warning")
                return

            try:
                # Simple validation for amount
                transfer_amount = float(amount.replace(',', '.')) 
                
                # Check 1: Is the amount valid?
                if transfer_amount <= 0:
                    self.show_message("Error", "Transfer amount must be positive.", "error")
                    return
                
                # --- EXECUTE SUBTRACTION (Simplified without error handling) ---
                current_balance = self.balance_to_float(self.sold_amount)
                
                if transfer_amount > current_balance:
                    self.show_message("Error", "Insufficient funds for this transfer.", "error")
                    return
                
                new_balance = current_balance - transfer_amount
                self.sold_amount = self.float_to_balance(new_balance)
                self.update_balance_display()

                # Close the pop-up and show confirmation
                transfer_window.destroy()
                self.show_message("Success", 
                                  f"Transferring {transfer_amount:,.2f} RON to {username}...", 
                                  "info")
            except ValueError:
                self.show_message("Error", "Invalid amount entered. Please use numbers.", "error")
        
        # SEND Button
        send_btn = tk.Button(button_frame, text="SEND", font=('Arial', 12, 'bold'),
                              bg='#52796f', fg='white', command=attempt_transfer, width=10)
        send_btn.pack(side='left', padx=10)
        
        # EXIT Button
        exit_btn = tk.Button(button_frame, text="EXIT", font=('Arial', 12),
                              bg='#354f52', fg='white', command=transfer_window.destroy, width=10)
        exit_btn.pack(side='left', padx=10)

    def is_valid_ro_iban(self, iban):
        """Checks if the string is a valid format for a Romanian IBAN."""
        iban = iban.strip().replace(' ', '').upper()
        # Romanian IBANs are 24 characters long and start with 'RO'
        return len(iban) == 24 and iban.startswith("RO")
    
    # --------------------------------------------------------------------------

    def show_iban_transfer_popup(self):
        transfer_window = tk.Toplevel(self.main)
        transfer_window.title("IBAN Transfer")
        transfer_window.configure(bg='#cad2c5')
        
        # Calculate position to center the window relative to the main window
        self.main.update_idletasks()
        main_width = self.main.winfo_width()
        main_height = self.main.winfo_height()
        
        popup_width = 380
        popup_height = 280
        
        x = self.main.winfo_x() + (main_width // 2) - (popup_width // 2)
        y = self.main.winfo_y() + (main_height // 2) - (popup_height // 2)
        
        transfer_window.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        transfer_window.resizable(False, False)
        transfer_window.grab_set() # Modal window: forces focus on this window
        
        # --- Recipient IBAN Input ---
        tk.Label(transfer_window, text="Recipient IBAN (RO...):", font=('Tex Gyre Chorus', 20, 'bold'),
                 bg='#cad2c5', fg='#354f52').pack(pady=(15, 2), padx=10, anchor='w')
        
        iban_entry = tk.Entry(transfer_window, font=('Arial', 12), relief='flat', bd=2, bg='white')
        iban_entry.pack(pady=(0, 10), padx=20, fill='x')
        
        # --- Transfer Sum Input ---
        tk.Label(transfer_window, text="Sum you want to transfer:", font=('Tex Gyre Chorus', 20, 'bold'),
                 bg='#cad2c5', fg='#354f52').pack(pady=(5, 2), padx=10, anchor='w')
        
        sum_entry = tk.Entry(transfer_window, font=('Arial', 12), relief='flat', bd=2, bg='white')
        sum_entry.pack(pady=(0, 15), padx=20, fill='x')
        
        # --- Button Frame ---
        button_frame = tk.Frame(transfer_window, bg='#cad2c5')
        button_frame.pack(pady=10)
        
        def attempt_iban_transfer():
            iban = iban_entry.get().strip()
            amount = sum_entry.get().strip()
            
            if not iban or not amount:
                self.show_message("Error", "Please fill in both fields.", "warning")
                return
            
            if not self.is_valid_ro_iban(iban):
                self.show_message("Error", "Incorrect IBAN format (must start with RO and be 24 characters).", "error")
                return
                
            try:
                transfer_amount = float(amount.replace(',', '.')) 
                
                if transfer_amount <= 0:
                    self.show_message("Error", "Transfer amount must be positive.", "error")
                    return
                
                current_balance = self.balance_to_float(self.sold_amount)
                
                if transfer_amount > current_balance:
                    self.show_message("Error", "Insufficient funds for this transfer.", "error")
                    return
                
                new_balance = current_balance - transfer_amount
                self.sold_amount = self.float_to_balance(new_balance)
                self.update_balance_display()

                transfer_window.destroy()
                self.show_message("Success", 
                                  f"Bank transfer of {transfer_amount:,.2f} RON to IBAN {iban} has been initiated.", 
                                  "info")
            except ValueError:
                self.show_message("Error", "Invalid amount entered. Please use numbers.", "error")

        # SEND Button
        send_btn = tk.Button(button_frame, text="SEND", font=('Arial', 12, 'bold'),
                              bg='#52796f', fg='white', command=attempt_iban_transfer, width=10)
        send_btn.pack(side='left', padx=10)
        
        # EXIT Button
        exit_btn = tk.Button(button_frame, text="EXIT", font=('Arial', 12),
                              bg='#354f52', fg='white', command=transfer_window.destroy, width=10)
        exit_btn.pack(side='left', padx=10)

# --- Application Launch ---
if __name__ == "__main__":
    root = tk.Tk()
    app = EDMBankApp(root) 
    root.mainloop()