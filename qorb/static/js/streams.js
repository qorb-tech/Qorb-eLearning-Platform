
const APP_ID = 'ea8afd3db07a44eeb9878e48c8295ea6'
const TOKEN = sessionStorage.getItem('token')
const CHANNEL = sessionStorage.getItem('room')
let UID = sessionStorage.getItem('UID')

let NAME = sessionStorage.getItem('name')

const client = AgoraRTC.createClient({mode:'rtc', codec:'vp8'})

let localTracks = []
let remoteUsers = {}

// let c = document.getElementById("myCanvas");

let joinAndDisplayLocalStream = async () => {
    document.getElementById('room-name').innerText = CHANNEL

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
    //console.log("TEST3"+localTracks[1]);
    
    //console.log(localTracks[1].getCurrentFrameData());
    
    // var c = document.getElementById("myCanvas");
    // var ctx = c.getContext("2d");
    // var imgData = localTracks[1].getCurrentFrameData();
    
    // console.log(imgData);
    //ctx.putImageData(imgData, 1, 2);
    // let myImageData = ctx.createImageData(120, 120);
    // ctx.putImageData(imgData, 1, 2);
    //var dataURL = c.toDataURL();
    // console.log(myImageData);

    
}

// function convertCanvasToImage() {
//     let canvas = document.getElementById("myCanvas");
//     let image = new Image();
//     image.src = canvas.toDataURL();
//     return image;
//   }

// let pnGImage;
// function cap(){
//     var ctx = c.getContext("2d");
//     var imgData = localTracks[1].getCurrentFrameData();
//     let myImageData = ctx.createImageData(120, 120);
//     ctx.putImageData(myImageData, 1, 2);
//     console.log(myImageData);
//     ctx.putImageData(imgData, 1, 2);


//     pnGImage = convertCanvasToImage();
//     document.body.appendChild(pnGImage);
//     console.log(pnGImage.src);

//     // let myImageData = ctx.createImageData(120, 120);
//     // ctx.putImageData(myImageData, 1, 2);
    

// }



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
 
    
        // var html = document.getElementById(`user_container_${current_uid}`).innerHTML;
        // var clone = document.getElementById('zoon_person');
        // clone.innerHTML = html;
        
        
        //document.getElementById('clones').appendChild(clone);
//   let zoom_user = `<div  class="zoon_person" id="${currentSlide}">
//     <div class="video-container" id="user_container_${current_uid}"></div>
//     <div class="username-wrapper"><span class="user-name">${current_member}</span></div>
//  </div>`

// document.getElementById('zoon_person').insertAdjacentHTML('beforeend', zoom_user)
      console.log(currentSlide);
     
    
    }
    
  }

  function removeAllActive() {
   for (var i = 0; i < array_user.length; i++) {
        array_user[i].classList.remove('active');
    }
  }
}

// var volume_now=0;
// var user_speak_now;
// let counter=0;
// client.enableAudioVolumeIndicator();
// client.on("volume-indicator", volumes => {
//   volumes.forEach((volume, index) => {
//     // console.log(`${index} UID ${volume.uid} Level ${volume.level}`);
//     if(volume.level >= volume_now){
//         volume_now=volume.level;
//         user_speak_now=volume.uid;
//         counter++;
//         console.log(user_speak_now);
//     }
//     console.log(counter);
//     if(counter>=5){
//         volume_now=0;
//         counter=0;
//     }

//   });
// })


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
//   var zoom_users = document.getElementsByClassName("zoon_person")
//   function removeAllActive() {
//       for(var i=0; i<zoom_users.length ; i++){
//         zoom_users[i].classList.remove('zoon_person');
//       }; 
//   }
  
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
// document.getElementById('cap-btn').addEventListener('click', cap)

