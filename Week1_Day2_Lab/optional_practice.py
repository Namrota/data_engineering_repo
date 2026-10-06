

# Q. 17 — Build a Small Order Cleaner
'''
Create:

a list of accepted orders;
a list of rejected orders;
a set of seen order IDs.
Reject:

duplicate order IDs;
non-positive amounts.

'''
orders = [
    {"order_id": 401, "city": "London", "amount_gbp": 45.50},
    {"order_id": 402, "city": "Manchester", "amount_gbp": -5.00},
    {"order_id": 401, "city": "London", "amount_gbp": 45.50},
    {"order_id": 403, "city": "Leeds", "amount_gbp": 30.00},
]

accepted_orders= []
rejected_orders= []
seen_ids= set()
for order in orders:
    if order['order_id'] in seen_ids or order['amount_gbp'] < 0:
        rejected_orders.append(order)
    else:
        accepted_orders.append(order)
        seen_ids.add(order["order_id"])

#print(f"Accepted orders: {accepted_orders}")
#print(f"Rejected orders: {rejected_orders}")
    

# Q. 18 — Revenue by City
'''

Using the accepted data from Q. 17, create a dictionary containing total revenue by city.
'''
revenue_dict= {}
for order in accepted_orders:
    city= order['city']
    amount= order['amount_gbp']
    if city not in revenue_dict:
        revenue_dict[city]= 0
    revenue_dict[city] += amount
print(revenue_dict)

# Q. 19 — Stop After Three Valid Orders

'''
Skip invalid values. Stop completely after three valid values have been processed.
'''
amounts = [10, -5, 20, 0, 30, 40]
clean_amounts= []
limit= 3

for amount in amounts:
    if amount <= 0: continue
    clean_amounts.append(amount)
    if len(clean_amounts) == limit: break

print(clean_amounts)

# Q. 20 — Choose the Structure
'''
For each case, choose list, tuple, set, or dictionary, and explain why.

Ordered daily file names. -> List
Unique customer IDs. -> Set
Fixed latitude and longitude. -> Tuple
Customer ID mapped to customer details. -> Dictionary

'''

