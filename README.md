# Python Dongle Driver

A Python implementation of a USB dongle driver for CarPlay and Android Auto devices.

This is a port of the original TypeScript implementation, providing the same functionality for communicating with CarPlay/Android Auto USB dongles in Python.

## Features

- USB device communication using PyUSB
- Support for CarPlay and Android Auto protocols
- Video and audio data streaming
- Touch input handling (single and multi-touch)
- Device configuration management
- Event-driven architecture

## Installation

### Prerequisites

- Python 3.7 or higher
- libusb (required by PyUSB)

#### Installing libusb

**Ubuntu/Debian:**
```bash
sudo apt-get install libusb-1.0-0-dev
```

**macOS:**
```bash
brew install libusb
```

**Windows:**
Download and install from: https://libusb.info/

### Install Python dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Basic Example
```python
import usb.core
from dongle_driver import DongleDriver, DEFAULT_CONFIG

# Find the USB dongle
device = usb.core.find(idVendor=0x1314, idProduct=0x1520)

# Create and initialize driver
driver = DongleDriver()

# Set up event handlers
def on_message(message):
    print(f"Received: {type(message).__name__}")

driver.on('message', on_message)

# Initialize and start
driver.initialize(device)
driver.start(DEFAULT_CONFIG)
```

### Complete Example

See `example.py` for a complete working example with error handling and proper cleanup.
```bash
python example.py
```

## Configuration

The `DongleConfig` class allows you to customize the dongle settings:
```python
from dongle_driver import DongleConfig, HandDriveType

config = DongleConfig(
    width=1024,
    height=768,
    fps=30,
    dpi=160,
    hand=HandDriveType.LHD,  # Left-hand drive
    night_mode=False,
    wifi_type='5ghz',
    mic_type='os',
    audio_transfer_mode=False
)

driver.start(config)
```

## Message Types

The driver handles various message types:

### Received Messages (from device)
- `VideoData` - Video frame data
- `AudioData` - Audio data or commands
- `Plugged` - Phone connection event
- `Unplugged` - Phone disconnection event
- `Command` - Device commands
- `MediaData` - Media playback information
- `BluetoothAddress` - Bluetooth address info
- `WifiDeviceName` - WiFi device name
- And more...

### Sendable Messages (to device)
- `SendTouch` - Single touch events
- `SendMultiTouch` - Multi-touch events
- `SendCommand` - Send commands to device
- `SendAudio` - Send audio data
- `SendOpen` - Initialize device
- `HeartBeat` - Keep connection alive

## Event Handlers

The driver emits the following events:

- `message` - Emitted when a message is received from the device
- `failure` - Emitted when the driver encounters too many errors
```python
driver.on('message', lambda msg: print(f"Got: {msg}"))
driver.on('failure', lambda: print("Driver failed"))
```

## Known Devices

The driver supports the following USB devices:

- Vendor ID: 0x1314, Product ID: 0x1520
- Vendor ID: 0x1314, Product ID: 0x1521

## Permissions (Linux)

On Linux, you may need to set up udev rules to access the USB device without root:

Create `/etc/udev/rules.d/99-carplay-dongle.rules`:
```
SUBSYSTEM=="usb", ATTR{idVendor}=="1314", ATTR{idProduct}=="1520", MODE="0666"
SUBSYSTEM=="usb", ATTR{idVendor}=="1314", ATTR{idProduct}=="1521", MODE="0666"
```

Then reload udev rules:
```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

## Architecture
```
dongle_driver.py          # Main driver class
├── events.py             # Event emitter implementation
└── messages/
    ├── common.py         # Message header and types
    ├── readable.py       # Messages received from device
    └── sendable.py       # Messages sent to device
```

## Differences from TypeScript Version

1. **USB Library**: Uses PyUSB instead of WebUSB/node-usb
2. **Threading**: Uses Python threading instead of Node.js async patterns
3. **Arrays**: Uses NumPy for audio data instead of Int16Array
4. **Event System**: Custom EventEmitter implementation

## Troubleshooting

**Device not found:**
- Check USB connection
- Verify device is in the known devices list
- Check USB permissions (Linux)

**Import errors:**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Ensure libusb is installed on your system

**USB errors:**
- Try running with sudo (not recommended for production)
- Set up proper udev rules (Linux)
- Check if device is already claimed by another process

## Attribution

This is a port of the TypeScript implementation Node-Carplay, which is itself a version of pycarplay. Full credit is given to @rhysmorgan134 for Node-Carplay and @electric-monk for pycarplay.

## AI Disclosure

This repository contains AI generated code.

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0).

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

For the full license text, see the [LICENSE](LICENSE) file in this repository.