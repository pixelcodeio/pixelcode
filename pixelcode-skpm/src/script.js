import globals from './globals';
import {createWebUI, createWebview, createWebViewChangeLocationDelegate, createWindow} from './webview/webview';
import WebUI from 'sketch-module-web-view';

function onRun (context) {
  var sketch = context.api();
  var app = NSApplication.sharedApplication();
  var layers = sketch.selectedDocument.selectedLayers;
  //var filepath = '/Users/Young/Documents/pixelcode/app/tests/';
  var filepath = globals.filepath;
  var webviewPath = globals.webviewPath;
  var application = new sketch.Application(context);

  // application.setSettingForKey('token', null);
  var token = application.settingForKey('token');
  if (token == null) {
    // createWebview('Log In', webviewPath + 'html/index.html', 520, 496);
    var window_ = createWindow(520, 496);
    var webview = createWebview(context, window_, webviewPath + 'html/index.html', 520, 496);
    createWebViewChangeLocationDelegate(application, context, window_, webview, null);
    NSApp.run();
    return;
  }

  if (application.settingForKey('projects') == null) {
    updateProjects(context);
  }

  context.document.showMessage('About to export');
  if (layers.isEmpty) {
    context.document.showMessage('PixelCode: No artboard selected.');
  } else {
    var artboards = [];
    var contentsPath = context.scriptPath.stringByDeletingLastPathComponent().stringByDeletingLastPathComponent();
    var exportsPath = contentsPath + '/Resources/exports/';
    console.log('Exports path is: ' + exportsPath);
    layers.iterate(function (layer) {
      if (layer.isArtboard) {
        // Add artboard name to list of artboards
        artboards.push(layer.name);
        var output = exportJSON(layer, exportsPath);

        var options = {
          'scales': '1',
          'formats': 'svg',
          'overwriting': 'true',
          'output': exportsPath
        };
        layer.export(options);
        layer.iterate(function (currentLayer) {
          renameLayers(currentLayer, output['originalNames']);
        });
        context.document.showMessage('Pixelcode: Export finished!');
      } else {
        context.document.showMessage('Pixelcode: No artboard selected.');
        return;
      }
    });
    // Create artboards.json
    var window_ = createWindow(560, 496);
    var webview = createWebview(context, window_, webviewPath + 'html/export.html', 560, 472);
    var info = {token: token, artboards: artboards};
    createWebViewChangeLocationDelegate(application, context, window_, webview, info);
    NSApp.run();
  }
}

function updateProjects (context) {
  var sketch = context.api();
  var application = new sketch.Application(context);
  var contentsPath = context.scriptPath.stringByDeletingLastPathComponent().stringByDeletingLastPathComponent();
  var webviewPath = globals.webviewPath;
  var token = application.settingForKey('token');

  if (token == null) {
    context.document.showMessage('Pixelcode: No user logged in.');
    return;
  }

  var options = {'method': 'GET', headers: {'Authorization': 'Token ' + token}};
  console.log('Token is: ' + token);
  fetch('http://0.0.0.0:8000/api/csrf/userprojects', options)
    .then(response => response.text())
    .then(text => {
      var responseJSON = JSON.parse(text);
      if (responseJSON.hasOwnProperty('detail')) {
        console.log('Error to query csrf userprojects');
        console.log(text);
        context.document.showMessage('Pixelcode: Failed to get projects.');
      } else {
        application.setSettingForKey('projects', text);
        var projectsStr = NSString.stringWithString(text);
        projectsStr.writeToFile_atomically_encoding_error(contentsPath + '/Resources/projects.json', true, NSUTF8StringEncoding, null);
      }
    }).catch(error => {
      console.log('Failed to get projects, in catch');
      console.log(error);
      context.document.showMessage('Pixelcode: Failed to get projects.');
    });
}

function renameLayers (layer, originalNames) {
  layer.name = originalNames[layer.id];
  if (layer.isGroup) {
    layer.iterate(function (subLayer) {
      renameLayers(subLayer, originalNames);
    });
  }
}

function exportJSON (artboard, filepath) {
  var layerArray = [];
  var ret = { 'layerNames': [], 'dictList': [], 'originalNames': {} };

  artboard.iterate(function (layer) {
    if (layer.isImage) {
      var options = {
        'scales': '1',
        'formats': 'png',
        'overwriting': 'true',
        'output': filepath
      };
      layer.export(options);
    }

    var output = checkFormatting(layer, ret['layerNames'], ret['originalNames']);
    ret = output;

    for (var i = 0; i < ret['dictList'].length; i++) {
      layerArray.push(ret['dictList'][i]);
    }
  });

  // Create JSON and save to file
  var artboardName = artboard.name;
  var jsonObj = { layers: layerArray };
  var file = NSString.stringWithString(JSON.stringify(jsonObj, null, '\t'));
  console.log('JSON exported to ' + filepath + artboardName + '.json');
  file.writeToFile_atomically_encoding_error(filepath + artboardName + '.json', true, NSUTF8StringEncoding, null);
  return ret;
}

// Account for sublayers in checking formatting
function checkFormatting (layer, layerNames, originalNames) {
  var ret = {
    'layerNames': layerNames,
    'dictList': [],
    'originalNames': originalNames
  };
  var stack = [layer];

  while (stack.length >= 1) {
    var currentLayer = stack.pop();
    var originalName = String(currentLayer.name);
    ret['originalNames'][currentLayer.id] = originalName;

    var layerName = String(currentLayer.name.replace(/\s+/, ''));
    layerName = lowerCaseFirstChar(layerName);

    if (arrayContains(layerName, ret['layerNames'])) {
      var name = layerName;
      var counter = 1;
      while (arrayContains(name, ret['layerNames'])) {
        name = layerName + counter;
        counter++;
      }
      layerName = name;
    }

    currentLayer.name = layerName;

    var currentDict = {};
    currentDict['originalName'] = originalName;
    currentDict['name'] = layerName;
    currentDict['x'] = String(currentLayer.frame.x);
    currentDict['y'] = String(currentLayer.frame.y);
    currentDict['height'] = String(currentLayer.frame.height);
    currentDict['width'] = String(currentLayer.frame.width);
    if (currentLayer.isText) {
      currentDict['text_align'] = String(currentLayer.alignment);
    }

    if (currentLayer.container.isArtboard) {
      currentDict['abs_x'] = currentDict['x'];
      currentDict['abs_y'] = currentDict['y'];
    } else {
      var absx = String(currentLayer.frame.x + currentLayer.container.frame.x);
      var absy = String(currentLayer.frame.y + currentLayer.container.frame.y);
      currentDict['abs_x'] = absx;
      currentDict['abs_y'] = absy;
    }

    ret['layerNames'].push(layerName);
    ret['dictList'].push(currentDict);

    if (currentLayer.isGroup) {
      currentLayer.iterate(function (subLayer) {
        stack.push(subLayer);
      });
    }
  }
  return ret;
}

function hasWhiteSpace (s) {
  return s.indexOf(' ') >= 0;
}

function arrayContains (needle, arrhaystack) {
  return (arrhaystack.indexOf(needle) > -1);
}

function lowerCaseFirstChar (string) {
  return string.charAt(0).toLowerCase() + string.slice(1);
}

// function getProjects (token) {
//   var headers = {'Authorization': 'Token ' + token};
//   var dataStr = request('http://192.168.1.11:8000/api/userprojects', headers, 'GET');
//   return dataStr;
// }

function createProjectsJSON (projects) {
  var filePath = '/Users/kevinchan/Documents/pixelcode/plugin/pixelcode.sketchplugin/Contents/Sketch/webview/';
  var file = NSString.stringWithString(JSON.stringify(projects, null, '\t'));
  // [file writeToFile:filePath+'projects.json' atomically:true encoding:NSUTF8StringEncoding error:null];
  file.writeToFile_atomically_encoding_error(filePath + 'projects.json', true, NSUTF8StringEncoding, null);
}

export default onRun;
