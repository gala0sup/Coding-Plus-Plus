window.addEventListener("scroll", ScrollBarProgress);
function ScrollBarProgress() {
  var winScroll = document.body.scrollTop || document.documentElement.scrollTop;
  var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
  var scrolled = (winScroll / height) * 100;

  document.getElementById("myBar").style.width = scrolled + "%";
}

var debugDiv = document.getElementById("debug_info");
var screen_dims = document.createTextNode(String((window).innerWidth)+"x"+String(window.innerHeight));
debugDiv.appendChild(screen_dims)

// w3school LOL 

var prevScrollpos = window.pageYOffset;
window.onscroll = function() {
  var curScrollPos = window.pageYOffset;
  if (prevScrollpos > curScrollPos) {
    document.getElementById("navbar").style.top = "0";
  } else {
    document.getElementById("navbar").style.top = String(-document.getElementById("navbar_to_hide").offsetHeight)+"px";
  }
  prevScrollpos = curScrollPos;

}