---
name: audio-transcription
description: "Transcribe uploaded audio files (MP3, WAV, M4A) to text using OpenAI Whisper. Generate clean text or SRT subtitles. Works offline after initial setup."
---

# Audio Transcription

This skill enables transcription of audio files to text using OpenAI Whisper, running locally via pip. Supports MP3, WAV, M4A formats with output as plain text or SRT subtitle files.

## Core Workflow

To transcribe an audio file:

1. **Prepare Audio**: Ensure file is in supported format (MP3, WAV, M4A) and accessible
2. **Run Transcription**: Use the script with your audio file
3. **Choose Output**: Get plain text transcription or SRT subtitles
4. **Process Results**: Use the generated text/subtitle file as needed

## Triggers
- "Transcribe this audio"
- "convert voice memo to text"
- "generate subtitles"

## Usage Examples

```bash
# Basic transcription to text
python scripts/transcribe_audio.py my_audio.mp3

# Generate SRT subtitles
python scripts/transcribe_audio.py my_audio.mp3 --output subtitles.srt

# Specify language (auto-detect by default)
python scripts/transcribe_audio.py my_audio.mp3 --language en
```

## Requirements
- **Python 3.8+**
- **openai-whisper**: `pip install openai-whisper`
- **FFmpeg**: Pre-installed or install via `choco install ffmpeg`
- **PyTorch**: Optional but recommended for GPU acceleration

## Bundled Resources

### Scripts
- `scripts/transcribe_audio.py`: Command-line tool for audio transcription

### References
- `references/whisper_guide.md`: Complete Whisper usage guide
- `references/audio_formats.md`: Supported formats and preprocessing
- `references/subtitles_guide.md`: SRT subtitle generation and formatting
