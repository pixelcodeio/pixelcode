import WebUI from 'sketch-module-web-view';
import {MochaJSDelegate} from './MochaJSDelegate';

export function createWebUI(context, application, name, html, width, height) {
  var options = {
    identifier: name, // to reuse the UI
    x: 0,
    y: 0,
    width: width,
    height: height,
    background: NSColor.whiteColor(),
    blurredBackground: false,
    onlyShowCloseButton: false,
    title: name,
    hideTitleBar: false,
    shouldKeepAround: false,
    show: true,
    styleMask: NSTitledWindowMask | NSClosableWindowMask,
    resizable: false,
    frameLoadDelegate: {
      'webView:didChangeLocationWithinPageForFrame:': function (webView, webFrame) {
        var windowObject = webView.windowScriptObject();
        var locationHash = windowObject.evaluateWebScript('window.location.hash');
        //The hash object exposes commands and parameters
        //In example, if you send updateHash('add','artboardName','Mark')
        //You’ll be able to use hash.artboardName to return 'Mark'
        var hash = parseHash(locationHash);
        console.log(hash);
        if (hash.hasOwnProperty('token')) {
          var token = hash['token'];
          application.setSettingForKey('token', token);
        } else if (hash.hasOwnProperty('projectHash')) {
          var projectHash = hash['projectHash'];
        }
      }
    },
    uiDelegate: {}, // https://developer.apple.com/reference/webkit/webuidelegate?language=objc
    onPanelClose: function () {
      context.document.showMessage('Deteced WINDOW CLOSE');
      console.log('detected close');
      return true;
      // Stuff
      // return `false` to prevent closing the panel
    }
  };

  // HTML path is relative to Contents/Resources directory
  var webUI = new WebUI(context, require('./html/' + html), options);
}

// export function createWebview(name, path, width, height) {
//   var webViewWindow = NSPanel.alloc().init();
//   webViewWindow.setFrame_display(NSMakeRect(0, 0, width, height), true);
//   webViewWindow.setStyleMask(NSTitledWindowMask | NSClosableWindowMask);
//
//   //Uncomment the following line to define the app bar color with an NSColor
//   //webViewWindow.setBackgroundColor(NSColor.whiteColor());
//   webViewWindow.standardWindowButton(NSWindowMiniaturizeButton).setHidden(true);
//   webViewWindow.standardWindowButton(NSWindowZoomButton).setHidden(true);
//   webViewWindow.setTitle(name);
//   webViewWindow.setTitlebarAppearsTransparent(true);
//   webViewWindow.becomeKeyWindow();
//   webViewWindow.setLevel(NSFloatingWindowLevel);
//   COScript.currentCOScript().setShouldKeepAround_(true);
//
//   //Add Web View to window
//   var webView = WebView.alloc().initWithFrame(NSMakeRect(0, 0, width, height - 24));
//   webView.setAutoresizingMask(NSViewWidthSizable|NSViewHeightSizable);
//   var windowObject = webView.windowScriptObject();
//   var delegate = new MochaJSDelegate({
//
//     //To get commands from the webView we observe the location hash: if it changes, we do something
//     'webView:didChangeLocationWithinPageForFrame:' : (function(webView, webFrame) {
//       var locationHash = windowObject.evaluateWebScript('window.location.hash');
//       //The hash object exposes commands and parameters
//       //In example, if you send updateHash('add','artboardName','Mark')
//       //You’ll be able to use hash.artboardName to return 'Mark'
//       var hash = parseHash(locationHash);
//       log(hash);
//       //We parse the location hash and check for the command we are sending from the UI
//       //If the command exist we run the following code
//       webViewWindow.close();
//      })
//   })
//
//   webView.setFrameLoadDelegate_(delegate.getClassInstance());
//   webView.setMainFrameURL_(NSURL.fileURLWithPath(path));
//   webViewWindow.contentView().addSubview(webView);
//   webViewWindow.center();
//   webViewWindow.makeKeyAndOrderFront(nil);
//   // Define the close window behaviour on the standard red traffic light button
//   var closeButton = webViewWindow.standardWindowButton(NSWindowCloseButton);
//   closeButton.setCOSJSTargetFunction(function(sender) {
//     COScript.currentCOScript().setShouldKeepAround(false);
//     webViewWindow.close();
//   });
//   closeButton.setAction('callAction:');
// }

export function createWebViewChangeLocationDelegate(application, context, window_, webView, token) {
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
      var hash = parseHash(locationHash);
      console.log(hash);
      if (hash.hasOwnProperty('token')) {
        var token = hash['token'];
        context.document.showMessage('Pixelcode: Login successful!');
        application.setSettingForKey('token', token);
      } else if (hash.hasOwnProperty('projectHash')) {
        var projectHash = hash['projectHash'];
        uploadToProject(projectHash, token);
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

function uploadToProject(projectHash, token) {
  // /api/project/[projecthash]/upload
  var url = 'http://0.0.0.0:8000/api/project' + projectHash + '/upload';
  fetch('http://0.0.0.0:8000/api/project/ +userprojects')
}

export function createWindow(width, height) {
  var window_ = NSWindow.alloc().init();
  window_.setFrame_display(NSMakeRect(0, 0, width, height), true);
  window_.setStyleMask(NSTitledWindowMask | NSClosableWindowMask);
  // var window_ = [[NSWindow.alloc()
  //     initWithContentRect:NSMakeRect(0, 0, width, height)
  //     styleMask:NSTitledWindowMask | NSClosableWindowMask
  //     backing:NSBackingStoreBuffered
  //     defer:false
  //   ] autorelease];
  window_.center();
  window_.makeKeyAndOrderFront_(window_);
  return window_;
}

export function createWebview(context, window_, htmlPath, width, height) {
  // create frame for loading content in
  var webviewFrame = NSMakeRect(0, 0, width, height);

  var requestUrl      = NSURL.fileURLWithPath(htmlPath);
  var urlRequest      = NSMutableURLRequest.requestWithURL(requestUrl);

  // Create the WebView, frame, and set content
  var webView = WebView.new();
  webView.initWithFrame(webviewFrame);
  webView.mainFrame().loadRequest(urlRequest);
  window_.contentView().addSubview(webView);

  return webView;
}

function parseHash(aURL) {
  aURL = aURL;
  var vars = {};
  var hashes = aURL.slice(aURL.indexOf('#') + 1).split('&');

    for(var i = 0; i < hashes.length; i++) {
       var hash = hashes[i].split('=');

       if(hash.length > 1) {
         vars[hash[0].toString()] = hash[1];
       } else {
        vars[hash[0].toString()] = null;
       }
    }

    return vars;
}
