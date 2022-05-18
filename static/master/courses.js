
btn = document.getElementById("btns").getElementsByTagName("button")[0];
btn_report = document.getElementById("btns").getElementsByTagName("button")[1];
btn_std = document.getElementById("btns").getElementsByTagName("button")[2];

course_lecs = document.getElementById("course_lecs");
reports=document.getElementById("reports");
student_list= document.getElementById("student_list");
garde = document.getElementById("garde");
var imagee1 = document.getElementById("imgg1");
var imagee2 = document.getElementById("imgg2");
var imagee3 = document.getElementById("imgg3");

function course_lec() {
    reports.style.display="none";
    garde.style.display="none";
    student_list.style.display="none";
    course_lecs.style.display="block";
    btn_report.classList.remove("active");
    btn_std.classList.remove("active");
    imagee1.src = "images/icons/content/opposite/ic_import_contacts_24px.svg" ;
    console.log("done")
}

function report() {
    course_lecs.style.display="none";
    student_list.style.display="none";
    garde.style.display="none";
    reports.style.display="block";
    btn.classList.remove("active");
    btn_std.classList.remove("active");
    imagee2.src = "{% static 'images/icons/content/opposite/Icon_doc_solid.svg' %}" ;
    console.log("done")
}

function std_list() {
    course_lecs.style.display="none";
    reports.style.display="none";
    garde.style.display="none";
    student_list.style.display="block";
    btn.classList.remove("active");
    btn_report.classList.remove("active");
    imagee2.src = "{% static 'images/icons/content/opposite/ic_group_24px.svg' %}" ;
    console.log("done")
}

function total_grade() {
    student_list.style.display="none";
    course_lecs.style.display="none";
    reports.style.display="none";
    garde.style.display="block";
    btn.classList.remove("active");
    console.log("done")
}
/*************new-lec********/
new_lec  = document.getElementById("new-lec");

function add_new_lecture() {
    new_lec.style.display="block"
}

function cancel_new_lecture() {
    new_lec.style.display="none"
}

/********************add_report ************/
function add_report() {
    btn_report.classList.add("active");
    new_report.style.display ="block";

}
function cancel_report() {
    new_report.style.display ="none";

}

/*****************************add_std***************/
function add_std(){
    btn_std.classList.add("active");
    new_std.style.display ="block";
}
function cancel_add_std(){
    new_std.style.display ="none";
}
