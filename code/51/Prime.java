import java.io.*;
import java.util.*;

class Prime
{
	public static void main(String arg[])
    {
    	
    	Scanner sc=new Scanner(System.in);
        
        int n=sc.nextInt();
        int c=0;
        for(int i=1;i<=n;i++)
        {
        	if(n%i==0)
            {
            	c++;
			}
        }
        
        if(c==2)
        {
        	System.out.println("Number is prime");
		}
        else
        {
        	System.out.println("Number is not prime");
        }
	}
}