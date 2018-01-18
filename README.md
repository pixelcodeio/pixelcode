# pixelcode

## Directory Structure

`plugin/`: Contains the sketch plugin

`app/`: Contains the code for the core app

`assets/`: Contains assets for running tests

## Plugin Setup

1. Run `npm install` in the `pixelcode-skpm` directory. 
2. Make a `globals.js` file in the `pixelcode-skpm/src/` directory (look at `globals.js.template`).
3. Make a `routes.js` file in the `pixelcode-skpm/plugin.sketchplugin/Contents/Resources` directory (look at `routes.js.template`).
4. Run `sh update.sh` in the `pixelcode-skpm` directory 

## Running Tests with Plugin

To install the plugin, run `update` in the `plugin/` directory.

Next, make sure that this repository is located in `~/Documents/pixelcode/`.

Install `fswatch` and `xargs` (information on installation can be found online).

```
cd app/
chmod +x run.sh
sh run.sh
```

Any artboards exported using the plugin should have `.svg` files created in `app/exports`, and their xcode files generated with an `.swift` extension.

## Swift Code Formatter Setup

1. Install [Homebrew](https://brew.sh/).
2. Run the following commands in your terminal

```
brew update
brew install swiftformat
```

## XCode Setup

### Podfile Setup
We use [SnapKit](http://snapkit.io/) to implement concise AutoLayout code. To setup SnapKit:

1. Go to project directory and run `pod init`.
2. Go into the generated `Podfile` and paste:
```
# Uncomment the next line to define a global platform for your project
# platform :ios, '11.0'

target '`Your project name`' do
  # Comment the next line if you're not using Swift and don't want to use dynamic frameworks
  use_frameworks!

    # Pods for '`Your project name`' 
    pod 'SnapKit'
    end
```
3. Run `pod install` in your project directory.
4. Done!

### Font Setup
To import fonts into Xcode, you can follow the steps below or the ones detailed [here](https://medium.com/yay-its-erica/how-to-import-fonts-into-xcode-swift-3-f0de7e921ef8
).

1. Download a font in OTF (OpenTypeFormat), i.e. `.otf`
2. Drag `.otf` file into XCode.
3. Click on the `.otf` file in XCode and make sure that your app is checked under "Target Membership" (on the right hand side)
4. Go to "Build Phases" -> "Bundle Resources" and make sure you see your `.otf` file listed.
5. Go to your Info.plist and add a new key called: "Fonts provided by application"
6. Click the arrow right next to "Fonts provided by application" where you should then see "Item 0". 
7. Type the name of your `.otf` file (with the ".otf" at the end) as the value of "Item 0"
8. Done!

