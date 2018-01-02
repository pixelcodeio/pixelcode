window.onload = function () {
  console.log('In script');
  var loginBtn = document.getElementById('loginBtn');
  console.log(loginBtn);
  loginBtn.onclick = function () {
    console.log('Login button clicked');
    // var username = document.getElementById('username').value;
    // var password = document.getElementById('password').value;
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    // updateHash('login&username=' + username + '&password=' + password);
    var loggedIn = function (response) {
      console.log(response);
      if (response.authenticated) {
        console.log('LOGIN succeeded');
        updateHash('login&token=' + response.token);
        window.location.href = "./close.html";
      } else {
        console.log('LOGIN failed');
      }
    };
    getToken(username, password, loggedIn);
  };
};

function getToken (username, password, callback) {
  console.log('Getting token');
  var params = {'username': username, 'password': password};
  var request = formDataRequest('http://192.168.1.13:8000/api/auth', params, 'POST');
  request.onreadystatechange = function () {
    var jsonStr = request.responseText;
    var jsonData = JSON.parse(jsonStr);
    if (request.readyState === 4) {
      if (request.status === 200) {
        callback({'authenticated': true, 'token': jsonData.token});
        console.log('Succeeded getting token');
      } else {
        console.log('Failed getting token.');
        callback({ 'authenticated': false });
      }
    }
  };
}

function updateHash (hash) {
    //We can send a simple command or a command with a parameter and value
    //You can extend this function to send multiple values. script.js will parse
    //all the values and expose them in the hash object so you can use them
    //new Date is there just to make sure the url is alwasy different
      window.location.hash = hash+'&date=' +new Date().getTime();
}

function formDataRequest (path, params, method) {
  var formData = new FormData();
  for (var key in params) {
    formData.append(key, params[key]);
  }
  var request = new XMLHttpRequest();
  request.open(method, path);
  request.setRequestHeader('X-CSRFToken', '');
  request.send(formData);
  return request;
}
