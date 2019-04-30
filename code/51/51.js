var readline = require('readline');

var rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: false
});

rl.on('line', function (line) {
	fact=1;
    if(line<0){
    console.log("Not valid");
    }
    else{
    for(var i=1;i<=line;i++){
    fact=fact*i;
    }
    console.log(fact);
    }
  
});
                                