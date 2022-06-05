
var q_nums = Array.from(document.querySelectorAll('.lkj'));
var q_nums_count = q_nums.length;
var current_qestion = 1;


var nextButton = document.getElementById('next');
var prevButton = document.getElementById('prev');


nextButton.onclick = nextquestion;
prevButton.onclick = prevquestion;

var nums_q = document.getElementById('nums_q');
var num_q = Array.from(document.querySelectorAll('#nums_q div'));

for (var i = 1; i <= q_nums_count; i++) {
    num_q[i-1].setAttribute('data-index', i);
  }
// Loop Through All nums-question Items
for (var i = 0; i < num_q.length; i++) {
    num_q[i].onclick = function () {
    current_qestion = parseInt(this.getAttribute('data-index'));
    theChecker();
  }
}

theChecker();

function nextquestion() {
  if (current_qestion == q_nums_count) {
    return false;
  } else {
    current_qestion++;
    theChecker();
  }
}
function prevquestion() {
  if (current_qestion == 1){
    return false;
  } else {
    current_qestion--;
    theChecker();
  }
}

function theChecker() {

  removeAllActive();

  q_nums[current_qestion - 1].classList.add('active1');

  nums_q.children[current_qestion - 1].classList.add('active2');
}

function removeAllActive() {
  // Loop Through q_nums
  q_nums.forEach(function (item) {
    item.classList.remove('active1');
  });
  // Loop Through nums
  num_q.forEach(function (bullet) {
   bullet.classList.remove('active2');
  });

}
