---
name: motion-graphics
description: "Generate motion graphics and animated videos using Python, FFmpeg, and Pillow. Use for: creating intro videos, data visualizations, animated diagrams, and text-based motion graphics."
---

# Motion Graphics

This skill enables the creation of programmatic motion graphics and animations within the Manus sandbox environment.

## Core Workflow

To create a motion graphics video, follow these steps:

1.  **Define Animation Parameters**: Determine the resolution (e.g., 1280x720), duration (e.g., 5 seconds), and framerate (e.g., 30 FPS).
2.  **Choose an Implementation Strategy**:
    *   **Frame-by-Frame (Recommended)**: Use Python with `Pillow` to draw each frame as an image, then assemble them with `FFmpeg`.
    *   **FFmpeg Filters**: Use complex filtergraphs for simpler animations like scrolls, zooms, and overlays.
    *   **Matplotlib Animation**: Best for mathematical or data-driven motion graphics.
3.  **Implement the Script**: Create a Python script (refer to `scripts/generate_motion.py` for a template) that:
    *   Calculates a `progress` variable (0.0 to 1.0) for each frame.
    *   Draws elements (shapes, text, images) based on the progress.
    *   Saves frames as numbered files (e.g., `frame_0001.png`).
4.  **Assemble and Encode**: Use `FFmpeg` to combine frames into a final video file (e.g., `.mp4`).
5.  **Clean Up**: Delete all temporary frame files after the video is generated.

## Bundled Resources

### Scripts
- `scripts/generate_motion.py`: A template script for frame-by-frame animation using Pillow and FFmpeg.

### References
- `references/techniques.md`: Detailed guide on animation techniques, FFmpeg filters, and best practices for high-quality output.

## Guidelines for Quality
- **Smoothness**: Use a consistent framerate (30 or 60 FPS).
- **Compatibility**: Always use `-pix_fmt yuv420p` in FFmpeg to ensure the output video plays correctly on all devices.
- **Resource Management**: The sandbox has limited storage; avoid generating thousands of high-resolution frames without cleanup.
- **Visuals**: Use `Pillow`'s `ImageDraw` for crisp vector-like shapes and `ImageFont` for professional typography.
