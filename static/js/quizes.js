function current_quizess() {
    student_list.style.display="none";
    course_lecs.style.display="block";
    btn_report.classList.remove("activee");
    btn_std.classList.remove("activee");
    imagee1.src = "/static/images/icons/content/opposite/ic_import_contacts_24px.svg" ;
    console.log("done")
}

function finished_quizess() {
   
    garde.style.display="none";
    reports.style.display="block";
    btn.classList.remove("activee");
    btn_std.classList.remove("activee");
    imagee2.src = '/static/images/icons/content/opposite/Icon_doc_solid.svg'  ;
    console.log("done")
}

// Get all buttons with class="btn" inside the container
var btns = document.getElementsByClassName("btn_exam");