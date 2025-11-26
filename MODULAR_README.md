# Modular CarPlay/Android Auto Components

This package provides reusable, modular components for building CarPlay and Android Auto applications in Python.

## Architecture

The codebase is split into independent, reusable modules:

```
├── video_decoder.py      # Video decoding (H.264, JPEG, RGB565)
├── audio_handler.py      # Audio playback and recording
├── touch_handler.py      # Touch input management
├── device_finder.py      # USB device discovery
├── stats_tracker.py      # Performance tracking
└── video_viewer_modular.py  # Example application
```

Each module can be used independently or combined to build complete applications.

## Module Overview

### 1. Video Decoder (`video_decoder.py`)

Flexible video decoding with multiple backends (PyAV, OpenCV) and automatic fallback.

**Features:**
- Multi-backend support (PyAV for H.264, OpenCV for JPEG/RGB565)
- Automatic decoder selection and fallback
- Frame statistics tracking
- Optional raw frame saving for debugging

**Example:**
```python
from video_decoder import VideoDecoder, FrameSaver

# Create decoder
decoder = VideoDecoder()

# Decode a frame
rgb_image = decoder.decode_frame(h264_data, width=800, height=600)

# Get statistics
stats = decoder.get_stats()
print(f"Success rate: {stats['success_rate']:.1f}%")

# Optional: Save raw frames for debugging
saver = FrameSaver(output_dir='debug_frames', max_frames=100)
saver.save_frame(h264_data, width, height)
```

### 2. Audio Handler (`audio_handler.py`)

Audio playback and recording with PyAudio.

**Features:**
- Audio output (playback from device)
- Audio input (microphone to device)
- Multiple format support
- Automatic stream management
- Device enumeration

**Example:**
```python
from audio_handler import AudioHandler, AudioFormat

# Create handler with callback for mic data
def on_mic_data(audio_samples):
    print(f"Received {len(audio_samples)} samples")
    # Send to device...

handler = AudioHandler(on_audio_data=on_mic_data)

# List available devices
handler.list_devices()

# Start audio output
format = AudioFormat(44100, 2, 16)  # 44.1kHz, stereo, 16-bit
handler.start_output(format)

# Play audio
handler.play_audio(audio_data)

# Start microphone
handler.start_input()  # Uses 16kHz mono by default

# Clean up
handler.close()
```

### 3. Touch Handler (`touch_handler.py`)

Touch input management with coordinate transformation.

**Features:**
- Single and multi-touch support
- Coordinate transformation (screen → device)
- Touch event tracking (down, move, up)
- Proper coordinate clamping

**Example:**
```python
from touch_handler import TouchHandler, TouchAction

# Create handler with send callback
def send_touch(x, y, action):
    print(f"Touch {action.name}: ({x:.3f}, {y:.3f})")
    # Send to device...

handler = TouchHandler(send_callback=send_touch)

# Update display info for coordinate conversion
handler.set_display_info(
    video_size=(800, 600),      # Original video size
    display_size=(640, 480),    # Scaled display size
    display_offset=(80, 60)     # Position in canvas
)

# Handle touch events
handler.handle_down(canvas_x=200, canvas_y=150)
handler.handle_move(canvas_x=250, canvas_y=180)
handler.handle_up(canvas_x=250, canvas_y=180)
```

### 4. Device Finder (`device_finder.py`)

USB device discovery and management.

**Features:**
- Automatic device detection
- Known device database
- Custom device registration
- Device information display

**Example:**
```python
from device_finder import DeviceFinder

# Create finder
finder = DeviceFinder()

# List known devices
finder.list_known_devices()

# Find a device
device = finder.find_device()

if device:
    print("Found device!")
    print(DeviceFinder.get_device_info_string(device))

# Add custom device
finder.add_device(0x1234, 0x5678, "My Custom Dongle")

# List all USB devices
DeviceFinder.list_all_usb_devices()
```

### 5. Stats Tracker (`stats_tracker.py`)

Performance and statistics tracking.

**Features:**
- Frame counting and FPS calculation
- Decode success rate tracking
- Resolution history
- Bitrate calculation
- Performance monitoring

**Example:**
```python
from stats_tracker import StatsTracker, PerformanceMonitor

# Create tracker
stats = StatsTracker()

# Record frames
stats.record_frame(
    decoded=True,
    resolution=(800, 600),
    data_size=50000
)

# Get statistics
print(f"FPS: {stats.get_fps():.1f}")
print(f"Decode rate: {stats.get_decode_rate():.1f}%")
print(f"Bitrate: {stats.get_bitrate():.2f} Mbps")

# Get all stats
stats_dict = stats.get_stats_dict()

# Performance monitoring
perf = PerformanceMonitor()

start = perf.start_operation('decode')
# ... decode operation ...
perf.end_operation('decode', start)

print(perf.get_report())
```

## Complete Example

The `video_viewer_modular.py` demonstrates how to combine all modules:

```bash
python video_viewer_modular.py
```

Options:
- `--save-frames` or `-s`: Save raw H.264 frames for debugging

## Building Your Own Application

Here's a minimal example of building a custom application:

```python
from video_decoder import VideoDecoder
from audio_handler import AudioHandler
from device_finder import DeviceFinder
from stats_tracker import StatsTracker
from dongle_driver import DongleDriver, DEFAULT_CONFIG

# Find device
finder = DeviceFinder()
device = finder.find_device()

# Create components
decoder = VideoDecoder()
audio = AudioHandler()
stats = StatsTracker()

# Create driver
driver = DongleDriver()

def on_message(message):
    if isinstance(message, VideoData):
        # Decode video
        frame = decoder.decode_frame(
            message.data,
            message.width,
            message.height
        )
        
        # Track stats
        stats.record_frame(
            decoded=frame is not None,
            resolution=(message.width, message.height)
        )
        
        # Display frame...
        
    elif isinstance(message, AudioData):
        # Handle audio...
        pass

# Setup and start
driver.on('message', on_message)
driver.initialize(device)
driver.start(DEFAULT_CONFIG)
```

## Use Cases

### 1. Simple Video Display
```python
from video_decoder import VideoDecoder
# Just decode and display video frames
```

### 2. Audio-Only Application
```python
from audio_handler import AudioHandler
# Handle audio playback/recording without video
```

### 3. Touch Input Testing
```python
from touch_handler import TouchHandler
# Test touch coordinate conversion
```

### 4. Device Discovery Tool
```python
from device_finder import DeviceFinder
# Build a device detection utility
```

### 5. Performance Analysis
```python
from stats_tracker import StatsTracker, PerformanceMonitor
# Analyze streaming performance
```

## Advantages of Modular Design

1. **Reusability**: Use components in multiple projects
2. **Testability**: Test each module independently
3. **Maintainability**: Fix bugs in one place
4. **Flexibility**: Mix and match components as needed
5. **Clarity**: Clear separation of concerns

## Dependencies

Each module has minimal dependencies:

**video_decoder.py:**
- numpy
- av (optional, for H.264)
- opencv-python (optional, for JPEG/RGB565)

**audio_handler.py:**
- numpy
- pyaudio

**touch_handler.py:**
- (no external dependencies)

**device_finder.py:**
- pyusb

**stats_tracker.py:**
- (no external dependencies)

## Installation

```bash
# Core dependencies
pip install numpy pyusb

# Video decoding (choose one or both)
pip install av              # For H.264
pip install opencv-python   # For JPEG/RGB565

# Audio support
pip install pyaudio

# For GUI applications
pip install pillow
```

## Testing Individual Modules

Each module can be tested independently:

```bash
# Test device finder
python device_finder.py

# Test decoder (create test script)
python -c "from video_decoder import VideoDecoder; d = VideoDecoder(); print(d.get_stats())"

# Test audio handler
python -c "from audio_handler import AudioHandler; a = AudioHandler(); a.list_devices()"
```

## Advanced Usage

### Custom Decoder Backend

```python
from video_decoder import VideoDecoder, DecoderBackend

# Prefer PyAV
decoder = VideoDecoder(preferred_backend=DecoderBackend.PYAV)

# Or prefer OpenCV
decoder = VideoDecoder(preferred_backend=DecoderBackend.OPENCV)
```

### Multi-Touch Support

```python
from touch_handler import MultiTouchHandler

handler = MultiTouchHandler(send_multitouch_callback=send_func)
handler.handle_multitouch_down(touch_id=0, x=100, y=150)
handler.handle_multitouch_move(touch_id=0, x=110, y=160)
handler.handle_multitouch_up(touch_id=0, x=110, y=160)
```

### Custom Audio Formats

```python
from audio_handler import AudioFormat

# 48kHz stereo
format = AudioFormat(48000, 2, 16)
handler.start_output(format)

# 8kHz mono (phone quality)
mic_format = AudioFormat(8000, 1, 16)
handler.start_input(mic_format)
```

## Contributing

When adding new features:

1. Keep modules independent
2. Add comprehensive docstrings
3. Include usage examples
4. Maintain backwards compatibility
5. Update this README

## Troubleshooting

**Video not decoding:**
- Install PyAV: `pip install av`
- Check decoder stats: `decoder.get_stats()`

**Audio issues:**
- List devices: `audio_handler.list_devices()`
- Check PyAudio: `pip install pyaudio`

**Touch not working:**
- Verify display info: `touch_handler.set_display_info(...)`
- Check coordinate conversion: `touch_handler.canvas_to_normalized(...)`

**Device not found:**
- List all devices: `DeviceFinder.list_all_usb_devices()`
- Check permissions (Linux): See main README for udev rules

## License

Same as the main dongle driver project.
