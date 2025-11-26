import tkinter as tk
from tkinter import ttk, messagebox, Text
# Assuming EDMBank_keyboard is in the same directory
from EDMBank_keyboard import AlphaNumericKeyboard 

class EDMBankContact:
    def __init__(self, parent_frame, logged_in_user, logged_in_email, switch_view_callback):
        # store essential references
        self.parent_frame = parent_frame
        self.logged_in_user = logged_in_user
        self.logged_in_email = logged_in_email 
        self.switch_view_callback = switch_view_callback
        
        # Initial data preparation
        self.last_name, self.first_name = self._split_name(self.logged_in_user)
        
        # Tkinter variables for user info (Read-only on this screen)
        self.first_name_var = tk.StringVar(value=self.first_name)
        self.last_name_var = tk.StringVar(value=self.last_name)
        self.email_var = tk.StringVar(value=self.logged_in_email)
        
        # Define the light background color consistent with the Profile view
        DARK_TEXT = '#2f3e46' 
        
        self.style = ttk.Style()
        
        # Contact.TButton: Button style
        self.style.configure('Contact.TButton', 
                             foreground=DARK_TEXT,
                             font=('Helvetica', 26, 'bold'), 
                             padding=10)
        
        # Contact.TLabel: Label style 
        self.style.configure('Contact.TLabel', 
                             background='#cad2c5', 
                             foreground=DARK_TEXT,
                             font=('Helvetica', 12))
        
        # Active state for buttons (e.g., hover)
        self.style.map('Contact.TButton',
                       background=[('active', '#84a98c')])
        
        self.keyboard_container = None
        self.keyboard_instance = None
        self.keyboard_visible = False
        
        self.create_interface()

    def _split_name(self, full_name):
        """Splits the full name into Last Name and First Name (assuming Last Name is first word)."""
        parts = full_name.split()
        if len(parts) >= 2:
            last_name = parts[0]
            first_name = " ".join(parts[1:])
            return last_name, first_name
        return full_name, "" 

    def _create_read_only_field(self, parent, label_text, textvariable, row):
        """Helper to create a label and a read-only Entry field in the new style."""
        LIGHT_BG = '#cad2c5'
        DARK_TEXT = '#2f3e46'
        ACCENT_COLOR = '#84a98c'
        
        # Label (Left Column)
        ttk.Label(parent, 
                  text=label_text, 
                  style='Contact.TLabel',
                  background=LIGHT_BG,
                  foreground=DARK_TEXT,
                  font=('Courier', 20, 'bold')
                  ).grid(row=row, column=0, padx=10, pady=5, sticky='w')
        
        # Entry (Right Column - Read Only)
        entry = tk.Entry(parent, 
                         textvariable=textvariable, 
                         font=('Courier', 20),
                         bg=ACCENT_COLOR,
                         fg=DARK_TEXT,
                         relief=tk.FLAT, 
                         bd=0,                   
                         insertbackground=DARK_TEXT) 
        
        entry.config(state='readonly')
        entry.grid(row=row, column=1, padx=10, pady=5, sticky='ew')
        return entry
    
    # --------------------------------------------------------------------------
    
    def create_interface(self):
        # Define colors locally
        LIGHT_BG = '#cad2c5' 
        DARK_TEXT = '#2f3e46'
        ACCENT_COLOR = '#84a98c'
        
        # clear any previous widgets in the parent frame
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        # Main content frame - Background: #cad2c5 (light background)
        self.content_frame = tk.Frame(self.parent_frame, bg=LIGHT_BG)
        self.content_frame.pack(fill='both', expand=True, padx=0, pady=0)
        
        # configure the grid for the content frame
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(7, weight=1) # Row for the large Text box

        # Row 0: Title Label
        title_label = tk.Label(self.content_frame, 
                               text="CONTACT SUPPORT",
                               font=('Arial', 40, 'bold'), 
                               bg=LIGHT_BG, 
                               fg=DARK_TEXT)
        title_label.grid(row=0, column=0, pady=(20, 30), sticky='ew')

        # Row 1: User Details Frame (Contains First Name, Last Name, Email)
        user_details_frame = tk.Frame(self.content_frame, bg=LIGHT_BG, padx=20, pady=10)
        user_details_frame.grid(row=1, column=0, sticky='ew')
        user_details_frame.grid_columnconfigure(1, weight=1) 

        self._create_read_only_field(user_details_frame, "First Name:", self.first_name_var, 0)
        self._create_read_only_field(user_details_frame, "Last Name:", self.last_name_var, 1)
        self._create_read_only_field(user_details_frame, "Email:", self.email_var, 2)


        # Row 2: Label for Problem Title
        ttk.Label(self.content_frame, 
                  text="Problem Title:", 
                  style='Contact.TLabel',
                  background=LIGHT_BG,
                  foreground=DARK_TEXT,
                  font=('Tex Gyre Chorus', 26, 'bold')).grid(row=2, column=0, sticky='w', padx=20, pady=(10, 0))
        
        # Row 3: Problem Title Entry (Editable)
        self.title_entry = tk.Entry(self.content_frame,
                                    width=10,
                                    font=('Courier', 20),  
                                    bg=ACCENT_COLOR,
                                    fg=DARK_TEXT,
                                    relief=tk.FLAT, 
                                    bd=0,                   
                                    insertbackground=DARK_TEXT)
        self.title_entry.grid(row=3, column=0, sticky='ew', padx=20, pady=(3, 10))
        
        # bind focus to title entry to SHOW keyboard
        self.title_entry.bind('<FocusIn>', lambda e: self.toggle_keyboard_visibility(self.title_entry))
        
        # Row 4: Label for Concern
        ttk.Label(self.content_frame, 
                  text="Describe your concern:", 
                  style='Contact.TLabel',
                  background=LIGHT_BG,
                  foreground=DARK_TEXT,
                  font=('Tex Gyre Chorus', 26, 'bold')).grid(row=4, column=0, sticky='w', padx=20, pady=(10, 0))
        
        # concern text (editable, takes up remaining vertical space)
        self.concern_text = Text(self.content_frame, 
                                 height=2, 
                                 width=30, 
                                 font=('Courier', 20), 
                                 relief=tk.FLAT, 
                                 bd=0, 
                                 bg=ACCENT_COLOR, 
                                 fg=DARK_TEXT,
                                 insertbackground=DARK_TEXT,
                                 padx=5, pady=10)
        self.concern_text.grid(row=5, column=0, sticky='nsew', padx=20, pady=(3, 20), rowspan=3) 
        self.content_frame.grid_rowconfigure(5, weight=1) # ensure the text area is the one that expands
        
        # bind focus in on concern text to show keyboard and update target
        self.concern_text.bind('<FocusIn>', lambda e: self.toggle_keyboard_visibility(self.concern_text)) 
        
        # button Frame
        button_frame = tk.Frame(self.content_frame, bg=LIGHT_BG)
        button_frame.grid(row=8, column=0, sticky='ew', pady=(0, 10), padx=20)
        
        # submit button
        submit_btn = ttk.Button(button_frame, 
                              text="Submit Concern", 
                              command=self.submit_concern, 
                              style='Contact.TButton')
        submit_btn.pack(side='left', expand=True, fill='x', padx=(3, 10))

        # back button
        back_btn = ttk.Button(button_frame, 
                              text="Back to Home", 
                              command=lambda: self.switch_view_callback("home"), 
                              style='Contact.TButton')
        back_btn.pack(side='right', expand=True, fill='x', padx=(10, 0))
        
        # Row 9: Keyboard Container
        self.keyboard_container = tk.Frame(self.content_frame, bg=LIGHT_BG)
        
        # initialize the keyboard instance
        self.keyboard_instance = AlphaNumericKeyboard(self.keyboard_container, self.title_entry)

        self.keyboard_container.grid(row=9, column=0, sticky='ew')
        # use grid_remove() to hide the keyboard initially
        self.keyboard_container.grid_remove()

    # --------------------------------------------------------------------------
    
    def toggle_keyboard_visibility(self, target_widget):
        
        # check if a supported widget is being focused
        if target_widget in (self.title_entry, self.concern_text):
            # if the keyboard is hidden or the target has changed, show it and update target
            if not self.keyboard_visible or self.keyboard_instance.target_entry != target_widget:
                # update the keyboard's target entry
                self.keyboard_instance.target_entry = target_widget 
                self.keyboard_container.grid() 
                self.keyboard_visible = True
        else:
            # if focus is elsewhere, hide the keyboard
            if self.keyboard_visible:
                self.keyboard_container.grid_remove() 
                self.keyboard_visible = False

    # --------------------------------------------------------------------------
    
    def submit_concern(self):
        
        # hide the keyboard on submission
        if self.keyboard_visible:
            self.keyboard_container.grid_remove() 
            self.keyboard_visible = False

        title = self.title_entry.get().strip()
        concern = self.concern_text.get("1.0", tk.END).strip()
        
        # basic validation
        if not title:
            messagebox.showerror("Submission Error", "Please provide a title for your problem.")
            return

        if not concern:
            messagebox.showerror("Submission Error", "Please write your concern in the message box.")
            return

        # confirmation message
        confirmation_message = (
            f"Your concern has been submitted successfully!\n\n"
            f"User: {self.last_name_var.get()} {self.first_name_var.get()}\n"
            f"Email: {self.email_var.get()}\n"
            f"Title: {title}\n"
            f"Message Snippet: {concern[:50]}..."
        )
        
        messagebox.showinfo("Submission Confirmed", confirmation_message)
        
        # clear the form after submission
        self.title_entry.delete(0, tk.END)
        self.concern_text.delete("1.0", tk.END)
        
        # after successful submission, go back home
        self.switch_view_callback("home")