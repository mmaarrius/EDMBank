import sys
import os
import tkinter as tk # Importul tk este mutat aici pentru a fi disponibil
from tkinter import TclError

# Add the project's root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from EDMBank_login import EDMBankLogin
from EDMBank_main import EDMBankApp
from services.bank_service import BankService
from DataBase.DataBase import Database

def apply_dpi_fix(root):
    try:
        root.tk.call('tk', 'scaling', 1.0) 
    except TclError:
        pass

def run_login_app(root, bank_service: BankService):
    # passes start_main_app as the success callback
    EDMBankLogin(root, start_main_app, bank_service)

def restart_app(current_root, bank_service):
    # store the current position and size for the new login window
    current_root.update_idletasks()
    x = current_root.winfo_x()
    y = current_root.winfo_y()
    width = current_root.winfo_width()
    height = current_root.winfo_height()
    
    # Destroy the current window
    current_root.destroy()
    
    # Create a new root for the login app
    new_root = tk.Tk()
    
    apply_dpi_fix(new_root)

    new_root.geometry(f"{width}x{height}+{x}+{y}")
    new_root.minsize(300, 500)
    
    run_login_app(new_root, bank_service)
    new_root.mainloop()

def start_main_app(username, login_window, bank_service: BankService):
    # get the position and size of the login window before destroying it
    login_window.update_idletasks()
    x = login_window.winfo_x()
    y = login_window.winfo_y()
    width = login_window.winfo_width()
    height = login_window.winfo_height()
    
    # destroy the login window
    login_window.destroy()
    
    # create a new main window in the EXACT same position and size
    main_root = tk.Tk()

    apply_dpi_fix(main_root)

    main_root.geometry(f"{width}x{height}+{x}+{y}")
    main_root.minsize(300, 500)
    
    # start the main app, passing the restart_app function as the logout callback
    app = EDMBankApp(main_root, relauch_login_callback=lambda: restart_app(main_root, bank_service))
    app.logged_in_user = username
    # update the card display for the logged in user
    app.update_card_display()
    main_root.mainloop()


# entry point
if __name__ == "__main__":
    root = tk.Tk()
    
    apply_dpi_fix(root)

    db = Database()
    bank_service = BankService(db)
    run_login_app(root, bank_service)
    root.mainloop()