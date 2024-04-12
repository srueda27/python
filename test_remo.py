def sort_inventory(products, sort_key, ascending=True):
    # Check if the sort_key is valid
    if not all(sort_key in product for product in products):
        raise ValueError(f"Invalid sort key: {sort_key}")
    
    # if sort_key not category, order and return
    if sort_key != 'category':
        # For other sort keys, directly sort products with a secondary sort by 'product_id'
        sorted_products = sorted(products, key=lambda x: (x[sort_key], x['product_id']), reverse=not ascending)
        return sorted_products
    
    # Calculate total stock for each category
    category_stock = {}
    for product in products:
        category = product['category']
        category_stock[category] = category_stock.get(category, 0) + product['stock_quantity']

    # Sort categories by their total stock. Reverse the sorting logic here
    # to correctly match the ascending/descending order specified.
    categories_sorted_by_total_stock = sorted(category_stock, key=category_stock.get, reverse=ascending)

    # Sort products within each category by stock_quantity in descending order
    sorted_products = []
    for category in categories_sorted_by_total_stock:
        products_in_category = [p for p in products if p['category'] == category]
        sorted_products_in_category = sorted(products_in_category, key=lambda x: x['stock_quantity'], reverse=True)
        sorted_products.extend(sorted_products_in_category)
        

    return sorted_products

# Examples  of usage to demonstrate sorting by all fields in both ascending and descending order
products = [
    {'product_id': 101, 'name': 'Widget A', 'category': 'Widgets', 'price': 19.99, 'stock_quantity': 25, 'rating': 4.5},
    {'product_id': 102, 'name': 'Widget B', 'category': 'Widgets', 'price': 24.99, 'stock_quantity': 15, 'rating': 4.7},
    {'product_id': 103, 'name': 'Gadget A', 'category': 'Gadgets', 'price': 29.99, 'stock_quantity': 30, 'rating': 4.8},
    {'product_id': 104, 'name': 'Gadget B', 'category': 'Gadgets', 'price': 14.99, 'stock_quantity': 50, 'rating': 4.2},
]


# Sorting by 'category' descending order
sorted_by_category_desc = sort_inventory(products, 'category', ascending=False)
print("\nSorted by Category (Descending by total stock):")
for product in sorted_by_category_desc:
    print(product)
    
# Sorting by 'rating' in ascending order
sorted_by_rating_asc = sort_inventory(products, 'rating', ascending=True)
print("Sorted by Rating (Ascending):")
for product in sorted_by_rating_asc:
    print(product)

# Sorting by 'rating' in descending order
sorted_by_rating_desc = sort_inventory(products, 'rating', ascending=False)
print("Sorted by Rating (Descending):")
for product in sorted_by_rating_desc:
    print(product)

# Sorting by 'stock_quantity' in ascending order
sorted_by_stock_asc = sort_inventory(products, 'stock_quantity', ascending=True)
print("\nSorted by Stock Quantity (Ascending):")
for product in sorted_by_stock_asc:
    print(product)
    
# Sorting by 'stock_quantity' in descending order
sorted_by_stock_asc = sort_inventory(products, 'stock_quantity', ascending=False)
print("\nSorted by Stock Quantity (Descending):")
for product in sorted_by_stock_asc:
    print(product)
    
# Sorting by 'name' in ascending order
sorted_by_name_asc = sort_inventory(products, 'name', ascending=True)
print("\nSorted by Name (Ascending):")
for product in sorted_by_name_asc:
    print(product)

# Sorting by 'name' in descending order
sorted_by_name_desc = sort_inventory(products, 'name', ascending=False)
print("\nSorted by Name (Descending):")
for product in sorted_by_name_desc:
    print(product)

# Attempting to sort by an inexistent key
try:
    sorted_by_inexistent_key = sort_inventory(products, 'non_existent_key', ascending=True)
except ValueError as e:
    print("\nError when sorting by an inexistent key:", e)