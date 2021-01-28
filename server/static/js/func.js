function click_profile() {
  getCookie("id");
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
