var imagee1 = document.getElementById("imgg1");
  var imagee2 = document.getElementById("imgg2");
  var imagee3 = document.getElementById("imgg3");
  function course_lec() {
      reports.style.display="none";
      
      student_list.style.display="none";
      course_lecs.style.display="block";
      btn_report.classList.remove("active");
      btn_std.classList.remove("active");
      imagee1.src = '/static/images/icons/content/opposite/ic_import_contacts_24px.svg' ;
      document.title = "المحتوى الدراسى";
      console.log("done")
  }

  function report() {
  course_lecs.style.display="none";
  student_list.style.display="none";
  
  reports.style.display="block";
  btn.classList.remove("active");
  btn_std.classList.remove("active");
  imagee2.src = '/static/images/icons/content/opposite/Icon_doc_solid.svg'  ;
  imagee1.src = '/static/images/icons/content/ic_import_contacts_24px.svg' ;
  document.title = " التقارير";
  console.log("done")
  }
  function std_list() {
  course_lecs.style.display="none";
  reports.style.display="none";

  student_list.style.display="block";
  btn.classList.remove("active");
  btn_report.classList.remove("active");
  imagee3.src = '/static/images/icons/content/opposite/ic_group_24px.svg'  ;
  imagee1.src = '/static/images/icons/content/ic_import_contacts_24px.svg' ;
  document.title = " قائمة الطلبة";
  console.log("done")
 }
  
const realFileBtn = document.getElementById("id_posti");
const customBtn = document.getElementById("custom-button");

customBtn.addEventListener("click", function() {
    realFileBtn.click();

});

const realFileBtn2 = document.getElementById("id_posti2");
const customBtn2 = document.getElementById("custom-button2");

customBtn2.addEventListener("click", function() {
    realFileBtn2.click();
});

var loadFile = function(event) {
    selected_file.innerHTML = id_posti.value;
    console.log(id_posti.value);
};
var loadFile2 = function(event) {
    selected_file2.innerHTML = id_posti2.value;
    console.log(id_post2.value);
};


function hoverr11(){
    imagee1.src ='/static/images/icons/content/opposite/ic_import_contacts_24px.svg';
    }
    function without_hover11() {
        if (course_lecs.style.display=="block"){
            imagee1.src ='/static/images/icons/content/opposite/ic_import_contacts_24px.svg';
        }
        else
        {
           imagee1.src = '/static/images/icons/content/ic_import_contacts_24px.svg';
        }
    }

    function hoverr22() {
    imagee2.src ='/static/images/icons/content/opposite/Icon_doc_solid.svg' ;
    }
    function without_hover22() {
    if (reports.style.display=="block"){
        imagee2.src ='/static/images/icons/content/opposite/Icon_doc_solid.svg' ;
        imagee1.src = '/static/images/icons/content/ic_import_contacts_24px.svg';
        }
        else
        {
            imagee2.src = '/static/images/icons/content/Icon_doc_solid.svg';
        }
    }
    function hoverr33() {
    imagee3.src = '/static/images/icons/content/opposite/ic_group_24px.svg' ;
    }
    function without_hover33() {
        if (student_list.style.display=="block"){
            imagee3.src = '/static/images/icons/content/opposite/ic_group_24px.svg' ;
            imagee1.src = '/static/images/icons/content/ic_import_contacts_24px.svg';
        }
        else
        {
            imagee3.src = '/static/images/icons/content/ic_group_24px.svg';
        }

    }
