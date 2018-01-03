var options = {'method': 'GET'};
var selectedIndex = -1;
var projects = {};

$(document).ready(function () {
  fetch('../projects.json', options)
    .then(response => response.json())
    .then(json => {
      projects = json;
      displayProjects(json);
      $('.project').click(function () {
        projectClicked($(this));
      });
      $('.project').dblclick(function () {
        projectClicked($(this));
        console.log(projects[selectedIndex]);
      });
    });
  $('#export').click(function () {
    if (selectedIndex > -1) {
      console.log(projects[selectedIndex]);
    }
  });
});

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
