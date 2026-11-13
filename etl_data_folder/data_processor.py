import json
import os
import csv
import logging



def read_orders(file_path):
    """
    param:
    file_path: str - path to the JSON file containing order data
    

    Definition:
    This function reads a JSON file containing order data, using the try-except block for Error
    handling. Returns the data or an empty list if the file is not found or if there is a JSON
    decoding error.
      
    """
    try:
        with open(file_path, 'r') as file:
            data= json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} is not a valid JSON file")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []
    finally:
        print(f"Finished data reading: {file_path}")


def clean_customer_name(name):
    """ 
    This function cleans the leading/trailing whitespace and converts the customer name to title case.
   
    """
    return name.strip().title() if isinstance(name, str) else ""


# Data validation and datatype conversion functions:
def validate_order(order: dict):
    """
    This function validates if the required field exist.
    Validates that quantity is a positive integer.
    Validates that price is a valid positive float.
    Returns True if valid, False otherwise.
    
    """
    required_fields= ['order_id', 'quantity', 'price']
    missing_fields=[field for field in required_fields if field not in order]
    if missing_fields:
        print(f"Error: Missing required fields: {missing_fields}")
        return False

    # Quantity:
    try:
        quantity= int(order.get('quantity'))

        if quantity <= 0:
            print(f"Error: Quantity must be a positive integer. Found: {quantity}")
            return False
    except (ValueError, TypeError):
        print(f"Error Exception: Quantity must be a positive integer. Found {order.get('quantity')}")
        return False
    
    # Price:
    try:
        price= float(order.get('price'))
        if price <= 0:
            print(f"Error: Price must be a positive float. Found {price}")
            return False
    except (ValueError, TypeError):
        print(f"Error Exception: Price must be a positive float. Found {order.get('price')}")
        return False
    
    return True


def normalize_order(order: dict) -> dict:

    """
    Cleans customer name using clean_customer_name function.
    Converts quantity to integer (handle string numbers).
    Converts price to float (handle string numbers).
    Returns normalized order dictionary.
    
    """
    normalized_order= order.copy()
    normalized_order['customer_name']= clean_customer_name(normalized_order.get('customer_name', ''))
    normalized_order['quantity']= int(normalized_order.get('quantity', 0))
    normalized_order['price']= float(normalized_order.get('price', 0.0))
    return normalized_order

# function to remove duplicates:
def remove_duplicates(orders) -> list:
    """
    Create a function remove_duplicates(orders) that:
    Uses a set or dictionary to track seen order_ids
    Returns a list with only unique orders (keep first occurrence)
    Uses list comprehension or a loop
    Hint: You can use a set to track seen IDs, or use a dictionary to keep the first occurrence.
    Expected outcome: A function that removes duplicate orders efficiently.

    """

    # removing duplicates for order_id
    seen_order_ids= set()
    cleaned_orders= []
    for order in orders:
        order_id= order.get('order_id')
        if order_id not in seen_order_ids:
            seen_order_ids.add(order_id)
            cleaned_orders.append(order)
    return cleaned_orders

# Process all orders:
def process_orders(orders) -> list:

    '''
    Filters out invalid orders using validate_order()
    Normalizes valid orders using normalize_order()
    Removes duplicates using remove_duplicates()
    Returns cleaned orders list
    
    '''
    cleaned_output= [ normalize_order(order) 
                     for order in orders
                     if validate_order(order)]
    return remove_duplicates(cleaned_output)

def calculate_summary(orders):
    """
    Calculates total number of orders
    Calculates total revenue (sum of quantity × price for all orders)
    Finds the most ordered product
    Returns a dictionary with these statistics

    """
    total_orders= len(orders)
    total_revenue= sum(order['quantity'] * order['price'] for order in orders)
    product_quantity= {}
    for order in orders:
        product= order['product']
        quantity= order['quantity']
        product_quantity[product]= (product_quantity.get(product, 0) + quantity)
    most_ordered_product= (
        max(product_quantity, key= product_quantity.get)
        if product_quantity else None)

    return {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "most_ordered_product": most_ordered_product
    }

#write output file:
def write_csv(orders, file_path):
    """
    Writes orders to a CSV file
    Uses the csv module
    Includes headers: order_id, customer_name, product, quantity, price, order_date
    Uses try-except for error handling
    
    
    """
    try:
        with open(file_path, 'w', newline='') as csvfile:
            field_header= ['order_id', 'customer_name', 'product', 'quantity', 'price', 'order_date']
            writer= csv.DictWriter(csvfile, fieldnames= field_header)
            writer.writeheader()
            writer.writerows(orders)

    except IOError as e:
        print(f"Error: Unable to write to file {file_path}: {e}")



def write_summary(summary, file_path):
    """
    Writes summary statistics to a text file
    Formats the output nicely
    Uses try-except for error handling

    """
    try:
        with open(file_path, 'w') as file:
            file.write("Summary Statistics\n")
            file.write("==================\n")
            file.write("Total Orders: {}\n".format(summary.get("total_orders", 0)))
            file.write("Total Revenue: {:.2f}\n".format(summary.get("total_revenue", 0.0)))
            file.write("Most Ordered Product: {}\n".format(summary.get("most_ordered_product", "None")))
    except IOError as e:
        print(f"Error: Unable to write to file {file_path}: {e}")



######################################## MAIN ##############################################

def main():

    # Files:
    input_file= "data/orders.json"
    output_file= "output/cleaned_orders.csv"
    summary_file= "output/summary.txt"

    print("Starting ETL Process....")
                        
    # Read orders from JSON file
    orders= read_orders(input_file)
    print(f"Orders read from {input_file} JSON file::{len(orders)}")
    # Clean Orders
    cleaned_orders= process_orders(orders)
    print(f"Cleaned orders after processing:: {len(cleaned_orders)}")
    # Calculate summary statistics
    summary= calculate_summary(cleaned_orders)
    # Write the cleaned orders to CSV
    write_csv(cleaned_orders, output_file)
    print(f"Cleaned orders written successfully to {output_file} CSV file")
    # Write the summary statistics to a text file:
    write_summary(summary, summary_file)
    print(f"Summary file successfully generated at {summary_file} text file")
    # Print summary statistics to console
    print("Summary Statistics: ")
    print(f"Total Orders: {summary.get('total_orders')}")
    print(f"Total Revenue: {summary.get('total_revenue')}")
    print(f"Most Ordered Product: {summary.get('most_ordered_product')}")


if __name__ == "__main__":
    main()