export function createWebViewChangeLocationDelegate(application, context, webView) {
    /**
     * Create a Delegate class and register it
     */
    var className = 'MochaJSDelegate_DynamicClass_SymbolUI_WebviewRedirectDelegate' + NSUUID.UUID().UUIDString();
    var delegateClassDesc = MOClassDescription.allocateDescriptionForClassWithName_superclass_(className, NSObject);
    delegateClassDesc.registerClass();

    /**
     * Register the "event" to respond to and specify the callback function
     */
    var windowObject = webView.windowScriptObject();
    var changeLocationEventSelector = NSSelectorFromString('webView:didChangeLocationWithinPageForFrame:');
    delegateClassDesc.addInstanceMethodWithSelector_function_(
      // The "event" - the WebView is about to redirect soon
      NSSelectorFromString('webView:didChangeLocationWithinPageForFrame:'),

      // The "listener" - a callback function to fire
      function(webView, webFrame) {
        var locationHash = windowObject.evaluateWebScript("window.location.hash");
        //The hash object exposes commands and parameters
        //In example, if you send updateHash('add','artboardName','Mark')
        //You’ll be able to use hash.artboardName to return 'Mark'
        var hash = parseHash(locationHash);
        log(hash);
        if (hash.hasOwnProperty("token")) {
          var token = hash["token"];
          application.setSettingForKey("token", token);
        } else if (hash.hasOwnProperty("projectHash")) {
          var projectHash = hash["projectHash"];
          log("PROJECT HASH:");
          log(projectHash);
        }
      }
    );

    // Associate the new delegate to the WebView we already created
    webView.setFrameLoadDelegate_(
      NSClassFromString(className).new()
    );

};


export function createWindow(width, height) {
  var window_ = [[[NSWindow alloc]
      initWithContentRect:NSMakeRect(0, 0, width, height)
      styleMask:NSTitledWindowMask | NSClosableWindowMask
      backing:NSBackingStoreBuffered
      defer:false
    ] autorelease];
  window_.center();
  window_.makeKeyAndOrderFront_(window_);
  return window_;
}

export function createWebView(context, window_, htmlFile, width, height) {
  // create frame for loading content in
  var webviewFrame = NSMakeRect(0, 0, width, height);

  // Request index.html
  var webviewFolder   = "/Users/kevinchan/Documents/pixelcode/plugin/pixelcode.sketchplugin/Contents/Sketch/webview/html/";
  var webviewHtmlFile = webviewFolder + htmlFile;
  log(webviewHtmlFile);
  var requestUrl      = [NSURL fileURLWithPath:webviewHtmlFile];
  var urlRequest      = [NSMutableURLRequest requestWithURL:requestUrl];

  // Create the WebView, frame, and set content
  var webView = WebView.new();
  webView.initWithFrame(webviewFrame);
  webView.mainFrame().loadRequest(urlRequest);
  window_.contentView().addSubview(webView);

  return webView;
}

export function parseHash(aURL) {
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

export function request(queryURL, headers, method) {
   var request = NSMutableURLRequest.new();
   [request setHTTPMethod:method];
   [request setURL:[NSURL URLWithString:queryURL]];

   for (var key in headers) {
      [request addValue:headers[key] forHTTPHeaderField:key];
   };

   var session = NSURLSession.sharedSession();
   var task = session.dataTaskWithRequest(request);
   task.resume()

   var error = NSError.new();
   var responseCode = null;

   var oResponseData = [NSURLConnection sendSynchronousRequest:request returningResponse:responseCode error:error];

   var dataString = [[NSString alloc] initWithData:oResponseData encoding:NSUTF8StringEncoding];

   return dataString;
}
