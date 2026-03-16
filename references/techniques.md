# Motion Graphics Techniques in Manus Sandbox

This document outlines the primary methods for creating motion graphics using pre-installed tools in the Manus environment.

## Core Tools
- **FFmpeg**: The primary engine for video encoding, frame assembly, and basic filters.
- **Pillow (PIL)**: Used for drawing 2D graphics, text, and handling image frames.
- **Matplotlib**: Ideal for data-driven animations and mathematical visualizations.

## Key Workflows

### 1. Frame-by-Frame Generation (Recommended)
This is the most flexible approach for custom graphics.
1. Define animation parameters (duration, FPS, resolution).
2. Use `Pillow` to draw each frame based on a `progress` variable (0.0 to 1.0).
3. Save frames as numbered images (e.g., `frame_0001.png`).
4. Assemble using FFmpeg:
   ```bash
   ffmpeg -y -framerate 30 -i frame_%04d.png -c:v libx264 -pix_fmt yuv420p output.mp4
   ```

### 2. FFmpeg Filter-Based Animation
For simpler effects like scrolls, fades, or overlays without external libraries.
- **Scrolling Text**:
  ```bash
  ffmpeg -f lavfi -i color=c=black:s=1280x720:d=10 -vf "drawtext=text='MOTION GRAPHICS':fontcolor=white:fontsize=64:x=w-mod(t*100\,w+tw):y=h/2" output.mp4
  ```
- **Zoom Effect**:
  ```bash
  ffmpeg -i image.jpg -vf "zoompan=z='min(zoom+0.0015,1.5)':d=125:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1280x720" output.mp4
  ```

### 3. Matplotlib Animation
Best for scientific or data-related motion graphics.
```python
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
# Define update function and create animation
# Save using writer='ffmpeg'
```

## Tips for High-Quality Output
- **Resolution**: Default to 1920x1080 (1080p) or 1280x720 (720p).
- **Framerate**: Use 30 or 60 FPS for smooth motion.
- **Pixel Format**: Always use `-pix_fmt yuv420p` for maximum compatibility with video players.
- **Cleanup**: Always delete temporary frame files after video generation to save disk space.
