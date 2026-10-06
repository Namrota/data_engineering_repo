'''
Part 3 — Lists, Tuples, and Sets
'''

# Q. 9 — Update a List of Stores
'''
Perform these tasks:
add Leeds;
change Bristol to Birmingham;
remove Manchester;
print the final list.
'''
#stores = ["London", "Manchester", "Bristol"]
#stores.append("Leeds")
#print(f"After adding Leeds in the list: {stores}")
# Using pop to remove the element from the specified index, if index not known then use remove()
#stores.pop(2)
#stores.insert(2, "Burmingham")
#print(f"After updating Bristol to Burmingham in the list: {stores}")

# Q. 10 — Remove Duplicate Store IDs
'''
Create a set to get unique store IDs.

Print:
the original count;
the unique count;
the unique values.

'''
#store_ids = ["LDN-01", "MAN-02", "LDN-01", "BRS-03", "MAN-02"]
#print(f"Original Count of store IDs: {len(store_ids)}")
#set_store_ids= set(store_ids)
#print(f"Unique count of store IDs: {len(set_store_ids)} | {set_store_ids}")

# Q. 11 — Use a Tuple for Fixed Values
'''
Print each value by position.

Then try to change "London" to "Leeds" and note what happens.
'''
store_location = ("LDN-01", "London", "South")
for idx, val in enumerate(store_location):
    print(f"{idx}: {val}")

# Since Tuple is immutable the elements cannot be updated

# Q. 12 — MCQ: Set
'''
Q. 12 — MCQ: Set
'''
#Answer: D. Keep unique values and quickly check membership.
