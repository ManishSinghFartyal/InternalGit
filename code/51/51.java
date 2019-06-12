import java.io.*;
import java.util.*;

public class Solution {

    public static void main(String[] args) {
        
        Scanner sc=new Scanner(System.in);
        String A=sc.next();
        /* Enter your code here. Print output to STDOUT. */
         temp=n;    
          while(n>0){    
           r=n%10;  //getting remainder  
           sum=(sum*10)+r;    
           n=n/10;    
          }    
          if(temp==sum)    
           System.out.println("palindrome number ");    
          else    
           System.out.println("not palindrome");    
        }  

    }
}
                                
                                
                                
                                
                                