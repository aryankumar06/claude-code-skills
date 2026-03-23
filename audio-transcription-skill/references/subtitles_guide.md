# SRT Subtitles Guide

This guide covers SRT (SubRip) subtitle format generation, formatting, and usage for video content.

## What is SRT Format?

SRT (SubRip Text) is the most common subtitle format used worldwide. It displays synchronized text over video content, commonly used for:
- Movie subtitles
- TV show captions
- Video tutorials
- Language translation
- Accessibility (closed captions)

## SRT File Structure

```
1
00:00:01,000 --> 00:00:04,500
Hello, welcome to this video tutorial.

2
00:00:04,500 --> 00:00:08,200
Today we'll learn about audio transcription.

3
00:00:08,200 --> 00:00:12,800
This process uses OpenAI's Whisper model.
```

### Components:
- **Sequence Number**: Incremental counter (1, 2, 3...)
- **Timestamp**: Start --> End time (HH:MM:SS,mmm format)
- **Text**: Subtitle text (1-3 lines recommended)

## Time Format

- **Hours**: 00-99 (HH)
- **Minutes**: 00-59 (MM)
- **Seconds**: 00-59 (SS)
- **Milliseconds**: 000-999 (mmm)

Examples:
- `00:00:05,000` = 5 seconds
- `00:01:30,500` = 1 minute, 30.5 seconds
- `01:15:45,250` = 1 hour, 15 minutes, 45.25 seconds

## Best Practices

### Timing Guidelines
- **Display Time**: 1-7 seconds per subtitle
- **Reading Speed**: 150-200 words per minute
- **Line Length**: 35-40 characters per line
- **Line Count**: 1-3 lines maximum

### Text Formatting
- **Case**: Sentence case preferred
- **Punctuation**: Proper grammar and punctuation
- **Numbers**: Spell out or use numerals consistently
- **Speaker Identification**: Use names when multiple speakers

### Positioning
- **Line Breaks**: Use `\n` or actual line breaks
- **Alignment**: Default is bottom center
- **Styling**: Basic SRT doesn't support styling

## Generating SRT from Whisper

```python
def generate_srt(whisper_result, output_file):
    """Convert Whisper result to SRT format"""

    with open(output_file, 'w', encoding='utf-8') as f:
        for i, segment in enumerate(whisper_result['segments'], 1):
            # Convert timestamps to SRT format
            start_time = format_timestamp(segment['start'])
            end_time = format_timestamp(segment['end'])

            # Write SRT entry
            f.write(f"{i}\n")
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{segment['text'].strip()}\n\n")

def format_timestamp(seconds):
    """Convert seconds to SRT timestamp format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)

    return "02d"

# Usage
result = model.transcribe("audio.mp3")
generate_srt(result, "subtitles.srt")
```

## Advanced SRT Features

### Multi-line Subtitles
```
1
00:00:01,000 --> 00:00:04,500
Hello, welcome to this video tutorial
about audio transcription technology.

2
00:00:04,500 --> 00:00:08,200
We'll explore how Whisper
can convert speech to text.
```

### Handling Long Segments
```python
def split_long_segments(segments, max_length=3.0):
    """Split segments longer than max_length seconds"""
    split_segments = []

    for segment in segments:
        duration = segment['end'] - segment['start']

        if duration <= max_length:
            split_segments.append(segment)
        else:
            # Split into smaller chunks
            num_splits = int(duration // max_length) + 1
            chunk_duration = duration / num_splits

            for i in range(num_splits):
                start = segment['start'] + (i * chunk_duration)
                end = min(start + chunk_duration, segment['end'])

                split_segment = segment.copy()
                split_segment['start'] = start
                split_segment['end'] = end
                split_segments.append(split_segment)

    return split_segments
```

## Quality Control

### Common Issues and Fixes

**Overlapping Timestamps**
```
Problem:
1
00:00:01,000 --> 00:00:04,000
Hello world
2
00:00:03,500 --> 00:00:06,000
How are you?

Fix: Adjust overlapping times
```

**Too Long Display Time**
```
Problem: Text displays for 15+ seconds
Fix: Break into smaller segments
```

**Missing Punctuation**
```
Problem: Running text without breaks
Fix: Add proper punctuation and line breaks
```

### Validation Script
```python
def validate_srt(file_path):
    """Basic SRT validation"""
    errors = []

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    i = 0
    seq_num = 1

    while i < len(lines):
        # Check sequence number
        try:
            if int(lines[i].strip()) != seq_num:
                errors.append(f"Wrong sequence number at line {i+1}")
        except ValueError:
            errors.append(f"Invalid sequence number at line {i+1}")

        i += 1

        # Check timestamp format
        if i >= len(lines) or '-->' not in lines[i]:
            errors.append(f"Missing timestamp at line {i+1}")
            break

        # Basic timestamp validation
        timestamp = lines[i].strip()
        if not re.match(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', timestamp):
            errors.append(f"Invalid timestamp format at line {i+1}")

        i += 1

        # Check text exists
        text_lines = 0
        while i < len(lines) and lines[i].strip():
            text_lines += 1
            i += 1

        if text_lines == 0:
            errors.append(f"Missing text for subtitle {seq_num}")

        # Skip empty line
        if i < len(lines) and not lines[i].strip():
            i += 1

        seq_num += 1

    return errors

# Usage
errors = validate_srt("subtitles.srt")
if errors:
    print("SRT Validation Errors:")
    for error in errors:
        print(f"- {error}")
else:
    print("SRT file is valid!")
```

## Integration with Video Editors

### Adding SRT to Video (FFmpeg)
```bash
# Burn subtitles into video
ffmpeg -i video.mp4 -vf "subtitles=subtitles.srt" output_with_subs.mp4

# Add subtitles as separate track
ffmpeg -i video.mp4 -i subtitles.srt -c copy -c:s mov_text output_with_subs.mp4
```

### Popular Video Editors
- **DaVinci Resolve**: Import SRT files directly
- **Adobe Premiere**: Import as caption files
- **Final Cut Pro**: Import SRT files
- **CapCut**: Supports SRT import/export
- **iMovie**: Limited SRT support

## Language and Encoding

### UTF-8 Support
- Save SRT files as UTF-8 for international characters
- Include BOM if required by some players
- Test with target video player

### Multi-language Subtitles
```
1
00:00:01,000 --> 00:00:04,500
Hello, welcome to this tutorial.

2
00:00:04,500 --> 00:00:08,200
こんにちは、このチュートリアルへようこそ。

3
00:00:08,200 --> 00:00:12,800
Hola, bienvenido a este tutorial.
```

## Conversion Tools

### SRT to Other Formats
```bash
# Convert SRT to VTT (WebVTT)
ffmpeg -i subtitles.srt subtitles.vtt

# Convert SRT to ASS (Advanced SubStation)
# Requires additional tools or manual conversion
```

### Other Formats to SRT
```bash
# VTT to SRT
ffmpeg -i subtitles.vtt subtitles.srt

# WebVTT to SRT
# Manual conversion or use online tools
```

## Performance Considerations

### File Size
- SRT files are very small text files
- No impact on video file size when burned in
- Minimal storage requirements

### Sync Accuracy
- Timestamps must match video exactly
- Account for audio delay in video files
- Test on target playback device

### Display Performance
- Modern devices handle SRT smoothly
- No performance impact on playback
- Hardware acceleration not required
