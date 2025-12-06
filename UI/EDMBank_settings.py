import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk 
import os

class EDMBankSettings:
    def __init__(self, parent_frame, current_user, bank_service, switch_view_callback, ui_helper):
        self.parent_frame = parent_frame
        self.current_user = current_user
        self.bank_service = bank_service
        self.logged_in_user = current_user.credentials.username
        self.logged_in_email = current_user.credentials.email 
        self.switch_view_callback = switch_view_callback
        self.ui = ui_helper
        
        # initial data
        # self.last_name, self.first_name = self._split_name(self.logged_in_user)
        # Use card expiry as a real data point
        self.card_expiry = current_user.card.expiry_date
        
        # variables for image (to maintain the profile picture on the left)
        self.profile_image_path = "profile_placeholder.png" 
        self.profile_photo_tk = None 
        
        self._set_styles()
        self.create_settings_view()

    # ------------------------------------------------------------------------------

    def _set_styles(self):
        style = ttk.Style()
        # Reduced font sizes for better fit
        style.configure('SettingsTitle.TLabel', background='#cad2c5', foreground='#354f52', font=self.ui.get_font('Tex Gyre Chorus', 14, 'bold'))
        style.configure('SettingsData.TLabel', background='#cad2c5', foreground='#2f3e46', font=self.ui.get_font('Courier', 12))

        # Reduced button font size and padding
        style.configure('Delete.TButton', foreground='white', background='#a90000', font=self.ui.get_font('Courier', 12, 'bold'), padding=self.ui.w_pct(1))
        style.map('Delete.TButton', background=[('active', '#ff6666')])
        
        # exit button
        style.configure('Exit.TButton', foreground='white', background='#354f52', font=self.ui.get_font('Courier', 12, 'bold'), padding=self.ui.w_pct(1))
        style.map('Exit.TButton', background=[('active', '#2f3e46')])

    # ------------------------------------------------------------------------------

    def _create_info_field(self, parent, label_text, info_text, row):
        # using the new fixed style names
        label = ttk.Label(parent, text=label_text, style='SettingsTitle.TLabel')
        label.grid(row=row, column=0, sticky='w', padx=self.ui.w_pct(1), pady=self.ui.h_pct(0.5))
        
        # Added wraplength to ensure text doesn't overflow horizontally
        info_label = ttk.Label(parent, text=info_text, style='SettingsData.TLabel', wraplength=self.ui.w_pct(40))
        info_label.grid(row=row, column=1, sticky='w', padx=self.ui.w_pct(2), pady=self.ui.h_pct(0.5))
        
        # add separator line
        ttk.Separator(parent, orient=tk.HORIZONTAL).grid(row=row+1, column=0, columnspan=2, sticky='ew')


    def load_profile_image(self, canvas, size_px):
        try:
            # load and resize the image
            original_image = Image.open(self.profile_image_path)
            size = (size_px, size_px)
            resized_image = original_image.resize(size, Image.LANCZOS)
            self.profile_photo_tk = ImageTk.PhotoImage(resized_image)
            
            # draw the image on the canvas
            canvas.create_image(size_px//2, size_px//2, image=self.profile_photo_tk, anchor='center')
        except Exception:
            # fallback text if image not found
            canvas.create_text(size_px//2, size_px//2, text="Profile\nPic", font=self.ui.get_font('Arial', 16), fill='black', justify=tk.CENTER)

    # ------------------------------------------------------------------------------

    def create_settings_view(self):
        
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
            
        main_content = tk.Frame(self.parent_frame, bg="#cad2c5", padx=self.ui.w_pct(4), pady=self.ui.h_pct(2))
        main_content.pack(fill='both', expand=True)

        # Reduced title font size
        tk.Label(main_content, text="ACCOUNT SETTINGS", font=self.ui.get_font('Arial', 24, 'bold'),
                 bg='#cad2c5', fg='#2f3e46').pack(pady=(self.ui.h_pct(2), self.ui.h_pct(4)))
        
        details_frame = tk.Frame(main_content, bg="#cad2c5")
        details_frame.pack(fill='x', pady=self.ui.h_pct(1))
        
        # configure columns for image (left) and fields (right)
        details_frame.grid_columnconfigure(0, weight=1) 
        details_frame.grid_columnconfigure(1, weight=3) 

        # profile picture section (mimics profile page visually)
        img_size = self.ui.get_size(120)
        image_canvas = tk.Canvas(details_frame, width=img_size, height=img_size, bg="lightgray", highlightthickness=0, borderwidth=2, relief='groove')
        image_canvas.grid(row=0, column=0, padx=self.ui.w_pct(2), pady=self.ui.h_pct(1), sticky='n', rowspan=4)
        self.load_profile_image(image_canvas, img_size)

        # fields frame (read-only info)
        fields_frame = tk.Frame(details_frame, bg="#cad2c5")
        fields_frame.grid(row=0, column=1, sticky='ew')
        fields_frame.grid_columnconfigure(1, weight=1) 

        # username
        self._create_info_field(fields_frame, "Username:", self.logged_in_user, 0)
        
        # email
        self._create_info_field(fields_frame, "Email:", self.logged_in_email, 2)
        
        # card expiry date
        self._create_info_field(fields_frame, "Card Expiry:", self.card_expiry, 4)
        
        action_frame = tk.Frame(main_content, bg='#cad2c5')
        action_frame.pack(fill='x', pady=self.ui.h_pct(4))
        action_frame.grid_columnconfigure(0, weight=1)
        action_frame.grid_columnconfigure(1, weight=1)
        
        # delete account button
        delete_btn = ttk.Button(action_frame, text="DELETE ACCOUNT", command=self.delete_account, style='Delete.TButton')
        delete_btn.grid(row=0, column=0, padx=self.ui.w_pct(1), sticky='ew')
        
        # exit button
        exit_btn = ttk.Button(action_frame, text="EXIT", command=self.exit_view, style='Exit.TButton')
        exit_btn.grid(row=0, column=1, padx=self.ui.w_pct(1), sticky='ew')


    # ------------------------------------------------------------------------------
    
    def delete_account(self):
        # confirm deletion
        confirm = messagebox.askyesno("Confirm Deletion", 
                                      "WARNING: Are you sure you want to permanently delete your account? This action cannot be undone.",
                                      parent=self.parent_frame)
        
        if confirm:
            try:
                self.bank_service.delete_user(self.current_user.credentials.username)
                # show the required message
                messagebox.showinfo("Account Deleted", "Your account has been deleted.", parent=self.parent_frame)
                
                # send back to login (using the same mechanism as logout)
                self.switch_view_callback("logout_relaunch")
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete account: {e}", parent=self.parent_frame)

    # ------------------------------------------------------------------------------

    def exit_view(self):
        self.switch_view_callback("home")