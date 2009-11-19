function checkLoginUser(){
  userId = document.form1.userId.value;
  passwd = document.form1.passwd.value;
  
  errMsg = '';
  if(!isUserId(userId)) errMsg += '用户名不正确，只允许20位的数字或字母组合';
  if(!isPasswd(passwd)) errMsg += '\n密码不正确，只允许20位的数字或字母组合';
  
  if(errMsg != "") {
    //byId("error").style.display='block';
    //byId("errMsg").value='rkk';
    alert(errMsg);
    return false;
  }
  
  passwd = SHA1(passwd);
  document.form1.passwd.value = passwd;
  return true;
}

function checkRegUser(){
  userId = document.form1.userId.value;
  email = document.form1.email.value;
  passwd = document.form1.passwd.value;
  repasswd = document.form1.repasswd.value;
  
  errMsg = '';
  if(!isUserId(userId)) errMsg += '用户名不正确，只允许20位的数字或字母组合';
  if(!isPasswd(passwd)) errMsg += '\n密码不正确，只允许20位的数字或字母组合';
  if(!verifyAddress(email)) errMsg += '\n邮箱格式不正确，例如: promingx@gmail.com';
  if(passwd != repasswd) errMsg += '\n确认密码不一致，请重新输入';
  
  if(errMsg != "") {
    //byId("error").style.display='block';
    //byId("errMsg").value='rkk';
    alert(errMsg);
    return false;
  }
  
  passwd = SHA1(passwd);
  document.form1.passwd.value = passwd;
  document.form1.repasswd.value = passwd;
  return true;
}

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

