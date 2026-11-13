# Day 1.1- Celsius to Fahrenheit converter

temperature= input("Enter the temperature in Celsius: ")
#temperature from Celsius to Fahrenheit
fahrenheit = (float(temperature) * 9/5) + 32
#rounding off the value to 2 decimal places
fahrenheit = round(fahrenheit, 2)
print(f"The temperature in Fahrenheit is: {fahrenheit}")