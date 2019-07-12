
// Code to dynamically add test cases with respective outputs/
function addTestCase(){ 
  var count=document.getElementById('id_total_testcases_count').value;
   if(count>=10){
    alert("You cannot add more than 10 test cases.")
   }
   else{
      count++;
      input_label = document.createElement('label');
      input_label.setAttribute('for','id_input_'+count);
      input_label.setAttribute('id','id_input_label_'+count) ; 
      input_label.innerHTML='Test Case : '+count+'&nbsp;&nbsp;';
      document.getElementById('tc').appendChild(input_label);

      input = document.createElement('input'); 
      input.setAttribute('name','input_'+count);
      input.setAttribute('size','35');
      input.setAttribute('id','id_input_'+count) ;
      document.getElementById('tc').appendChild(input);

     /* add_more = document.createElement('a'); 
      add_more.setAttribute('name','add_more_'+count);
      add_more.setAttribute('href','#');
      add_more.setAttribute('onclick','add_more_input(this)');      
      add_more.setAttribute('size','35');
      add_more.setAttribute('id','add_more_'+count);
      add_more.innerHTML='+';

      document.getElementById('tc').appendChild(add_more);
*/
      output_label = document.createElement('label');
      output_label.setAttribute('for','id_output_'+count);
      output_label.setAttribute('id','id_output_label_'+count) ; 
      output_label.innerHTML='&nbsp;&nbsp&nbsp;Output : '+count+'&nbsp;&nbsp;';
      document.getElementById('tc').appendChild(output_label);

      output = document.createElement('input');  
      output.setAttribute('name','output_'+count);  
      output.setAttribute('size','35');  
      output.setAttribute('id','id_output_'+count)  ;
      document.getElementById('tc').appendChild(output) ;
      document.getElementById('id_total_testcases_count').value=count;

      remove_str = 'removeTestCase(id_input_'+count+',id_output_'+count+',remove_'+count+',id_input_label_'+count+',id_output_label_'+count+',hr_'+count+')';
      remove = document.createElement('a');
      remove.innerHTML='&nbsp;&nbsp;<img src="/static/admin/img/remove.png" width=35px height=25px>';
      remove.setAttribute('onclick',remove_str);
      remove.setAttribute('id',"remove_"+count);
      remove.setAttribute('href','#');        
      document.getElementById('tc').appendChild(remove);

      hr=document.createElement('hr')
      hr.setAttribute('id',"hr_"+count);
      document.getElementById('tc').appendChild(hr) ;
     }
  };


//To remove the test case
function removeTestCase(id1,id2,id3,id4,id5,id6){
  tc =document.getElementById('tc')
  tc.removeChild(id1)
  tc.removeChild(id2)
  tc.removeChild(id3)
  tc.removeChild(id4)
  tc.removeChild(id5)
  tc.removeChild(id6)
  var total=document.getElementById('id_total_testcases_count').value;
  var remaining=total-1;
  var count=1;
  if(remaining>=1){
    for(i=1;i<10;i++){      
      id = document.getElementById('id_input_'+i);
      if(id){
        document.getElementById('id_input_'+i).name = 'input_'+count;
        document.getElementById('id_input_'+i).id = 'id_input_'+count;    
        document.getElementById('id_input_label_'+i).innerHTML = 'Test Case : '+count;    
        document.getElementById('id_input_label_'+i).id = 'id_input_label_'+count;
        document.getElementById('id_output_'+i).name='output_'+count;
        document.getElementById('id_output_'+i).id='id_output_'+count;    
        document.getElementById('id_output_label_'+i).innerHTML = 'Output : '+count;      
        document.getElementById('id_output_label_'+i).id='id_output_label_'+count;
        remove_str = 'removeTestCase(id_input_'+count+',id_output_'+count+',remove_'+count+',id_input_label_'+count+',id_output_label_'+count+',hr_'+count+')';
        console.log('remove_'+i+'   '+remove_str);
        a=document.getElementById('remove_'+i)
        a.setAttribute('onclick',remove_str)
        a.id='remove_'+count;
        document.getElementById('hr_'+i).id='hr_'+count;
        count = count+1;
      }
      else{
        continue;
      }
    }    
  }  
  else{
    document.getElementById('id_total_testcases_count').value = 0;
  }
  document.getElementById('id_total_testcases_count').value = remaining;
}



//Code to add options dynamically
function addOptions(){ 
  var ph=''
  var count=document.getElementById('id_total_options').value; 
   if(count>=6){
    alert("You cannot add more than 6 options")
   }
   else{
      count++;
      if(count==1){
        ph=1
      }
      else if(count==2){
        ph=2
      }
      else if(count==3){
        ph=3
      }
      else if(count==4){
        ph=4
      }
      else if(count==5){
        ph=5
      }
     else if(count==6){
        ph=6
      }

      

      input_label = document.createElement('label');
      input_label.setAttribute('for','id_input_'+count);
      input_label.setAttribute('id','id_input_label_'+count);
      input_label.innerHTML='Option : '+ph+'&nbsp;&nbsp;';
      document.getElementById('op').appendChild(input_label);

      input = document.createElement('input'); 
      input.setAttribute('name','option_'+count);
      input.setAttribute('size','80px');
      input.setAttribute('required','true');
      input.setAttribute('id','id_option_'+count); 
      document.getElementById('op').appendChild(input);
      document.getElementById('id_total_options').value=count;
      
      remove_str = 'removeOptions(id_input_label_'+count+',id_option_'+count+',remove_'+count+',hr_'+count+')';
      remove = document.createElement('a');
      remove.innerHTML='&nbsp;&nbsp;<img src="/static/admin/img/remove.png" width=35px height=25px>';
      remove.setAttribute('onclick',remove_str);
      remove.setAttribute('id',"remove_"+count);
      remove.setAttribute('href','#');        
      document.getElementById('op').appendChild(remove);


      hr=document.createElement('hr')
      hr.setAttribute('id',"hr_"+count);
      document.getElementById('op').appendChild(hr);

     }
  };

  //To remove the test case
function removeOptions(id1,id2,id3,id4){
  tc =document.getElementById('op')
  tc.removeChild(id1)
  tc.removeChild(id2)
  tc.removeChild(id3)
  tc.removeChild(id4)
  var total=document.getElementById('id_total_options').value;
  var remaining=total-1;
  var count=1;
  if(remaining>=1){
    for(i=1;i<=6;i++){      
      id = document.getElementById('id_input_label_'+i);
      if(id){
        document.getElementById('id_input_label_'+i).name = 'input_'+count;
        document.getElementById('id_input_label_'+i).innerHTML = 'Option : '+count;    
        document.getElementById('id_input_label_'+i).id = 'id_input_label_'+count;    
        document.getElementById('id_option_'+i).name='option_'+count;
        document.getElementById('id_option_'+i).id='id_option_'+count;            
        remove_str = 'removeOptions(id_input_label_'+count+',id_option_'+count+',remove_'+count+',hr_'+count+')';
        a=document.getElementById('remove_'+i)
        a.setAttribute('onclick',remove_str)
        a.id='remove_'+count;
        document.getElementById('hr_'+i).id='hr_'+count;
        count = count+1;
      }
      else{
        continue;
      }
    }    
  }  
  else{
    document.getElementById('id_total_options').value = 0;
  }
  document.getElementById('id_total_options').value = remaining;
}





// Code to show respective question form when selecting type of question 
function showAddQuestion(){

  type=document.getElementById('qtype').value;
  if(type == 'ct')
  {
    height = document.getElementById("codeTest").offsetHeight;
    width = document.getElementById("resize").offsetWidth;
    document.getElementById("resize").style.height = height - 20 +'px';
    document.getElementById("codeTest").style.width = width - 90 +'px';
    document.getElementById('addct').style.visibility = "visible"
    document.getElementById('addmcq').style.visibility = "hidden"
    document.getElementById('id_question').setAttribute('required','false')
    document.getElementById('id_title').setAttribute('required','true')
    document.getElementById('id_description').setAttribute('required','true')
    document.getElementById('id_snippet').setAttribute('required','true')
  }    
  else if(type == 'mcq'){

    height = document.getElementById("mcqTest").offsetHeight;
    width = document.getElementById("resize").offsetWidth;
    document.getElementById("resize").style.height = height - 20 +'px';
    document.getElementById("mcqTest").style.width = width - 90 +'px';
    document.getElementById('addmcq').style.visibility = "visible" 
    document.getElementById('addct').style.visibility = "hidden"
    document.getElementById('id_title').setAttribute('required','false')
    document.getElementById('id_description').setAttribute('required','false')
    document.getElementById('id_snippet').setAttribute('required','false')
    document.getElementById('id_question').setAttribute('required','true')
  }    
};

/*function add_more_input(c){
    count_array = c.name.split("_");
    count=Number(count_array[2])+1;
    console.log(count)   

    input = document.createElement('input'); 
    input.setAttribute('name',c.name);
    input.setAttribute('placeholder',"Input value "+count++);
    input.setAttribute('size','35');
    input.setAttribute('id',c.id) ;
    document.getElementById('tc').appendChild(input);

    add_more = document.createElement('a'); 
    add_more.setAttribute('name','add_more_'+count);
    add_more.setAttribute('href','#');
    add_more.setAttribute('onclick','add_more_input(this)');      
    add_more.setAttribute('size','35');
    add_more.setAttribute('id','add_more_'+count);
    add_more.innerHTML='+';  
};

*/

