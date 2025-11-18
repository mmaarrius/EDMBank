import tkinter as tk
from tkinter import ttk, messagebox
import os
import random
from unicodedata import digit

class EDMBankApp:
    # self = this (Java refference :)) )
    def __init__(self, main, relauch_login_callback=None): # New argument
        self.main = main # a root window
        self.main.title("EDM Bank")
        self.relauch_login_callback = relauch_login_callback # Store the callback

        # initial dimensions for mobile: FORMAT 9 X 16 - RESPONSIVE
        screen_width = main.winfo_screenwidth()
        screen_height = main.winfo_screenheight()
        
        # START WITH SMALLER SIZE THAT FITS ON SCREEN BUT KEEP 9:16 ASPECT RATIO
        max_width = min(990, screen_width )  # Ensure it fits with margin
        max_height = min(1760, screen_height - 100)  # Ensure it fits with margin
        
        # Calculate proportional size maintaining 9:16 aspect ratio
        if max_width / max_height > 9/16:
            # Height is limiting factor
            initial_width = int(max_height * 9/16)
            initial_height = max_height
        else:
            # Width is limiting factor
            initial_width = max_width
            initial_height = int(max_width * 16/9)
            
        # Center the window
        x = (screen_width - initial_width) // 2
        y = (screen_height - initial_height) // 2
        self.main.geometry(f"{initial_width}x{initial_height}+{x}+{y}")
        self.main.minsize(300, 500)  # minimum reasonable size
        # allow maximizing
        self.main.configure(bg="#354f52")

        # variables for user and card
        self.sold_visible = False
        self.card_data_visible = False
        self.sold_amount = "1.250,00 RON"
        self.is_large_screen = False
        self.logged_in_user = "POPESCU IRIS-MARIA"  # default user
        self.card_number = self.generate_card_number()  # generate unique card number
        self.card_cvv = f"{random.randint(0,999):03d}"  # random CVV
        self.card_expiry = "02/26"  # expiring date

        # main frame that expands (border padding)
        self.main_container = tk.Frame(self.main, bg="#354f52")
        self.main_container.pack(fill='both', expand=True, padx=10, pady=10)  # ADDED PADDING

        # configure grid for scaling (with weight = 1 the content expands, if not it stays fixed)
        self.main_container.grid_rowconfigure(1, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        # create interface
        self.create_top_menu()
        self.create_main_content()
        self.create_bottom_menu()

        # bind for resizing
        self.main.bind('<Configure>', self.on_resize)
    
    # --------------------------------------------------------------------------

    def show_message(self, title, message, message_type="info"):
        # calculates center position of the main window for centering the messagebox
        self.main.update_idletasks()
        x = self.main.winfo_x() + self.main.winfo_width() // 2 - 150
        y = self.main.winfo_y() + self.main.winfo_height() // 2 - 75
        

        if message_type == "info":
            messagebox.showinfo(title, message, parent=self.main)
        elif message_type == "warning":
            messagebox.showwarning(title, message, parent=self.main)
        elif message_type == "error":
            messagebox.showerror(title, message, parent=self.main)

        # force positioning (sometimes Tkinter ignores parent)
        for window in self.main.winfo_children():
            if isinstance(window, tk.Toplevel):
                window.geometry(f"+{x}+{y}")
                break

    # function to generate a random card number (16 random characters)
    def generate_card_number(self):
        # generate 16 random digits
        digits = ''.join([str(random.randint(0, 9)) for _ in range(16)])
        return digits

    # hide all but last 4 digits of card number
    def format_card_number(self, number, show_full=False):
        if show_full:
            return ' '.join([number[i:i+4] for i in range(0, 16, 4)])
        else:
            return f"•••• •••• •••• {number[-4:]}"
    
    # handle resizing for responsive design
    def on_resize(self, event):
        if hasattr(self, 'buttons_frame'):
            window_width = self.main.winfo_width()
            
            if window_width > 600 and not self.is_large_screen:
                self.switch_to_desktop_layout()
                self.is_large_screen = True
            elif window_width <= 600 and self.is_large_screen:
                self.switch_to_mobile_layout()
                self.is_large_screen = False
    
    # --------------------------------------------------------------------------

    # switch layout to desktop (large screen)
    def switch_to_desktop_layout(self):
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
            btn = tk.Button(self.buttons_frame, text=text, font=('Arial', 16, 'bold'), 
                           bg='#52796f', fg='white', relief='flat', borderwidth=2,
                           height=3, command=command)
            btn.pack(fill='x', padx=10, pady=6)
        
        # KEEP ORIGINAL CARD DIMENSIONS BUT MAKE RESPONSIVE
        self.card_frame.configure(height=360, width=500)
        self.card_frame.grid_propagate(False)
        self.update_card_display()
    
    # --------------------------------------------------------------------------

    def switch_to_mobile_layout(self):
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()
        
        self.buttons_frame.grid_columnconfigure(0, weight=1)
        self.buttons_frame.grid_columnconfigure(1, weight=1)
        self.buttons_frame.grid_rowconfigure(0, weight=1)
        self.buttons_frame.grid_rowconfigure(1, weight=1)
        self.buttons_frame.grid_rowconfigure(2, weight=1)
        self.buttons_frame.grid_rowconfigure(3, weight=1)
        
        buttons_data = [
            ("$ TRANSFER", self.transfer, 0, 0),
            ("⇄ IBAN TRANSFER", self.transfer_iban, 0 , 1),
            ("⎙ TRANSACTION HISTORY", self.transaction_history, 1, 0),
            ("⤾ ADD MONEY", self.add_money, 1, 1),
            ("ⓘ SHOW CARD DETAILS", self.toggle_card_data, 2, 0),
            ("✎ MAKE PAYMENT", self.make_payment, 2, 1),
            ("⚙︎ ACCOUNT SETTINGS", self.settings, 3, 0)
        ]
        
        # create buttons in a grid
        for text, command, row, col in buttons_data:
            btn = tk.Button(self.buttons_frame, text=text, font=('Arial', 11), 
                           bg='#354f52', fg="white", relief='flat',
                           height=2, command=command)
            btn.grid(row=row, column=col, padx=6, pady=6, sticky='nsew')
        
        # KEEP ORIGINAL CARD DIMENSIONS BUT MAKE RESPONSIVE
        self.card_frame.configure(height=240, width=400)
        self.card_frame.grid_propagate(False)
        self.update_card_display()
    
# --------------------------------------------------------------------------

    def update_card_display(self):
        display_number = self.format_card_number(self.card_number, self.card_data_visible)
        self.card_number_label.configure(text=display_number)
        
        if self.card_data_visible:
            self.card_holder_label.configure(text=self.logged_in_user)
        else:
            self.card_holder_label.configure(text="POPESCU IRINA-MARIA")

    # --------------------------------------------------------------------------

    # create head bar with toggle menu, title and login button
    def create_top_menu(self):
        # header frame
        top_frame = tk.Frame(self.main_container, bg="#354f52", height=120)
        top_frame.grid(row=0, column=0, sticky='ew', padx=20, pady=10)
        top_frame.grid_propagate(False)
        top_frame.grid_columnconfigure(1, weight=1)

        # toggle menu
        self.dropdown_var = tk.StringVar()
        self.dropdown_var.set("Menu")
        dropdown = ttk.Combobox(top_frame, textvariable=self.dropdown_var, 
                               values=["Accounts", "Savings", "Settings", "Cards", "Payments"], 
                               state="readonly", width=12)
        dropdown.grid(row=0, column=0, sticky='w', padx=(0, 10))

        # EDM Bank title
        title_label = tk.Label(top_frame, text="EDM Bank", font=('Arial', 30, 'bold'),
                              bg='#354f52', fg="#FFFFFF")
        title_label.grid(row=0, column=1, sticky='ew')

        # login button
        # Changed text to LOGOUT and command to the new logout method
        login_btn = tk.Button(top_frame, text="LOGOUT", font=('Arial', 12, 'bold'), 
                             bg="#354f52", fg='white', relief='flat', padx=25,
                             height=2, command=self.logout_and_relaunch_login)
        login_btn.grid(row=0, column=2, sticky='e', padx=(10, 0))

    # --------------------------------------------------------------------------

    def create_main_content(self):
        # background
        main_frame = tk.Frame(self.main_container, bg="#cad2c5")
        main_frame.grid(row=1, column=0, sticky='nsew', padx=20, pady=10)
        
        # configure grid for scaling (weight=1 makes it expand)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # create card
        self.create_card(main_frame)

        # sold button - VIEW BALANCE
        sold_btn = tk.Button(main_frame, text="VIEW BALANCE", font=('Open Sans', 10, 'bold'),
                            bg='#52796f', fg='#ffffff', relief='flat',
                            height=3, command=self.toggle_sold)
        sold_btn.grid(row=1, column=0, sticky='ew', pady=15)

        # sold amount label
        self.sold_label = tk.Label(main_frame, text=self.sold_amount,
                                  font=('Arial', 20, 'bold'), bg='#cad2c5', fg='#2f3e46')
        self.sold_label.grid(row=2, column=0, pady=10)
        self.sold_label.grid_remove()
        
        self.buttons_frame = tk.Frame(main_frame, bg='#cad2c5')
        self.buttons_frame.grid(row=3, column=0, sticky='nsew', pady=20)
        
        self.switch_to_mobile_layout()
    
    # --------------------------------------------------------------------------

    def create_card(self, parent):
        #borders of the card
        
        # TODO: replace with image later
        # KEEP ORIGINAL CARD DIMENSIONS
        self.card_frame = tk.Frame(parent, bg="#2f3e46", height=160, width=300)
        self.card_frame.grid(row=0, column=0, sticky='n', pady=20)
        self.card_frame.grid_propagate(False)

        # center of the card
        card_content = tk.Frame(self.card_frame, bg='#2f3e46')
        card_content.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.9, relheight=0.8)

        top_row = tk.Frame(card_content, bg='#2f3e46')
        top_row.pack(fill='x', pady=(0, 15))
        
        bank_label = tk.Label(top_row, text="EDM Bank", font=('Arial', 16, 'bold'), 
                             bg='#2f3e46', fg='white')
        bank_label.pack(side='left')
        
        # chip icon
        # TODO: replace with image later
        chip_label = tk.Label(top_row, text="◘ Chip", font=('Arial', 12), 
                             bg='#2f3e46', fg='white')
        chip_label.pack(side='right')
        
        # card number
        self.card_number_label = tk.Label(card_content, text=self.format_card_number(self.card_number), 
                              font=('Arial', 18, 'bold'), bg='#2f3e46', fg='white')
        self.card_number_label.pack(expand=True)

        # bottom row
        bottom_row = tk.Frame(card_content, bg='#2f3e46')
        bottom_row.pack(fill='x', pady=(15, 0))

        # card holder name
        self.card_holder_label = tk.Label(bottom_row, text="POPESCU IRINA-MARIA", font=('Arial', 12),
                                           bg='#2f3e46', fg='white')
        self.card_holder_label.pack(side='left')
        
        # card expiry date
        expiry_label = tk.Label(bottom_row, text="12/25", font=('Arial', 12), 
                               bg='#2f3e46', fg='white')
        expiry_label.pack(side='right')

    # --------------------------------------------------------------------------

    def create_bottom_menu(self):
        nav_frame = tk.Frame(self.main_container, bg="#7ecd9d", height=80)
        nav_frame.grid(row=2, column=0, sticky='ew', padx=0, pady=0)
        nav_frame.grid_propagate(False)
        
        
        # TODO: replace with image later
        nav_buttons = [
            ("⌂", "HOME", self.go_home),
            ("🖨", "CARDS", self.show_cards),
            ("🈷", "STATISTICS", self.show_stats),
            ("˙ᵕ˙", "PROFILE", self.show_profile),
            ("🗣", "CHAT", self.open_chat)
        ]
        
        #  bottom header
        for i, (icon, text, command) in enumerate(nav_buttons):
            btn_frame = tk.Frame(nav_frame, bg="#354f52")
            btn_frame.pack(side='left', expand=True, fill='both')
            
            # icon and text labels down
            icon_label = tk.Label(btn_frame, text=icon, font=('FreeMono', 25, 'bold'), 
                                 bg="#84a98c", fg="#323A87", cursor='hand2')
            icon_label.pack(pady=(10, 2))

            # the text near icons down
            text_label = tk.Label(btn_frame, text=text, font=('FreeMono', 9, 'bold'),
                                 bg="#354f52", fg='#ffffff', cursor='hand2')
            text_label.pack(pady=(0, 10))
            
            # bind click events
            for widget in [btn_frame, icon_label, text_label]:
                widget.bind("<Button-1>", lambda e, cmd=command: cmd())
    
    # --------------------------------------------------------------------------

    def toggle_sold(self):
        if self.sold_visible:
            self.sold_label.grid_remove()
            self.sold_visible = False
        else:
            self.sold_label.grid()
            self.sold_visible = True

    # --------------------------------------------------------------------------

    def toggle_card_data(self):
        # show card details in messagebox
        if not self.card_data_visible:
            self.card_data_visible = True
            self.update_card_display()
            # using personalized show_message instead of messagebox directly
            self.show_message("Card Details", 
                            f"Card Number: {self.format_card_number(self.card_number, True)}\n"
                            f"Holder: {self.logged_in_user}\n"
                            f"Expiry Date: {self.card_expiry}\n"
                            f"CVV: {self.card_cvv}\n\n"
                            "⚠️ Keep this information safe!",
                            "info")
        # hide card details
        else:
            self.card_data_visible = False
            self.update_card_display()
            self.show_message("Card Details", "Card details have been hidden", "info")

    # --------------------------------------------------------------------------

    def logout_and_relaunch_login(self):
        """Destroys the main app and relaunches the login screen."""
        if self.relauch_login_callback:
            self.relauch_login_callback()
        else:
             # Fallback: if launched standalone, just show the in-app login
             self.show_in_app_login() 
             
    def show_in_app_login(self):
        """Login window centered on application (used as fallback or for user switching)"""
        login_window = tk.Toplevel(self.main)
        login_window.title("Login EDM Bank")
        # made login window responsive
        login_window_width = min(300, self.main.winfo_width() - 100)
        login_window_height = min(200, self.main.winfo_height() - 100)
        login_window.geometry(f"{login_window_width}x{login_window_height}")
        login_window.configure(bg='#b0c4b1')
        login_window.transient(self.main)  # Make the window dependent on the parent
        login_window.grab_set()  # Modal - blocks interaction with parent

        # center the login window on the application
        self.main.update_idletasks()
        x = self.main.winfo_x() + self.main.winfo_width() // 2 - login_window_width // 2
        y = self.main.winfo_y() + self.main.winfo_height() // 2 - login_window_height // 2
        login_window.geometry(f"+{x}+{y}")
        
        # no resizing allowed
        login_window.resizable(False, False)

        tk.Label(login_window, text="Username:", font=('URW Gothic', 20),
                bg='#b0c4b1').pack(pady=10)
        
        username_entry = tk.Entry(login_window, font=('Arial', 12))
        username_entry.pack(pady=5, padx=20, fill='x')
        username_entry.insert(0, self.logged_in_user)
        username_entry.focus_set()  # Focus on text field
        
        # login function
        def do_login():
            username = username_entry.get().strip().upper()
            if username:
                self.logged_in_user = username
                self.update_card_display()
                login_window.destroy()
                self.show_message("Login", f"Welcome, {username}!", "info")
            else:
                self.show_message("Error", "Please enter a username!", "error")

        # bind Enter key to login
        def on_enter(event):
            do_login()
        
        # Bind Enter key
        username_entry.bind('<Return>', on_enter)
        
        login_btn = tk.Button(login_window, text="LOGIN", font=('Arial', 12, 'bold'),
                             bg='#2f3e46', fg='white', command=do_login)
        login_btn.pack(pady=20)

        # Bind to close on Escape key
        login_window.bind('<Escape>', lambda e: login_window.destroy())
    
    def transfer(self):
        self.show_message("Transfer", "Fast transfer to contacts", "info")
    
    def transfer_iban(self):
        self.show_message("Transfer IBAN", "Transfer by entering IBAN", "info")

    def transaction_history(self):
        self.show_message("Transaction History", "Your transaction history", "info")

    def add_money(self):
        self.show_message("Add Money", "Deposit or transfer to account", "info")
    
    def make_payment(self):
        self.show_message("Payments", "Pay bills and services", "info")

    def settings(self):
        self.show_message("Settings", "Application settings", "info")

    def go_home(self):
        self.show_message("Home", "Main page", "info")
    
    def show_cards(self):
        self.show_message("Cards", "Manage your cards", "info")

    def show_stats(self):
        self.show_message("Statistics", "Spending statistics", "info")

    def show_profile(self):
        self.show_message("Profile", f"Profile of {self.logged_in_user}", "info")
    
    def open_chat(self):
        self.show_message("Chat", "24/7 chat assistance", "info")

if __name__ == "__main__":
    main = tk.Tk()
    # Provide a simple callback for standalone testing
    app = EDMBankApp(main, relauch_login_callback=lambda: print("Logout called in standalone mode."))
    main.mainloop()