// JavaScript source code
function myFunction(cl) {
    var els = document.getElementsByClassName(cl);
    for (var i = 0; i < els.length; ++i) {
        var s = els[i].style;
        s.display = s.display === 'none' ? 'block' : 'none';
    };
}

/*
function myFunction(cl){
    var x = document.getElementById(cl);
    if (x.style.visibility === 'hidden') {
        x.style.visibility = 'visible';
    } else {
        x.style.visibility = 'hidden';
    }
}*/