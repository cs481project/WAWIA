// JavaScript source code
function myFunction(cl) {
    var els = document.getElementsByClassName(cl);
    for (var i = 0; i < els.length; ++i) {
        var s = els[i].style;
        s.display = s.display === 'none' ? 'block' : 'none';
    };
}


var divs = ["Start", "Stop", "Close"];
var visibleDivId = null;
function myFunction2(divId) {
    if (visibleDivId === divId) {
        //visibleDivId = null;
    } else {
        visibleDivId = divId;
    }
    hideNonVisibleDivs();
}
function hideNonVisibleDivs() {
    var i, divId, div;
    for (i = 0; i < divs.length; i++) {
        divId = divs[i];
        div = document.getElementById(divId);
        if (visibleDivId === divId) {
            div.style.display = "block";
        } else {
            div.style.display = "none";
        }
    }
}
$(document).ready(function () {
    var refresh = function () {
        $('.text7').load(location.href + ' .text7');
        $('#text6').load(location.href + ' #text6');

    }
    setInterval(refresh, 10000);
    refresh();
});