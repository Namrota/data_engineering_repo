# Q. 9 — Check Whether an Order Is High Value
# amount= float(input("Enter the order amount: "))
# is_high_value= amount >= 100.00
# print(f"Is the order value high? {is_high_value}")


# Q. 10 — Combine Two Conditions

status= "complete"
amount= 45.50
accept_order= (status== "complete" and amount > 0)
print(f"Accept order: {accept_order}")

status= "cancelled"
amount= 45.50
accept_order= (status== "complete" and amount > 0)
print(f"Accept order: {accept_order}")

status= "complete"
amount= -5.50
accept_order= (status== "complete" and amount > 0)
print(f"Accept order: {accept_order}")