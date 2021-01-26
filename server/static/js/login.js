document.getElementById('login_click').onclick = function() {
  Kakao.init('734a58ba8d1de6eb1485389492741493');
  Kakao.Auth.login({
    success:(auth)=>{
      console.log("로그인 완료",auth)
    },
    fail:(err)=>{
      console.error(err)
    }
  });
  Kakao.API.request({
    url: '/v2/user/me',
    success: function(response) {
      console.log(response['id'])
      document.getElementById('login_click').innerText = String(response['properties']['nickname'])+" 님";
      document.getElementById('login_click').setAttribute('id','profile');
      $.ajax({
        type: 'POST',
        url: "/log_res",
        data: JSON.stringify(response['id']),
        success: function(result) {
          if (result) {
            console.log("등록 완료");
          } else {
            console.log("잠시 후에 시도해주세요.");
          }
        }
      });
    },
    fail: function(error) {
      console.log(error);
    }
  });
};
