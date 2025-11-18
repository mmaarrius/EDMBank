import tkinter as tk

class AlphaNumericKeyboard:
    def __init__(self, parent_frame, target_entry):
        self.parent_frame = parent_frame
        self.target_entry = target_entry
        self.is_shift_active = False
        
        # configure grid for the keyboard rows (10 columns)
        for i in range(10):
            self.parent_frame.grid_columnconfigure(i, weight=1)
        
        # button data
        self.buttons = [
            # row 1 (Numbers)
            ('1', 0, 0), ('2', 0, 1), ('3', 0, 2), ('4', 0, 3), ('5', 0, 4), 
            ('6', 0, 5), ('7', 0, 6), ('8', 0, 7), ('9', 0, 8), ('0', 0, 9),
            # row 2 (QWERT)
            ('Q', 1, 0), ('W', 1, 1), ('E', 1, 2), ('R', 1, 3), ('T', 1, 4), 
            ('Y', 1, 5), ('U', 1, 6), ('I', 1, 7), ('O', 1, 8), ('P', 1, 9),
            # row 3 (ASDFG)
            ('A', 2, 0), ('S', 2, 1), ('D', 2, 2), ('F', 2, 3), ('G', 2, 4), 
            ('H', 2, 5), ('J', 2, 6), ('K', 2, 7), ('L', 2, 8), ('_', 2, 9),
            # row 4 (Shift, ZXCVB, Backspace)
            ('⬆', 3, 0, 2), # Shift takes 2 columns
            ('Z', 3, 2), ('X', 3, 3), ('C', 3, 4), ('V', 3, 5), ('B', 3, 6), 
            ('N', 3, 7), ('M', 3, 8), 
            ('⌫', 3, 9, 1), # Backspace takes 1 column (M is at 3,8, so 3,9 is last key)
            # row 5 (Space and Enter)
            ('@', 4, 0), ('.', 4, 1), 
            (' ', 4, 2, 6),  # Space takes 6 columns
            ('Enter', 4, 8, 2) # Enter takes 2 columns
        ]
        
        self.create_buttons()
    
    # --------------------------------------------------------------------------
    # create buttons based on the self.buttons data
    def create_buttons(self):
        for item in self.buttons:
            text = item[0]
            row = item[1]
            col = item[2]
            col_span = item[3] if len(item) > 3 else 1 
            
            # button styling and command logic
            if text in ('⬆', '⌫'):
                bg_color = '#64748b'
                fg_color = 'white'
                command = self.toggle_shift if text == '⬆' else self.backspace
            elif text in (' ', '@', '.', '_'):
                bg_color = '#475569'
                fg_color = 'white'
                command = lambda t=text: self.type_character(t)
            elif text == 'Enter':
                bg_color = '#588157'
                fg_color = 'white'
                command = self.submit 
            else:
                # standard alphanumeric keys and numbers
                bg_color = '#84a98c'
                fg_color = '#2f3e46'
                command = lambda t=text: self.type_character(t)
            
            # key change: smaller font (10) and no explicit height
            btn = tk.Button(self.parent_frame, text=text, font=('Arial', 10, 'bold'),
                           bg=bg_color, fg=fg_color, relief='flat',
                           command=command)
            btn.grid(row=row, column=col, columnspan=col_span, padx=1, pady=1, sticky='nsew')
            
            # store the button for later updates (e.g., shift state)
            if text.isalpha() or text.isdigit():
                if not hasattr(self, 'letter_buttons'):
                    self.letter_buttons = {}
                self.letter_buttons[text] = btn

        # configure rows to expand vertically
        for i in range(5):
            self.parent_frame.grid_rowconfigure(i, weight=1)
    
    # --------------------------------------------------------------------------
    # handle typing a character into the target entry
    def type_character(self, char):
        current_text = self.target_entry.get()
        cursor_pos = self.target_entry.index(tk.INSERT)
        
        char_to_insert = char
        
        # handle case sensitivity for letters
        if char.isalpha():
            if self.is_shift_active:
                char_to_insert = char.upper()
            else:
                char_to_insert = char.lower()
        
        self.target_entry.insert(cursor_pos, char_to_insert)

    # --------------------------------------------------------------------------
    # handle backspace functionality
    def backspace(self):
        current_text = self.target_entry.get()
        cursor_pos = self.target_entry.index(tk.INSERT)
        
        if cursor_pos > 0:
            new_text = current_text[:cursor_pos-1] + current_text[cursor_pos:]
            self.target_entry.delete(0, tk.END)
            self.target_entry.insert(0, new_text)
            self.target_entry.icursor(cursor_pos - 1)

    # --------------------------------------------------------------------------
    # handle shift toggle
    def toggle_shift(self):
        self.is_shift_active = not self.is_shift_active
        
        # update button text to reflect case
        for text, btn in self.letter_buttons.items():
            if text.isalpha():
                if self.is_shift_active:
                    btn.config(text=text.upper())
                else:
                    btn.config(text=text.lower())
    
    # --------------------------------------------------------------------------
    # handle submit (Enter key)
    def submit(self):
        # hides the keyboard when "Enter" is pressed
        self.target_entry.icursor(tk.END)
        self.target_entry.focus_force() 
        self.parent_frame.pack_forget()