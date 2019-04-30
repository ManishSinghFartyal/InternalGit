var readline = require('readline');

var rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: false
});

rl.on('line', function (ff) {
   /* write your code from here */
   /* take value as the number for which factorial needs to be find */
   if(ff<0){
   console.log("Not valid");   
   }
   else{
   fact=1;
   for(var i=1;i<=ff;i++){
   fact = fact*i;
   }
   console.log(fact);
   }
});
                                
                                
                                
                                
                                