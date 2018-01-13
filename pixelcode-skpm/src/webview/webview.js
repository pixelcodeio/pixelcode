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
      var locationHash = windowObject.evaluateWebScript('window.location.hash');
      //The hash object exposes commands and parameters
      //In example, if you send updateHash('add','artboardName','Mark')
      //You’ll be able to use hash.artboardName to return 'Mark'
      window_.close();
      console.log('window closed');
      var hash = parseHash(locationHash);
      console.log(hash);
      if (hash.hasOwnProperty('token')) {
        var token = hash['token'];
        context.document.showMessage('Pixelcode: Login successful!');
        application.setSettingForKey('token', token);
      } else if (hash.hasOwnProperty('projectHash')) {
        var projectHash = hash['projectHash'];
        uploadToProject(context, projectHash, info.token, info.artboards);
        context.document.showMessage('Pixelcode: Uploaded to project!');
        console.log('PROJECT HASH:');
        console.log(projectHash);
      }
    }
  );

  // Associate the new delegate to the WebView we already created
  webView.setFrameLoadDelegate_(
    NSClassFromString(className).new()
  );
};

export function uploadArtboardToProject (projectHash, exportsPath, token, artboard) {
  // /Users/kevinchan/Library/Application Support/com.bohemiancoding.sketch3/Plugins/pixelcode-skpm/plugin.sketchplugin/Contents
  var jsonContents = String(NSString.stringWithContentsOfFile(exportsPath + artboard + '.json'));
  var svgContents = String(NSString.stringWithContentsOfFile(exportsPath + artboard + '.svg'));
  // var pngContents = NSString.stringWithContentsOfFile(exportsPath + artboard + '@3x.png');
  var pngData = NSData.dataWithContentsOfFile_options_error(exportsPath + artboard + '@3x.png', NSDataReadingUncached, null);
  console.log('made data');
  // var pngContents = String(NSString.stringWithUTF8String(pngData));
  var pngContents = String(pngData.base64EncodedStringWithOptions(0));
  console.log('made png contents LOL' + pngContents);
  // pngContents.writeToFile_atomically_encoding_error(exportsPath + 'test.png', true, NSUTF8StringEncoding, null);
  // if (filename.includes('.png') && filename.includes('@')) {
  //   var atSymbolIndex = filename.indexOf('@');
  //   var dotIndex = filename.indexOf('.png');
  //   filename = filename.substring(0, atSymbolIndex) + filename.substring(dotIndex);
  // }
  // console.log('Uploading file: ABC ' + filename);
  var body = JSON.stringify({'asset_name': artboard, 'json': jsonContents, 'svg': svgContents, 'png': pngContents});
  // var form = new FormData();
  // console.log('MADE FORM');
  // form.append('asset_name', artboard);
  // form.append('json', jsonContents);
  // form.append('svg', svgContents);
  // form.append('png', pngContents);
  var options = {
    method: 'PUT',
    body: body,
    headers: {
      'Authorization': 'Token ' + token,
      'Content-Type': 'application/json'
      // 'Content-Disposition': 'form-data; filename=' + filename
    }
  };
  var uploadUrl = globals.uploadToProjectRoute + projectHash + '/upload';
  fetch(uploadUrl, options)
    .then(response => response.text())
    .then(text => console.log('UPLOAD URL RESPONSE TEXT IS: ' + text))
    .catch(error => console.log('Upload error is: ' + error));
}

export function uploadToProject (context, projectHash, token, artboards) {
  console.log('Uploading to Project');
  var contentsPath = context.scriptPath.stringByDeletingLastPathComponent().stringByDeletingLastPathComponent();
  var exportsPath = contentsPath + '/Resources/exports/';
  for (var i = 0; i < artboards.length; i++) {
    var artboard = String(artboards[i]);
    uploadArtboardToProject(projectHash, exportsPath, token, artboard);
  }

  // for (var i = 0; i < artboards.length; i++) {
  //   var artboard = artboards[i];
  //   console.log('artboard: ' + artboard);
  //
  //   uploadFileToProject(projectHash, exportsPath, token, artboard + '.json');
  //   uploadFileToProject(projectHash, exportsPath, token, artboard + '.svg');
  //   uploadFileToProject(projectHash, exportsPath, token, artboard + '@3x.png');
  //   console.log('Uploading artboards .json, .svg, and .png: ' + artboard);
  // }

  // var files = NSFileManager.defaultManager().contentsOfDirectoryAtPath_error(exportsPath, null);
  // for (var i = 0; i < files.length; i++) {
  //   var filename = files[i];
  //   console.log('Uploading ' + filename);
  //   uploadFileToProject(projectHash, exportsPath, token, filename);
  // }
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
