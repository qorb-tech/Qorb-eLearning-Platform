var imageee1 = document.getElementById("image-ex");
exams_btn = document.getElementById("exams_btn").getElementsByTagName("button")[0];
available_exams = document.getElementById("available_exams");
finish_exams=document.getElementById("finish_exams");
ava_btn = document.getElementById("exams_btn").getElementsByTagName("button")[0];
fin_btn = document.getElementById("exams_btn").getElementsByTagName("button")[1];

function available_exam() {
    finish_exams.style.display="none";
    available_exams.style.display="block";
    fin_btn.classList.remove("active");
    ava_btn.classList.add("active");
    console.log("done")
    imageee1.src = '/static/images/std/hover/Group.svg' ;
}

function finish_exam() {
    available_exams.style.display="none";
    finish_exams.style.display="block";
    ava_btn.classList.remove("active");
    fin_btn.classList.add("active");
    console.log("done")
    imageee1.src = '/static/images/std/nohover/Group.svg';

}

function hover_std(){
    imageee1.src = '/static/images/std/hover/Group.svg' ;
}
function without_hover_std(){
    if (available_exams.style.display=="block"){
        imageee1.src ='/static/images/std/hover/Group.svg';
    }
    else
    {
     
        imageee1.src = '/static/images/std/nohover/Group.svg';
    }
}