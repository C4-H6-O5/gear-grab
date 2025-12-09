import customtkinter as ctk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta

# Refactored imports
import database as db
from config import *
from ui_components import CleanCard, AddItemWindow, MyBorrowingsWindow, PaymentInfoWindow

# Configure Global Theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class LensLockerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gear Grab - Focus BatStateU Camera Club")
        self.geometry("1300x850")
        self.minsize(1100, 700)
        
        # Apply Background Color
        self.configure(fg_color=COLOR_BG)

        self.current_user = None
        self.selected_card_widget = None
        self.current_selection_data = None

        # Main Container
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=25, pady=25)

        self.show_login_screen()

    # ============================================
    # SCREEN 1: ELEGANT LOGIN
    # ============================================
    def show_login_screen(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        # Main Login Frame with elegant design
        login_container = ctk.CTkFrame(self.container, fg_color="transparent")
        login_container.pack(fill="both", expand=True)
        
        # Left side - Branding
        brand_frame = ctk.CTkFrame(login_container, fg_color="transparent", width=400)
        brand_frame.pack(side="left", fill="both", expand=True, padx=(0, 40))
        
        # Elegant Logo/Branding
        ctk.CTkLabel(brand_frame, text="GEAR GRAB", 
                    font=("Montserrat", 48, "bold"), 
                    text_color=COLOR_ACCENT_PRIMARY).pack(pady=(100, 10))
        
        ctk.CTkLabel(brand_frame, text="BATSTATEU CAMERA CLUB", 
                    font=("Montserrat", 18), 
                    text_color=COLOR_TEXT_GRAY).pack(pady=(0, 40))
        
        # Camera Icon
        ctk.CTkLabel(brand_frame, text="📷", font=("Montserrat", 48), text_color=COLOR_TEXT_GRAY).pack(pady=(0, 20))
        
        # Tagline
        ctk.CTkLabel(brand_frame, text="Camera Club Equipment Management", 
                    font=("Montserrat", 14), 
                    text_color=COLOR_TEXT_GRAY).pack(pady=20)
        
        # Right side - Login Form
        login_frame = ctk.CTkFrame(login_container, width=400, height=500, 
                                  fg_color=COLOR_CARD, corner_radius=16,
                                  border_color=COLOR_BG, border_width=1)
        login_frame.pack(side="right", fill="both", expand=True, pady=100)
        login_frame.pack_propagate(False)
        
        # Form Header
        ctk.CTkLabel(login_frame, text="Welcome Back", 
                    font=("Montserrat", 28, "bold"), 
                    text_color=COLOR_TEXT_WHITE).pack(pady=(50, 10))
        
        ctk.CTkLabel(login_frame, text="Sign in to access club gear", 
                    font=("Montserrat", 14), 
                    text_color=COLOR_TEXT_GRAY).pack(pady=(0, 40))
        
        # Input Field with modern styling
        input_frame = ctk.CTkFrame(login_frame, fg_color="transparent")
        input_frame.pack(pady=20, padx=40)
        
        ctk.CTkLabel(input_frame, text="Member ID", 
                    font=("Montserrat", 12, "bold"), 
                    text_color=COLOR_TEXT_GRAY).pack(anchor="w", pady=(0, 5))
        
        self.entry_id = ctk.CTkEntry(input_frame, placeholder_text="Enter your member ID", 
                                     width=320, height=45,
                                     fg_color=COLOR_BG, 
                                     border_color=COLOR_BG,
                                     text_color=COLOR_TEXT_WHITE,
                                     font=("Montserrat", 14),
                                     corner_radius=8)
        self.entry_id.pack(pady=(0, 20))
        self.entry_id.bind('<Return>', lambda event: self.process_login())
        
        # Login Button
        btn_login = ctk.CTkButton(login_frame, text="Access System", 
                                  width=320, height=45,
                                  fg_color=COLOR_ACCENT_PRIMARY, 
                                  text_color="white",
                                  font=("Montserrat", 14, "bold"),
                                  corner_radius=8,
                                  hover_color=COLOR_ACCENT_SECONDARY,
                                  command=self.process_login)
        btn_login.pack(pady=20)
        
        # Demo hint
        hint_frame = ctk.CTkFrame(login_frame, fg_color=COLOR_BG, corner_radius=8)
        hint_frame.pack(pady=30, padx=40, fill="x")
        ctk.CTkLabel(hint_frame, text="💡 Try ID: 1 (John) or 2 (Officer Justine)", 
                    font=("Montserrat", 11), 
                    text_color=COLOR_TEXT_GRAY,
                    pady=10).pack()

    def process_login(self):
        user_input = self.entry_id.get().strip()
        if not user_input.isdigit():
            messagebox.showerror("Error", "Please enter a numeric Member ID.")
            return

        user = db.get_member_by_id(user_input)

        if user:
            self.current_user = dict(user)
            self.show_dashboard_screen()
        else:
            messagebox.showerror("Error", "Member ID not found.")

    # ============================================
    # SCREEN 2: MODERN DASHBOARD
    # ============================================
    def show_dashboard_screen(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        # --- HEADER ---
        header_frame = ctk.CTkFrame(self.container, fg_color=COLOR_CARD, corner_radius=12)
        header_frame.pack(fill="x", pady=(0, 20))
        
        # User info
        user_info = ctk.CTkFrame(header_frame, fg_color="transparent")
        user_info.pack(side="left", padx=30, pady=15)
        
        ctk.CTkLabel(user_info, 
                    text=f"👤 {self.current_user['Name']}",
                    font=("Montserrat", 18, "bold"),
                    text_color=COLOR_TEXT_WHITE).pack(anchor="w")
        
        role_text = "Officer" if self.current_user['IsOfficer'] else "Member"
        role_color = COLOR_ACCENT_PRIMARY if self.current_user['IsOfficer'] else COLOR_TEXT_GRAY
        ctk.CTkLabel(user_info, 
                    text=role_text,
                    font=("Montserrat", 12),
                    text_color=role_color).pack(anchor="w", pady=(2, 0))
        
        # Action buttons
        action_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        action_frame.pack(side="right", padx=30, pady=15)
        
        if self.current_user['IsOfficer']:
            ctk.CTkButton(action_frame, text="+ Add Equipment", 
                         width=120, height=35,
                         fg_color=COLOR_ACCENT_SECONDARY,
                         text_color="white",
                         font=("Montserrat", 12, "bold"),
                         corner_radius=8,
                         command=self.open_add_item_window).pack(side="left", padx=5) # This now calls the class
        
        # Add Payment Info button to header
        ctk.CTkButton(action_frame, text="💰 Payment Info", 
                     width=120, height=35,
                     fg_color="transparent",
                     border_color=COLOR_WARNING,
                     border_width=2,
                     text_color=COLOR_WARNING,
                     font=("Montserrat", 12),
                     corner_radius=8,
                     command=lambda: PaymentInfoWindow(self)).pack(side="left", padx=5)
        
        ctk.CTkButton(action_frame, text="My Borrowed Items", 
                     width=140, height=35,
                     fg_color="transparent",
                     border_color=COLOR_ACCENT_PRIMARY,
                     border_width=2,
                     text_color=COLOR_ACCENT_PRIMARY,
                     font=("Montserrat", 12),
                     corner_radius=8,
                     command=lambda: MyBorrowingsWindow(self)).pack(side="left", padx=5)
        
        ctk.CTkButton(action_frame, text="Logout", 
                     width=80, height=35,
                     fg_color="transparent",
                     border_color=COLOR_BG,
                     border_width=1,
                     text_color=COLOR_TEXT_GRAY,
                     font=("Montserrat", 12),
                     corner_radius=8,
                     command=self.logout).pack(side="left", padx=5)
        
        # --- SEARCH & FILTER ---
        filter_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        filter_frame.pack(fill="x", pady=(0, 15))
        
        # Search bar
        search_container = ctk.CTkFrame(filter_frame, fg_color=COLOR_CARD, corner_radius=8, height=45)
        search_container.pack(side="left", fill="x", expand=True, padx=(0, 10))
        search_container.pack_propagate(False)
        
        ctk.CTkLabel(search_container, text="🔍", 
                    font=("Montserrat", 16),
                    text_color=COLOR_TEXT_GRAY).pack(side="left", padx=15)
        
        self.search_var = ctk.StringVar()
        self.search_var.trace("w", self.filter_inventory)
        
        search_entry = ctk.CTkEntry(search_container, 
                                   placeholder_text="Search for cameras, lenses, etc...",
                                   textvariable=self.search_var,
                                   fg_color="transparent",
                                   border_width=0,
                                   text_color=COLOR_TEXT_WHITE,
                                   font=("Montserrat", 13),
                                   height=45)
        search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Category filter
        filter_container = ctk.CTkFrame(filter_frame, fg_color=COLOR_CARD, corner_radius=8, height=45)
        filter_container.pack(side="right", padx=(10, 0))
        filter_container.pack_propagate(False)
        
        self.cat_filter = ctk.CTkComboBox(filter_container, 
                                         values=["All Categories", "Camera Body", "Camera Lens", "Lighting", 
                                                 "Tripods & Support", "Audio & Microphones", "Drones", 
                                                 "Stabilizers & Gimbals", "Studio Accessories"],
                                         command=self.filter_inventory,
                                         width=200,
                                         height=35,
                                         fg_color=COLOR_BG,
                                         border_color=COLOR_BG,
                                         button_color=COLOR_ACCENT_PRIMARY,
                                         button_hover_color=COLOR_ACCENT_SECONDARY,
                                         text_color=COLOR_TEXT_WHITE,
                                         dropdown_fg_color=COLOR_CARD,
                                         dropdown_text_color=COLOR_TEXT_WHITE)
        self.cat_filter.set("All Categories")
        self.cat_filter.pack(pady=5, padx=10)
        
        # --- INVENTORY CARDS AREA ---
        self.scroll_frame = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True)
        
        # --- SELECTION ACTION BAR ---
        self.action_bar = ctk.CTkFrame(self.container, fg_color=COLOR_CARD, corner_radius=12, height=70)
        self.action_bar.pack(fill="x", pady=(15, 0))
        self.action_bar.pack_propagate(False)
        
        # Selection info
        self.lbl_selection = ctk.CTkFrame(self.action_bar, fg_color="transparent")
        self.lbl_selection.pack(side="left", padx=30, fill="both", expand=True)
        
        self.lbl_selected = ctk.CTkLabel(self.lbl_selection, 
                                        text="No equipment selected",
                                        font=("Montserrat", 14),
                                        text_color=COLOR_TEXT_GRAY)
        self.lbl_selected.pack(anchor="w")
        
        self.lbl_status = ctk.CTkLabel(self.lbl_selection,
                                      text="Select an item to view details.",
                                      font=("Montserrat", 12),
                                      text_color=COLOR_TEXT_GRAY)
        self.lbl_status.pack(anchor="w", pady=(2, 0))
        
        # Action buttons container
        btn_container = ctk.CTkFrame(self.action_bar, fg_color="transparent")
        btn_container.pack(side="right", padx=30)
        
        if self.current_user['IsOfficer']:
            # Officer-only controls
            officer_controls = ctk.CTkFrame(btn_container, fg_color="transparent")
            officer_controls.pack(side="left", padx=(0, 10))
            
            self.btn_delete = ctk.CTkButton(officer_controls, text="Remove",
                                           width=100, height=35,
                                           fg_color="transparent",
                                           border_color=COLOR_BG,
                                           border_width=1,
                                           text_color=COLOR_TEXT_GRAY,
                                           font=("Montserrat", 12),
                                           state="disabled",
                                           corner_radius=8,
                                           command=self.delete_item)
            self.btn_delete.pack(side="left", padx=5)
            
            # Status change dropdown for officers - REMOVED "Internal" option
            self.status_var = ctk.StringVar(value="Change Status")
            self.status_dropdown = ctk.CTkOptionMenu(officer_controls,
                                                   values=["Available", "Maintenance", "Lost"],  # Removed "Internal"
                                                   variable=self.status_var,
                                                   width=140,
                                                   height=35,
                                                   fg_color=COLOR_BG,
                                                   button_color=COLOR_ACCENT_SECONDARY,
                                                   button_hover_color=COLOR_ACCENT_PRIMARY,
                                                   text_color=COLOR_TEXT_WHITE,
                                                   state="disabled",
                                                   command=self.change_item_status)
            self.status_dropdown.pack(side="left", padx=5)
            
            # Keep internal use switch for borrowing
            self.internal_use_var = ctk.BooleanVar(value=False)
            self.switch_internal = ctk.CTkSwitch(btn_container, 
                                                text="Internal Use",
                                                variable=self.internal_use_var,
                                                progress_color=COLOR_ACCENT_SECONDARY,
                                                text_color=COLOR_TEXT_GRAY,
                                                font=("Montserrat", 12))
            self.switch_internal.pack(side="left", padx=10)
        
        # Borrow button for all users
        self.btn_borrow = ctk.CTkButton(btn_container, text="Borrow",
                                       width=120, height=35,
                                       fg_color=COLOR_ACCENT_PRIMARY,
                                       text_color="white",
                                       font=("Montserrat", 12, "bold"),
                                       state="disabled",
                                       corner_radius=8,
                                       command=self.process_borrow)
        self.btn_borrow.pack(side="left", padx=5)
        
        # Load data
        self.load_inventory_data()

    # ============================================
    # NEW CARD DESIGN - Clean, left strip, no prices
    # ============================================
    def load_inventory_data(self):
        self.all_inventory = db.get_all_inventory()
        self.filter_inventory()

    def filter_inventory(self, *args):
        # Clear existing cards
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        self.selected_card_widget = None
        self.current_selection_data = None
        self.update_selection_display()

        search_text = self.search_var.get().lower()
        cat_filter = self.cat_filter.get()

        # Create cards in a responsive grid
        cards = []
        for row_data in self.all_inventory:
            match_search = search_text in row_data['ModelName'].lower() or search_text in row_data['AssetTag'].lower()
            match_cat = cat_filter == "All Categories" or cat_filter == row_data['CatName']

            if match_search and match_cat:
                cards.append(row_data)

        # Create grid - use 4 columns by default
        cols = 4
        for i in range(cols):
            self.scroll_frame.grid_columnconfigure(i, weight=1)

        # Create cards in grid
        row, col = 0, 0
        for data in cards:
            self.create_clean_card(data, row, col)
            col += 1
            if col >= cols:
                col = 0
                row += 1

    def create_clean_card(self, data, row, col):
        # Get status color and icon
        status_color = STATUS_COLORS.get(data['Status'], COLOR_NEUTRAL)
        CleanCard(self.scroll_frame, data, row, col, self)

    def select_card(self, data, card_container):
        # Reset all cards to normal state
        for child in self.scroll_frame.winfo_children():
            if isinstance(child, CleanCard):
                child.deselect()
        
        # Mark as selected with full card color change
        card_container.select()
        
        # Store selection
        self.selected_card_widget = card_container
        self.current_selection_data = data
        
        # Update selection display
        self.update_selection_display()
        
        # Enable/disable buttons based on status
        if data['Status'] == 'Available':
            self.btn_borrow.configure(state="normal", 
                                     fg_color=COLOR_ACCENT_PRIMARY,
                                     text_color="white")
        else:
            self.btn_borrow.configure(state="disabled", 
                                     fg_color="#2A2A36",
                                     text_color=COLOR_TEXT_GRAY)
        
        if self.current_user['IsOfficer']:
            self.btn_delete.configure(state="normal",
                                     text_color="white",
                                     fg_color=COLOR_DANGER,
                                     border_width=0)
            self.status_dropdown.configure(state="normal")

    def update_selection_display(self):
        if not self.current_selection_data:
            self.lbl_selected.configure(text="No equipment selected",
                                       text_color=COLOR_TEXT_GRAY)
            self.lbl_status.configure(text="Select an item to view details.",
                                     text_color=COLOR_TEXT_GRAY, font=("Montserrat", 12))
            return
        
        data = self.current_selection_data
        self.lbl_selected.configure(text=f"{data['ModelName']}",
                                   text_color=COLOR_TEXT_WHITE)
        
        status_color = STATUS_COLORS.get(data['Status'], COLOR_TEXT_GRAY)
        self.lbl_status.configure(text=f"{data['AssetTag']} • {data['CatName']} • Status: {data['Status']}",
                                 text_color=status_color)

    # ============================================
    # OFFICER: CHANGE ITEM STATUS
    # ============================================
    def change_item_status(self, new_status):
        if not self.current_selection_data:
            return
        
        asset_tag = self.current_selection_data['AssetTag']
        current_status = self.current_selection_data['Status']
        
        if new_status == current_status:
            return
        
        # Confirmation
        confirm = messagebox.askyesno("Change Status",
                                     f"Change {asset_tag} from '{current_status}' to '{new_status}'?")
        
        if confirm:
            db.update_item_status(asset_tag, new_status)

            messagebox.showinfo("Status Updated", 
                              f"✅ {asset_tag} status changed to '{new_status}'")
            
            # Refresh UI
            self.load_inventory_data()
            self.status_var.set("Change Status")
            self.status_dropdown.configure(state="disabled")

    # ============================================
    # ENHANCED BORROW/RETURN WITH LOST/DAMAGE FLAGGING
    # ============================================
    def process_borrow(self):
        if not self.current_selection_data:
            return
        
        asset_tag = self.current_selection_data['AssetTag']
        member_id = self.current_user['MemberID']
        
        is_internal = False
        if self.current_user['IsOfficer']:
            is_internal = self.internal_use_var.get()

        try:
            conn = db.get_db_connection() # Keep connection for multiple checks
            cursor = conn.cursor()
            # Check for overdue items
            overdue = cursor.execute('''SELECT COUNT(*) FROM Borrowings WHERE MemberID = ? AND DateReturned IS NULL AND DueDate < datetime('now')''', (member_id,)).fetchone()[0]
            if overdue > 0:
                messagebox.showerror("Cannot Borrow", "You have overdue items. Please return them first.")
                conn.close()
                return

            # Check max active loans (for non-officers or non-internal use)
            if not is_internal and not self.current_user['IsOfficer']:
                active_loans = cursor.execute('''SELECT COUNT(*) FROM Borrowings WHERE MemberID = ? AND DateReturned IS NULL''', (member_id,)).fetchone()[0]
                if active_loans >= 3:
                    messagebox.showerror("Cannot Borrow", "Maximum 3 items can be borrowed at once.")
                    conn.close()
                    return
            conn.close() # Close after checks
            due_date = db.borrow_item(member_id, asset_tag, is_internal)
            
            # Success message with details
            due_str = "for internal use" if is_internal else f"due {due_date.strftime('%b %d, %Y')}"
            messagebox.showinfo("Success", 
                              f"✅ {asset_tag} has been checked out!\n\n"
                              f"Model: {self.current_selection_data['ModelName']}\n"
                              f"Status: {due_str}")
            
            # Refresh UI
            self.load_inventory_data()
            self.btn_borrow.configure(state="disabled", fg_color="#2A2A36")

        except Exception as e:
            messagebox.showerror("System Error", f"An error occurred:\n{str(e)}")

    # ============================================
    # OTHER FUNCTIONS
    # ============================================
    def logout(self):
        self.current_user = None
        self.show_login_screen()

    def delete_item(self):
        if not self.current_selection_data:
            return
        
        asset_tag = self.current_selection_data['AssetTag']
        model_name = self.current_selection_data['ModelName']
        
        confirm = messagebox.askyesno("Confirm Removal", 
                                     f"Are you sure you want to remove this equipment?\n\n"
                                     f"Asset: {asset_tag}\n"
                                     f"Model: {model_name}\n\n"
                                     f"⚠️ This action cannot be undone.")
        
        if confirm:
            db.delete_inventory_item(asset_tag)
            messagebox.showinfo("Removed", f"{asset_tag} has been removed from inventory.")
            self.load_inventory_data()

    # ============================================
    # ADD EQUIPMENT FORM (UPDATED)
    # ============================================
    def open_add_item_window(self):
        """Opens the Add Item window."""
        AddItemWindow(self)

if __name__ == "__main__":
    app = LensLockerApp()
    app.mainloop()