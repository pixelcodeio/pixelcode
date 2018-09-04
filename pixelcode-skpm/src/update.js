import globals from './globals';

function onRun (context) {
  var sketch = context.api();
  var application = new sketch.Application(context);
  var contentsPath = context.scriptPath.stringByDeletingLastPathComponent().stringByDeletingLastPathComponent();
  var resourcesPath = contentsPath + '/Resources';
  var token = application.settingForKey('token');

  if (token == null) {
    context.document.showMessage('Pixelcode: No user logged in.');
    return;
  }

  var options = {'method': 'GET', headers: {'Authorization': 'Token ' + token}};
  fetch(globals.userProjectsRoute, options)
    .then(response => response.text())
    .then(text => {
      var responseJSON = JSON.parse(text);
      if (responseJSON.hasOwnProperty('detail')) {
        context.document.showMessage('Pixelcode: Failed to get projects.');
      } else {
        context.document.showMessage('Pixelcode: Successfully updated projects!');
        application.setSettingForKey('projects', text);
        var projectsStr = NSString.stringWithString(text);
        projectsStr.writeToFile_atomically_encoding_error(resourcesPath + '/projects.json', true, NSUTF8StringEncoding, null);
      }
    }).catch(error => {
      context.document.showMessage('Pixelcode: Failed to get projects.');
    });
}

export default onRun;
