#!/usr/bin/env python3
"""
Example usage of the DongleDriver

This script demonstrates how to:
1. Find a compatible USB dongle
2. Initialize the driver
3. Set up event handlers
4. Start the driver with configuration
"""

import sys
import os
import usb.core
import time

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dongle_driver import DongleDriver, DEFAULT_CONFIG, HandDriveType
from readable import VideoData, AudioData, Plugged, Command


def find_dongle():
    """Find a compatible USB dongle"""
    for device_info in DongleDriver.KNOWN_DEVICES:
        device = usb.core.find(
            idVendor=device_info['vendor_id'],
            idProduct=device_info['product_id']
        )
        if device:
            return device
    return None


def on_message(message):
    """Handle incoming messages from the dongle"""
    try:
        if isinstance(message, VideoData):
            print(f"Received video frame: {message.width}x{message.height}, "
                  f"{len(message.data)} bytes")
        elif isinstance(message, AudioData):
            if message.data is not None:
                print(f"Received audio data: {len(message.data)} samples")
            elif message.command:
                print(f"Received audio command: {message.command.name}")
        elif isinstance(message, Plugged):
            print(f"Phone plugged: {message.phone_type.name}")
        elif isinstance(message, Command):
            print(f"Received command: {message.value.name}")
        else:
            print(f"Received message: {type(message).__name__}")
    except Exception as e:
        print(f"Error handling message: {e}")


def on_failure():
    """Handle driver failure"""
    print("Driver failed!")


def main():
    # Find the USB dongle
    print("Looking for USB dongle...")
    device = find_dongle()
    
    if not device:
        print("No compatible USB dongle found!")
        print("Make sure the device is plugged in and you have proper permissions.")
        return
    
    print(f"Found device: {device}")
    
    # Create driver instance
    driver = DongleDriver()
    
    # Set up event handlers
    driver.on('message', on_message)
    driver.on('failure', on_failure)
    
    try:
        # Initialize the driver
        print("Initializing driver...")
        driver.initialize(device)
        
        # Create custom configuration (or use DEFAULT_CONFIG)
        config = DEFAULT_CONFIG
        # Customize if needed:
        # config.width = 1024
        # config.height = 768
        # config.fps = 30
        # config.hand = HandDriveType.RHD  # Right-hand drive
        
        # Start the driver
        print("Starting driver...")
        driver.start(config)
        
        print("Driver running! Press Ctrl+C to stop...")
        
        # Keep running until interrupted
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nStopping driver...")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        driver.close()
        print("Driver closed.")


if __name__ == '__main__':
    main()