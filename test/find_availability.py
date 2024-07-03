from cs50 import SQL

db = SQL("sqlite:///amazon.db")


def find_availability(item_id):
    """Returns a list of warehouses in which an item with `item_id` is in stock"""
    available = db.execute("SELECT warehouse_id, warehouses.latitude, warehouses.longitude FROM stock JOIN items ON stock.item_id = items.item_id JOIN warehouses ON stock.warehouse_id = warehouses.warehouse_id WHERE item_id = ? AND quantity > 0", item_id)
    return available
    