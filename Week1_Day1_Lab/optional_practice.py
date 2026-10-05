



# Q. 17 — Build a Small Order Calculator

order_id= input("Enter the order ID: ")
city= input("Enter the city: ")
unit_price= float(input("Enter the unit price: "))
quantity= int(input("Enter the quantity: "))
discount_percent= float(input("Enter the discount percentage: "))

# Calculate subtotal, discount amount, final total:
subtotal= unit_price * quantity
discount_amount= subtotal * (discount_percent / 100)
final_total= subtotal - discount_amount

# Display the order summary:
print(f"{order_id} - {city} | Subtotal: €{subtotal:.2f} | Discount: €{discount_amount:.2f} | Final Total: €{final_total:.2f}")

# Q. 18 — Create Validation Flags

valid_quantity= quantity > 0
valid_discount= 0 <= discount_percent <=100
all_valid= valid_quantity and valid_discount

print(f"Valid Quantity: {valid_quantity}, Valid Discount: {valid_discount}, All Valid: {all_valid}")

# Q. 19 — Debug an Input and Comparison Script
city = input("City: ")
# the value of amount needs to be typecasted from str to flaot to allow for comparison operator to work
amount = float(input("Amount: ")) 
is_high_value = amount >= 100
print(f"{city} | £{amount:.2f} | High value: {is_high_value}")