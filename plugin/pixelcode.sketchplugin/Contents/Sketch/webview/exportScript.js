$(document).ready(function () {
  var options = {'method': 'GET'};
  fetch('./projects.json', options)
  .then(response => response.json())
  .then(json => {
    displayProjects(json);
    $('.project').click(function () {
      $('.project').removeClass('active');
      $(this).addClass('active');
    });
  });
});

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
  var imageHTML = '';
  if (image === null) {
    imageHTML = '<img style = "width: 58px; height: 102px">\n';
  } else {
    imageHTML = '<img src = "' + image + '">\n';
  }
  var html = '<div class = "project" id = project' + index + '>\n' +
             '<div class = "image">\n' +
             imageHTML +
             '</div>\n' +
             '<div class = "info">\n' +
             '<label class = "name">' + name + '</label>\n' +
             '<label class = "timestamp">Last updated ' + timestamp + ' ago</label>\n' +
             '</div>\n' +
             '</div>\n'
  return html;
}
