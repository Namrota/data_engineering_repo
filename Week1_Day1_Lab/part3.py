# Q. 9 — Check Whether an Order Is High Value
# amount= float(input("Enter the order amount: "))
# is_high_value= amount >= 100.00
# print(f"Is the order value high? {is_high_value}")


# Q. 10 — Combine Two Conditions

 #status= "complete"
#amount= 45.50
#accept_order= (status== "complete" and amount > 0)
#print(f"Accept order: {accept_order}")

#status= "cancelled"
#amount= 45.50
#accept_order= (status== "complete" and amount > 0)
#print(f"Accept order: {accept_order}")

#status= "complete"
#amount= -5.50
#accept_order= (status== "complete" and amount > 0)
#print(f"Accept order: {accept_order}")

# Q. 11 — Build a Small Interactive Check
store_name= input("Enter store name: ")
order_amount= float(input("Enter the order amount: "))

accept_order= order_amount>0
print(f"{store_name} order accepted: {accept_order}")

#Q. 12 — MCQ: Comparison Result
# Answer : True