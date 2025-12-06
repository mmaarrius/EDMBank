import tkinter as tk
from tkinter import ttk, messagebox, Text
from exceptions import RequestError

class EDMBankContact:
    def __init__(self, parent_frame, current_user, bank_service, switch_view_callback, ui_helper):
        # store essential references
        self.parent_frame = parent_frame
        self.current_user = current_user
        self.bank_service = bank_service
        self.logged_in_user = current_user.credentials.username
        self.logged_in_email = current_user.credentials.email 
        self.switch_view_callback = switch_view_callback
        self.ui = ui_helper
        
        # Initial data preparation
        # self.last_name, self.first_name = self._split_name(self.logged_in_user)
        
        # Tkinter variables for user info (Read-only on this screen)
        self.username_var = tk.StringVar(value=self.logged_in_user)
        self.email_var = tk.StringVar(value=self.logged_in_email)
        
        # Define the light background color consistent with the Profile view
        DARK_TEXT = '#2f3e46' 
        
        self.style = ttk.Style()
        
        # Contact.TButton: Button style
        self.style.configure('Contact.TButton', 
                             foreground=DARK_TEXT,
                             font=self.ui.get_font('Helvetica', 14, 'bold'), 
                             padding=self.ui.w_pct(1))
        
        # Contact.TLabel: Label style 
        self.style.configure('Contact.TLabel', 
                             background='#cad2c5', 
                             foreground=DARK_TEXT,
                             font=self.ui.get_font('Helvetica', 12))
        
        # Active state for buttons (e.g., hover)
        self.style.map('Contact.TButton',
                       background=[('active', '#84a98c')])
        
        self.create_interface()

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
                  font=self.ui.get_font('Tex Gyre Chorus', 18, 'bold')
                  ).grid(row=row, column=0, padx=self.ui.w_pct(1), pady=self.ui.h_pct(0.5), sticky='w')
        
        # Entry (Right Column - Read Only)
        entry = tk.Entry(parent, 
                         textvariable=textvariable, 
                         font=self.ui.get_font('Courier', 14),
                         bg=ACCENT_COLOR,
                         fg=DARK_TEXT,
                         relief=tk.FLAT, 
                         bd=0,                   
                         insertbackground=DARK_TEXT) 
        
        entry.config(state='readonly')
        entry.grid(row=row, column=1, padx=self.ui.w_pct(1), pady=self.ui.h_pct(0.5), sticky='ew')
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
                               font=self.ui.get_font('Arial', 28, 'bold'), 
                               bg=LIGHT_BG, 
                               fg=DARK_TEXT)
        title_label.grid(row=0, column=0, pady=(self.ui.h_pct(2), self.ui.h_pct(3)), sticky='ew')

        # Row 1: User Details Frame (Contains Username, Email)
        user_details_frame = tk.Frame(self.content_frame, bg=LIGHT_BG, padx=self.ui.w_pct(2), pady=self.ui.h_pct(1))
        user_details_frame.grid(row=1, column=0, sticky='ew')
        user_details_frame.grid_columnconfigure(1, weight=1) 

        self._create_read_only_field(user_details_frame, "Username:", self.username_var, 0)
        self._create_read_only_field(user_details_frame, "Email:", self.email_var, 1)


        # Row 2: Label for Problem Title
        ttk.Label(self.content_frame, 
                  text="Problem Title:", 
                  style='Contact.TLabel',
                  background=LIGHT_BG,
                  foreground=DARK_TEXT,
                  font=self.ui.get_font('Tex Gyre Chorus', 18, 'bold')).grid(row=2, column=0, sticky='w', padx=self.ui.w_pct(2), pady=(self.ui.h_pct(1), 0))
        
        # Row 3: Problem Title Entry (Editable)
        self.title_entry = tk.Entry(self.content_frame,
                                    width=10,
                                    font=self.ui.get_font('Courier', 14),  
                                    bg=ACCENT_COLOR,
                                    fg=DARK_TEXT,
                                    relief=tk.FLAT, 
                                    bd=0,                   
                                    insertbackground=DARK_TEXT)
        self.title_entry.grid(row=3, column=0, sticky='ew', padx=self.ui.w_pct(2), pady=(self.ui.h_pct(0.5), self.ui.h_pct(1)))
        
        # Row 4: Label for Concern
        ttk.Label(self.content_frame, 
                  text="Describe your concern:", 
                  style='Contact.TLabel',
                  background=LIGHT_BG,
                  foreground=DARK_TEXT,
                  font=self.ui.get_font('Tex Gyre Chorus', 18, 'bold')).grid(row=4, column=0, sticky='w', padx=self.ui.w_pct(2), pady=(self.ui.h_pct(1), 0))
        
        # concern text (editable, takes up remaining vertical space)
        self.concern_text = Text(self.content_frame, 
                                 height=2, 
                                 width=30, 
                                 font=self.ui.get_font('Courier', 14), 
                                 relief=tk.FLAT, 
                                 bd=0, 
                                 bg=ACCENT_COLOR, 
                                 fg=DARK_TEXT,
                                 insertbackground=DARK_TEXT,
                                 padx=5, pady=10)
        self.concern_text.grid(row=5, column=0, sticky='nsew', padx=self.ui.w_pct(2), pady=(self.ui.h_pct(0.5), self.ui.h_pct(2)), rowspan=3) 
        self.content_frame.grid_rowconfigure(5, weight=1) # ensure the text area is the one that expands
        
        # button Frame
        button_frame = tk.Frame(self.content_frame, bg=LIGHT_BG)
        button_frame.grid(row=8, column=0, sticky='ew', pady=(0, self.ui.h_pct(1)), padx=self.ui.w_pct(2))
        
        # submit button
        submit_btn = ttk.Button(button_frame, 
                              text="Submit Concern", 
                              command=self.submit_concern, 
                              style='Contact.TButton')
        submit_btn.pack(side='left', expand=True, fill='x', padx=(self.ui.w_pct(0.5), self.ui.w_pct(1)))

        # back button
        back_btn = ttk.Button(button_frame, 
                              text="Back to Home", 
                              command=lambda: self.switch_view_callback("home"), 
                              style='Contact.TButton')
        back_btn.pack(side='right', expand=True, fill='x', padx=(self.ui.w_pct(1), 0))

    # --------------------------------------------------------------------------
    
    def submit_concern(self):
        
        title = self.title_entry.get().strip()
        concern = self.concern_text.get("1.0", tk.END).strip()
        
        # basic validation
        if not title:
            messagebox.showerror("Submission Error", "Please provide a title for your problem.")
            return

        if not concern:
            messagebox.showerror("Submission Error", "Please write your concern in the message box.")
            return

        try:
            # Send request to bank service
            self.bank_service.create_support_request(self.current_user, title, concern)

            # confirmation message
            confirmation_message = (
                f"Your concern has been submitted successfully!\n\n"
                f"User: {self.username_var.get()}\n"
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

        except RequestError as e:
            messagebox.showerror("Submission Error", f"Failed to submit request: {e}")
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {e}")
