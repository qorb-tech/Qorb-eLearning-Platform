new_exam = document.getElementById("new_exam");
id_course = document.querySelectorAll('#id_course option')
// id_course = document.getElementById("id_course").getElementsByTagName("option")

for(var i=0 ;i < id_course.length ;i++) {
id_course[i].classList.add("optn");
console.log('option');
}
function add_exam(){
    new_exam.style.display ="block";
    console.log('option');
    console.log("new-exam");
}
function cancel_exam () {
    new_exam.style.display ="none";
    console.log("cancel-exam");
}
