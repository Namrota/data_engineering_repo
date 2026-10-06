


# Q. 1 — Classify Order Values
'''
For each amount below, print:
High when the amount is at least 100;
Medium when the amount is at least 50 but below 100;
Low when the amount is below 50.

'''
#amounts = [24.50, 55.00, 120.00, 49.99, 99.50]
#for amount in amounts:
#    if amount >= 100:
#        print(f"High: {amount}")

#    elif amount >= 50 and amount < 100:
#        print(f"Medium: {amount}")

#    else:
#        print(f"Low: {amount}")

#Q. 2 — Apply Two Business Rules
'''
Case 1: amount = 125, member = True
Case 2: amount = 125, member = False
Case 3: amount = 65, member = True

amount >= 100
AND
member is True
'''

#Case 1:
#amount= 125
#is_member= True
#if amount >= 100 and is_member:
#    print(f"Case 1: Amount: {amount}, Member: {is_member}")

#Case 2:
#amount= 125
#is_member= False
#if amount >= 100 and is_member:
#    print(f"Amount: {amount}, Member: {is_member}")
#else:
#    print("Case 2: Not a member or amount less than 100")

#Case 3:
#amount= 65
#is_member= True
#if amount >= 100 and is_member:
#    print(f"Amount: {amount}, Member: {is_member}")
#else:
#    print("Case 3: Not a member or amount less than 100")

# Q. 3 — Calculate Completed Revenue

'''
Use a for loop with range() and an if condition to calculate completed revenue.
'''
statuses = [
    "complete",
    "cancelled",
    "complete",
    "complete",
]
 
amounts = [
    45.50,
    18.00,
    62.25,
    30.00,
]

total_completed_revenue= 0
for i in range(len(statuses)):
    if statuses[i] == "complete":
        total_completed_revenue += amounts[i]

print(f"Total completed revenue: {total_completed_revenue:.2f}")

# Q. 4 — MCQ: if, elif, else
'''
What happens after Python finds the first true condition in an if / elif / else chain?

'''
# Amswer: C. It runs that branch and skips the remaining branches.
