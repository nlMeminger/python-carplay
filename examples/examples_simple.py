#!/usr/bin/env python3
"""
Simple Examples - Using Individual Modules

These examples show how to use each module independently.
"""

# =============================================================================
# Example 1: Video Decoder Only
# =============================================================================

def example_video_decoder():
    """Example: Use video decoder to decode frames"""
    print("=" * 60)
    print("Example 1: Video Decoder")
    print("=" * 60)
    
    from video_decoder import VideoDecoder
    import numpy as np
    
    # Create decoder
    decoder = VideoDecoder()
    
    # Simulate receiving a frame (in real use, this comes from the dongle)
    # For this example, we'll just use dummy data
    fake_h264_data = b'\x00\x00\x00\x01' + b'\x00' * 1000
    width, height = 800, 600
    
    # Decode frame
    rgb_image = decoder.decode_frame(fake_h264_data, width, height)
    
    if rgb_image is not None:
        print(f"✓ Decoded frame: {rgb_image.shape}")
    else:
        print("✗ Failed to decode (expected with fake data)")
    
    # Get statistics
    stats = decoder.get_stats()
    print(f"\nDecoder stats:")
    print(f"  Total frames: {stats['total_frames']}")
    print(f"  Successful: {stats['successful_decodes']}")
    print(f"  Failed: {stats['failed_decodes']}")
    print(f"  Success rate: {stats['success_rate']:.1f}%")
    print(f"  Available decoders: {stats['available_decoders']}")
    print()


# =============================================================================
# Example 2: Audio Handler Only
# =============================================================================

def example_audio_handler():
    """Example: Use audio handler for recording"""
    print("=" * 60)
    print("Example 2: Audio Handler")
    print("=" * 60)
    
    from audio_handler import AudioHandler
    import time
    
    # Callback for microphone data
    sample_count = [0]  # Use list to allow modification in callback
    
    def on_audio_data(audio_samples):
        sample_count[0] += 1
        if sample_count[0] % 10 == 0:
            print(f"Received audio sample #{sample_count[0]}: {len(audio_samples)} samples")
    
    # Create handler
    handler = AudioHandler(on_audio_data=on_audio_data)
    
    # List devices
    handler.list_devices()
    
    # Start microphone (comment out if you don't want to actually record)
    print("\nStarting microphone for 3 seconds...")
    print("(Make some noise!)")
    handler.start_input()
    
    time.sleep(3)
    
    handler.stop_input()
    print(f"Recorded {sample_count[0]} samples")
    
    # Clean up
    handler.close()
    print()


# =============================================================================
# Example 3: Touch Handler Only
# =============================================================================

def example_touch_handler():
    """Example: Use touch handler for coordinate conversion"""
    print("=" * 60)
    print("Example 3: Touch Handler")
    print("=" * 60)
    
    from touch_handler import TouchHandler, TouchAction
    
    # Callback for touch events
    def send_touch(x, y, action):
        print(f"  Touch {action.name}: ({x:.3f}, {y:.3f})")
    
    # Create handler
    handler = TouchHandler(send_callback=send_touch)
    
    # Set up display info
    # Video is 800x600, displayed at 640x480, centered at (80, 60)
    handler.set_display_info(
        video_size=(800, 600),
        display_size=(640, 480),
        display_offset=(80, 60)
    )
    
    # Simulate touch events
    print("\nSimulating touch sequence:")
    
    print("1. Touch down at canvas (200, 150)")
    handler.handle_down(200, 150)
    
    print("2. Drag to (300, 250)")
    handler.handle_move(300, 250)
    
    print("3. Release at (300, 250)")
    handler.handle_up(300, 250)
    
    # Test coordinate conversion
    print("\nCoordinate conversion test:")
    test_points = [
        (80, 60),      # Top-left of display
        (400, 300),    # Center
        (720, 540),    # Bottom-right
        (0, 0),        # Outside display
    ]
    
    for x, y in test_points:
        coords = handler.canvas_to_normalized(x, y)
        if coords:
            print(f"  Canvas ({x}, {y}) -> Normalized ({coords[0]:.3f}, {coords[1]:.3f})")
        else:
            print(f"  Canvas ({x}, {y}) -> Outside display area")
    
    print()


# =============================================================================
# Example 4: Device Finder Only
# =============================================================================

def example_device_finder():
    """Example: Use device finder to discover USB devices"""
    print("=" * 60)
    print("Example 4: Device Finder")
    print("=" * 60)
    
    from device_finder import DeviceFinder
    
    # Create finder
    finder = DeviceFinder()
    
    # List known devices
    finder.list_known_devices()
    
    # Search for device
    print("\nSearching for compatible device...")
    device = finder.find_device()
    
    if device:
        print("\n✓ Found device!")
        print(DeviceFinder.get_device_info_string(device))
    else:
        print("\n✗ No compatible device found")
        print("\nShowing all USB devices:")
        DeviceFinder.list_all_usb_devices()
    
    print()


# =============================================================================
# Example 5: Stats Tracker Only
# =============================================================================

def example_stats_tracker():
    """Example: Use stats tracker to monitor performance"""
    print("=" * 60)
    print("Example 5: Stats Tracker")
    print("=" * 60)
    
    from stats_tracker import StatsTracker, PerformanceMonitor
    import time
    import random
    
    # Create tracker
    stats = StatsTracker()
    
    # Simulate receiving frames
    print("\nSimulating video stream...")
    for i in range(50):
        # Simulate some frames being decoded successfully, some failing
        decoded = random.random() > 0.1  # 90% success rate
        
        stats.record_frame(
            decoded=decoded,
            resolution=(800, 600),
            data_size=50000 + random.randint(-10000, 10000)
        )
        
        time.sleep(0.033)  # ~30 FPS
        
        if i % 10 == 0:
            print(f"Frame {i}: FPS={stats.get_fps():.1f}, Decode={stats.get_decode_rate():.1f}%")
    
    # Get final statistics
    print("\nFinal Statistics:")
    print(stats.get_stats_string())
    
    # Performance monitoring example
    print("\n" + "=" * 60)
    print("Performance Monitoring Example")
    print("=" * 60)
    
    perf = PerformanceMonitor()
    
    # Simulate operations
    for i in range(10):
        # Simulate decode operation
        start = perf.start_operation('decode')
        time.sleep(random.uniform(0.01, 0.03))
        perf.end_operation('decode', start)
        
        # Simulate display operation
        start = perf.start_operation('display')
        time.sleep(random.uniform(0.005, 0.015))
        perf.end_operation('display', start)
    
    print("\n" + perf.get_report())


# =============================================================================
# Example 6: Combining Multiple Modules
# =============================================================================

def example_combined():
    """Example: Combine video decoder and stats tracker"""
    print("=" * 60)
    print("Example 6: Combined Modules")
    print("=" * 60)
    
    from video_decoder import VideoDecoder
    from stats_tracker import StatsTracker
    
    decoder = VideoDecoder()
    stats = StatsTracker()
    
    print("\nSimulating decode pipeline...")
    
    # Simulate processing 20 frames
    fake_data = b'\x00\x00\x00\x01' + b'\x00' * 1000
    
    for i in range(20):
        # Decode
        result = decoder.decode_frame(fake_data, 800, 600)
        
        # Track stats
        stats.record_frame(
            decoded=result is not None,
            resolution=(800, 600),
            data_size=len(fake_data)
        )
    
    # Show results
    print("\nDecoder Statistics:")
    decoder_stats = decoder.get_stats()
    for key, value in decoder_stats.items():
        print(f"  {key}: {value}")
    
    print("\nStream Statistics:")
    print(stats.get_stats_string())


# =============================================================================
# Main Menu
# =============================================================================

def main():
    """Run all examples"""
    examples = [
        ("Video Decoder", example_video_decoder),
        ("Audio Handler", example_audio_handler),
        ("Touch Handler", example_touch_handler),
        ("Device Finder", example_device_finder),
        ("Stats Tracker", example_stats_tracker),
        ("Combined Modules", example_combined),
    ]
    
    print("\n" + "=" * 60)
    print("MODULAR COMPONENT EXAMPLES")
    print("=" * 60)
    print("\nAvailable examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    print("  0. Run all examples")
    
    choice = input("\nEnter choice (0-6): ").strip()
    
    if choice == '0':
        for name, func in examples:
            print()
            func()
    elif choice.isdigit() and 1 <= int(choice) <= len(examples):
        examples[int(choice) - 1][1]()
    else:
        print("Invalid choice")


if __name__ == '__main__':
    main()
