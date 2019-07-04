# Python program to find the factorial of a number using recursion

def recur_factorial(n):
   """Function to return the factorial
   of a number using recursion"""
   if n == 1:
       return n
   else:
       return n*recur_factorial(n-1)

# Change this value for a different result


# uncomment to take input from the user
num = int(input())

# check is the number is negative
if num < 0:
   print("Negative numbers")
elif num == 0:
   print(1)
else:
   print(recur_factorial(num))