function ajaxRequest(url, pars, fun){
  var myAjax = new Ajax.Request(
    url,
    {
      method: 'post',
      parameters: pars,
      onComplete: fun,
      onFailure: serverErr,
      onException: serverErr
    }
  );
}

function serverErr() {
  $('error_box').style.display='block';
  $('error_box').innerHTML= '服务器异常，请稍候再重试！';
}

/**
 * 登录用户响应函数
 */
function loginUser(){
  userId = document.form1.userId.value;
  passwd = document.form1.passwd.value;
  
  errMsg = '';
  if(!isUserId(userId)) errMsg += '用户名不正确，只允许20位的数字或字母组合!';
  if(!isPasswd(passwd)) errMsg += '<br>密码不正确，只允许20位的数字或字母组合!';
  
  if(errMsg != "") {
    $('error_box').style.display='block';
    $('error_box').innerHTML= errMsg;
    return false;
  }
  passwd = SHA1(passwd);
  document.form1.passwd.value = passwd;
  
  var pars={
    userId : document.form1.userId.value,
    passwd : document.form1.passwd.value
  };
  ajaxRequest($('form1').action, pars, loginUserResponse);
  return false;
}

function loginUserResponse(response) {
  var result = JSON.parse(response.responseText);
  if (result.status == 0) {
    $('error_box').style.display='block';
    $('error_box').innerHTML= result.msg;
    document.form1.passwd.value = '';
  } else {
    $('error_box').style.display='block';
    $('error_box').innerHTML= result.msg;
    createCookie('userLoginId', result.userLoginId, 7);
    createCookie('userLoginAuth', result.userLoginAuth, 7);
    gotoDashBoard();
  }
}

function gotoDashBoard() {
  document.location.href='/';
}

/**
 * 0 注册用户响应函数
 * 1 重设密码响应函数
 * 2 修改密码响应函数
 * 3 修改用户信息响应函数
 */
function modifyUser(flag){
  responseFun = null;
  form = '';
  if(flag == 0 || flag == 1) {
    responseFun = regUserResponse;
    form = 'form1';
  } else if(flag == 2) {
    responseFun = changePasswdResponse;
    form = 'infoform';
  } else if(flag == 3) {
    responseFun = updateInfoResponse;
    form = 'form1';
  }

  userId = $(form).userId.value;
  email = '';
  if(flag != 2) {//功能不是修改密码时
    email = $(form).email.value;
  }
  passwd = $(form).passwd.value;
  repasswd = ''
  if(flag != 3) {//功能不是修改用户信息时
    repasswd = $(form).repasswd.value;
  }
  nrepasswd = ''
  if(flag == 2) {//功能是修改密码时
    nrepasswd = $(form).nrepasswd.value;
  }
  remark = ' '
  if(flag == 3) {//功能是修改用户信息时
    remark = $(form).remark.value;
  }
  
  errMsg = '';
  if(!isUserId(userId)) errMsg += '用户名不正确，只允许20位的数字或字母组合!';
  if(!isPasswd(passwd)) errMsg += '<br>密码不正确，只允许20位的数字或字母组合!';
  //功能不是修改密码时
  if(flag != 2 && !verifyAddress(email)) errMsg += '<br>邮箱格式不正确，例如: promingx@gmail.com!';
  //功能不是修改用户信息时
  if(flag != 3 && flag != 2 && passwd != repasswd) errMsg += '<br>确认密码不一致，请重新输入!';
  //功能是修改密码时
  if(flag == 2 && repasswd != nrepasswd) errMsg += '<br>确认密码不一致，请重新输入!';
  
  if(flag != 2 && errMsg != "") {
    $('error_box').style.display='block';
    $('error_box').innerHTML= errMsg;
    return false;
  } else if(flag == 2 && errMsg != "") {
    $('error_box1').style.display='block';
    $('error_box1').innerHTML= errMsg;
    return false;
  }
  
  passwd = SHA1(passwd);
  $(form).passwd.value = passwd;
  //功能不是修改用户信息时
  if(flag != 3 && flag != 2) {
    repasswd = passwd;
    $(form).repasswd.value = repasswd;
  }

  if(flag == 2) {//功能是修改密码时
    repasswd = SHA1(repasswd);
    $(form).repasswd.value = repasswd;
    nrepasswd = repasswd;
    $(form).nrepasswd.value = nrepasswd;
  }
  
  var pars={
    userId : userId,
    email : email,
    passwd : passwd,
    repasswd : repasswd,
    remark: remark
  };
  ajaxRequest($(form).action, pars, responseFun);
  return false;
}

function regUserResponse(response) {
  var result = JSON.parse(response.responseText);
  if (result.status == 0) {
    $('error_box').style.display='block';
    $('error_box').innerHTML= result.msg;
    document.form1.passwd.value = '';
    document.form1.repasswd.value = '';
  } else {
    $('error_box').style.display='block';
    $('error_box').innerHTML= result.msg + "<br>5s后将自动跳转到登录页面...";
    document.form1.passwd.value = '';
    document.form1.repasswd.value = '';
    window.setTimeout("gotoLogin()", 5000);
  }
}

function gotoLogin() {
  window.location.replace("/login");
}

/**
 * 修改用户信息响应函数
 */
function updateInfo(){
  userId = document.form1.userId.value;
  email = document.form1.email.value;
  passwd = document.form1.passwd.value;
  remark = document.form1.remark.value;
  
  errMsg = '';
  if(!isUserId(userId)) errMsg += '用户名不正确，只允许20位的数字或字母组合!';
  if(!isPasswd(passwd)) errMsg += '<br>密码不正确，只允许20位的数字或字母组合!';
  if(!verifyAddress(email)) errMsg += '<br>邮箱格式不正确，例如: promingx@gmail.com!';
  
  if(errMsg != "") {
    $('error_box').style.display='block';
    $('error_box').innerHTML= errMsg;
    return false;
  }
  
  passwd = SHA1(passwd);
  document.form1.passwd.value = passwd;
  
  var pars={
    userId : userId,
    email : email,
    passwd : passwd,
    remark: remark
  };
  ajaxRequest($('form1').action, pars, updateInfoResponse);
  return false;
}

function updateInfoResponse(response) {
  var result = JSON.parse(response.responseText);
  if (result.status == 0) {
    $('error_box').style.display='block';
    $('error_box').innerHTML= result.msg;
    document.form1.passwd.value = '';
  } else {
    $('error_box').style.display='block';
    $('error_box').innerHTML= result.msg;
    document.form1.passwd.value = '';
  }
}


function changePasswdResponse(response) {
  var result = JSON.parse(response.responseText);
  if (result.status == 0) {
    $('error_box1').style.display='block';
    $('error_box1').innerHTML= result.msg;
    document.infoform.passwd.value = '';
    document.infoform.repasswd.value = '';
  } else {
    $('error_box1').style.display='block';
    $('error_box1').innerHTML= result.msg;
    document.infoform.passwd.value = '';
    document.infoform.repasswd.value = '';
    document.infoform.nrepasswd.value = '';
  }
}

function updateInfoResponse(response) {
  var result = JSON.parse(response.responseText);
  if (result.status == 0) {
    $('error_box').style.display='block';
    $('error_box').innerHTML= result.msg;
    document.form1.passwd.value = '';
  } else {
    $('error_box').style.display='block';
    $('error_box').innerHTML= result.msg;
    document.form1.passwd.value = '';
  }
}

/**
 * 找回密码响应函数
 */
function forgotPasswd(){
  userId = document.form1.userId.value;
  email = document.form1.email.value;
  
  errMsg = '';
  if(!isUserId(userId)) errMsg += '用户名不正确，只允许20位的数字或字母组合!';
  if(!verifyAddress(email)) errMsg += '<br>邮箱格式不正确，例如: promingx@gmail.com!';
  
  if(errMsg != "") {
    $('error_box').style.display='block';
    $('error_box').innerHTML= errMsg;
    return false;
  }
  
  var pars={
    userId : document.form1.userId.value,
    email : document.form1.email.value
  };
  ajaxRequest($('form1').action, pars, forgotPasswdResponse);
  return false;
}

function forgotPasswdResponse(response) {
  var result = JSON.parse(response.responseText);
  if (result.status == 0) {
    $('error_box').style.display='block';
    $('error_box').innerHTML= result.msg;
  } else {
    $('error_box').style.display='block';
    $('error_box').innerHTML= result.msg;
  }
}

/**
 * 表单校验方法
 */
function isUserId(s)
{
  var patrn=/^[a-zA-Z]{1}([a-zA-Z0-9]|[._]){4,19}$/;
  if (!patrn.exec(s)) return false;
  return true;
}

function isPasswd(s)
{
  var patrn=/([a-zA-Z0-9]|[._ ]){1,20}$/;
  if (!patrn.exec(s)) return false;
  return true;
}

 function verifyAddress(s)
{ 
  var patrn = /^[a-zA-Z]([a-zA-Z0-9]*[-_.]?[a-zA-Z0-9]+)+@([\w-]+\.)+[a-zA-Z]{2,}$/;   
  if (!patrn.exec(s)) return false;
  return true;
}

function byId(id) {
  return document.getElementById(id);
}

/**
 * cookie读写函数
 */
function createCookie(key,value,days) {
  if (days) {
     var date = new Date();
     date.setTime(date.getTime()+(days*24*60*60*1000));
     var expires = "; expires="+date.toGMTString();
   }
   else var expires = "";
   document.cookie = key+"="+escape(value)+expires+"; path=/";
}

function readCookie(key) {
   var nameEQ = key + "=";
   var ca = document.cookie.split(';');
   for(var i=0;i < ca.length;i++) {
     var c = ca[i];
     while (c.charAt(0)==' ') c = c.substring(1,c.length);
     if (c.indexOf(nameEQ) == 0) return unescape(c.substring(nameEQ.length,c.length));
   }
   return null;
}

function eraseCookie(key) {
   createCookie(key,"",-1);
}

function showCookie(key) {
   alert(readCookie(key));
}


function addCookie(key,value,days) {
   if (readCookie(key) != null) {
     var oldvalue = readCookie(key);
     var newvalue = oldvalue+","+value;
   }
   else var newvalue = value;
   createCookie(key,newvalue,days);
}

function getHistory(key) {
   var sHistory = readCookie(key);
   if(sHistory) {
     var aHistroy = sHistory.split(",");
     for (x in aHistroy)
     {
         //do something ...
     }
   }
}
