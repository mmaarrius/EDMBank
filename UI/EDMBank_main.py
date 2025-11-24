import tkinter as tk
from tkinter import ttk, messagebox
import os
import random
from PIL import Image, ImageTk 

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
            btn = tk.Button(self.buttons_frame, text=text, font=('Arial', 16, 'bold'), 
                            bg='#52796f', fg='white', relief='flat', borderwidth=2,
                            height=3, command=command)
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
            btn = tk.Button(self.buttons_frame, text=text, font=('Arial', 11), 
                            bg='#354f52', fg="white", relief='flat',
                            height=2, command=command)
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
        
        style.theme_use('default') 
        style.configure("Green.TCombobox", 
                        fieldbackground='#52796f', # Darker green for the input field
                        background='#84a98c',    # Lighter green for the button/arrow part
                        foreground='white',
                        selectbackground='#84a98c',
                        selectforeground='white',
                        font=('Courier', 26, 'bold'),
                        padding=10) # Add some padding

        style.map('Green.TCombobox', 
                  fieldbackground=[('readonly', '#52796f')],
                  background=[('readonly', '#84a98c')])
        
        # Set the font for the options in the dropdown list (affects the listbox pop-up)
        self.main.option_add('*TCombobox*Listbox.font', ('Courier', 14))

        self.dropdown_var = tk.StringVar()
        self.dropdown_var.set("Menu")
        
        dropdown = ttk.Combobox(top_frame, textvariable=self.dropdown_var, 
                                 values=["Accounts", "Savings", "Settings", "Cards", "Payments"], 
                                 state="readonly", width=12, background='#52796f', # Adjusted width to look better with larger font
                                 style="Green.TCombobox") # Apply the new style

        dropdown.grid(row=0, column=0, sticky='w', padx=(0, 10))
        # -----------------------------------------------------------

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

        sold_btn = tk.Button(self.content_frame, text="VIEW BALANCE", font=('Open Sans', 10, 'bold'),
                              bg='#52796f', fg='#ffffff', relief='flat',
                              height=3, command=self.toggle_sold)
        sold_btn.grid(row=1, column=0, sticky='ew', pady=15)

        self.sold_label = tk.Label(self.content_frame, text=self.sold_amount,
                                     font=('Arial', 20, 'bold'), bg='#cad2c5', fg='#2f3e46')
        self.sold_label.grid(row=2, column=0, pady=10)
        self.sold_label.grid_remove()
        
        self.buttons_frame = tk.Frame(self.content_frame, bg='#cad2c5')
        self.buttons_frame.grid(row=3, column=0, sticky='nsew', pady=20)
        
        self.switch_to_mobile_layout()
    
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
            self.content_frame.grid_rowconfigure(0, weight=0)
            self.content_frame.grid_rowconfigure(1, weight=1)  
            self.content_frame.grid_columnconfigure(0, weight=1)
            try:
                # from EDMBank_contact import EDMBankContact 
                # EDMBankContact(self.content_frame, self.logged_in_user, self.logged_in_user_email, self.switch_view)
                lbl = tk.Label(self.content_frame, text="Chat/Contact View Placeholder", bg="#cad2c5")
                lbl.grid(row=0, column=0, pady=50)
            except ImportError as e:
                self.show_message("Error", f"EDMBank_contact.py error: {e}", "error")
        else:
            self.show_message("Navigation Error", f"View '{view_name}' is not yet implemented.", "warning")

    def create_bottom_menu(self):
        nav_frame = tk.Frame(self.main_container, bg="#7ecd9d", height=80)
        nav_frame.grid(row=2, column=0, sticky='ew', padx=0, pady=30)
        nav_frame.grid_propagate(False)
        
        nav_buttons_data = [
            ("HOME", "./icons/icon_home.png", self.go_home),
            ("CARD", "./icons/icon_card.png", self.show_cards),
            ("STATISTICS", "./icons/icon_stats.png", self.show_stats),
            ("PROFILE", "./icons/icon_profile.png", self.show_profile),
            ("CHAT", "./icons/icon_contact.png", self.open_chat)
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
    
    def show_cards(self):
        self.show_message("Cards", "Manage your cards", "info")

    def show_stats(self):
        self.show_message("Statistics", "Spending statistics", "info")
    
    def show_profile(self):
        self.show_message("Profile", f"User: {self.logged_in_user}", "info")

# --- Application Launch ---
if __name__ == "__main__":
    root = tk.Tk()
    app = EDMBankApp(root)
    root.mainloop()