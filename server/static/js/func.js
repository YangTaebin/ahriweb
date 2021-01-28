function click_profile() {
  alert(getCookie("id"));
  location.href="/profile";
}
function setCookie(name, value, exp) {
  var data = new Date();
  data.setTime(data.getTime() + exp*60*60*1000);
  document.cookie = name + "=" + value + ";expires=" + data.toUTCString() + ";path=/";
}
function getCookie(cookie_name) {
  var x, y;
  var val = document.cookie.split(';');

  for (var i = 0; i < val.length; i++) {
    x = val[i].substr(0, val[i].indexOf('='));
    y = val[i].substr(val[i].indexOf('=') + 1);
    x = x.replace(/^\s+|\s+$/g, ''); // 앞과 뒤의 공백 제거하기
    if (x == cookie_name) {
      return unescape(y); // unescape로 디코딩 후 값 리턴
    }
  }
}
var deleteCookie = function(name) {
  document.cookie = name + '=; expires=Thu, 01 Jan 1999 00:00:10 GMT;';
}
function menu_over_1(){
  document.getElementById("yang").id = "sin";
}
function menu_out_1(){
  document.getElementById("sin").id = "yang";
}
function menu_over_2(){
  document.getElementById("tae").id = "sae";
}
function menu_out_2(){
  document.getElementById("sae").id = "tae";
}
function menu_over_3(){
  document.getElementById("bin").id = "ggi";
}
function menu_out_3(){
  document.getElementById("ggi").id = "bin";
}
function menu_over_4(){
  document.getElementById("byeong").id = "fuck";
}
function menu_out_4(){
  document.getElementById("fuck").id = "byeong";
}
