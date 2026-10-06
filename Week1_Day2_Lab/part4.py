

# Q. 13 — Create a Customer Dictionary
'''
Store the values in one dictionary. Print the customer name and spend.
'''
#cust_dict= {'customer_id': "C101",
#            'customer_name': "Amelia Clarke",
#            'city': "London",
#            'total_spend': 425.50}

#print(cust_dict['total_spend'])

# Q. 14 — Create a Nested Dictionary
'''
Use the store ID as the outer dictionary key.

Print Manchester's revenue.
'''
#stores= {"LDN-01":
#          {"city": "London", 
#            "revenue": 5000},
#         "MAN-02": {
#             "city": "Manchester",
#             "revenue": 4200}
#        }
#print(stores["MAN-02"]["revenue"])

# Q. 15 — Count Orders by City
'''
Create a dictionary where each key is a city and each value is the number of orders for that city.

'''
from collections import Counter
cities = ["London", "Manchester", "London", "Leeds", "London", "Manchester"]
counter= Counter(cities)
print(counter)

# Q. 16 — MCQ: Choosing a Data Structure
'''
You need to store customer details such as name, city, and total spend under clear field names. Which structure is the best starting choice?
'''
#Answer: B. Dictionary