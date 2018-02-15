// JavaScript source code
function myFunction(cl) {
    var els = document.getElementsByClassName(cl);
    for (var i = 0; i < els.length; ++i) {
        var s = els[i].style;
        s.display = s.display === 'none' ? 'block' : 'none';
    };
}
function myFunction2(cl1) {
    var els = document.getElementsByClassName(cl1);
    for (var i = 0; i < els.length; ++i) {
        var s = els[i].style;
        s.display = s.display === 'block' ? 'none' : 'block';
    };
}