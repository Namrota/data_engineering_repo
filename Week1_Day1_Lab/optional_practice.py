



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