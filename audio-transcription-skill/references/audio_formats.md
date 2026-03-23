# Audio Formats and Preprocessing Guide

This guide covers audio format support, conversion, and preprocessing techniques for optimal Whisper transcription results.

## Supported Audio Formats

Whisper supports most common audio formats through FFmpeg:

### Native Support
- **WAV**: Uncompressed, highest quality
- **FLAC**: Lossless compression
- **MP3**: Most common compressed format
- **M4A/AAC**: Good compression ratio
- **OGG/Opus**: Open source format

### FFmpeg-Dependent Formats
- **WMA**: Windows Media Audio
- **AIFF**: Apple format
- **AU**: Sun/Unix format
- **WebM**: Web audio format

## Audio Quality Guidelines

### Sample Rate
- **Minimum**: 16kHz (Whisper's native rate)
- **Recommended**: 44.1kHz or 48kHz
- **Maximum**: No strict limit, but higher rates increase processing time

### Bit Depth
- **Recommended**: 16-bit or 24-bit
- **Minimum**: 8-bit (acceptable but lower quality)

### Channels
- **Mono**: Preferred for faster processing
- **Stereo**: Automatically converted to mono by Whisper

## Preprocessing Techniques

### Audio Normalization
```python
import subprocess

def normalize_audio(input_file, output_file):
    """Normalize audio volume levels"""
    subprocess.run([
        'ffmpeg',
        '-i', input_file,
        '-af', 'loudnorm',
        '-c:a', 'mp3',
        output_file
    ])

# Usage
normalize_audio('noisy_audio.mp3', 'normalized_audio.mp3')
```

### Noise Reduction
```python
def reduce_noise(input_file, output_file):
    """Apply noise reduction filter"""
    subprocess.run([
        'ffmpeg',
        '-i', input_file,
        '-af', 'highpass=f=80,lowpass=f=3400',
        '-c:a', 'mp3',
        output_file
    ])

# Usage
reduce_noise('noisy_audio.mp3', 'clean_audio.mp3')
```

### Convert to Mono
```python
def convert_to_mono(input_file, output_file):
    """Convert stereo to mono"""
    subprocess.run([
        'ffmpeg',
        '-i', input_file,
        '-ac', '1',  # 1 channel (mono)
        '-c:a', 'mp3',
        output_file
    ])

# Usage
convert_to_mono('stereo_audio.mp3', 'mono_audio.mp3')
```

### Resample Audio
```python
def resample_audio(input_file, output_file, sample_rate=16000):
    """Resample to optimal rate for Whisper"""
    subprocess.run([
        'ffmpeg',
        '-i', input_file,
        '-ar', str(sample_rate),  # Sample rate
        '-c:a', 'mp3',
        output_file
    ])

# Usage
resample_audio('high_rate.wav', 'resampled.mp3', 16000)
```

## Format Conversion

### Convert Any Format to MP3
```python
def convert_to_mp3(input_file, output_file):
    """Convert any audio format to MP3"""
    subprocess.run([
        'ffmpeg',
        '-i', input_file,
        '-c:a', 'libmp3lame',
        '-q:a', '2',  # High quality
        output_file
    ])

# Usage
convert_to_mp3('audio.m4a', 'audio.mp3')
```

### Convert Video to Audio
```python
def extract_audio_from_video(video_file, audio_file):
    """Extract audio track from video file"""
    subprocess.run([
        'ffmpeg',
        '-i', video_file,
        '-vn',  # No video
        '-c:a', 'libmp3lame',
        '-q:a', '2',
        audio_file
    ])

# Usage
extract_audio_from_video('lecture.mp4', 'lecture_audio.mp3')
```

## Batch Processing

### Process Multiple Files
```python
from pathlib import Path
import subprocess

def batch_convert(directory, output_dir, target_format='mp3'):
    """Convert all audio files in directory"""
    input_path = Path(directory)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    audio_extensions = ['.wav', '.flac', '.m4a', '.ogg', '.wma', '.aiff']

    for file_path in input_path.rglob('*'):
        if file_path.suffix.lower() in audio_extensions:
            output_file = output_path / f"{file_path.stem}.{target_format}"

            print(f"Converting: {file_path} -> {output_file}")
            subprocess.run([
                'ffmpeg',
                '-i', str(file_path),
                '-c:a', 'libmp3lame' if target_format == 'mp3' else 'pcm_s16le',
                str(output_file)
            ])

# Usage
batch_convert('raw_audio/', 'processed_audio/')
```

## Quality Assessment

### Audio Quality Check
```python
def check_audio_quality(file_path):
    """Get audio file properties"""
    result = subprocess.run([
        'ffprobe',
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_format',
        '-show_streams',
        file_path
    ], capture_output=True, text=True)

    import json
    data = json.loads(result.stdout)

    for stream in data['streams']:
        if stream['codec_type'] == 'audio':
            print(f"Codec: {stream['codec_name']}")
            print(f"Sample Rate: {stream['sample_rate']} Hz")
            print(f"Channels: {stream['channels']}")
            print(f"Bit Rate: {stream.get('bit_rate', 'N/A')}")
            break

# Usage
check_audio_quality('audio.mp3')
```

## Common Issues and Solutions

### "Invalid audio file" Error
**Cause**: Unsupported format or corrupted file
**Solution**: Convert to MP3 or WAV first

### Poor Transcription Quality
**Cause**: Low bitrate, background noise, or poor recording
**Solutions**:
- Normalize volume
- Apply noise reduction
- Convert to higher quality format
- Ensure minimum 16kHz sample rate

### Long Processing Time
**Cause**: High sample rate or long audio file
**Solutions**:
- Resample to 16kHz
- Split long files into segments
- Use GPU acceleration

### Memory Issues
**Cause**: Large audio files or high sample rates
**Solutions**:
- Convert to mono
- Reduce sample rate
- Split into smaller chunks

## Advanced Preprocessing

### Voice Activity Detection
```python
def detect_speech_segments(audio_file, threshold=0.3):
    """Detect segments with speech (requires additional libraries)"""
    # This would require libraries like pyAudioAnalysis
    # Basic implementation using Whisper's VAD
    model = whisper.load_model("base")
    result = model.transcribe(audio_file, verbose=True)

    speech_segments = []
    for segment in result['segments']:
        # Filter segments above threshold
        if segment.get('no_speech_prob', 1.0) < threshold:
            speech_segments.append(segment)

    return speech_segments
```

### Automatic Gain Control
```python
def apply_agc(input_file, output_file):
    """Apply automatic gain control"""
    subprocess.run([
        'ffmpeg',
        '-i', input_file,
        '-af', 'agc',
        '-c:a', 'mp3',
        output_file
    ])
```

## Performance Optimization

### Parallel Processing
```python
import concurrent.futures
from pathlib import Path

def process_audio_batch(audio_files, model_size='base'):
    """Process multiple audio files in parallel"""
    model = whisper.load_model(model_size)

    def transcribe_single(file_path):
        result = model.transcribe(str(file_path))
        return file_path, result

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(transcribe_single, audio_files))

    return results

# Usage
audio_files = list(Path('batch_audio/').glob('*.mp3'))
results = process_audio_batch(audio_files)
```

### Memory Management
```python
def transcribe_with_memory_management(audio_file, model_size='base', chunk_size=600):
    """Transcribe long audio in chunks to manage memory"""
    import math

    # Get audio duration
    probe = subprocess.run([
        'ffprobe', '-v', 'quiet', '-print_format', 'json',
        '-show_format', audio_file
    ], capture_output=True, text=True)

    import json
    duration = float(json.loads(probe.stdout)['format']['duration'])

    model = whisper.load_model(model_size)
    full_transcript = []

    # Process in chunks
    for start_time in range(0, int(duration), chunk_size):
        end_time = min(start_time + chunk_size, duration)

        # Extract chunk
        chunk_file = f"temp_chunk_{start_time}.mp3"
        subprocess.run([
            'ffmpeg', '-i', audio_file,
            '-ss', str(start_time), '-t', str(chunk_size),
            '-c:a', 'mp3', chunk_file
        ])

        # Transcribe chunk
        result = model.transcribe(chunk_file)
        full_transcript.extend(result['segments'])

        # Clean up
        os.remove(chunk_file)

    # Combine results
    combined_text = ' '.join([seg['text'] for seg in full_transcript])
    return {'text': combined_text, 'segments': full_transcript}
```

## Recommended Workflow

1. **Initial Check**: Verify audio format and quality
2. **Preprocessing**: Apply normalization and noise reduction if needed
3. **Format Conversion**: Convert to MP3 with optimal settings
4. **Transcription**: Use Whisper with appropriate model size
5. **Post-processing**: Generate SRT or text output as needed

This ensures consistent, high-quality transcription results across different audio sources.
