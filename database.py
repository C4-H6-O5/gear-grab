import sqlite3
from datetime import datetime, timedelta

DB_NAME = 'geargrab.db'

def get_db_connection():
    """Establishes a connection to the database."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def get_member_by_id(member_id):
    """Fetches a member from the database by their ID."""
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM Members WHERE MemberID = ?", (member_id,)).fetchone()
    conn.close()
    return user

def get_all_inventory():
    """Fetches all inventory items with their model and category names."""
    conn = get_db_connection()
    query = '''
        SELECT i.AssetTag, m.Name as ModelName, c.Name as CatName, i.Status, 
               i.PurchaseDate, m.ModelID, c.CategoryID, m.ReplacementCost
        FROM Inventory_Items i
        JOIN Equipment_Models m ON i.ModelID = m.ModelID
        JOIN Categories c ON m.CategoryID = c.CategoryID
    '''
    inventory = conn.execute(query).fetchall()
    conn.close()
    return inventory

def update_item_status(asset_tag, new_status):
    """Updates the status of a specific inventory item."""
    conn = get_db_connection()
    conn.execute("UPDATE Inventory_Items SET Status = ? WHERE AssetTag = ?", (new_status, asset_tag))
    conn.commit()

    # If an item is made 'Available' again, it implies any pending payments
    # for its 'Lost' or 'Damaged' state have been resolved.
    if new_status == 'Available':
        # Find the latest borrowing record for this item that has an outstanding payment
        # and mark it as resolved.
        conn.execute('''UPDATE Borrowings 
                        SET PaymentStatus = 'Resolved' 
                        WHERE AssetTag = ? AND PaymentStatus IN ('Unpaid', 'Pending Assessment')''', 
                     (asset_tag,))
        conn.commit()
    conn.close()

def borrow_item(member_id, asset_tag, is_internal):
    """Creates a new borrowing record and updates the item's status."""
    conn = get_db_connection()
    days = 0 if is_internal else 3
    due_date = datetime.now() + timedelta(days=days)
    new_status = 'Internal' if is_internal else 'Borrowed'

    conn.execute("INSERT INTO Borrowings (MemberID, AssetTag, DueDate) VALUES (?, ?, ?)", 
                  (member_id, asset_tag, due_date))
    conn.execute("UPDATE Inventory_Items SET Status = ? WHERE AssetTag = ?", 
                  (new_status, asset_tag))
    conn.commit()
    conn.close()
    return due_date

def get_member_borrowings(member_id):
    """Fetches all currently borrowed items for a specific member."""
    conn = get_db_connection()
    items = conn.execute('''SELECT b.BorrowID, b.AssetTag, m.Name, b.DueDate, m.ReplacementCost
                          FROM Borrowings b 
                          JOIN Inventory_Items i ON b.AssetTag = i.AssetTag 
                          JOIN Equipment_Models m ON i.ModelID = m.ModelID 
                          WHERE b.MemberID = ? AND b.DateReturned IS NULL''', 
                        (member_id,)).fetchall()
    conn.close()
    return items

def return_item(borrow_id, asset_tag, condition):
    """Updates a borrowing record to mark an item as returned and updates the item's status."""
    if condition == "Good":
        new_status = "Available"
    elif condition == "Damaged":
        new_status = "Maintenance"
    else: # Lost
        new_status = "Lost"
    
    payment_status = 'N/A'
    if condition == 'Lost': # This is the only place 'Unpaid' is set
        payment_status = 'Unpaid'
    elif condition == 'Damaged':
        payment_status = 'Pending Assessment'

    conn = get_db_connection()
    conn.execute("UPDATE Borrowings SET DateReturned = CURRENT_TIMESTAMP, ReturnCondition = ?, PaymentStatus = ? WHERE BorrowID = ?",
                (condition, payment_status, borrow_id))
    conn.execute("UPDATE Inventory_Items SET Status = ? WHERE AssetTag = ?",
                (new_status, asset_tag))
    conn.commit()
    conn.close()

def delete_inventory_item(asset_tag):
    """Deletes an item from the inventory."""
    conn = get_db_connection()
    conn.execute("DELETE FROM Inventory_Items WHERE AssetTag = ?", (asset_tag,))
    conn.commit()
    conn.close()

def get_models_and_categories():
    """Fetches all models and categories for the 'Add Item' form."""
    conn = get_db_connection()
    models = conn.execute("SELECT ModelID, Name FROM Equipment_Models").fetchall()
    categories = conn.execute("SELECT CategoryID, Name FROM Categories").fetchall()
    conn.close()
    return models, categories

def add_new_item(asset_tag, model_id, purchase_date):
    """Adds a new item to the inventory."""
    conn = get_db_connection()
    conn.execute("INSERT INTO Inventory_Items (AssetTag, ModelID, Status, PurchaseDate) VALUES (?, ?, ?, ?)",
                (asset_tag, model_id, 'Available', purchase_date))
    conn.commit()
    conn.close()

def get_officers():
    """Fetches all members who are officers."""
    conn = get_db_connection()
    officers = conn.execute("SELECT Name, Email FROM Members WHERE IsOfficer = 1").fetchall()
    conn.close()
    return officers

def get_unpaid_borrowings(member_id):
    """Fetches all borrowings for a member that have an outstanding payment."""
    conn = get_db_connection()
    items = conn.execute('''SELECT b.AssetTag, m.Name, m.ReplacementCost, b.PaymentStatus
                          FROM Borrowings b
                          JOIN Inventory_Items i ON b.AssetTag = i.AssetTag
                          JOIN Equipment_Models m ON i.ModelID = m.ModelID
                          WHERE b.MemberID = ? AND b.PaymentStatus IN ('Unpaid', 'Pending Assessment')''', # This query remains correct
                         (member_id,)).fetchall()
    conn.close()
    return items