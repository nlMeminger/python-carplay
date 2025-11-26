# Modular Architecture Diagram

## Component Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                      Application Layer                              │
│                   (video_viewer_modular.py)                         │
└─────────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
                ▼               ▼               ▼
    ┌──────────────────┐  ┌──────────┐  ┌──────────────┐
    │  Video Pipeline  │  │   GUI    │  │ Device Mgmt  │
    └──────────────────┘  └──────────┘  └──────────────┘
```

## Detailed Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                          YOUR APPLICATION                              │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │              Application-Specific Logic                          │ │
│  └──────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────┘
                                  │
                ┌─────────────────┼─────────────────┐
                │                 │                 │
                ▼                 ▼                 ▼
┌───────────────────────┐  ┌──────────────┐  ┌──────────────────┐
│   video_decoder.py    │  │ audio_handler│  │  touch_handler   │
│  ┌─────────────────┐  │  │     .py      │  │      .py         │
│  │ PyAV (H.264)    │  │  │              │  │                  │
│  │ OpenCV (JPEG)   │  │  │  ┌────────┐  │  │  ┌────────────┐  │
│  │ Automatic       │  │  │  │ PyAudio│  │  │  │ Coordinate │  │
│  │ Fallback        │  │  │  │ Input  │  │  │  │ Transform  │  │
│  └─────────────────┘  │  │  │ Output │  │  │  └────────────┘  │
│                       │  │  └────────┘  │  │                  │
└───────────────────────┘  └──────────────┘  └──────────────────┘
         │                        │                    │
         └────────────────────────┼────────────────────┘
                                  │
                ┌─────────────────┼─────────────────┐
                │                 │                 │
                ▼                 ▼                 ▼
┌───────────────────────┐  ┌──────────────┐  ┌──────────────────┐
│   device_finder.py    │  │ stats_tracker│  │  dongle_driver   │
│                       │  │     .py      │  │      .py         │
│  ┌─────────────────┐  │  │              │  │  (from uploads)  │
│  │ USB Discovery   │  │  │  ┌────────┐  │  │                  │
│  │ Known Devices   │  │  │  │  FPS   │  │  │  ┌────────────┐  │
│  │ Device Info     │  │  │  │ Decode │  │  │  │ USB Comm   │  │
│  └─────────────────┘  │  │  │  Rate  │  │  │  │ Messages   │  │
│                       │  │  └────────┘  │  │  └────────────┘  │
└───────────────────────┘  └──────────────┘  └──────────────────┘
         │                        │                    │
         └────────────────────────┴────────────────────┘
                                  │
                                  ▼
                         ┌────────────────┐
                         │   USB Device   │
                         │ (CarPlay/AA)   │
                         └────────────────┘
```

## Data Flow Diagrams

### Video Pipeline

```
Phone Device
    │
    │ H.264 frames
    ▼
┌──────────────┐
│ USB Driver   │ (dongle_driver.py)
└──────────────┘
    │
    │ VideoData messages
    ▼
┌──────────────┐
│Video Decoder │ (video_decoder.py)
│ ┌──────────┐ │
│ │  PyAV    │ │ ← Try first
│ └──────────┘ │
│ ┌──────────┐ │
│ │ OpenCV   │ │ ← Fallback
│ └──────────┘ │
└──────────────┘
    │
    │ RGB numpy array
    ▼
┌──────────────┐
│Stats Tracker │ (stats_tracker.py)
│ - FPS        │
│ - Decode %   │
└──────────────┘
    │
    │ Image
    ▼
┌──────────────┐
│ GUI Display  │ (tkinter)
└──────────────┘
```

### Audio Pipeline

```
Phone Device                           Microphone
    │                                      │
    │ Audio samples                        │ Audio input
    ▼                                      ▼
┌──────────────┐                   ┌──────────────┐
│ USB Driver   │                   │Audio Handler │
└──────────────┘                   │  (input)     │
    │                               └──────────────┘
    │ AudioData messages                  │
    ▼                                     │
┌──────────────┐                          │
│Audio Handler │                          │
│  (output)    │                          │
└──────────────┘                          │
    │                                     │
    │ PCM data                            │ PCM data
    ▼                                     ▼
 Speakers                            USB Driver → Phone
```

### Touch Pipeline

```
Mouse/Touch Input
    │
    │ Canvas coordinates (x, y)
    ▼
┌──────────────┐
│Touch Handler │ (touch_handler.py)
│              │
│ Coordinate   │
│ Transform    │
│              │
│ Canvas       │
│    ↓         │
│ Display      │
│    ↓         │
│ Video        │
│    ↓         │
│ Normalized   │
│ (0.0 - 1.0)  │
└──────────────┘
    │
    │ SendTouch message
    ▼
┌──────────────┐
│ USB Driver   │
└──────────────┘
    │
    │
    ▼
Phone Device
```

## Module Dependencies Graph

```
video_viewer_modular.py
    ├── video_decoder.py
    │   ├── numpy
    │   ├── av (optional)
    │   └── opencv-python (optional)
    │
    ├── audio_handler.py
    │   ├── numpy
    │   └── pyaudio
    │
    ├── touch_handler.py
    │   └── (no external deps)
    │
    ├── device_finder.py
    │   └── pyusb
    │
    ├── stats_tracker.py
    │   └── (no external deps)
    │
    └── dongle_driver.py (from uploads/)
        ├── pyusb
        ├── readable.py
        ├── sendable.py
        ├── common.py
        └── events.py
```

## Component Interaction

```
┌─────────────────────────────────────────────────────────────┐
│                    Main Application                         │
├─────────────────────────────────────────────────────────────┤
│  1. Create all components                                   │
│     - VideoDecoder()                                        │
│     - AudioHandler(callback)                                │
│     - TouchHandler(callback)                                │
│     - DeviceFinder()                                        │
│     - StatsTracker()                                        │
│                                                             │
│  2. Find and initialize USB device                          │
│     device = finder.find_device()                           │
│                                                             │
│  3. Set up message handler                                  │
│     def on_message(msg):                                    │
│         if VideoData:                                       │
│             frame = decoder.decode_frame(...)               │
│             stats.record_frame(...)                         │
│             display(frame)                                  │
│         elif AudioData:                                     │
│             audio.play_audio(...)                           │
│                                                             │
│  4. Handle user input                                       │
│     touch_handler.handle_down(x, y)                         │
│     → sends via driver                                      │
│                                                             │
│  5. Monitor performance                                     │
│     fps = stats.get_fps()                                   │
│     decode_rate = stats.get_decode_rate()                   │
└─────────────────────────────────────────────────────────────┘
```

## Reusability Examples

### Example 1: Video-Only App
```
Your App
  └── video_decoder.py
      └── stats_tracker.py
```

### Example 2: Audio-Only App
```
Your App
  └── audio_handler.py
```

### Example 3: Touch Testing App
```
Your App
  └── touch_handler.py
```

### Example 4: Device Scanner
```
Your App
  └── device_finder.py
```

### Example 5: Full Featured App
```
Your App
  ├── video_decoder.py
  ├── audio_handler.py
  ├── touch_handler.py
  ├── device_finder.py
  └── stats_tracker.py
```

## Benefits Visualization

```
BEFORE (Monolithic)              AFTER (Modular)
┌──────────────────┐            ┌────┬────┬────┬────┬────┐
│                  │            │ V  │ A  │ T  │ D  │ S  │
│   Everything     │    →→→     │ i  │ u  │ o  │ e  │ t  │
│   in one file    │            │ d  │ d  │ u  │ v  │ a  │
│                  │            │ e  │ i  │ c  │ i  │ t  │
│   (800 lines)    │            │ o  │ o  │ h  │ c  │ s  │
│                  │            └────┴────┴────┴────┴────┘
└──────────────────┘              5 independent modules
                                  (~200-280 lines each)

Hard to:                          Easy to:
❌ Test parts independently        ✅ Test each module
❌ Reuse in other projects         ✅ Use anywhere
❌ Understand code flow            ✅ Follow logic
❌ Make changes safely             ✅ Modify safely
❌ Add new features                ✅ Extend features
```

## Summary

The modular architecture provides:

1. **Separation of Concerns**: Each module has a single responsibility
2. **Independence**: Modules can be used separately
3. **Reusability**: Components work in different projects
4. **Testability**: Each module can be tested in isolation
5. **Maintainability**: Easier to understand and modify
6. **Flexibility**: Mix and match as needed
7. **Scalability**: Easy to add new features

Legend:
- V = video_decoder
- A = audio_handler
- T = touch_handler
- D = device_finder
- S = stats_tracker
