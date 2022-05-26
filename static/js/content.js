lecs_js = document.getElementById("lecs_js");
reports = document.getElementById("reports");
st_lst = document.getElementById("st_list");
bt_cont = document.getElementById("bt-cont").getElementsByTagName("a")[0];
var imagee1 = document.getElementById("imgg1");

/************************lec_cont *************/
function lec_cont(){
    st_lst.style.display ="none";
    reports.style.display ="none";
    lecs_js.style.display ="block";
    imagee1.src = "{% static 'images/icons/content/opposite/ic_import_contacts_24px.svg' %}" ;
}
/*********************reports*********/
function report() {
    st_lst.style.display ="none";
    lecs_js.style.display ="none";
    reports.style.display ="block";
    bt_cont.classList.remove("active");
    console.log("done");
}

/*********************st_list******************/
function st_list(){
    lecs_js.style.display ="none";
    reports.style.display ="none";
    st_lst.style.display ="block";
    bt_cont.classList.remove("active");
    console.log("done");

}

/******************************pop-up****************/
pop_up_lec = document.getElementById("pop_up_lec");
pop_up_report = document.getElementById("pop_up_report")
pop_up_std = document.getElementById("pop_up_std");
/********************add_lecture ************/
function add_lecture() {
    pop_up_lec.style.display ="block";

}
function cancel_lec() {
    pop_up_lec.style.display ="none";
}


/********************add_report ************/
function add_report() {
    pop_up_report.style.display ="block";

}
function cancel_report() {
    pop_up_report.style.display ="none";

}

/*****************************add_std***************/
function add_std(){
    pop_up_std.style.display ="block";
}
function cancel_add_std(){
    pop_up_std.style.display ="none";
}
