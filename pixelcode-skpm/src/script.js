import globals from './globals';
import {createWebview, createWebViewChangeLocationDelegate, createWindow} from './webview/webview';

function onRun (context) {
  var sketch = context.api();
  var app = NSApplication.sharedApplication();
  var layers = sketch.selectedDocument.selectedLayers;
  var contentsPath = context.scriptPath.stringByDeletingLastPathComponent().stringByDeletingLastPathComponent();
  var resourcesPath = contentsPath + '/Resources';
  var application = new sketch.Application(context);

  application.setSettingForKey('token', null);
  var token = application.settingForKey('token');
  if (token == null) {
    // Open Login window
    var window_ = createWindow(520, 496);
    var webview = createWebview(context, window_, resourcesPath + '/html/index.html', 520, 496);
    createWebViewChangeLocationDelegate(application, context, window_, webview, null);
    NSApp.run();
    return;
  }

  if (application.settingForKey('projects') == null) {
    updateProjects(context);
  }

  if (layers.isEmpty) {
    context.document.showMessage('PixelCode: No artboard selected.');
  } else {
    var artboards = [];
    var exportsPath = resourcesPath + '/exports/';
    console.log('Exports path is: ' + exportsPath);
    layers.iterate(function (layer) {
      if (layer.isArtboard) {
        // Add artboard name to list of artboards
        artboards.push(layer.name);
        var output = exportJSON(layer, exportsPath);

        var svgOptions = {
          'scales': '1',
          'formats': 'svg',
          'overwriting': 'true',
          'output': exportsPath
        };
        layer.export(svgOptions);

        var pngOptions = {
          'scales': '3',
          'formats': 'png',
          'overwriting': 'true',
          'output': exportsPath
        };
        layer.export(pngOptions);

        layer.iterate(function (currentLayer) {
          renameLayers(currentLayer, output['originalNames']);
        });
      } else {
        context.document.showMessage('Pixelcode: No artboard selected.');
        return;
      }
    });

    // Open Export to Projects window
    var window_ = createWindow(560, 496);
    var webview = createWebview(context, window_, resourcesPath + '/html/export.html', 560, 472);
    var info = {token: token, artboards: artboards};
    createWebViewChangeLocationDelegate(application, context, window_, webview, info);
    NSApp.run();
  }
}

function updateProjects (context) {
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
  console.log('Token is: ' + token);
  fetch(globals.userProjectsRoute, options)
    .then(response => response.text())
    .then(text => {
      var responseJSON = JSON.parse(text);
      if (responseJSON.hasOwnProperty('detail')) {
        context.document.showMessage('Pixelcode: Failed to get projects.');
      } else {
        application.setSettingForKey('projects', text);
        var projectsStr = NSString.stringWithString(text);
        projectsStr.writeToFile_atomically_encoding_error(resourcesPath + '/projects.json', true, NSUTF8StringEncoding, null);
      }
    }).catch(error => {
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
    exportImages(layer, filepath);

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

function exportImages (layer, filepath) {
  var options = {
    'scales': '1',
    'formats': 'png',
    'overwriting': 'true',
    'output': filepath
  };
  if (layer.isImage) {
    layer.export(options);
  } else if (layer.isGroup) {
    layer.iterate(function (sublayer) {
      exportImages(sublayer, filepath);
    });
  }
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

export default onRun;
