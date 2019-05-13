num = int(input())  
if num > 1:
   for i in range(num):
       if (num % i) == 0:  
           print(num,"is not a prime number")            
           break
   else:
       print(num,"is a prime number")     
else:
   print(num,"is not a prime number")
