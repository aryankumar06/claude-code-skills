# Audio Transcription Skill

Transcribe uploaded audio files (MP3, WAV, M4A) to text using OpenAI Whisper. Runs locally via pip, works offline after initial model download. Generate clean text transcriptions or SRT subtitle files.

## Overview

The **Audio Transcription Skill** provides seamless audio-to-text conversion using OpenAI's Whisper model. Perfect for transcribing voice memos, lectures, meetings, or any audio content. Works entirely offline once the model is downloaded.

## Features

- **Multiple Formats**: Supports MP3, WAV, M4A audio files
- **Offline Processing**: Works without internet after initial setup
- **Dual Output**: Generate plain text or SRT subtitle files
- **Language Detection**: Automatic language detection with manual override
- **GPU Acceleration**: Optional CUDA support for faster processing
- **High Accuracy**: State-of-the-art speech recognition

## Quick Start

### Installation

1. Install OpenAI Whisper:
   ```bash
   pip install openai-whisper
   ```

2. Install FFmpeg (required for audio processing):
   ```bash
   # Windows (Chocolatey)
   choco install ffmpeg

   # macOS
   brew install ffmpeg

   # Linux
   sudo apt install ffmpeg
   ```

3. Optional: Install PyTorch with CUDA for GPU acceleration:
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

### Basic Usage

```bash
# Navigate to the skill directory
cd audio-transcription-skill

# Transcribe audio to text (default output: transcription.txt)
python scripts/transcribe_audio.py path/to/your/audio.mp3

# Generate SRT subtitles
python scripts/transcribe_audio.py path/to/your/audio.mp3 --output subtitles.srt

# Specify language (helps with accuracy)
python scripts/transcribe_audio.py path/to/your/audio.mp3 --language en
```

## Core Concepts

### Supported Formats
- **MP3**: Most common compressed format
- **WAV**: Uncompressed, highest quality
- **M4A**: AAC compressed, good quality/size balance

### Output Formats
- **Text (.txt)**: Plain text transcription with timestamps
- **SRT (.srt)**: Standard subtitle format for videos

### Model Sizes
- **tiny**: Fastest, least accurate (~39 MB)
- **base**: Good balance (~74 MB)
- **small**: Better accuracy (~244 MB)
- **medium**: High accuracy (~769 MB)
- **large**: Best accuracy (~1550 MB)

## Examples

### Example 1: Basic Transcription
```bash
python scripts/transcribe_audio.py lecture.mp3
```
Output: `transcription.txt` with the full text and timestamps.

### Example 2: Generate Subtitles
```bash
python scripts/transcribe_audio.py podcast.mp3 --output podcast.srt --model medium
```
Output: `podcast.srt` subtitle file compatible with video editors.

### Example 3: Language-Specific Transcription
```bash
python scripts/transcribe_audio.py interview.wav --language es --model base
```
Forces Spanish language detection for better accuracy.

## Best Practices

### Audio Quality
- **Clean Audio**: Remove background noise for better results
- **Sample Rate**: 16kHz or higher recommended
- **Mono**: Convert stereo to mono for faster processing
- **Volume**: Normalize audio levels

### Performance Tips
- **Model Selection**: Use smaller models for simple audio, larger for complex
- **GPU Usage**: Enable CUDA if available for 3-5x speedup
- **Batch Processing**: Process multiple files sequentially
- **Temp Space**: Ensure adequate disk space for model download

### Common Pitfalls
- **Wrong Format**: Convert unsupported formats first
- **Poor Quality**: Very low bitrate audio may have accuracy issues
- **Missing Dependencies**: Ensure FFmpeg and Whisper are properly installed
- **Large Files**: Split very long audio files for better performance

## Bundled Resources

### Scripts
- `scripts/transcribe_audio.py`: Main transcription tool with CLI options

### References
- `references/whisper_guide.md`: Complete Whisper API documentation
- `references/audio_formats.md`: Audio format conversion and optimization
- `references/subtitles_guide.md`: SRT format specification and usage

## Requirements

- **Python 3.8+**
- **openai-whisper**: Core transcription library
- **FFmpeg**: Audio processing and format conversion
- **PyTorch** (optional): GPU acceleration support

## Troubleshooting

### "Module not found" errors
- Ensure `pip install openai-whisper` completed successfully
- Check Python version compatibility (3.8+ required)

### FFmpeg not found
- Install FFmpeg using package manager
- Add FFmpeg to system PATH
- Verify installation: `ffmpeg -version`

### CUDA/GPU issues
- Install correct PyTorch version for your CUDA version
- Fallback to CPU if GPU memory insufficient
- Check GPU memory requirements for large models

### Poor transcription quality
- Try larger model size
- Specify correct language
- Improve audio quality (noise reduction, normalization)
- Check for accents or specialized vocabulary

### Out of memory errors
- Use smaller model (tiny/base instead of medium/large)
- Process shorter audio segments
- Close other GPU-intensive applications
- Switch to CPU processing if needed

## Contributing

Contributions welcome! Areas for improvement:
- Additional audio format support
- Batch processing capabilities
- Integration with video editors
- Custom vocabulary/dictionary support

## License

Provided as-is for use with Claude and compatible AI agents.

## Support

For issues or questions:
- Check the troubleshooting section above
- Review the reference guides in `references/`
- Open an issue on the project repository

---

**Created for seamless audio transcription workflows** 🎵✨
