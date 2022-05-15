function activateTimer(val){
    const timerValue = val * 60;

           let time = localStorage.getItem('saved_timer');
           if(time == null) {
               const saved_timer = new Date().getTime() + (timerValue * 1000);
               localStorage.setItem('saved_timer', saved_timer);
               time = saved_timer;
            }

           console.log(time)
           const timerID = setInterval(() => {
               const now = new Date().getTime();
               const difference = time - now;
                // console.log(time)
                // consle.log(now)
               //    console.log("diff", difference)
               const totalSeconds = Math.floor(difference/1000);
               const minutes = Math.floor(totalSeconds / 60);
               const seconds = totalSeconds % 60;
               //    console.log('before')
            //    console.log(minutes, seconds)
               document.querySelector("#timerBox").innerText = 'Time Left: ' + minutes + ':' + ((seconds < 10) ? '0' + seconds : seconds);
            //    console.log('after')
            //    console.log(minutes, seconds)

               if(totalSeconds <= 0) {
                   clearInterval(timerID);
                   document.getElementById("quizSubmitForm").submit()
                   alert('Time over your choices have been submitted successfully!')
                   localStorage.removeItem('saved_timer');
               }
           }, 1000);
}
