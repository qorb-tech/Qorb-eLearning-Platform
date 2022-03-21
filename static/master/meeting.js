meeting_btns = document.getElementById("meeting_btns").getElementsByTagName("button")[1];

chat = document.getElementById("chat");
attendance = document.getElementById("attendance");

function cht() {
    attendance.style.display="none";
    chat.style.display="block";
    console.log("ok");
}
function attend() {
    chat.style.display="none";
    attendance.style.display="block";
    meeting_btns.classList.remove("btn_active");
    console.log("ok");
}