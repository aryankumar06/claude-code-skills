# Claude Skills Collection

A collection of specialized skills for Claude Code, providing powerful automation and creative tools for developers and content creators.

## Available Skills

### 🎬 Motion Graphics Skill
Generate motion graphics and animated videos using Python, FFmpeg, and Pillow. Perfect for creating intro videos, data visualizations, animated diagrams, and text-based motion graphics.

**Location**: `motion-graphics-skill/` (this directory)

### 🎵 Audio Transcription Skill
Transcribe uploaded audio files (MP3, WAV, M4A) to text using OpenAI Whisper. Generate clean text transcriptions or SRT subtitle files. Works offline after initial setup.

**Location**: `audio-transcription-skill/`

---

> **Note**: Each skill is self-contained in its own directory. See individual skill READMEs for detailed usage instructions.

## Features

- **Frame-by-Frame Animation**: Create custom animations by drawing each frame with Pillow
- **FFmpeg Integration**: Assemble frames into high-quality MP4 videos
- **Multiple Strategies**: Support for Pillow-based graphics, FFmpeg filters, and Matplotlib animations
- **Professional Output**: Generate 1080p, 720p, or custom resolution videos at 30 or 60 FPS
- **Easy Customization**: Template scripts make it simple to build animations for your specific use case

## Quick Start

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/aryankumar06/motion-graphics-skill.git
   cd motion-graphics-skill
   ```

2. For Claude Code, add to your project's `.claude/skills/` directory:
   ```bash
   cp -r . ~/.claude/skills/motion-graphics/
   ```

### Basic Usage

The skill includes a template script (`scripts/generate_motion.py`) that demonstrates frame-by-frame animation:

```python
from PIL import Image, ImageDraw

def create_frame(index, total_frames, width=1280, height=720):
    image = Image.new('RGB', (width, height), color=(30, 30, 30))
    draw = ImageDraw.Draw(image)
    
    progress = index / total_frames
    # Draw animated elements based on progress (0.0 to 1.0)
    
    image.save(f"frame_{index:04d}.png")
    return f"frame_{index:04d}.png"

def generate_video(output_filename="output.mp4", fps=30, duration=3):
    total_frames = fps * duration
    for i in range(total_frames):
        create_frame(i, total_frames)
    
    # Assemble with FFmpeg
    subprocess.run([
        'ffmpeg', '-y',
        '-framerate', str(fps),
        '-i', 'frame_%04d.png',
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        output_filename
    ])
```

## Core Concepts

### Animation Parameters

Define these before starting:
- **Resolution**: 1920x1080 (1080p), 1280x720 (720p), or custom
- **Duration**: Length in seconds
- **Framerate**: 30 FPS (standard) or 60 FPS (smooth)

### Progress Variable

The key to smooth animations is the `progress` variable (0.0 to 1.0):

```python
progress = current_frame / total_frames
# Use progress to animate elements:
# - Position: x = start_x + (end_x - start_x) * progress
# - Scale: size = min_size + (max_size - min_size) * progress
# - Opacity: alpha = start_alpha + (end_alpha - start_alpha) * progress
```

### Implementation Strategies

1. **Frame-by-Frame (Recommended)**: Use Pillow to draw each frame, then assemble with FFmpeg
2. **FFmpeg Filters**: Use complex filtergraphs for scrolls, zooms, and overlays
3. **Matplotlib**: Best for mathematical or data-driven animations

## Examples

### Example 1: Animated Circle

```python
import math
from PIL import Image, ImageDraw

def animated_circle(output_file="circle.mp4", fps=30, duration=2):
    total_frames = fps * duration
    
    for frame_idx in range(total_frames):
        progress = frame_idx / total_frames
        
        img = Image.new('RGB', (1280, 720), color=(20, 20, 20))
        draw = ImageDraw.Draw(img)
        
        # Animate circle radius
        radius = 50 + 150 * progress
        center_x, center_y = 640, 360
        
        draw.ellipse(
            [center_x - radius, center_y - radius, center_x + radius, center_y + radius],
            outline=(255, 100, 100),
            width=3
        )
        
        img.save(f"frame_{frame_idx:04d}.png")
    
    # Assemble video (see generate_motion.py for full FFmpeg command)
```

### Example 2: Text Animation

```python
from PIL import Image, ImageDraw, ImageFont

def animated_text(output_file="text.mp4", text="Hello Motion Graphics"):
    total_frames = 90
    font = ImageFont.load_default()
    
    for frame_idx in range(total_frames):
        progress = frame_idx / total_frames
        
        img = Image.new('RGB', (1280, 720), color=(30, 30, 30))
        draw = ImageDraw.Draw(img)
        
        # Animate text position (slide in from left)
        x = -500 + (640 + 500) * progress
        draw.text((x, 360), text, fill=(255, 255, 255), font=font)
        
        img.save(f"frame_{frame_idx:04d}.png")
```

## Best Practices

### Quality Guidelines

- **Smoothness**: Use consistent 30 or 60 FPS for professional results
- **Compatibility**: Always use `-pix_fmt yuv420p` in FFmpeg for universal playback
- **Resolution**: Default to 1920x1080 or 1280x720 for web compatibility
- **Cleanup**: Delete temporary frame files after video generation to save disk space

### Performance Tips

- Avoid generating thousands of high-resolution frames without cleanup
- Use Pillow's `ImageDraw` for crisp vector-like shapes
- Pre-calculate animation values before the frame loop for efficiency
- Consider generating lower-resolution previews first before final output

### Common Pitfalls

- **Forgetting cleanup**: Temporary frame files can consume significant disk space
- **Inconsistent framerate**: Mix of 30 and 60 FPS can cause stuttering
- **Wrong pixel format**: Videos may not play on all devices without `-pix_fmt yuv420p`
- **Missing progress variable**: Animations won't be smooth without proper interpolation

## Bundled Resources

### Scripts
- `scripts/generate_motion.py`: Template script for frame-by-frame animation using Pillow and FFmpeg

### References
- `references/techniques.md`: Detailed guide on animation techniques, FFmpeg filters, and best practices

## Requirements

- **Python 3.7+**
- **Pillow** (PIL): For image drawing
- **FFmpeg**: For video encoding (pre-installed on most systems)
- **Matplotlib** (optional): For data-driven animations

## Troubleshooting

### Video won't play on some devices
- Ensure you're using `-pix_fmt yuv420p` in FFmpeg command
- Try a lower resolution (1280x720 instead of 1920x1080)

### Frames not assembling into video
- Check that frame files are named sequentially: `frame_0000.png`, `frame_0001.png`, etc.
- Verify FFmpeg is installed: `ffmpeg -version`

### Animation is choppy or stutters
- Ensure consistent framerate throughout
- Verify all frames are the same resolution
- Check that progress variable is calculated correctly

### Out of disk space
- Implement cleanup to delete frame files after video generation
- Generate lower-resolution previews first
- Use a temporary directory for frame storage

## Contributing

We welcome contributions! If you have improvements, bug fixes, or new animation techniques to share:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request with a clear description

## License

This skill is provided as-is for use with Claude and compatible AI agents. See LICENSE.txt for details.

## Support

For questions, issues, or feature requests, please open an issue on GitHub or refer to the official SkillsMP documentation.

## Related Resources

- [Agent Skills Specification](https://github.com/anthropics/skills)
- [SkillsMP Marketplace](https://skillsmp.com)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [Pillow Documentation](https://pillow.readthedocs.io/)

---

**Created with ❤️ for the AI agent community**
