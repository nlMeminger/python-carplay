# Quick Reference Card

## Module Imports

```python
# Video decoding
from video_decoder import VideoDecoder, FrameSaver, DecoderBackend

# Audio handling
from audio_handler import AudioHandler, AudioFormat

# Touch input
from touch_handler import TouchHandler, TouchAction, MultiTouchHandler

# Device discovery
from device_finder import DeviceFinder, DeviceInfo

# Performance tracking
from stats_tracker import StatsTracker, PerformanceMonitor
```

## Common Operations

### Video Decoding
```python
# Create decoder
decoder = VideoDecoder()

# Decode frame
rgb_array = decoder.decode_frame(h264_data, width, height)

# Get stats
stats = decoder.get_stats()
print(f"Success: {stats['success_rate']:.1f}%")
```

### Audio Playback
```python
# Create handler
audio = AudioHandler()

# Start output
audio.start_output(AudioFormat(44100, 2, 16))

# Play audio
audio.play_audio(audio_data)

# Clean up
audio.close()
```

### Audio Recording
```python
# Create handler with callback
def on_mic_data(samples):
    # Process microphone data
    pass

audio = AudioHandler(on_audio_data=on_mic_data)

# Start microphone
audio.start_input()

# Stop microphone
audio.stop_input()
```

### Touch Handling
```python
# Create handler with send callback
def send_touch(x, y, action):
    # Send to device
    pass

touch = TouchHandler(send_callback=send_touch)

# Set display info
touch.set_display_info(
    video_size=(800, 600),
    display_size=(640, 480),
    display_offset=(80, 60)
)

# Handle events
touch.handle_down(x, y)
touch.handle_move(x, y)
touch.handle_up(x, y)
```

### Device Discovery
```python
# Create finder
finder = DeviceFinder()

# Find device
device = finder.find_device()

# Add custom device
finder.add_device(0x1234, 0x5678, "My Device")

# List all USB devices
DeviceFinder.list_all_usb_devices()
```

### Performance Tracking
```python
# Create tracker
stats = StatsTracker()

# Record frame
stats.record_frame(
    decoded=True,
    resolution=(800, 600),
    data_size=50000
)

# Get metrics
fps = stats.get_fps()
decode_rate = stats.get_decode_rate()
bitrate = stats.get_bitrate()

# Print report
print(stats.get_stats_string())
```

## API Quick Reference

### VideoDecoder
| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `__init__` | `preferred_backend` | `VideoDecoder` | Create decoder |
| `decode_frame` | `data, width, height` | `np.ndarray` or `None` | Decode frame |
| `get_stats` | - | `dict` | Get statistics |
| `reset_stats` | - | - | Reset counters |

### AudioHandler
| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `__init__` | `on_audio_data` | `AudioHandler` | Create handler |
| `start_output` | `format` | - | Start playback |
| `stop_output` | - | - | Stop playback |
| `play_audio` | `audio_data` | - | Play samples |
| `start_input` | `format` | - | Start recording |
| `stop_input` | - | - | Stop recording |
| `list_devices` | - | - | Show devices |
| `close` | - | - | Clean up |

### TouchHandler
| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `__init__` | `send_callback` | `TouchHandler` | Create handler |
| `set_display_info` | `video_size, display_size, offset` | - | Set display |
| `handle_down` | `x, y` | `bool` | Touch down |
| `handle_move` | `x, y` | `bool` | Touch move |
| `handle_up` | `x, y` | `bool` | Touch up |
| `canvas_to_normalized` | `x, y` | `(float, float)` | Convert coords |

### DeviceFinder
| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `__init__` | `custom_devices` | `DeviceFinder` | Create finder |
| `find_device` | - | `Device` or `None` | Find one device |
| `find_all_devices` | - | `List[Device]` | Find all devices |
| `add_device` | `vid, pid, desc` | - | Add custom device |
| `list_known_devices` | - | - | Show known devices |
| `list_all_usb_devices` | - | - | Show all USB (static) |

### StatsTracker
| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `__init__` | `fps_window` | `StatsTracker` | Create tracker |
| `record_frame` | `decoded, resolution, data_size` | - | Record frame |
| `get_fps` | - | `float` | Get FPS |
| `get_decode_rate` | - | `float` | Get % decoded |
| `get_bitrate` | - | `float` | Get Mbps |
| `get_stats_dict` | - | `dict` | All stats |
| `get_stats_string` | - | `str` | Formatted stats |
| `reset` | - | - | Reset all |

## Typical Usage Patterns

### Pattern 1: Decode Only
```python
decoder = VideoDecoder()
frame = decoder.decode_frame(data, w, h)
if frame:
    display(frame)
```

### Pattern 2: Audio Playback
```python
audio = AudioHandler()
audio.start_output(AudioFormat(44100, 2, 16))
audio.play_audio(samples)
```

### Pattern 3: Touch Input
```python
touch = TouchHandler(send_callback)
touch.set_display_info(...)
touch.handle_down(x, y)
```

### Pattern 4: Device Search
```python
finder = DeviceFinder()
device = finder.find_device()
```

### Pattern 5: Performance Monitor
```python
stats = StatsTracker()
stats.record_frame(True, (800,600), 50000)
print(f"FPS: {stats.get_fps()}")
```

## Common Code Snippets

### Complete Video Pipeline
```python
from video_decoder import VideoDecoder
from stats_tracker import StatsTracker

decoder = VideoDecoder()
stats = StatsTracker()

# In message handler:
def handle_video(video_data):
    frame = decoder.decode_frame(
        video_data.data,
        video_data.width,
        video_data.height
    )
    stats.record_frame(
        decoded=frame is not None,
        resolution=(video_data.width, video_data.height),
        data_size=len(video_data.data)
    )
    if frame:
        display(frame)
```

### Complete Audio Pipeline
```python
from audio_handler import AudioHandler, AudioFormat

def send_to_device(audio_samples):
    driver.send(SendAudio(audio_samples))

audio = AudioHandler(on_audio_data=send_to_device)

# Play audio from device
audio.start_output(AudioFormat(44100, 2, 16))
audio.play_audio(samples)

# Send mic to device
audio.start_input()  # Automatically sends via callback
```

### Complete Touch Pipeline
```python
from touch_handler import TouchHandler, TouchAction

def send_touch_to_device(x, y, action):
    driver.send(SendTouch(x, y, action))

touch = TouchHandler(send_callback=send_touch_to_device)

# In GUI:
def on_mouse_down(event):
    touch.handle_down(event.x, event.y)

def on_mouse_move(event):
    touch.handle_move(event.x, event.y)

def on_mouse_up(event):
    touch.handle_up(event.x, event.y)
```

## Constants and Enums

### TouchAction
- `TouchAction.Down = 14`
- `TouchAction.Move = 15`
- `TouchAction.Up = 16`

### DecoderBackend
- `DecoderBackend.PYAV = 1`
- `DecoderBackend.OPENCV = 2`

### AudioFormat
```python
AudioFormat(frequency, channels, bit_depth)

# Common formats:
AudioFormat(44100, 2, 16)  # CD quality
AudioFormat(48000, 2, 16)  # Professional
AudioFormat(16000, 1, 16)  # Voice quality
AudioFormat(8000, 1, 16)   # Phone quality
```

## Error Handling

### Video Decoder
```python
try:
    frame = decoder.decode_frame(data, w, h)
    if frame is None:
        print("Decode failed")
except Exception as e:
    print(f"Error: {e}")
```

### Audio Handler
```python
try:
    audio.start_input()
except Exception as e:
    print(f"Mic error: {e}")
    # Try with different format
    audio.start_input(AudioFormat(8000, 1, 16))
```

### Touch Handler
```python
coords = touch.canvas_to_normalized(x, y)
if coords is None:
    print("Touch outside display area")
else:
    tx, ty = coords
    send_touch(tx, ty, action)
```

## Debugging Tips

### Check Decoder
```python
stats = decoder.get_stats()
print(f"Available: {stats['available_decoders']}")
print(f"Success: {stats['success_rate']:.1f}%")
```

### Check Audio
```python
audio.list_devices()  # See available devices
```

### Check Touch
```python
# Test coordinate conversion
result = touch.canvas_to_normalized(100, 100)
print(f"Converted: {result}")
```

### Check Performance
```python
print(stats.get_stats_string())
# Shows FPS, decode rate, bitrate, etc.
```

## Dependencies by Module

```
video_decoder:  numpy, av (opt), opencv-python (opt)
audio_handler:  numpy, pyaudio
touch_handler:  (none)
device_finder:  pyusb
stats_tracker:  (none)
```

## Files to Run

```bash
# Complete application
python video_viewer_modular.py

# Test individual modules
python examples_simple.py

# Test device finder
python device_finder.py
```

## Help Resources

- **SUMMARY.md** - Overview of all files
- **MODULAR_README.md** - Full documentation
- **ARCHITECTURE.md** - System diagrams
- **examples_simple.py** - Working examples
- **Module docstrings** - Detailed API docs

---

Keep this card handy for quick reference! 🚀
