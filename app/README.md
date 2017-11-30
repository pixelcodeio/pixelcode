# Pixelcode

Central code for exporting a svg + json pair into runnable Swift code.

## Installation

```bash
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

## Editor Setup

Atom is required.

```bash
sudo python3 -m pip install mypy
sudo python3 -m pip install pylint
```

## Usage

Export an artboard from Sketch, and run `python main.py` after activating
the virtualenv. The generated `.out` file corresponds to the artboard.

## Testing

`sh runtests`
