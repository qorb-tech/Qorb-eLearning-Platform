
menu = document.getElementById("menu");
active1 = document.getElementById("activee")

/*******************sticky**********/
window.addEventListener("scroll", function(){
    active1.classList.toggle('sticky', window.scrollY || 0);

})
function nav_active() {
    if(menu.style.display === "none"){
        menu.style.display = "block";
        active1.style.backgroundColor ="rgba(72, 89, 127, 0.6)"
        //  active.style.display = "block";
        console.log("ok")
    }
    else{
        menu.style.display = "none";
        active1.style.backgroundColor ="transparent"
        // active.style.display = "none";

    }
}
