
exams_btn = document.getElementById("exams_btn").getElementsByTagName("button")[0];

available_exams = document.getElementById("available_exams");
finish_exams=document.getElementById("finish_exams");


function available_exam() {
    finish_exams.style.display="none";
    available_exams.style.display="block";
    console.log("done")
} 

function finish_exam() {
    
    available_exams.style.display="none";
    finish_exams.style.display="block";
    exams_btn.classList.remove("active");
    console.log("done")
}


