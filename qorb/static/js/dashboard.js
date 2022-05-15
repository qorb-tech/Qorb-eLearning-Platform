var profile_features = document.getElementById("profile_features");
var profile_feature_active = profile_features.getElementsByClassName("profile_feature")
 function dashboard_teacher(){
  for (var i = 0; i < profile_feature_active.length; i++) {
        var current = profile_features.getElementsByClassName("active");
        // If there's no active class
        if (current.length > 0) {
          current[0].className = current[0].className.replace(" active", "");
        }
          profile_feature_active[0].classList.add("active")
          console.log("dashboard_teacher")
}
}
function profile_teacher(){
  for (var i = 0; i < profile_feature_active.length; i++) {
        var current = profile_features.getElementsByClassName("active");
        // If there's no active class
        if (current.length > 0) {
          current[0].className = current[0].className.replace(" active", "");
        }
          profile_feature_active[1].classList.add("active")
          console.log("profile_teacher")
}
}

function courses(){
  for (var i = 0; i < profile_feature_active.length; i++) {
        var current = profile_features.getElementsByClassName("active");
        // If there's no active class
        if (current.length > 0) {
          current[0].className = current[0].className.replace(" active", "");
        }
          profile_feature_active[2].classList.add("active")
          console.log("courses")
}
}
function reports(){
  for (var i = 0; i < profile_feature_active.length; i++) {
        var current = profile_features.getElementsByClassName("active");
        // If there's no active class
        if (current.length > 0) {
          current[0].className = current[0].className.replace(" active", "");
        }
          profile_feature_active[3].classList.add("active")
          console.log("reports")
}
}
function exams(){
  for (var i = 0; i < profile_feature_active.length; i++) {
        var current = profile_features.getElementsByClassName("active");
        // If there's no active class
        if (current.length > 0) {
          current[0].className = current[0].className.replace(" active", "");
        }
          profile_feature_active[4].classList.add("active")
          console.log("exams")
}
}
