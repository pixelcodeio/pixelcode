var selectedIndex = -1;
var projects = {};

$(document).ready(function () {
  fetch('../projects.json', {'method': 'GET'})
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
        updateHash('upload&projectHash=' + projects[selectedIndex].hashed);
        console.log(projects[selectedIndex]);
      });
    });
  $('#export').click(function () {
    if (selectedIndex > -1) {
      console.log(projects[selectedIndex]);
      console.log('Exporting');
      updateHash('upload&projectHash=' + projects[selectedIndex].hashed);
    }
  });
  $('#cancel').click(function () {
    updateHash('cancel');
  });
});

function updateHash (hash) {
    // We can send a simple command or a command with a parameter and value
    // You can extend this function to send multiple values. script.js will parse
    // all the values and expose them in the hash object so you can use them
    // new Date is there just to make sure the url is alwasy different
      window.location.hash = hash + '&date=' + new Date().getTime();
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
