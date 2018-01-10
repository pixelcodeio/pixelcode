var selectedIndex = -1;
var projects = {};
var artboards = [];
var zip = null;

$(document).ready(function () {
  fetch('../../../../src/webview/projects.json', {'method': 'GET'})
    .then(response => response.json())
    .then(json => {
      console.log("Projects JSON is: " + json);
      projects = json;
      displayProjects(json);
      $('.project').click(function () {
        projectClicked($(this));
      });
      $('.project').dblclick(function () {
        projectClicked($(this));
        uploadProject();
        console.log(projects[selectedIndex]);
      });
    });
  fetch('../../../../src/webview/artboards.txt', {'method': 'GET'})
    .then(response => response.text())
    .then(text => {
      console.log(text);
      artboards = text.split(',');
      zip = new JSZip();
      artboards.forEach(function (artboard) {
        var folder = artboard + '/';
        zip.folder(folder);
        var svg = artboard + '.svg';
        var json = artboard + '.json';
        fetch('../../exports/' + artboard + '.svg', {'method': 'GET'})
          .then(response => response.text())
          .then(text => zip.file(folder + svg, text));
        fetch('../../exports/' + artboard + '.json', {'method': 'GET'})
          .then(response => response.text())
          .then(text => zip.file(folder + json, text));
      });
      console.log('ZIP:');
      console.log(zip);
    });
  $('#export').click(function () {
    if (selectedIndex > -1) {
      console.log(projects[selectedIndex]);
      // uploadProject();
      updateHash('upload&projectHash=' + projects[selectedIndex].hashed);
      window.location.href = '../html/uploadClose.html';
    }
  });
});

function updateHash (hash) {
    // We can send a simple command or a command with a parameter and value
    // You can extend this function to send multiple values. script.js will parse
    // all the values and expose them in the hash object so you can use them
    // new Date is there just to make sure the url is alwasy different
      window.location.hash = hash + '&date=' + new Date().getTime();
}

function uploadProject () {
  console.log('UPLOAD PROJECT CALLED');
  console.log(artboards);
  zip.generateAsync({type: 'blob'})
    .then(function (content) {
      console.log('CONTENT:');
      console.log(content);
      var projectHash = projects[selectedIndex].hashed;
      var options = {'method': 'POST', 'ContentType': 'application/zip', 'body': content};
      fetch('http://192.168.1.11:8000/api/project/' + projectHash + '/upload', options)
        .then(response => console.log(response));
    });
}

function projectClicked (project) {
  $('#export').css('color', 'white');
  $('.project').removeClass('active');
  project.addClass('active');
  selectedIndex = project.attr('index');
  console.log(selectedIndex);
}

function displayProjects (projects) {
  console.log(projects);
  var div = document.createElement('div');
  var divHTML = '';
  for (var i = 0; i < projects.length; i++) {
    divHTML += generateProjectHTML(projects[i], i);
  }
  div.innerHTML = divHTML;
  var projectsDiv = document.getElementById('projects');
  projectsDiv.append(div);
}

function generateProjectHTML (project, index) {
  var name = project.name;
  var timestamp = project.timestamp;
  var image = project.image;
  var html = '<div class = "project" index = ' + index + '>\n' +
             '<div class = "image" style = "background-image: url(' + image +
             '); background-size: 100%; overflow: hidden;">\n</div>\n' +
             '<div class = "info">\n' +
             '<label class = "name">' + name + '</label>\n' +
             '<label class = "timestamp">Last updated ' + timestamp +
             ' ago</label>\n</div>\n</div>\n'
  return html;
}
