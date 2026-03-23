# OpenAI Whisper Guide

This guide covers the complete usage of OpenAI Whisper for audio transcription in the Manus sandbox environment.

## What is Whisper?

Whisper is OpenAI's state-of-the-art speech recognition model that can transcribe audio with high accuracy. It supports multiple languages and works entirely offline after the initial model download.

## Model Sizes and Performance

| Model | Size | RAM | Speed | Accuracy | Use Case |
|-------|------|-----|-------|----------|----------|
| tiny | 39 MB | ~1 GB | Very Fast | Basic | Quick tests, simple audio |
| base | 74 MB | ~1 GB | Fast | Good | General use, most languages |
| small | 244 MB | ~2 GB | Medium | Better | Complex audio, accents |
| medium | 769 MB | ~5 GB | Slow | High | Professional transcription |
| large | 1.5 GB | ~10 GB | Slowest | Best | Maximum accuracy needed |

## Installation

```bash
# Install Whisper
pip install openai-whisper

# Optional: GPU acceleration
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## Basic Usage

```python
import whisper

# Load model
model = whisper.load_model("base")

# Transcribe audio file
result = model.transcribe("audio.mp3")

# Get the text
text = result["text"]
print(text)
```

## Advanced Features

### Language Specification
```python
# Auto-detect language (default)
result = model.transcribe("audio.mp3")

# Force specific language
result = model.transcribe("audio.mp3", language="en")
result = model.transcribe("audio.mp3", language="es")
```

### Verbose Output
```python
# Get detailed information including timestamps
result = model.transcribe("audio.mp3", verbose=True)

print("Full text:", result["text"])
print("Language:", result["language"])
print("Segments:", len(result["segments"]))
```

### Custom Options
```python
# Advanced transcription options
result = model.transcribe("audio.mp3",
    temperature=0.0,          # Deterministic results
    no_speech_threshold=0.6,  # Speech detection sensitivity
    logprob_threshold=-1.0,   # Confidence threshold
    compression_ratio_threshold=2.4,  # Filter repetitive speech
    condition_on_previous_text=True   # Use context from previous segments
)
```

## Result Structure

```python
{
    "text": "Full transcription text",
    "language": "en",
    "segments": [
        {
            "start": 0.0,
            "end": 3.5,
            "text": "Hello, this is a test.",
            "tokens": [50364, 2425, 11, 341, 307, 257, 5604, 13, 50594],
            "temperature": 0.0,
            "avg_logprob": -0.187,
            "compression_ratio": 1.0,
            "no_speech_prob": 0.096
        }
    ]
}
```

## Supported Audio Formats

- **MP3**: Most common compressed format
- **WAV**: Uncompressed, highest quality
- **M4A/AAC**: Good compression ratio
- **FLAC**: Lossless compression
- **OGG**: Open source format

## Best Practices

### Audio Preparation
1. **Sample Rate**: 16kHz minimum, 44.1kHz optimal
2. **Channels**: Mono preferred for faster processing
3. **Bit Depth**: 16-bit or higher
4. **Normalize**: Consistent volume levels

### Performance Optimization
1. **Choose Right Model**: Balance speed vs accuracy
2. **GPU Usage**: Use CUDA for 3-5x speedup
3. **Batch Processing**: Process multiple files sequentially
4. **Memory Management**: Free models when done

### Accuracy Improvement
1. **Specify Language**: Explicit language often improves results
2. **Clean Audio**: Remove background noise
3. **Segment Long Audio**: Break into 10-30 minute chunks
4. **Use Context**: Enable `condition_on_previous_text`

## Troubleshooting

### Common Issues

**"Model download failed"**
- Check internet connection
- Use different model size
- Manual download from Hugging Face

**"CUDA out of memory"**
- Use smaller model
- Switch to CPU: `model = whisper.load_model("base", device="cpu")`
- Close other GPU applications

**"FFmpeg not found"**
- Install FFmpeg: `choco install ffmpeg` (Windows)
- Add to PATH environment variable

**Poor transcription quality**
- Try larger model
- Specify correct language
- Improve audio quality
- Check for strong accents

### Error Messages

```
ModuleNotFoundError: No module named 'whisper'
```
→ Install package: `pip install openai-whisper`

```
RuntimeError: CUDA out of memory
```
→ Use CPU or smaller model

```
FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'
```
→ Install FFmpeg and ensure it's in PATH

## Integration Examples

### With Video Files
```python
# Extract audio from video first
import subprocess

def extract_audio(video_path, audio_path):
    subprocess.run([
        'ffmpeg', '-i', video_path, '-vn', '-acodec', 'mp3', audio_path
    ])

# Then transcribe
extract_audio("video.mp4", "audio.mp3")
result = model.transcribe("audio.mp3")
```

### Batch Processing
```python
import os
from pathlib import Path

def batch_transcribe(audio_dir, output_dir):
    audio_files = Path(audio_dir).glob("*.mp3")

    for audio_file in audio_files:
        result = model.transcribe(str(audio_file))
        output_file = Path(output_dir) / f"{audio_file.stem}_transcript.txt"

        with open(output_file, 'w') as f:
            f.write(result["text"])

batch_transcribe("audio_files/", "transcripts/")
```

### Real-time Transcription
```python
# For live audio streams (requires additional setup)
import pyaudio
import wave

# Record audio chunk
# ... recording code ...

# Transcribe chunk
result = model.transcribe("chunk.wav")
print("Live transcription:", result["text"])
```

## Performance Benchmarks

Approximate processing speeds (on modern hardware):

- **tiny**: 10-15x real-time
- **base**: 4-6x real-time
- **small**: 2-3x real-time
- **medium**: 1-1.5x real-time
- **large**: 0.5-0.8x real-time

GPU acceleration provides 3-5x speedup over CPU.

## Language Support

Whisper supports 99 languages including:
- English (en)
- Spanish (es)
- French (fr)
- German (de)
- Italian (it)
- Portuguese (pt)
- Russian (ru)
- Japanese (ja)
- Korean (ko)
- Chinese (zh)
- Arabic (ar)
- Hindi (hi)
- And many more...

For best results, specify the language when known.
