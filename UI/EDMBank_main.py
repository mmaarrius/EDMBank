import tkinter as tk
from tkinter import ttk, messagebox
import os
import random

class EDMBankApp:
    def __init__(self, main):
        self.main = main # a root window
        self.main.title("EDM Bank")

        # initial dimensions for mobile: FORMAT 9 X 16
        self.main.geometry("990x1760")
        self.main.minsize(990, 1760)

        # allow maximizing
        self.main.configure(bg="#1e1e1e")

        # variables for user and card
        self.sold_visible = False
        self.card_data_visible = False
        self.sold_amount = "1.250,00 RON"
        self.is_large_screen = False
        self.logged_in_user = "POPESCU IRIS-MARIA"  # default user
        self.card_number = self.generate_card_number()  # generate unique card number
        self.card_cvv = f"{random.randint(0,999):03d}"  # random CVV
        self.card_expiry = "02/26"  # expiring date

        # main frame that expands
        self.main_container = tk.Frame(self.main, bg="#d9baef")
        self.main_container.pack(fill='both', expand=True)

        # configure grid for scaling (with weight = 1 the content expands, if not it stays fixed)
        self.main_container.grid_rowconfigure(1, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        # create interface
        self.create_top_menu()
        self.create_main_content()
        self.create_bottom_menu()

        # bind for resizing
        self.main.bind('<Configure>', self.on_resize)
    
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
    
    def generate_card_number(self):
        prefix = random.choice(['4', '5'])
        other_digits = ''.join([str(random.randint(0, 9)) for _ in range(15)])
        return prefix + other_digits
    
    def format_card_number(self, number, show_full=False):
        if show_full:
            return ' '.join([number[i:i+4] for i in range(0, 16, 4)])
        else:
            return f"•••• •••• •••• {number[-4:]}"
    
    def on_resize(self, event):
        if hasattr(self, 'buttons_frame'):
            window_width = self.main.winfo_width()
            
            if window_width > 600 and not self.is_large_screen:
                self.switch_to_desktop_layout()
                self.is_large_screen = True
            elif window_width <= 600 and self.is_large_screen:
                self.switch_to_mobile_layout()
                self.is_large_screen = False
    
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
                           bg='white', fg='#333333', relief='flat', borderwidth=2,
                           height=3, command=command)
            btn.pack(fill='x', padx=10, pady=6)
        
        self.card_frame.configure(height=240, width=360)
        self.card_frame.grid_propagate(False)
        self.update_card_display()
    
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
        
        for text, command, row, col in buttons_data:
            btn = tk.Button(self.buttons_frame, text=text, font=('Arial', 11), 
                           bg='white', fg='#333333', relief='flat',
                           height=2, command=command)
            btn.grid(row=row, column=col, padx=6, pady=6, sticky='nsew')
        
        self.card_frame.configure(height=160, width=300)
        self.card_frame.grid_propagate(False)
        self.update_card_display()
    
    def update_card_display(self):
        display_number = self.format_card_number(self.card_number, self.card_data_visible)
        self.card_number_label.configure(text=display_number)
        
        if self.card_data_visible:
            self.card_holder_label.configure(text=self.logged_in_user)
        else:
            self.card_holder_label.configure(text="POPESCU IRINA-MARIA")
    
    def create_top_menu(self):
        top_frame = tk.Frame(self.main_container, bg='#f0f0f0', height=70)
        top_frame.grid(row=0, column=0, sticky='ew', padx=20, pady=10)
        top_frame.grid_propagate(False)
        top_frame.grid_columnconfigure(1, weight=1)
        
        self.dropdown_var = tk.StringVar()
        self.dropdown_var.set("Menu")
        dropdown = ttk.Combobox(top_frame, textvariable=self.dropdown_var, 
                               values=["Accounts", "Savings", "Settings", "Cards", "Payments"], 
                               state="readonly", width=12)
        dropdown.grid(row=0, column=0, sticky='w', padx=(0, 10))
        
        title_label = tk.Label(top_frame, text="EDM Bank", font=('Arial', 10, 'bold'), 
                              bg='#f0f0f0', fg='#333333')
        title_label.grid(row=0, column=1, sticky='ew')
        
        login_btn = tk.Button(top_frame, text="LOGIN", font=('Arial', 12, 'bold'), 
                             bg='#6a0dad', fg='white', relief='flat', padx=25,
                             height=2, command=self.login)
        login_btn.grid(row=0, column=2, sticky='e', padx=(10, 0))
    
    def create_main_content(self):
        main_frame = tk.Frame(self.main_container, bg='#f0f0f0')
        main_frame.grid(row=1, column=0, sticky='nsew', padx=20, pady=10)
        
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        self.create_card(main_frame)

        sold_btn = tk.Button(main_frame, text="VIEW BALANCE", font=('Arial', 14, 'bold'),
                            bg='#6a0dad', fg='white', relief='flat',
                            height=3, command=self.toggle_sold)
        sold_btn.grid(row=1, column=0, sticky='ew', pady=15)
        
        self.sold_label = tk.Label(main_frame, text=self.sold_amount, 
                                  font=('Arial', 20, 'bold'), bg='#f0f0f0', fg='#6a0dad')
        self.sold_label.grid(row=2, column=0, pady=10)
        self.sold_label.grid_remove()
        
        self.buttons_frame = tk.Frame(main_frame, bg='#f0f0f0')
        self.buttons_frame.grid(row=3, column=0, sticky='nsew', pady=20)
        
        self.switch_to_mobile_layout()
    
    def create_card(self, parent):
        self.card_frame = tk.Frame(parent, bg='#6a0dad', height=160, width=300)
        self.card_frame.grid(row=0, column=0, sticky='n', pady=20)
        self.card_frame.grid_propagate(False)
        
        card_content = tk.Frame(self.card_frame, bg='#6a0dad')
        card_content.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.9, relheight=0.8)
        
        top_row = tk.Frame(card_content, bg='#6a0dad')
        top_row.pack(fill='x', pady=(0, 15))
        
        bank_label = tk.Label(top_row, text="EDM Bank", font=('Arial', 16, 'bold'), 
                             bg='#6a0dad', fg='white')
        bank_label.pack(side='left')
        
        chip_label = tk.Label(top_row, text="◘ Chip", font=('Arial', 12), 
                             bg='#6a0dad', fg='white')
        chip_label.pack(side='right')
        
        self.card_number_label = tk.Label(card_content, text=self.format_card_number(self.card_number), 
                              font=('Arial', 18, 'bold'), bg='#6a0dad', fg='white')
        self.card_number_label.pack(expand=True)
        
        bottom_row = tk.Frame(card_content, bg='#6a0dad')
        bottom_row.pack(fill='x', pady=(15, 0))

        self.card_holder_label = tk.Label(bottom_row, text="POPESCU IRINA-MARIA", font=('Arial', 12),
                                           bg='#6a0dad', fg='white')
        self.card_holder_label.pack(side='left')
        
        expiry_label = tk.Label(bottom_row, text="12/25", font=('Arial', 12), 
                               bg='#6a0dad', fg='white')
        expiry_label.pack(side='right')
    
    def create_bottom_menu(self):
        nav_frame = tk.Frame(self.main_container, bg='#ffffff', height=80)
        nav_frame.grid(row=2, column=0, sticky='ew', padx=0, pady=0)
        nav_frame.grid_propagate(False)
        
        nav_buttons = [
            ("⌂", "HOME", self.go_home),
            ("🖨", "CARDS", self.show_cards),
            ("🈷", "STATISTICS", self.show_stats),
            ("˙ᵕ˙", "PROFILE", self.show_profile),
            ("🗣", "CHAT", self.open_chat)
        ]
        
        for i, (icon, text, command) in enumerate(nav_buttons):
            btn_frame = tk.Frame(nav_frame, bg='#ffffff')
            btn_frame.pack(side='left', expand=True, fill='both')
            
            icon_label = tk.Label(btn_frame, text=icon, font=('Arial', 20), 
                                 bg='#ffffff', fg='#6a0dad', cursor='hand2')
            icon_label.pack(pady=(10, 2))
            
            text_label = tk.Label(btn_frame, text=text, font=('Arial', 9, 'bold'), 
                                 bg='#ffffff', fg='#333333', cursor='hand2')
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
            # using personalized show_message instead of messagebox directly
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
    
    def login(self):
        """Login window centered on application"""
        login_window = tk.Toplevel(self.main)
        login_window.title("Login EDM Bank")
        login_window.geometry("300x200")
        login_window.configure(bg='#f0f0f0')
        login_window.transient(self.main)  # Make the window dependent on the parent
        login_window.grab_set()  # Modal - blocks interaction with parent

        # Center the login window on the application
        self.main.update_idletasks()
        x = self.main.winfo_x() + self.main.winfo_width() // 2 - 150
        y = self.main.winfo_y() + self.main.winfo_height() // 2 - 100
        login_window.geometry(f"300x200+{x}+{y}")
        
        # Impedă redimensionarea
        login_window.resizable(False, False)

        tk.Label(login_window, text="Username:", font=('Arial', 12),
                bg='#f0f0f0').pack(pady=10)
        
        username_entry = tk.Entry(login_window, font=('Arial', 12))
        username_entry.pack(pady=5, padx=20, fill='x')
        username_entry.insert(0, self.logged_in_user)
        username_entry.focus_set()  # Focus on text field
        
        def do_login():
            username = username_entry.get().strip().upper()
            if username:
                self.logged_in_user = username
                self.update_card_display()
                login_window.destroy()
                self.show_message("Login", f"Welcome, {username}!", "info")
            else:
                self.show_message("Error", "Please enter a username!", "error")

        def on_enter(event):
            do_login()
        
        # Bind Enter key
        username_entry.bind('<Return>', on_enter)
        
        login_btn = tk.Button(login_window, text="LOGIN", font=('Arial', 12, 'bold'),
                             bg='#6a0dad', fg='white', command=do_login)
        login_btn.pack(pady=20)
        
        # Bind pentru a în chide fereastra cu ESC
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
    app = EDMBankApp(main)
    main.mainloop()

