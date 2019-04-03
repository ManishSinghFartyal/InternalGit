 <script type="text/javascript">
   

    window.onload = checkThis();
    function checkThis(){
       var time = "{{paper_details.max_time}}";
       if(sessionStorage.getItem("hours")==null){
       hours = Math.floor(time/60);
       }
       else{
        hours = sessionStorage["hours"]
        console.log(hours) 
       }
       if(sessionStorage.getItem("minutes")==null){
         minutes = time%60;                
       }else{
        minutes = sessionStorage["minutes"]
       }
       if(sessionStorage.getItem("seconds")==null){
         seconds = 10;
       }        
       else{
        seconds=sessionStorage["seconds"]
       }
      {% for ke,va in pages.items %}
        key = "{{ke}}"
      {%endfor%}
      if(key in sessionStorage){
        id = sessionStorage.getItem(key)
        document.getElementById(id).checked = true;
      }
      for(var a in sessionStorage){
        if(!isNaN(a)){
          radioClicked(sessionStorage[a])          
        }        
      }      
    }

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
     document.getElementById("hours").value = hours;
     document.getElementById("minutes").value = minutes;
     document.getElementById("seconds").value =seconds;     
    }, 1000);

     var editor = CodeMirror.fromTextArea(document.querySelector('#code'), {
      lineNumbers: true,
      mode:  "java",
      theme: 'duotone-light',
    });  

  /* (function() {
    var editor = CodeMirror.fromTextArea(document.querySelector('#code'), {
      lineNumbers: true,
      mode:  "java",
      theme: 'duotone-light',
    });   
  })();
*/
 $("#runajax").click(function(){
  code = editor.getValue()
  $.ajax({
    type : "GET",
    url : "http://127.0.0.1:8000/candidate/hello/",
    dataType :"text",
    csrfmiddlewaretoken: '{{ csrf_token }}',
    data:{
      "code" : code,
    },
    success : function(data){
      $("#output").val(data);  
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
</script>