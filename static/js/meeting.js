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


/*************meeting***************/
meting_full = document.getElementById("meting_full");
all_chat = document.getElementById("all_chat");

function toggle_chat() {
    if(all_chat.style.display != "none"){
        all_chat.style.display ="none";
        meting_full.style.display ="block";
    }
    else{
        meting_full.style.display ="flex";
        all_chat.style.display ="block";

    }

}
var video_streams = document.getElementById("video-streams")
function toggle_screen(){
    if(video_streams.style.display=="flex"){
        video_streams.style.display ="none";
    }
    else{
        video_streams.style.display ="flex";
    }
}
