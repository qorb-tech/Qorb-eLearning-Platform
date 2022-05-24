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

const realFileBtn = document.getElementById("id_posti");
const customBtn = document.getElementById("custom-button");

customBtn.addEventListener("click", function() {
    realFileBtn.click();
});
var loadFile = function(event) {
    var image = document.getElementById('output');
    image.src = URL.createObjectURL(event.target.files[0]);
};