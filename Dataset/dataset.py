import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# --- 1. Product Definitions (25 Products) ---

products = {
    'Food': {
        'F01': ('Organic Apples', 3.50), 'F02': ('Whole Wheat Bread', 4.99),
        'F03': ('Premium Coffee Beans', 12.50), 'F04': ('Aged Cheddar Cheese', 6.99),
        'F05': ('Olive Oil (Extra Virgin)', 15.99), 'F06': ('Dark Chocolate Bar', 3.99),
        'F07': ('Free-Range Eggs', 5.50), 'F08': ('Fresh Salmon Fillet', 18.99),
        'F09': ('Sparkling Water Case', 8.00), 'F10': ('Organic Pasta Sauce', 4.25)
    },
    'Apparel': {
        'C01': ('Men\'s Slim-Fit Jeans', 79.99), 'C02': ('Women\'s Cotton T-Shirt', 19.99),
        'C03': ('Casual Sneakers', 55.00), 'C04': ('Winter Wool Scarf', 35.00),
        'C05': ('Leather Wallet', 35.00), 'C06': ('Business Suit Jacket', 199.99),
        'C07': ('Kids\' Rain Boots', 25.00), 'C08': ('Athletic Sports Dress', 45.00),
        'C09': ('Dress Socks (Pack of 5)', 12.00), 'C10': ('Designer Handbag', 150.00)
    },
    'Electronics': {
        'E01': ('Noise-Cancelling Headphones', 199.99), 'E02': ('Wireless Charging Pad', 39.99),
        'E03': ('Portable Bluetooth Speaker', 55.00), 'E04': ('24-inch LED Monitor', 129.00),
        'E05': ('USB-C Flash Drive (128GB)', 15.00)
    }
}
# 1. Choose ONE category (enforcing the constraint)
chosen_category = random.choice(list(products.keys()))

# 2. Choose 1 to 5 unique products from that category
# ... (sampling from the chosen category)
# --- 2. Demographic and Setup ---
age_groups = ['18-25', '26-35', '36-50', '51-65', '65+']
income_levels = ['Low', 'Medium', 'High']
NUM_CUSTOMERS = 2000
customer_ids = [f'C{i:04d}' for i in range(1, NUM_CUSTOMERS + 1)]

# Assign a fixed demographic profile to each customer
customer_demographics = {
    cid: {
        'Age_Group': random.choice(age_groups),
        'Income_Level': random.choice(income_levels)
    }
    for cid in customer_ids
}

# --- 3. Transaction Generation Logic ---
data = []
transaction_counter = 1
start_date = datetime.now() - timedelta(days=365)

# Simulate transactions for all 2000 customers
for customer_id in customer_ids:
    # Each customer has between 3 and 15 transactions
    num_transactions = random.randint(3, 15)
    
    for _ in range(num_transactions):
        transaction_id = f'T{transaction_counter:05d}'
        transaction_counter += 1
        
        # 1. Choose ONE category (enforcing the constraint)
        chosen_category = random.choice(list(products.keys()))
        
        # 2. Choose 1 to 5 unique products from that category
        available_pids = list(products[chosen_category].keys())
        num_items = random.randint(1, min(5, len(available_pids)))
        bought_pids = random.sample(available_pids, num_items)
        
        # 3. Choose a random purchase date
        random_days = random.randint(1, 365)
        purchase_date = (start_date + timedelta(days=random_days)).strftime('%Y-%m-%d')
        
        # 4. Generate line items
        for product_id in bought_pids:
            name, price = products[chosen_category][product_id]
            quantity = random.randint(1, 4)
            
            data.append({
                'Customer ID': customer_id,
                'Transaction ID': transaction_id,
                'Product ID': product_id,
                'Product Category': chosen_category,
                'Product Name': name,
                'Quantity': quantity,
                'Price': price,
                'Date of Purchase': purchase_date,
                'Demographics (Age, Income)': f"Age: {customer_demographics[customer_id]['Age_Group']}, Income: {customer_demographics[customer_id]['Income_Level']}"
            })

# --- 4. Create DataFrame and Export ---
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
output_filename = 'customer_purchase_data.csv'
df.to_csv(output_filename, index=False)

print(f"✅ Successfully generated dataset for {NUM_CUSTOMERS} customers.")
print(f"File saved as '{output_filename}'.")
print(f"Total rows (line items): {len(df)}")