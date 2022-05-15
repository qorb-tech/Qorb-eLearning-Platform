coursess = document.getElementById("coursess");
Ncontnt = document.getElementById("Ncontnt");

function new_course() {
    coursess.style.display = "none";
    Ncontnt.style.display ="block";
}

function canel_new_course() {
    Ncontnt.style.display ="none";
    coursess.style.display = "block";

}
