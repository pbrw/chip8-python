# CHIP-8 Python Emulator
CHIP-8 emulator written in Python. No graphic library, only command line interface.

Simmulates instruction cycle, timers, diplay rendering and input control (at configurable frequecies). All of it in a single thread!

**Dependencies:**
 - keyboard

Emulator was tested on Ubuntu 22.04 with Python 3.10.12

## Run
Emulator needs to be run with root privileges in order to control pressed buttons.

```
pip install -r requirements.txt
sudo `which python` main.py test/snake3.ch8
```




