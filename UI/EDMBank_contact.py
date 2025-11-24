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
        
        self.style = ttk.Style()
        self.style.configure('Contact.TButton', 
                             foreground='#2f3e46',
                             font=('Helvetica', 26, 'bold'), 
                             padding=10)
        self.style.configure('Contact.TLabel', 
                             background='#354f52',
                             foreground='#cad2c5',
                             font=('Helvetica', 12))
        self.style.map('Contact.TButton',
                       background=[('active', '#84a98c')])
        
        self.style.configure('Dark.TEntry',
                             fieldbackground='#354f52',
                             foreground='#cad2c5',
                             insertcolor='#cad2c5',
                             borderwidth=0,
                             relief='flat')
        self.style.map('Dark.TEntry',
                       fieldbackground=[('focus', '#354f52')])

        self.keyboard_container = None
        self.keyboard_instance = None
        self.keyboard_visible = False
        
        self.create_interface()

    # --------------------------------------------------------------------------
    
    def create_interface(self):
        # clear any previous widgets in the parent frame
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        self.content_frame = tk.Frame(self.parent_frame, bg='#354f52')
        self.content_frame.pack(fill='both', expand=True, padx=0, pady=0)
        
        # configure the grid for the content frame
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(5, weight=1) # Row for the large Text box

        title_label = tk.Label(self.content_frame, 
                               text="Contact Support",
                               font=('Arial', 40, 'bold'), 
                               bg='#354f52', 
                               fg='#cad2c5')
        title_label.grid(row=0, column=0, pady=(20, 60), sticky='ew')

        info_frame = tk.Frame(self.content_frame, bg='#354f52', padx=10, pady=10)
        info_frame.grid(row=1, column=0, sticky='ew', pady=10)
        
        ttk.Label(info_frame, 
                  text=f"User: {self.logged_in_user.upper()}", 
                  style='Contact.TLabel', 
                  background='#354f52',
                  font=('Courier', 26, 'bold')).pack(anchor='w')
        
        ttk.Label(info_frame, 
                  text=f"Email: {self.logged_in_email}", 
                  style='Contact.TLabel', 
                  background='#354f52',
                  font=('Courier', 26)).pack(anchor='w')
        
        # Label for Title
        ttk.Label(self.content_frame, text="Problem Title:", style='Contact.TLabel',font=('Tex Gyre Chorus', 26, 'bold')).grid(row=2, column=0, sticky='w', pady=(10, 0))
        
        # Title Entry
        self.title_entry = tk.Entry(self.content_frame,
                                    width=10,
                                    font=('Courier', 20),  
                                    bg="#84a98c",
                                    fg="#052A30",
                                    relief=tk.FLAT,         
                                    bd=0,                   
                                    insertbackground='#cad2c5')
        self.title_entry.grid(row=3, column=0, sticky='ew', pady=(3, 10))
        
        # bind focus to title entry to SHOW keyboard
        self.title_entry.bind('<FocusIn>', lambda e: self.toggle_keyboard_visibility(self.title_entry))
        
        # Label for Concern - Uses Contact.TLabel style (Font 12)
        ttk.Label(self.content_frame, text="Describe your concern:", style='Contact.TLabel',font=('Tex Gyre Chorus', 26, 'bold')).grid(row=4, column=0, sticky='w', pady=(10, 0))
        
        # Concern Text - FONT MĂRIT: 12 -> 14
        self.concern_text = Text(self.content_frame, 
                                 height=2, 
                                 width=30, 
                                 font=('Courier', 20), 
                                 relief=tk.FLAT, 
                                 bd=0, 
                                 bg="#84a98c", 
                                 fg="#052A30",
                                 insertbackground='#cad2c5',
                                 padx=5, pady=10)
        # this is the expanding row (weight=1)
        self.concern_text.grid(row=5, column=0, sticky='nsew', pady=(3, 20)) 
        
        # bind focus in on concern text to SHOW keyboard and update target
        self.concern_text.bind('<FocusIn>', lambda e: self.toggle_keyboard_visibility(self.concern_text)) 
        
        button_frame = tk.Frame(self.content_frame, bg='#354f52')
        button_frame.grid(row=6, column=0, sticky='ew', pady=(0, 10))
        
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
        
        self.keyboard_container = tk.Frame(self.content_frame, bg='#354f52')
        
        # initialize the keyboard instance
        self.keyboard_instance = AlphaNumericKeyboard(self.keyboard_container, self.title_entry)

        self.keyboard_container.grid(row=7, column=0, sticky='ew')
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
            f"User: {self.logged_in_user.upper()}\n"
            f"Email: {self.logged_in_email}\n"
            f"Title: {title}\n"
            f"Message Snippet: {concern[:50]}..."
        )
        
        messagebox.showinfo("Submission Confirmed", confirmation_message)
        
        # clear the form after submission
        self.title_entry.delete(0, tk.END)
        self.concern_text.delete("1.0", tk.END)
        
        # after successful submission, go back home
        self.switch_view_callback("home")