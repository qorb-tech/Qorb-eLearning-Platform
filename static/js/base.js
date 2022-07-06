var profile_features = document.getElementById("profile_features");
var profile_feature_active = profile_features.getElementsByClassName("profile_feature")
var image1 = document.getElementById("image1");
var image2 = document.getElementById("image2");
var image3 = document.getElementById("image3");
var image5 = document.getElementById("image5");
var image6 = document.getElementById("image6");

//---hover account
function hoverr1(){
   image1.src ='/static/images/icons/dashboard/oppsite/Group 183.svg';
    }
    function without_hover1(){
      if(image1.src == '/static/images/icons/dashboard/oppsite/Group 183.svg'){
        image1.src ='/static/images/icons/dashboard/oppsite/Group 183.svg';
      }
      else{
        image1.src = '/static/images/icons/dashboard/main page.svg';
      }
    }
function hoverr2(){
    image2.src ='/static/images/icons/dashboard/oppsite/ic_account_circle_24px.svg' ;
    }
    function without_hover2(){
      
    image2.src = '/static/images/icons/dashboard/ic_account_circle_24px.svg';
    }
  //----hover-courses
  function hoverr3(){
   image3.src ='/static/images/icons/dashboard/oppsite/Group 186.svg' ;
  }
  function without_hover3(){
   image3.src = '/static/images/icons/dashboard/Group 186.svg';
  }
 //---hover exams
  function hoverr5(){
   image5.src ='/static/images/icons/dashboard/oppsite/Group 184.svg' ;
  }
  function without_hover5(){
   image5.src = '/static/images/icons/dashboard/exams.svg' ;
  }
  
   //---hover orders
  function hoverr6(){
    image6.src ='/static/images/icons/hover/Icon_attention_solid.svg';
    
   }
   function without_hover6(){
    image6.src = '/static/images/icons/nohover/Icon_attention_solid.svg';
 
   }
  function teacher_dash(){
    for (var i = 0; i < profile_feature_active.length; i++) {
        var current = profile_features.getElementsByClassName("activee");
        // If there's no active class
        if (current.length > 0) {
          current[0].className = current[0].className.replace(" activee", "");
          image1.src = '/static/images/icons/dashboard/main page.svg';
        }
          profile_feature_active[0].classList.add("activee")
          image1.src ='/static/images/icons/dashboard/oppsite/Group 183.svg';
          console.log("dashboard_teacher")
    }
}

function profile() {
    for (var i = 0; i < profile_feature_active.length; i++) {
        var current = profile_features.getElementsByClassName("activee");
        // If there's no active class
        if (current.length > 0) {
          current[0].className = current[0].className.replace(" activee", "");
          image2.src = '/static/images/icons/dashboard/ic_account_circle_24px.svg';
        }
          profile_feature_active[1].classList.add("activee")
          console.log("dashboard_teacher");
          image2.src ='/static/images/icons/dashboard/oppsite/ic_account_circle_24px.svg';
    }
}

function coursesi(){
    for (var i = 0; i < profile_feature_active.length; i++) {
        var current = profile_features.getElementsByClassName("activee");
        // If there's no active class
        if (current.length > 0) {
          current[0].className = current[0].className.replace(" activee", "");
          image3.src ='/static/images/icons/dashboard/Group 186.svg';
        }
          profile_feature_active[2].classList.add("activee")
          image3.src ='/static/images/icons/dashboard/oppsite/Group 186.svg' ;
          console.log("courses")
    }
}

function quiz(){
    for (var i = 0; i < profile_feature_active.length; i++) {
        var current = profile_features.getElementsByClassName("activee");
        // If there's no active class
        if (current.length > 0) {
          current[0].className = current[0].className.replace(" activee", "");
          image5.src = '/static/images/icons/dashboard/exams.svg' ;
        }
          profile_feature_active[3].classList.add("activee")
          image5.src ='/static/images/icons/dashboard/oppsite/Group 184.svg' ;
          console.log("quize")
    }
}

function orders(){
  for (var i = 0; i < profile_feature_active.length; i++) {
      var current = profile_features.getElementsByClassName("activee");
      // If there's no active class
      if (current.length > 0) {
        current[0].className = current[0].className.replace(" activee", "");
        image6.src = '/static/images/icons/nohover/Icon_attention_solid.svg';
       
      }
        profile_feature_active[4].classList.add("activee")
        image6.src ='/static/images/icons/hover/Icon_attention_solid.svg';
        console.log("orders")
  }
}
