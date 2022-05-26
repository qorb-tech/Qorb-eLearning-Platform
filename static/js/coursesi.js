var profile_features = document.getElementById("profile_features");
var profile_feature_active = profile_features.getElementsByClassName("profile_feature")
    
for (var i = 0; i < profile_feature_active.length; i++) {
    var current = profile_features.getElementsByClassName("activee");
    // If there's no active class
    if (current.length > 0) {
      current[0].className = current[0].className.replace(" activee", "");
      image3.src = '/static/images/icons/dashboard/Group 186.svg';
    }
      profile_feature_active[2].classList.add("activee")
      image3.src ='/static/images/icons/dashboard/oppsite/Group 186.svg' ;
      console.log("courses")
}