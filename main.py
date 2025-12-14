import customtkinter as ctk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
import os

import database as db
from config import *
from ui_components import CleanCard, AddItemWindow, MyBorrowingsWindow, PaymentInfoWindow
from setup import setup_database

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class GearGrabApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gear Grab - Focus BatStateU Camera Club")
        self.geometry("1300x850")
        self.minsize(1100, 700)
        
        self.configure(fg_color=COLOR_BG)

        self.current_user = None
        self.selected_card_widget = None
        self.current_selection_data = None

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=25, pady=25)

        self.show_login_screen()

    def show_login_screen(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        login_frame = ctk.CTkFrame(self.container, fg_color=COLOR_CARD, corner_radius=16, width=450)
        login_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(login_frame, text="GEAR GRAB", 
                    font=("Montserrat", 40, "bold"), 
                    text_color=COLOR_ACCENT_PRIMARY).pack(pady=(40, 5))
        
        ctk.CTkLabel(login_frame, text="Focus BatStateU Camera Club", 
                    font=("Montserrat", 14), 
                    text_color=COLOR_TEXT_GRAY).pack(pady=(0, 30))
        
        icons_text = " · ".join(CATEGORY_ICONS.values())
        ctk.CTkLabel(login_frame, text=icons_text, font=("Montserrat", 16), text_color="#333445").pack(pady=10)
        
        ctk.CTkLabel(login_frame, text="Member ID", 
                    font=("Montserrat", 12, "bold"), 
                    text_color=COLOR_TEXT_GRAY).pack(anchor="w", pady=(30, 5), padx=40)
        
        self.entry_id = ctk.CTkEntry(login_frame, placeholder_text="Enter your member ID", 
                                     width=320, height=45,
                                     fg_color=COLOR_BG, 
                                     border_color=COLOR_BG,
                                     text_color=COLOR_TEXT_WHITE,
                                     font=("Montserrat", 14),
                                     corner_radius=8)
        self.entry_id.pack(pady=(0, 20), padx=40)
        self.entry_id.bind('<Return>', lambda event: self.process_login())
        
        btn_login = ctk.CTkButton(login_frame, text="Access System", 
                                  width=320, height=45,
                                  fg_color=COLOR_ACCENT_PRIMARY, 
                                  text_color=COLOR_BG,
                                  font=("Montserrat", 14, "bold"),
                                  corner_radius=8,
                                  hover_color=COLOR_ACCENT_SECONDARY,
                                  command=self.process_login)
        btn_login.pack(pady=(10, 20), padx=40)
        
        hint_frame = ctk.CTkFrame(login_frame, fg_color=COLOR_BG, corner_radius=8)
        hint_frame.pack(pady=(20, 40), padx=40, fill="x")
        ctk.CTkLabel(hint_frame, text="💡 Try ID: 1 (Juan DelaCruz) or 2 (Officer Mhalik Perez)", 
                    font=("Montserrat", 11), 
                    text_color=COLOR_TEXT_GRAY,
                    pady=10).pack(padx=10)

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

    def show_dashboard_screen(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        header_frame = ctk.CTkFrame(self.container, fg_color=COLOR_CARD, corner_radius=12)
        header_frame.pack(fill="x", pady=(0, 20))
        
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
        
        action_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        action_frame.pack(side="right", padx=30, pady=15)
        
        if self.current_user['IsOfficer']:
            ctk.CTkButton(action_frame, text="+ Add Equipment", 
                         width=120, height=35,
                         fg_color=COLOR_ACCENT_SECONDARY,
                         text_color="white",
                         font=("Montserrat", 12, "bold"),
                         corner_radius=8,
                         command=self.open_add_item_window).pack(side="left", padx=5)
        
        ctk.CTkButton(action_frame, text="💰 Penalties", 
                     width=120, height=35,
                     fg_color="transparent",
                     border_color=COLOR_WARNING,
                     border_width=2,
                     text_color=COLOR_WARNING,
                     font=("Montserrat", 12),
                     corner_radius=8,
                     command=lambda: PaymentInfoWindow(self)).pack(side="left", padx=5)
        
        ctk.CTkButton(action_frame, text="Logout", 
                     width=80, height=35,
                     fg_color="transparent",
                     border_color=COLOR_BG,
                     border_width=1,
                     text_color=COLOR_TEXT_GRAY,
                     font=("Montserrat", 12),
                     corner_radius=8,
                     command=self.logout).pack(side="left", padx=5)
        
        filter_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        filter_frame.pack(fill="x", pady=(0, 15))
        
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
        
        filter_container = ctk.CTkFrame(filter_frame, fg_color=COLOR_CARD, corner_radius=8, height=45)
        filter_container.pack(side="right", padx=(10, 0))
        filter_container.pack_propagate(False)
        
        categories_with_icons = ["All Categories"]
        plain_categories = ["Camera Body", "Camera Lens", "Lighting", "Tripods & Support", 
                            "Audio & Microphones", "Drones", "Stabilizers & Gimbals", "Studio Accessories"]
        for cat in plain_categories:
            icon = CATEGORY_ICONS.get(cat, CATEGORY_ICONS.get("Default", ""))
            categories_with_icons.append(f"{icon} {cat}")
        
        self.cat_filter = ctk.CTkComboBox(filter_container, 
                                         values=categories_with_icons,
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
        
        main_content_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        main_content_frame.pack(fill="both", expand=True)
        
        self.scroll_frame = ctk.CTkScrollableFrame(main_content_frame, fg_color="transparent")
        self.scroll_frame.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        self.action_bar = ctk.CTkFrame(main_content_frame, fg_color=COLOR_CARD, corner_radius=12, width=350)
        self.action_bar.pack(side="right", fill="y")
        self.action_bar.pack_propagate(False)
        
        self.lbl_selection = ctk.CTkFrame(self.action_bar, fg_color="transparent")
        self.lbl_selection.pack(fill="x", padx=30, pady=(30, 20))
        
        self.lbl_selected = ctk.CTkLabel(self.lbl_selection, 
                                        text="No equipment selected",
                                        font=("Montserrat", 16, "bold"),
                                        text_color=COLOR_TEXT_GRAY)
        self.lbl_selected.pack(anchor="w")
        
        self.lbl_status = ctk.CTkLabel(self.lbl_selection,
                                      text="Select an item to view details.",
                                      font=("Montserrat", 12),
                                      text_color=COLOR_TEXT_GRAY)
        self.lbl_status.pack(anchor="w", pady=(2, 0))
        
        self.btn_container = ctk.CTkFrame(self.action_bar, fg_color="transparent")
        self.btn_container.pack(fill="x", padx=30, pady=20)
        
        if self.current_user['IsOfficer']:
            officer_controls = ctk.CTkFrame(self.btn_container, fg_color="transparent")
            officer_controls.pack(fill="x")
            
            self.btn_delete = ctk.CTkButton(officer_controls, text="Remove",
                                           width=100, height=35,
                                           fg_color="#252635",
                                           text_color="#707080",
                                           font=("Montserrat", 12, "bold"),
                                           state="disabled",
                                           corner_radius=8,
                                           command=self.delete_item)
            self.btn_delete.pack(fill="x", pady=(0, 10))
            
            self.status_var = ctk.StringVar(value="Change Status")
            self.status_dropdown = ctk.CTkOptionMenu(officer_controls,
                                                   values=["Available", "Maintenance", "Lost"],
                                                   variable=self.status_var,
                                                   width=140,
                                                   height=35,
                                                   fg_color=COLOR_BG,
                                                   button_color=COLOR_ACCENT_SECONDARY,
                                                   button_hover_color=COLOR_ACCENT_PRIMARY,
                                                   text_color=COLOR_TEXT_WHITE,
                                                   state="disabled",
                                                   command=self.change_item_status)
            self.status_dropdown.pack(fill="x", pady=(0, 20))
            
            self.internal_use_var = ctk.BooleanVar(value=False)
            self.switch_internal = ctk.CTkSwitch(self.btn_container, 
                                                text="Internal Use",
                                                variable=self.internal_use_var,
                                                progress_color=COLOR_ACCENT_SECONDARY,
                                                text_color=COLOR_TEXT_GRAY,
                                                font=("Montserrat", 12))
            self.switch_internal.pack(anchor="w", pady=(0, 10))
        
        self.btn_borrow = ctk.CTkButton(self.btn_container, text="Borrow",
                                       height=45,
                                       fg_color=COLOR_ACCENT_PRIMARY, 
                                       text_color=COLOR_BG,
                                       font=("Montserrat", 14, "bold"),
                                       state="disabled",
                                       corner_radius=8,
                                       command=self.process_borrow)
        self.btn_borrow.configure(fg_color="#252635", text_color="#707080")
        self.btn_borrow.pack(fill="x") 

        ctk.CTkFrame(self.action_bar, height=2, fg_color=COLOR_BG).pack(fill="x", padx=30, pady=20)

        ctk.CTkLabel(self.action_bar, text="My Current Borrows",
                     font=("Montserrat", 14, "bold"),
                     text_color=COLOR_TEXT_WHITE).pack(anchor="w", padx=30, pady=(0, 10))
        
        self.my_borrowings_frame = ctk.CTkScrollableFrame(self.action_bar, fg_color="transparent")
        self.my_borrowings_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.load_inventory_data()
        self.update_my_borrowings_panel()

    def update_my_borrowings_panel(self):
        """Populates the 'My Borrowed Items' panel on the dashboard."""
        for widget in self.my_borrowings_frame.winfo_children():
            widget.destroy()

        items = db.get_member_borrowings(self.current_user['MemberID'])

        if not items:
            ctk.CTkLabel(self.my_borrowings_frame, text="You have no items borrowed.",
                         font=("Montserrat", 12), text_color=COLOR_TEXT_GRAY).pack(pady=20)
        else:
            for item in items:
                card = ctk.CTkFrame(self.my_borrowings_frame, fg_color=COLOR_BG, corner_radius=8)
                card.pack(fill="x", pady=4)

                info_frame = ctk.CTkFrame(card, fg_color="transparent")
                info_frame.pack(side="left", fill="x", expand=True, padx=15, pady=10)

                ctk.CTkLabel(info_frame, text=item['Name'], font=("Montserrat", 12, "bold"),
                             text_color=COLOR_TEXT_WHITE, anchor="w").pack(anchor="w")

                if item['DueDate']:
                    due_date = datetime.strptime(item['DueDate'][:10], "%Y-%m-%d")
                    is_overdue = due_date < datetime.now()
                    due_text = f"Due: {due_date.strftime('%b %d, %Y')}"
                    due_color = COLOR_DANGER if is_overdue else COLOR_TEXT_GRAY
                else:
                    due_text = "Internal Use"
                    due_color = COLOR_ACCENT_SECONDARY

                ctk.CTkLabel(info_frame, text=due_text, font=("Montserrat", 11),
                             text_color=due_color,
                             anchor="w").pack(anchor="w", pady=(2, 0))

                ctk.CTkButton(card, text="Return", width=60, height=28,
                              fg_color=COLOR_ACCENT_PRIMARY, text_color=COLOR_BG,
                              font=("Montserrat", 11, "bold"),
                              command=lambda b_id=item['BorrowID'], tag=item['AssetTag'],
                                           name=item['Name'], cost=item['ReplacementCost']:
                                           self._open_return_dialog(b_id, tag, name, cost)).pack(side="right", padx=15)

    def load_inventory_data(self):
        self.all_inventory = db.get_all_inventory()
        self.filter_inventory()

    def filter_inventory(self, *args):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        self.selected_card_widget = None
        self.current_selection_data = None
        self.update_selection_display()

        search_text = self.search_var.get().lower()
        cat_filter_raw = self.cat_filter.get()
        if cat_filter_raw == "All Categories":
            cat_filter = "All Categories"
        else:
            cat_filter = ' '.join(cat_filter_raw.split(' ')[1:])

        cards = []
        for row_data in self.all_inventory:
            match_search = search_text in row_data['ModelName'].lower() or search_text in row_data['AssetTag'].lower()
            match_cat = cat_filter == "All Categories" or cat_filter == row_data['CatName']

            if match_search and match_cat:
                cards.append(row_data)

        cols = 4
        for i in range(cols):
            self.scroll_frame.grid_columnconfigure(i, weight=1)

        row, col = 0, 0
        for data in cards:
            self.create_clean_card(data, row, col)
            col += 1
            if col >= cols:
                col = 0
                row += 1

    def create_clean_card(self, data, row, col):
        status_color = STATUS_COLORS.get(data['Status'], COLOR_NEUTRAL)
        CleanCard(self.scroll_frame, data, row, col, self)

    def select_card(self, data, card_container):
        for child in self.scroll_frame.winfo_children():
            if isinstance(child, CleanCard):
                child.deselect()
        
        card_container.select()
        
        self.selected_card_widget = card_container
        self.current_selection_data = data
        
        self.update_selection_display()
        
        if data['Status'] == 'Available':
            self.btn_borrow.configure(state="normal", 
                                     fg_color=COLOR_ACCENT_PRIMARY,
                                     text_color=COLOR_BG)
        else:
            self.btn_borrow.configure(state="disabled", 
                                     fg_color="#252635",
                                     text_color="#707080")
        
        if self.current_user['IsOfficer']:
            self.btn_delete.configure(state="normal",
                                     fg_color=COLOR_DANGER,
                                     text_color=COLOR_BG,
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
                                   text_color=COLOR_TEXT_WHITE, font=("Montserrat", 16, "bold"))
        
        status_color = STATUS_COLORS.get(data['Status'], COLOR_TEXT_GRAY)
        self.lbl_status.configure(text=f"{data['AssetTag']} • {data['CatName']} • Status: {data['Status']}",
                                 text_color=status_color)
        
    def change_item_status(self, new_status):
        if not self.current_selection_data:
            return
        
        asset_tag = self.current_selection_data['AssetTag']
        current_status = self.current_selection_data['Status']
        
        if new_status == current_status:
            return
        
        confirm = messagebox.askyesno("Change Status",
                                     f"Change {asset_tag} from '{current_status}' to '{new_status}'?")
        
        if confirm:
            db.update_item_status(asset_tag, new_status)

            messagebox.showinfo("Status Updated", 
                              f"✅ {asset_tag} status changed to '{new_status}'")
            
            self.load_inventory_data()
            self.status_var.set("Change Status")
            self.status_dropdown.configure(state="disabled")

    def _open_return_dialog(self, borrow_id, asset_tag, item_name, replacement_cost):
        """Opens the return dialog and provides a callback to run on success."""
        dialog = MyBorrowingsWindow.ReturnDialog(self, self, borrow_id, asset_tag, item_name, replacement_cost, on_success=self._on_return_success)

    def _on_return_success(self):
        self.load_inventory_data()
        self.update_my_borrowings_panel()

    def process_borrow(self):
        if not self.current_selection_data:
            return
        
        asset_tag = self.current_selection_data['AssetTag']
        member_id = self.current_user['MemberID']
        
        is_internal = False
        if self.current_user['IsOfficer']:
            is_internal = self.internal_use_var.get()

        try:
            conn = db.get_db_connection()
            cursor = conn.cursor()
            overdue = cursor.execute('''SELECT COUNT(*) FROM Borrowings WHERE MemberID = ? AND DateReturned IS NULL AND DueDate < datetime('now')''', (member_id,)).fetchone()[0]
            if overdue > 0:
                messagebox.showerror("Cannot Borrow", "You have overdue items. Please return them first.")
                conn.close()
                return

            if not is_internal and not self.current_user['IsOfficer']:
                active_loans = cursor.execute('''SELECT COUNT(*) FROM Borrowings WHERE MemberID = ? AND DateReturned IS NULL''', (member_id,)).fetchone()[0]
                if active_loans >= 3:
                    messagebox.showerror("Cannot Borrow", "Maximum 3 items can be borrowed at once.")
                    conn.close()
                    return
            conn.close()
            due_date = db.borrow_item(member_id, asset_tag, is_internal)
            
            due_str = "for internal use" if is_internal else f"due {due_date.strftime('%b %d, %Y')}"
            messagebox.showinfo("Success", 
                              f"✅ {asset_tag} has been checked out!\n\n"
                              f"Model: {self.current_selection_data['ModelName']}\n"
                              f"Status: {due_str}")
            
            self.load_inventory_data()
            self.btn_borrow.configure(state="disabled", fg_color="#252635", text_color="#707080")
            self.update_my_borrowings_panel()

        except Exception as e:
            messagebox.showerror("System Error", f"An error occurred:\n{str(e)}")

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

    def open_add_item_window(self):
        """Opens the Add Item window."""
        AddItemWindow(self)

if __name__ == "__main__":
    if not os.path.exists('geargrab.db') or os.path.getsize('geargrab.db') == 0:
        print("Database not found or empty. Initializing...")
        setup_database()

    app = GearGrabApp()
    app.mainloop()