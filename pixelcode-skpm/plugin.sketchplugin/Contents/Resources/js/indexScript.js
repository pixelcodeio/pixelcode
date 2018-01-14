var getTokenRoute = '';

window.onload = function () {
  fetch('../routes.js', {method: 'GET'})
    .then(response => response.json())
    .then(json => {
      getTokenRoute = json.getTokenRoute;
    }).catch(error => console.log('Error with trying to log in'));
  var loginBtn = document.getElementById('loginBtn');
  loginBtn.onclick = function () {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    getToken(username, password, loggedIn);
  };
};

function loggedIn (response) {
  if (response.authenticated) {
    updateHash('login&token=' + response.token);
  } else {
    $('#username').css('border-color', 'red');
    $('#password').css('border-color', 'red');
  }
}

function getToken (username, password, callback) {
  console.log('Getting token');
  var params = {'username': username, 'password': password};
  var options = {method: 'POST', body: JSON.stringify(params), headers: {'Content-Type': 'application/json'}};
  fetch(getTokenRoute, options)
    .then(response => response.text())
    .then(text => JSON.parse(text))
    .then(json => callback({'authenticated': true, 'token': json.token}))
    .catch(error => callback({'authenticated': false}))
}

function updateHash (hash) {
  window.location.hash = hash+'&date=' +new Date().getTime();
}
