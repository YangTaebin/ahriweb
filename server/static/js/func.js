function login_cont() {
  if(document.cookie != "") {
    var id = getCookie("id");
    var name = getCookie("name");
    document.getElementById('login_click').innerText = String(name)+" 님";
    document.getElementById('login_click').setAttribute('id','profile');
    document.getElementById('profile').setAttribute('onclick','click_profile()');
  }
}

function click_profile() {
  var id = getCookie("id");
  var name = getCookie("name");

  document.write('<form action="/profile" id="smb_form" method="post"><input type="hidden" id="id" name="id" value="'+ id +'"></form>');
  document.getElementById("smb_form").submit();
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
  document.getElementById("yang").id = "seong";
}
function menu_out_1(){
  document.getElementById("seong").id = "yang";
}
function menu_over_2(){
  document.getElementById("tae").id = "hyeok";
}
function menu_out_2(){
  document.getElementById("hyeok").id = "tae";
}
function menu_over_3(){
  document.getElementById("bin").id = "bao";
}
function menu_out_3(){
  document.getElementById("bao").id = "bin";
}
function menu_over_4(){
  document.getElementById("park").id = "bo";
}
function menu_out_4(){
  document.getElementById("bo").id = "park";
}

function submit_writing(){
  if(document.cookie==""){
    alert("로그인을 해주세요.")
    location.href="/"
    return 0
  }
  var writing_form = document.getElementById("writing");
  var name = document.createElement("input");
  name.type="hidden";
  console.log(getCookie("name"));
  name.value=getCookie("name");
  name.name="writer";
  writing_form.appendChild(name);
  writing_form.submit();
  console.log("완료")
}

function show_content(num){
  console.log(typeof(num));
  var show_content = document.createElement("form");
  show_content.method="GET";
  show_content.action="/show_content";
  show_content.id="show_content";
  var n = document.createElement("input");
  n.type="hidden";
  n.value = String(num);
  n.name = "N";
  show_content.appendChild(n);
  document.body.appendChild(show_content);
  show_content.submit();
}
function regis_sys(){
  id = getCookie("id");

  var les_sys = document.createElement("form");
  les_sys.method="POST";
  les_sys.action="/les_sys";
  les_sys.id="les_sys";
  var id_input = document.createElement("input");
  id_input.type="hidden";
  id_input.value = String(id);
  id_input.name = "id";
  les_sys.appendChild(id_input);
  document.body.appendChild(les_sys);
  les_sys.submit();
}
function quit(){
  id = getCookie("id");
  var les_sys = document.createElement("form");
  les_sys.method="POST";
  les_sys.action="/quit";
  var id_input = document.createElement("input");
  id_input.type="hidden";
  id_input.value = String(id);
  id_input.name = "id";
  les_sys.appendChild(id_input);
  document.body.appendChild(les_sys);
  les_sys.submit();
}
