# pixelcode

## Directory Structure

`plugin/`: Contains the sketch plugin

`app/`: Contains the code for the core app

## Running Tests with Plugin

To install the plugin, run `script.sh` in the `plugin/` directory.

Next, make sure that this repository is located in `~/Documents/sketch-to-swift/`.

Install `fswatch` and `xargs` (information on installation can be found online).

```
cd app/
chmod +x run.sh
sh run.sh
```

Any artboards exported using the plugin should have `.svg` files created in `app/tests`, and their xcode files generated with an `.out` extension.
