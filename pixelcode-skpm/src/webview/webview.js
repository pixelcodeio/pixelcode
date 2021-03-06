import globals from '../globals';
import {MochaJSDelegate} from './MochaJSDelegate';

export function createWebViewChangeLocationDelegate (application, context, window_, webView, info) {
  /**
   * Create a Delegate class and register it
   */
  var className = 'MochaJSDelegate_DynamicClass_SymbolUI_WebviewRedirectDelegate' + NSUUID.UUID().UUIDString();
  var delegateClassDesc = MOClassDescription.allocateDescriptionForClassWithName_superclass_(className, NSObject);
  delegateClassDesc.registerClass();

  /**
   * Register the 'event' to respond to and specify the callback function
   */
  var windowObject = webView.windowScriptObject();
  var changeLocationEventSelector = NSSelectorFromString('webView:didChangeLocationWithinPageForFrame:');
  delegateClassDesc.addInstanceMethodWithSelector_function_(
    // The 'event' - the WebView is about to redirect soon
    NSSelectorFromString('webView:didChangeLocationWithinPageForFrame:'),

    // The 'listener' - a callback function to fire
    function(webView, webFrame) {
      window_.close();
      var locationHash = windowObject.evaluateWebScript('window.location.hash');
      //The hash object exposes commands and parameters
      var hash = parseHash(locationHash);
      if (hash.hasOwnProperty('token')) {
        var token = hash['token'];
        context.document.showMessage('Pixelcode: Login successful!');
        application.setSettingForKey('token', token);
      } else if (hash.hasOwnProperty('projectHash')) {
        var projectHash = hash['projectHash'];
        uploadToProject(context, projectHash, info.token, info.artboards, info.assetNames);
        context.document.showMessage('Pixelcode: Uploaded to project!');
      }
    }
  );

  // Associate the new delegate to the WebView we already created
  webView.setFrameLoadDelegate_(
    NSClassFromString(className).new()
  );
};

function uploadArtboardToProject (context, projectHash, token, artboard) {
  var contentsPath = context.scriptPath.stringByDeletingLastPathComponent().stringByDeletingLastPathComponent();
  var exportsPath = contentsPath + '/Resources/exports/';
  var jsonData = NSData.dataWithContentsOfFile_options_error(exportsPath + artboard + '.json', NSDataReadingUncached, null);
  var jsonContents = String(jsonData.base64EncodedStringWithOptions(0));
  var svgData = NSData.dataWithContentsOfFile_options_error(exportsPath + artboard + '.svg', NSDataReadingUncached, null);
  var svgContents = String(svgData.base64EncodedStringWithOptions(0));
  var pngData = NSData.dataWithContentsOfFile_options_error(exportsPath + artboard + '@3x.png', NSDataReadingUncached, null);
  var pngContents = String(pngData.base64EncodedStringWithOptions(0));
  var body = JSON.stringify({'asset_name': artboard, 'json': jsonContents, 'svg': svgContents, 'png': pngContents});
  var options = {
    method: 'PUT',
    body: body,
    headers: {
      'Authorization': 'Token ' + token,
      'Content-Type': 'application/json'
    }
  };
  var uploadUrl = globals.uploadToProjectRoute + projectHash + '/upload';
  fetch(uploadUrl, options)
    .then(response => response.text())
    .then(text => {
      console.log(text);
      context.document.showMessage('Pixelcode: Uploaded to Project!');
    }).catch(error => {
       context.document.showMessage('Pixelcode: Failed to upload to project.');
       console.log(error);
    });
}

function uploadAssetsToProejct (context, projectHash, token, assetNames) {
  var contentsPath = context.scriptPath.stringByDeletingLastPathComponent().stringByDeletingLastPathComponent();
  var exportsPath = contentsPath + '/Resources/exports/';
  var assetDict = {};
  for (var i = 0; i < assetNames.length; i++) {
    var assetName = String(assetNames[i]);
    var pngData = NSData.dataWithContentsOfFile_options_error(exportsPath + assetName + '.png', NSDataReadingUncached, null);
    var pngContents = String(pngData.base64EncodedStringWithOptions(0));
    assetDict[assetName] = pngContents;
  }
  var options = {};
  var uploadURL = '';
  fetch(uploadURL, options)
    .then(response => response.text())
    .then(text => context.document.showMessage('Pixelcode: Uploaded assets.'))
    .catch(error => context.document.showMessage('Pixelcode: Failed to upload asset'))
}

function uploadToProject (context, projectHash, token, artboards, assetNames) {
  for (var i = 0; i < artboards.length; i++) {
    var artboard = String(artboards[i]);
    uploadArtboardToProject(context, projectHash, token, artboard);
  }
  uploadAssetsToProject(context, projectHash, token, assetNames);
}

export function createWindow(width, height) {
  var window_ = NSWindow.alloc().init();
  window_.setFrame_display(NSMakeRect(0, 0, width, height), true);
  window_.setStyleMask(NSTitledWindowMask | NSClosableWindowMask);
  window_.center();
  window_.makeKeyAndOrderFront_(window_);
  return window_;
}

export function createWebview(context, window_, htmlPath, width, height) {
  // create frame for loading content in
  var webviewFrame = NSMakeRect(0, 0, width, height);

  var requestUrl = NSURL.fileURLWithPath(htmlPath);
  var urlRequest = NSMutableURLRequest.requestWithURL(requestUrl);

  // Create the WebView, frame, and set content
  var webView = WebView.new();
  webView.initWithFrame(webviewFrame);
  webView.mainFrame().loadRequest(urlRequest);
  window_.contentView().addSubview(webView);

  return webView;
}

function parseHash (aURL) {
  var vars = {};
  var hashes = aURL.slice(aURL.indexOf('#') + 1).split('&');
  for (var i = 0; i < hashes.length; i++) {
    var hash = hashes[i].split('=');
    if (hash.length > 1) {
      vars[hash[0].toString()] = hash[1];
    } else {
      vars[hash[0].toString()] = null;
    }
  }
  return vars;
}
