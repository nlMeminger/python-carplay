"""
Python Dongle Driver for CarPlay/Android Auto USB devices

This is a Python port of a TypeScript USB dongle driver for communicating
with CarPlay and Android Auto dongles.
"""

from . import *
from dongle_driver import (
    HandDriveType,
    DongleConfig,
    DEFAULT_CONFIG,
    DongleDriver,
    DriverStateError,
)

__all__ = [
    'HandDriveType',
    'DongleConfig',
    'DEFAULT_CONFIG',
    'DongleDriver',
    'DriverStateError',
]
