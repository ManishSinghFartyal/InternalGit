import java.util.Scanner; 
public class PrimeNumber 
{ 
                public static void main(String args[]) 
             { 
                  int num,b,c; 
                  Scanner s=new Scanner(System.in); 
                  num =s.nextInt(); 
                  b=1; 
                  c=0; 
                   while(b<= num) 
                      { 
                          if((num%b)==0) 
                             c=c+1; 
                             b++; 
                      } 
                       if(c==2) 
                       System.out.println("Number is prime"); 
                       else 
                       System.out.println("Number is not prime"); 
             } 
}
                      