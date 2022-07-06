const APP_ID = 'ea8afd3db07a44eeb9878e48c8295ea6'
const TOKEN = sessionStorage.getItem('token')
const CHANNEL = sessionStorage.getItem('room')




let UID = sessionStorage.getItem('UID')
let NAME = sessionStorage.getItem('name')

const client = AgoraRTC.createClient({mode:'rtc', codec:'vp8'})

let localTracks = []
let remoteUsers = {}

const CHANNEL_NAME = sessionStorage.getItem('ch_name')

let joinAndDisplayLocalStream = async () => {
    document.getElementById('room-name').innerText = CHANNEL_NAME
    document.getElementById('chat_pop_up').href = "https://qorb.tech/chat/" + CHANNEL_NAME
    client.on('user-published', handleUserJoined)
    client.on('user-left', handleUserLeft)

    try{
        UID = await client.join(APP_ID, CHANNEL, TOKEN, UID)
    }catch(error){
        console.error(error)
        window.open('/', '_self')
    }

    localTracks = await AgoraRTC.createMicrophoneAndCameraTracks({})

    let member = await createMember()

    let player = `<div  class="video-container" id="user_container_${UID}">
                     <div class="video-player" id="user-${UID}"></div>
                     <div class="username-wrapper"><span class="user-name">${member.name}</span></div>
                  </div>`

    document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)

    localTracks[1].play(`user-${UID}`)
    await client.publish([localTracks[0], localTracks[1]])
    



}


// Capture , resize to  48 * 48 and send data every 10 sec.
let myImageData=[];
let ok = true;
function capture_send_data() {
    var c = document.querySelector("canvas");
    var ctx = c.getContext("2d");
    var imgData = localTracks[1].getCurrentFrameData();

    ctx.putImageData(imgData, 0, 0);
    var dataURL = c.toDataURL();

    var image = new Image();
    image.src = dataURL;


    var c2 = document.getElementById("canvas2");
    var ctx2 = c2.getContext("2d");
    ctx2.drawImage(c,0, 0, 48, 48);

    myImageData = ctx2.getImageData(0, 0, 48, 48);


    var normalArray = Array.from(myImageData.data);
    
    // if(ok){
    //     const start_time = (new Date().getMinutes());
    //     localStorage.setItem('start_time', start_time);
    //     ok = false;
    // }


    // let time =  (new Date().getMinutes()) - localStorage.getItem('start_time');
    let time = (new Date().getMinutes());
   

    var data = {
        "frame": normalArray,
        "time": time,
        "meeting_name":CHANNEL
    }

    // console.log(localTracks[1].getCurrentFrameData())
    var csrftoken = getCookie('csrftoken');


    $.ajax({
        headers: {'Access-Control-Allow-Origin': '*' ,
        "Content-type": "application/json"
    },
        
        type: 'POST',
        url: 'https://api.qorb.tech/sendphoto/',
        contentType: "application/json",  
        dataType: 'json', 
        data: JSON.stringify(data),
        success: function(data){
            console.log(data);
            myImageData=[];

        }
    });
};

setInterval(capture_send_data, 10000);


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



var sliderusers = [];
let handleUserJoined = async (user, mediaType) => {
    remoteUsers[user.uid] = user
    await client.subscribe(user, mediaType)

    if (mediaType === 'video'){
        let player = document.getElementById(`user_container_${user.uid}`)
        if (player != null){
            player.remove()
        }

        let member = await getMember(user)

        player = `<div  class="video-container" id="user_container_${user.uid}">
            <div class="video-player" id="user_${user.uid}"></div>
            <div class="username-wrapper"><span class="user-name">${member.name}</span></div>
        </div>`

        document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)
        user.videoTrack.play(`user_${user.uid}`)
       sliderusers.push(UID);
        console.log("Array11"+sliderusers)
    }

    if (mediaType === 'audio'){
        user.audioTrack.play()
    }

    var array_user= document.getElementsByClassName("video-container");
var currentSlide,current_uid,current_member;
console.log(array_user)

for (var i = 0; i < array_user.length; i++) {

    array_user[i].onclick = function () {
        removeAllActive()
        this.classList.add("active");

      currentSlide = this.getAttribute('id');
      current_uid=parseInt(currentSlide.replace(/[^0-9]/g,''))
      current_member =this.querySelector(".user-name").innerHTML

      console.log(currentSlide);


    }

  }

  function removeAllActive() {
   for (var i = 0; i < array_user.length; i++) {
        array_user[i].classList.remove('active');
    }
  }
}



let handleUserLeft = async (user) => {
    delete remoteUsers[user.uid]
    document.getElementById(`user_${user.uid}`).remove()
}

let leaveAndRemoveLocalStream = async () => {
    for (let i=0; localTracks.length > i; i++){
        localTracks[i].stop()
        localTracks[i].close()
    }

    await client.leave()
    //This is somewhat of an issue because if user leaves without actaull pressing leave button, it will not trigger
    deleteMember()
    window.open('/', '_self')
}

 //var arr=[];
let toggleCamera = async (e) => {
    console.log(UID)
    // arr.push(UID)
    // console.log("arr"+arr)

    console.log(`user-${UID}`)
    console.log('TOGGLE CAMERA TRIGGERED')
    var user_vedio = document.getElementById(`user-${UID}`)
    var img= document.getElementById(`user_container_${UID}`)

    var camera_btn = document.getElementById("camera-btn")
    var camera_off = camera_btn.getElementsByClassName("activee")
    if(localTracks[1].muted){
        await localTracks[1].setMuted(false)
     //   user_vedio.style.opacity="1";
        // user_vedio.style.display="block";

        //e.target.style.backgroundColor = 'blue'
        camera_off[0].style.display="none";

    }else{
        await localTracks[1].setMuted(true)
        console.log(user_vedio);
      //  user_vedio.style.opacity="0";
        // img.style.background="url(../media/student_profile_images/waled/121.jpg)"
        // img.style.backgroundSize="cover"
      //  e.target.style.backgroundColor = 'rgb(255, 80, 80, 1)'
        camera_off[0].style.display="block";
    }
}

let toggleMic = async (e) => {
    console.log('TOGGLE MIC TRIGGERED')
    if(localTracks[0].muted){
        await localTracks[0].setMuted(false)
        e.target.style.backgroundColor = '#fff'
    }else{
        await localTracks[0].setMuted(true)

        e.target.style.backgroundColor = 'rgb(255, 80, 80, 1)'
    }
}


var array_user= document.getElementsByClassName("video-container");
var currentSlide,current_uid,current_member;
console.log(array_user)

for (var i = 0; i < array_user.length; i++) {

    array_user[i].onclick = function () {

      currentSlide = this.getAttribute('id');
      current_uid= currentSlide.replace(/[^0-9]/g,'')
      current_member =this.querySelector(".user-name").innerHTML

  let zoom_user = `<div  class="zoon_person" id="${currentSlide}">
    <div class="video-player" id="user-${currentSlide}"></div>
    <div class="username-wrapper"><span class="user-name">${current_member}</span></div>
 </div>`

document.getElementById('zoon_person').insertAdjacentHTML('beforeend', zoom_user)
      console.log(currentSlide);

     // removeAllActive();
    }
  }

let createMember = async () => {
    let response = await fetch('/create_member/', {
        method:'POST',
        headers: {
            'Content-Type':'application/json'
        },
        body:JSON.stringify({'name':NAME, 'room_name':CHANNEL, 'UID':UID})
    })
    let member = await response.json()
    return member
}


let getMember = async (user) => {
    let response = await fetch(`/get_member/?UID=${user.uid}&room_name=${CHANNEL}`)
    let member = await response.json()
    return member
}

let deleteMember = async () => {
    let response = await fetch('/delete_member/', {
        method:'POST',
        headers: {
            'Content-Type':'application/json'
        },
        body:JSON.stringify({'name':NAME, 'room_name':CHANNEL, 'UID':UID})
    })
    let member = await response.json()
}

window.addEventListener("beforeunload",deleteMember);

joinAndDisplayLocalStream()

document.getElementById('leave-btn').addEventListener('click', leaveAndRemoveLocalStream)
document.getElementById('camera-btn').addEventListener('click', toggleCamera)
document.getElementById('mic-btn').addEventListener('click', toggleMic)


