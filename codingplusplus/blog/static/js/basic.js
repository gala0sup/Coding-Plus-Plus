window.addEventListener("scroll", ScrollBarProgress);


function ScrollBarProgress() {
  var winScroll = document.body.scrollTop || document.documentElement.scrollTop;
  var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
  var scrolled = (winScroll / height) * 100;

  document.getElementById("myBar").style.width = scrolled + "%";
}

// function HeaderShadow(){
//     if (scrolled > 0) {
//         document.getElementById('header').style.boxShadow = "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)";
//     } else {
//         document.getElementById('header').style.boxShadow = "0 0 0 1px rgba(0, 0, 0, 0.05)";
//     }
// }
