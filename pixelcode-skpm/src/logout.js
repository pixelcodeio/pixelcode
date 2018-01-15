function onRun (context) {
  var sketch = context.api();
  var application = new sketch.Application(context);
  application.setSettingForKey('token', null);
  context.document.showMessage('Pixelcode: Successfully logged out!');
}

export default onRun;
