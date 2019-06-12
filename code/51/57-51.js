var readline = require('readline');

var rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout

});

rl.question("", function(number) {
   /* number is the number for which you need to find factorial */
   /* write your code here */
   fact=1;
   for(i=1;i<=number;i++){
   fact = fact*i;
   }
   console.log(fact);
   rl.close();
});
                        