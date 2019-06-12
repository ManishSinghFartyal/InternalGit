
  pid = "{{pid}}";
  tid = "{{tid}}";
  window.onload = checkThis();
  function checkThis(){
    if(!document.getElementsByClassName('CodeMirror-scroll')){
      var editor = CodeMirror.fromTextArea(document.querySelector('#code'), {
        lineNumbers: true,
        mode:  "java",
        theme: 'eclipse'
      });  
    }

    {% if paginator.has_other_pages %}
    {% for key,value in paper.items %}
    {% if key in mcq_answered or key in code_answered%}
    str= "{{value.sr}}-count";
    document.getElementById(str).style.background = "#9999";
    {% endif %}
    {% endfor %}
    {% endif %}

    hours=document.getElementById('hours').value; 
    minutes=document.getElementById('minutes').value;
    seconds= document.getElementById('seconds').value;
  };


  function allcheck(){
   {% if paginator.has_next is False %}
   alert("You have successfully attempted all questions. Please submit the test.")
   {% endif %}     
 };


 function radioClicked(key){
  console.log(key)
  key_split=key;
  arr=  key_split.split("|")
  arr = arr[2]
  str = arr + "-count"
  document.getElementById(str).style.background = '#9119';
};


function radioClicked2(value,key){
  sessionStorage.setItem(value,key.value)
  key.setAttribute("id",value)    
  radioClicked(key.value); 
};


function answerChange(){
  hours=document.getElementById('hours').value; 
  minutes=document.getElementById('minutes').value;
  seconds= document.getElementById('seconds').value;
  sessionStorage.setItem("hours",hours)
  sessionStorage.setItem("minutes",minutes)
  sessionStorage.setItem("seconds",seconds)      
  return false;
};


var downloadTimer = setInterval(function(){
  if(seconds>0){
    seconds--;
  }
  else if(minutes>0){
    minutes--;
    seconds=60
  }
  else if(hours>0){
    hours--;
    minutes=60;
    seconds=60;
  }
  else{        
   document.getElementById("quit").click();
 }
 document.getElementById("hours").value = hours;
 document.getElementById("minutes").value = minutes;
 document.getElementById("seconds").value =seconds;
}, 1000);

var editor = CodeMirror.fromTextArea(document.querySelector('#code'), {
  lineNumbers: true,
  mode:  "java",
  theme: 'eclipse'
});  





$("#runajax").click(function(){
  //Hiding the loader
  document.getElementById('loader').style.visibility="visible";  

  //Running code
  id_lang = this.name;
  arr=  id_lang.split("-");
  que_id = arr[0];
  language = arr[1];  
  url = "http://127.0.0.1:8000/candidate/hello/"+que_id;
  code = editor.getValue()
  $.ajax({
    type : "GET",
    url : url,
    dataType :"text",
    csrfmiddlewaretoken: '{{ csrf_token }}',
    data:{
      "code" : code,
      "testid" : pid,
      "language":language,
      "tid":tid,
    },
    contentType: 'application/json',
    success : function(data){
      $("#output").val(data);
      testcases_matched(data)
    },
    failure: function(data) { 
      console.log("Got error");
    },
    error: function(xhr,status,error) { 
      console.log(xhr.responseText + " error  "+error);
    }
  });
  return false;
});



function testcases_matched(json){
 json = JSON.parse(json); 
 check = document.getElementById('testcases-info')
 if(check){
  check.remove();
}
testcases = document.createElement('div');
testcases.setAttribute('id','testcases-info');
testcases.setAttribute('class','row lead');
i=1;
for (var key in json) {     
 result = document.createElement('p');
 if(json[key].result == 'incorrect'){
   result.setAttribute("class","lead btn-danger")
   incorrect_output(i,json[key].input,json[key].result,json[key].your_output,json[key].expected_output,testcases)
   break;
 }
 else{
   line = document.createElement('hr');
   divcol11 = document.createElement('div'); 
   divcol11.setAttribute("class","col-sm-3 text-right");
   divcol12 = document.createElement('div');          
   divcol12.setAttribute("class","col-sm-3 text-right");
   divcol1 = document.createElement('div');
   divcol1.setAttribute("class","col-sm-1 text-center");
   divcol1.setAttribute("id","testcase-style1");
   image = document.createElement("img");
   image.setAttribute("src","{% static 'admin/img/right.svg' %}");
   image.setAttribute("width","30px");
   image.setAttribute("height","30px");
   divcol1.appendChild(image)
   divcol2 = document.createElement('div');
   divcol2.setAttribute("id","testcase-style2");  
   divcol2.setAttribute("class","col-sm-5 text-left");
   divcol2.innerHTML='Testcase '+i+ '&nbsp;&nbsp;&nbsp;&nbsp;'+json[key].result;
   result.setAttribute("class","lead btn btn-sm btn-success");
 }
 line = document.createElement('hr');
     //result.setAttribute('id','result');
     //result.innerHTML='Testcase '+i+ '&nbsp;&nbsp;&nbsp;&nbsp;'+json[key].result
     testcases.appendChild(divcol11);
     testcases.appendChild(divcol1);
     testcases.appendChild(divcol2);
     testcases.appendChild(divcol12);     
     testcases.appendChild(line);
     i++;
   }
   document.getElementById('loader').style.visibility="hidden";
   document.getElementById('testcase').appendChild(testcases);
 }

 function incorrect_output(testcase,input,result1,output,expected,div){  
   form_group1= document.createElement('div');
   form_group1.setAttribute("class","form-group col-sm-12") 
   line = document.createElement('hr');
   result = document.createElement('p');
   result.setAttribute("class","lead col-sm-12")
   result.setAttribute('id','result');
   result.innerHTML='Testcase '+i+ '&nbsp;&nbsp;&nbsp;&nbsp;'+result1;
   label1 = document.createElement('label');
   label1.setAttribute("for","inputvalue");
   label1.innerHTML = "Input";
   input1 = document.createElement('input');
   input1.setAttribute("type","text");
   input1.setAttribute("class","form-control");
   input1.setAttribute("id","inputvalue");
   input1.setAttribute("disabled","True");
   input1.setAttribute("value",input);
   form_group1.appendChild(label1);
   form_group1.appendChild(input1);
   form_group2= document.createElement('div');
   form_group2.setAttribute("class","form-group col-sm-12") 
   label2 = document.createElement('label');
   label2.setAttribute("for","outputvalue");
   label2.innerHTML = "Your output";
   output1 = document.createElement('textarea');
   output1.setAttribute("type","text");
   output1.setAttribute("class","form-control");
   output1.setAttribute("disabled","True");
   output1.setAttribute("id","outputvalue");     
   output1.innerHTML = output;     
   if(output.length > 80){
    output1.setAttribute("rows","5");
  }
  else {
    output1.setAttribute("cols","50");
  }
  form_group2.appendChild(label2);
  form_group2.appendChild(output1);
  form_group3= document.createElement('div');
  form_group3.setAttribute("class","form-group col-sm-12") 
  label3 = document.createElement('label');
  label3.setAttribute("for","outputvalue1");
  label3.innerHTML = "Expected output";
  output2 = document.createElement('input');
  output2.setAttribute("type","text");
  output2.setAttribute("class","form-control");
  output2.setAttribute("disabled","True");
  output2.setAttribute("value",expected);
  output2.setAttribute("id","outputvalue1");     
  form_group3.appendChild(label3);
  form_group3.appendChild(output2);
  div.appendChild(result);
  div.appendChild(form_group1);
  div.appendChild(form_group2);
  div.appendChild(form_group3);
}

shortcut.add("ctrl+enter", function() {
 document.getElementById('runajax').click();
}); 

