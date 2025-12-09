import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import sqlite3

import database as db
from config import *

class CleanCard(ctk.CTkFrame):
    def __init__(self, master, data, row, col, app):
        super().__init__(master, fg_color=COLOR_CARD, corner_radius=12, border_width=0)
        
        self.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        self.data = data
        self.is_selected = False
        self.app = app

        self._create_widgets()
        self._bind_events()

    def _create_widgets(self):
        status_color = STATUS_COLORS.get(self.data['Status'], "#4361EE")
        status_icons = {
            'Available': '✓', 'Borrowed': '⏳', 'Internal': '🏢',
            'Maintenance': '🔧', 'Lost': '❌'
        }
        status_icon = status_icons.get(self.data['Status'], '●')

        # Left status strip
        status_strip = ctk.CTkFrame(self, fg_color=status_color, corner_radius=12, width=8, border_width=0)
        status_strip.place(x=0, y=0, relheight=1.0)
        
        # Content frame
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.place(x=15, y=0, relwidth=0.95, relheight=1.0)
        
        # Status badge
        status_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        status_frame.pack(anchor="w", pady=(15, 10))
        ctk.CTkLabel(status_frame, text=f"{status_icon} {self.data['Status'].upper()}",
                     font=("Montserrat", 10, "bold"), text_color=status_color).pack(side="left")
        
        # Model name (truncated)
        model_name = self.data['ModelName']
        if len(model_name) > 25:
            model_name = model_name[:22] + "..."
        
        ctk.CTkLabel(content_frame, text=model_name, font=("Montserrat", 14, "bold"),
                     text_color=COLOR_TEXT_WHITE, anchor="w").pack(anchor="w", pady=(0, 5))
        
        # Asset tag
        ctk.CTkLabel(content_frame, text=self.data['AssetTag'], font=("Montserrat", 12, "bold"),
                     text_color=COLOR_ACCENT_PRIMARY, anchor="w").pack(anchor="w", pady=(0, 5))
        
        # Category
        ctk.CTkLabel(content_frame, text=self.data['CatName'], font=("Montserrat", 11),
                     text_color=COLOR_TEXT_GRAY, anchor="w").pack(anchor="w", pady=(0, 15))
        
        # Purchase date
        if self.data['PurchaseDate']:
            purchase_year = self.data['PurchaseDate'][:4]
            ctk.CTkLabel(content_frame, text=f"Purchased {purchase_year}", font=("Montserrat", 10),
                         text_color=COLOR_TEXT_GRAY).pack(anchor="w", side="bottom", pady=(0, 15))

    def _on_enter(self, e):
        if not self.is_selected:
            self.configure(fg_color="#20202A")
    
    def _on_leave(self, e):
        if not self.is_selected:
            self.configure(fg_color=COLOR_CARD)
    
    def _on_click(self, e):
        self.app.select_card(self.data, self)

    def _bind_events(self):
        """Recursively bind events to all child widgets for consistent hover/click."""
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        
        def bind_all_children(widget):
            for child in widget.winfo_children():
                child.bind("<Enter>", self._on_enter)
                child.bind("<Leave>", self._on_leave)
                child.bind("<Button-1>", self._on_click)
                bind_all_children(child)

        bind_all_children(self)

    def select(self):
        """Visually marks the card as selected."""
        self.is_selected = True
        self.configure(fg_color="#242430")

    def deselect(self):
        """Resets the card's visual state to normal."""
        self.is_selected = False
        self.configure(fg_color=COLOR_CARD)


# ============================================
# ADD EQUIPMENT WINDOW
# ============================================
class AddItemWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.app = master

        self.title("Add New Equipment")
        self.geometry("500x600")
        self.configure(fg_color=COLOR_BG)
        self.attributes('-topmost', True)
        
        self._create_widgets()

    def _create_widgets(self):
        # Header
        header = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=12, height=80)
        header.pack(fill="x", padx=20, pady=20)
        header.pack_propagate(False)
        
        ctk.CTkLabel(header, text="➕ Add New Equipment", font=("Montserrat", 20, "bold"),
                     text_color=COLOR_TEXT_WHITE).pack(side="left", padx=30, pady=20)
        
        # Form
        form_frame = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=12)
        form_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        models, categories = db.get_models_and_categories()
        self.model_dict = {m['Name']: m['ModelID'] for m in models}
        self.category_dict = {c['Name']: c['CategoryID'] for c in categories}
        
        fields = [
            ("Category", "Select category", "combobox", list(self.category_dict.keys())),
            ("Model Name", "Enter equipment model (e.g., Sony A7 IV)", "entry", None),
            ("Replacement Cost", "Enter cost in PHP (optional)", "entry", None),
            ("Asset Tag", "Enter unique asset tag (e.g., CAM-99)", "entry", None),
            ("Purchase Date", "YYYY-MM-DD (optional)", "entry", None),
        ]
        
        self.add_item_vars = {}
        for i, (label, placeholder, field_type, options) in enumerate(fields):
            ctk.CTkLabel(form_frame, text=label, font=("Montserrat", 12, "bold"),
                         text_color=COLOR_TEXT_WHITE).pack(anchor="w", padx=30, pady=(20 if i==0 else 30, 5))
            
            if field_type == "combobox":
                var = ctk.StringVar()
                combo = ctk.CTkComboBox(form_frame, values=options, variable=var, width=400, height=40,
                                        fg_color=COLOR_BG, border_color=COLOR_BG,
                                        button_color=COLOR_ACCENT_PRIMARY, text_color=COLOR_TEXT_WHITE)
                combo.pack(padx=30, pady=(0, 10))
                self.add_item_vars[label.lower().replace(" ", "_")] = var
            else:
                entry = ctk.CTkEntry(form_frame, placeholder_text=placeholder, width=400, height=40,
                                     fg_color=COLOR_BG, border_color=COLOR_BG, text_color=COLOR_TEXT_WHITE)
                entry.pack(padx=30, pady=(0, 10))
                self.add_item_vars[label.lower().replace(" ", "_")] = entry
        
        ctk.CTkButton(form_frame, text="Save to Inventory", width=400, height=45,
                      fg_color=COLOR_ACCENT_SECONDARY, text_color="white",
                      font=("Montserrat", 14, "bold"), corner_radius=8,
                      command=self._save_new_item).pack(pady=40)

    def _save_new_item(self):
        try:
            category_name = self.add_item_vars['category'].get()
            model_name = self.add_item_vars['model_name'].get().strip()
            replacement_cost = self.add_item_vars['replacement_cost'].get().strip()
            asset_tag = self.add_item_vars['asset_tag'].get().upper().strip()
            purchase_date = self.add_item_vars['purchase_date'].get().strip()
            
            if not category_name or not model_name or not asset_tag:
                messagebox.showerror("Error", "Please fill in Category, Model Name, and Asset Tag.", parent=self)
                return
            
            replacement_cost = float(replacement_cost) if replacement_cost else 0.0
            if not purchase_date:
                purchase_date = datetime.now().strftime("%Y-%m-%d")
            
            conn = db.get_db_connection()
            cursor = conn.cursor()
            category_id = self.category_dict.get(category_name)
            if not category_id:
                messagebox.showerror("Error", "Invalid category selected.", parent=self)
                return
            
            try:
                # Check if the model already exists
                existing_model = cursor.execute("SELECT ModelID FROM Equipment_Models WHERE Name = ?", (model_name,)).fetchone()
                
                if existing_model:
                    model_id = existing_model['ModelID']
                else:
                    # If the model doesn't exist, create it
                    cursor.execute("INSERT INTO Equipment_Models (CategoryID, Name, ReplacementCost) VALUES (?, ?, ?)",
                                   (category_id, model_name, replacement_cost))
                    model_id = cursor.lastrowid
                
                # Add the new inventory item using the model_id
                cursor.execute("INSERT INTO Inventory_Items (AssetTag, ModelID, Status, PurchaseDate) VALUES (?, ?, 'Available', ?)",
                               (asset_tag, model_id, purchase_date))
                conn.commit()
            finally:
                conn.close()
            
            messagebox.showinfo("Success", f"✅ {asset_tag} added to inventory!", parent=self)
            self.app.load_inventory_data()
            self.destroy()
            
        except sqlite3.IntegrityError as e:
            if "Inventory_Items.AssetTag" in str(e):
                messagebox.showerror("Error", f"Asset Tag '{asset_tag}' already exists.", parent=self)
            else:
                messagebox.showerror("Database Error", f"An integrity error occurred: {e}", parent=self)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add item:\n{str(e)}", parent=self)


# ============================================
# MY BORROWINGS WINDOW
# ============================================
class MyBorrowingsWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.app = master

        self.title("My Borrowed Equipment")
        self.geometry("700x500")
        self.configure(fg_color=COLOR_BG)
        self.attributes('-topmost', True)

        self._create_widgets()

    def _create_widgets(self):
        header = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=12, height=80)
        header.pack(fill="x", padx=20, pady=20)
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="📦 My Borrowed Equipment", font=("Montserrat", 20, "bold"),
                     text_color=COLOR_TEXT_WHITE).pack(side="left", padx=30, pady=20)
        
        list_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        items = db.get_member_borrowings(self.app.current_user['MemberID'])

        if not items:
            empty_frame = ctk.CTkFrame(list_frame, fg_color=COLOR_CARD, corner_radius=12, height=100)
            empty_frame.pack(fill="x", pady=10)
            empty_frame.pack_propagate(False)
            ctk.CTkLabel(empty_frame, text="No equipment currently borrowed", font=("Montserrat", 14),
                         text_color=COLOR_TEXT_GRAY).pack(expand=True)
        else:
            for item in items:
                card = ctk.CTkFrame(list_frame, fg_color=COLOR_CARD, corner_radius=12, height=100)
                card.pack(fill="x", pady=8)
                card.pack_propagate(False)
                
                content = ctk.CTkFrame(card, fg_color="transparent")
                content.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95, relheight=0.9)
                
                info_frame = ctk.CTkFrame(content, fg_color="transparent")
                info_frame.pack(side="left", fill="both", expand=True)
                
                ctk.CTkLabel(info_frame, text=item['Name'], font=("Montserrat", 14, "bold"),
                             text_color=COLOR_TEXT_WHITE, anchor="w").pack(anchor="w", pady=(5, 0))
                ctk.CTkLabel(info_frame, text=f"Tag: {item['AssetTag']}", font=("Montserrat", 12),
                             text_color=COLOR_TEXT_GRAY, anchor="w").pack(anchor="w", pady=(2, 0))
                
                due_date = datetime.strptime(item['DueDate'][:10], "%Y-%m-%d")
                is_overdue = due_date < datetime.now()
                ctk.CTkLabel(info_frame, text=f"Due: {item['DueDate'][:10]}", font=("Montserrat", 12),
                             text_color=COLOR_WARNING if is_overdue else COLOR_TEXT_GRAY,
                             anchor="w").pack(anchor="w", pady=(2, 5))
                
                btn_frame = ctk.CTkFrame(content, fg_color="transparent")
                btn_frame.pack(side="right", fill="y", pady=20)
                
                ctk.CTkButton(btn_frame, text="Return", width=100, fg_color=COLOR_ACCENT_PRIMARY,
                              text_color="white", font=("Montserrat", 12, "bold"),
                              command=lambda b_id=item['BorrowID'], tag=item['AssetTag'], 
                                           name=item['Name'], cost=item['ReplacementCost']: 
                                           self._open_return_dialog(b_id, tag, name, cost)).pack()

    def _open_return_dialog(self, borrow_id, asset_tag, item_name, replacement_cost):
        """Opens the return dialog and provides a callback to run on success."""
        dialog = ReturnDialog(self, self.app, borrow_id, asset_tag, item_name, replacement_cost, on_success=self._on_return_success)

    def _on_return_success(self):
        """Callback function to close the borrowings window and refresh the main app."""
        self.destroy()
        self.destroy() # Close the 'My Borrowings' window
        self.app.load_inventory_data()


# ============================================
# RETURN DIALOG
# ============================================
class ReturnDialog(ctk.CTkToplevel):
    def __init__(self, master, app, borrow_id, asset_tag, item_name, replacement_cost, on_success=None):
        super().__init__(master)
        self.app = app
        self.borrow_id = borrow_id
        self.asset_tag = asset_tag
        self.item_name = item_name
        self.replacement_cost = replacement_cost
        self.parent_window = master
        self.on_success_callback = on_success

        self.title(f"Return {asset_tag}")
        self.geometry("500x450")
        self.configure(fg_color=COLOR_BG)
        self.attributes('-topmost', True)
        self.transient(master)  # Keep window on top of its parent
        self.grab_set()         # Modal behavior: block interaction with parent
        
        self._create_widgets()

    def _create_widgets(self):
        ctk.CTkLabel(self, text=f"Return: {self.item_name}", font=("Montserrat", 20, "bold"),
                     text_color=COLOR_TEXT_WHITE).pack(pady=(30, 10))
        ctk.CTkLabel(self, text=f"Asset Tag: {self.asset_tag}", font=("Montserrat", 14),
                     text_color=COLOR_TEXT_GRAY).pack(pady=(0, 30))
        
        ctk.CTkLabel(self, text="Select item condition:", font=("Montserrat", 14, "bold"),
                     text_color=COLOR_TEXT_WHITE).pack(pady=(0, 15))
        
        self.condition_var = ctk.StringVar(value="Good")
        
        conditions_frame = ctk.CTkFrame(self, fg_color="transparent")
        conditions_frame.pack(pady=10)
        
        conditions = [("Good", "Item in good condition", COLOR_SUCCESS),
                      ("Damaged", "Item has minor damage", COLOR_WARNING),
                      ("Lost", "Item is lost/stolen", COLOR_DANGER)]
        
        for cond, desc, color in conditions:
            frame = ctk.CTkFrame(conditions_frame, fg_color="transparent")
            frame.pack(fill="x", pady=5)
            rb = ctk.CTkRadioButton(frame, text=cond, variable=self.condition_var, value=cond,
                                  fg_color=color, text_color=COLOR_TEXT_WHITE, font=("Montserrat", 12, "bold"))
            rb.pack(side="left", padx=(0, 10))
            ctk.CTkLabel(frame, text=desc, text_color=COLOR_TEXT_GRAY, font=("Montserrat", 11)).pack(side="left")
        
        ctk.CTkButton(self, text="Confirm Return", width=200, height=45, fg_color=COLOR_ACCENT_PRIMARY,
                      text_color="white", font=("Montserrat", 14, "bold"), corner_radius=8,
                      command=self._process_return).pack(pady=30)

    def _process_return(self):
        condition = self.condition_var.get()
        db.return_item(self.borrow_id, self.asset_tag, condition)

        # The dialog's job is done. Now, inform the parent about the result.
        # This avoids the dialog having to know about other windows like PaymentInfoWindow.
        self.after(10, lambda: self._safe_close(condition))

    def _safe_close(self, condition):
        # Now, handle post-return actions in the main app context
        if condition == "Lost":
            messagebox.showinfo("Item Marked as Lost",
                              f"❌ {self.asset_tag} has been marked as LOST.\n\n"
                              f"Replacement cost: ₱{float(self.replacement_cost):,.2f}\n"
                              f"Please contact club officers for payment.", parent=self.parent_window)
        elif condition == "Damaged":
            messagebox.showinfo("Item Marked as Damaged",
                              f"🔧 {self.asset_tag} has been moved to MAINTENANCE.\n\n"
                              f"An officer will assess repair costs.", parent=self.parent_window)
        else:
            messagebox.showinfo("Return Complete", f"✅ {self.asset_tag} has been returned successfully.", parent=self.parent_window)

        self.destroy()  # Destroy the dialog itself
        if self.on_success_callback:
            self.on_success_callback()  # Trigger the parent's cleanup

# ============================================
# PAYMENT INFO WINDOW
# ============================================
class PaymentInfoWindow(ctk.CTkToplevel):
    def __init__(self, master, item_name=None, asset_tag=None, replacement_cost=None):
        super().__init__(master)
        self.app = master

        self.title("Payment Information")
        self.geometry("700x600")
        self.configure(fg_color=COLOR_BG)
        self.attributes('-topmost', True)

        self._create_widgets(item_name, asset_tag, replacement_cost)

    def _create_widgets(self, item_name, asset_tag, replacement_cost):
        header = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=12, height=100)
        header.pack(fill="x", padx=20, pady=20)
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="💰 Payment Information", font=("Montserrat", 24, "bold"),
                     text_color=COLOR_TEXT_WHITE).pack(side="left", padx=30, pady=30)
        
        content_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # --- Outstanding Payments Section ---
        unpaid_items = db.get_unpaid_borrowings(self.app.current_user['MemberID'])

        ctk.CTkLabel(content_frame, text="Outstanding Payments", font=("Montserrat", 18, "bold"), text_color=COLOR_TEXT_WHITE).pack(anchor="w", pady=(0, 15))

        if not unpaid_items:
            empty_frame = ctk.CTkFrame(content_frame, fg_color=COLOR_CARD, corner_radius=12, height=100)
            empty_frame.pack(fill="x", pady=10)
            empty_frame.pack_propagate(False)
            ctk.CTkLabel(empty_frame, text="🎉 You have no outstanding payments!", font=("Montserrat", 14), text_color=COLOR_TEXT_GRAY).pack(expand=True)
        else:
            for item in unpaid_items:
                card = ctk.CTkFrame(content_frame, fg_color=COLOR_CARD, corner_radius=12)
                card.pack(fill="x", pady=8)
                
                # Card content
                content = ctk.CTkFrame(card, fg_color="transparent")
                content.pack(fill="x", padx=20, pady=15)
                
                ctk.CTkLabel(content, text=item['Name'], font=("Montserrat", 14, "bold"), text_color=COLOR_TEXT_WHITE, anchor="w").pack(anchor="w")
                ctk.CTkLabel(content, text=f"Asset Tag: {item['AssetTag']}", font=("Montserrat", 12), text_color=COLOR_TEXT_GRAY, anchor="w").pack(anchor="w", pady=(2, 10))
                
                status_text = ""
                cost_text = ""
                if item['PaymentStatus'] == 'Unpaid':
                    status_text = "Status: LOST"
                    cost_text = f"Replacement Cost: ₱{float(item['ReplacementCost']):,.2f}"
                elif item['PaymentStatus'] == 'Pending Assessment':
                    status_text = "Status: DAMAGED"
                    cost_text = "Repair Cost: Pending Assessment"

                ctk.CTkLabel(content, text=status_text, font=("Montserrat", 12, "bold"), text_color=COLOR_DANGER, anchor="w").pack(anchor="w")
                ctk.CTkLabel(content, text=cost_text, font=("Montserrat", 12, "bold"), text_color=COLOR_WARNING, anchor="w").pack(anchor="w", pady=(2, 0))

        # Important notice
        notice_frame = ctk.CTkFrame(content_frame, fg_color="#3A0C00", corner_radius=12, border_color="#FF6B6B", border_width=1)
        notice_frame.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(notice_frame, text="⚠️ Important Notice", font=("Montserrat", 16, "bold"), text_color="#FF6B6B").pack(anchor="w", padx=20, pady=(15, 10))
        notice_text = "According to club policy, you are responsible for lost or damaged equipment. Please follow the procedure below to resolve this matter."
        ctk.CTkLabel(notice_frame, text=notice_text, font=("Montserrat", 13), text_color="#FFD6D6", wraplength=600, justify="left").pack(anchor="w", padx=20, pady=(0, 15))

        # Steps section
        steps_frame = ctk.CTkFrame(content_frame, fg_color=COLOR_CARD, corner_radius=12)
        steps_frame.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(steps_frame, text="Steps to Resolve", font=("Montserrat", 16, "bold"), text_color=COLOR_TEXT_WHITE).pack(anchor="w", padx=20, pady=(15, 10))
        steps = [
            "1. Contact a club officer immediately to report the issue.",
            "2. Discuss replacement or repair options and costs.",
            "3. Make payment using an approved method.",
            "4. Provide proof of payment to the officer for verification."
        ]
        for step in steps:
            ctk.CTkLabel(steps_frame, text=step, font=("Montserrat", 13), text_color=COLOR_TEXT_GRAY, wraplength=600, justify="left").pack(anchor="w", padx=35, pady=(0, 8))

        # Contact officers section
        contact_frame = ctk.CTkFrame(content_frame, fg_color=COLOR_CARD, corner_radius=12)
        contact_frame.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(contact_frame, text="Contact Club Officers", font=("Montserrat", 16, "bold"), text_color=COLOR_TEXT_WHITE).pack(anchor="w", padx=20, pady=(15, 10))
        
        officers = db.get_officers()
        if officers:
            for officer in officers:
                officer_frame = ctk.CTkFrame(contact_frame, fg_color=COLOR_BG, corner_radius=8)
                officer_frame.pack(fill="x", padx=20, pady=5)
                ctk.CTkLabel(officer_frame, text=f"👤 {officer['Name']}", font=("Montserrat", 13, "bold"), text_color=COLOR_TEXT_WHITE).pack(anchor="w", padx=15, pady=(10, 0))
                ctk.CTkLabel(officer_frame, text=f"📧 {officer['Email']}", font=("Montserrat", 12), text_color=COLOR_ACCENT_PRIMARY).pack(anchor="w", padx=15, pady=(0, 10))
        else:
            ctk.CTkLabel(contact_frame, text="No officers found in database. Please visit the club room.", font=("Montserrat", 13), text_color=COLOR_TEXT_GRAY).pack(anchor="w", padx=20, pady=(0, 15))

        # Payment methods
        payment_frame = ctk.CTkFrame(content_frame, fg_color=COLOR_CARD, corner_radius=12)
        payment_frame.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(payment_frame, text="Accepted Payment Methods", font=("Montserrat", 16, "bold"), text_color=COLOR_TEXT_WHITE).pack(anchor="w", padx=20, pady=(15, 10))
        methods = [
            "• Club bank transfer (details provided by officers)",
            "• GCash/Maya transfer to the club account",
            "• Cash payment (must be issued an official receipt)"
        ]
        for method in methods:
            ctk.CTkLabel(payment_frame, text=method, font=("Montserrat", 13), text_color=COLOR_TEXT_GRAY, justify="left").pack(anchor="w", padx=35, pady=(0, 5))
        
        # Close button
        close_btn = ctk.CTkButton(self, text="Close Window", width=200, height=40,
                                  fg_color=COLOR_ACCENT_PRIMARY, text_color="white",
                                  font=("Montserrat", 14, "bold"), corner_radius=8,
                                  command=self.destroy)
        close_btn.pack(pady=(10, 20))
        
        # Footer
        footer_frame = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=12, height=60)
        footer_frame.pack(fill="x", padx=20, pady=(0, 20))
        footer_frame.pack_propagate(False)
        ctk.CTkLabel(footer_frame, text="For questions, contact: focus-batstateu@example.com",
                     font=("Montserrat", 11), text_color=COLOR_TEXT_GRAY).pack(expand=True)