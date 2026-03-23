#!/usr/bin/env python3
"""
Audio Transcription Script using OpenAI Whisper

This script transcribes audio files (MP3, WAV, M4A) to text using OpenAI Whisper.
Supports output as plain text or SRT subtitle format.

Usage:
    python transcribe_audio.py audio_file.mp3
    python transcribe_audio.py audio_file.mp3 --output subtitles.srt
    python transcribe_audio.py audio_file.mp3 --language en --model base

Requirements:
    - pip install openai-whisper
    - FFmpeg (for audio processing)
"""

import argparse
import os
import sys
import time
from pathlib import Path

try:
    import whisper
except ImportError:
    print("Error: openai-whisper not installed. Run: pip install openai-whisper")
    sys.exit(1)

def format_timestamp(seconds):
    """Convert seconds to SRT timestamp format (HH:MM:SS,mmm)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)

    return "02d"

def generate_srt(result, output_file):
    """Generate SRT subtitle file from Whisper result"""
    print(f"Generating SRT subtitles: {output_file}")

    with open(output_file, 'w', encoding='utf-8') as f:
        for i, segment in enumerate(result['segments'], 1):
            start_time = format_timestamp(segment['start'])
            end_time = format_timestamp(segment['end'])
            text = segment['text'].strip()

            f.write(f"{i}\n")
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{text}\n\n")

    print(f"SRT file created: {output_file}")

def generate_text(result, output_file):
    """Generate plain text transcription"""
    print(f"Generating text transcription: {output_file}")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result['text'])

    print(f"Text file created: {output_file}")

def check_dependencies():
    """Check if required dependencies are available"""
    # Check FFmpeg
    import subprocess
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Warning: FFmpeg not found. Audio processing may fail.")
        print("Install FFmpeg: choco install ffmpeg (Windows)")
        return False
    return True

def main():
    parser = argparse.ArgumentParser(description='Transcribe audio using OpenAI Whisper')
    parser.add_argument('audio_file', help='Path to audio file (MP3, WAV, M4A)')
    parser.add_argument('--output', '-o', help='Output file path (default: transcription.txt or based on extension)')
    parser.add_argument('--model', '-m', default='base',
                       choices=['tiny', 'base', 'small', 'medium', 'large'],
                       help='Whisper model size (default: base)')
    parser.add_argument('--language', '-l', help='Language code (e.g., en, es, fr). Auto-detect if not specified')
    parser.add_argument('--device', '-d', default='auto', choices=['auto', 'cpu', 'cuda'],
                       help='Device to use (default: auto)')

    args = parser.parse_args()

    # Check if audio file exists
    audio_path = Path(args.audio_file)
    if not audio_path.exists():
        print(f"Error: Audio file not found: {audio_path}")
        sys.exit(1)

    # Check dependencies
    check_dependencies()

    # Determine output file
    if args.output:
        output_path = Path(args.output)
    else:
        # Default output based on input filename
        base_name = audio_path.stem
        output_path = Path(f"{base_name}_transcription.txt")

    # Determine output format
    if output_path.suffix.lower() == '.srt':
        output_format = 'srt'
    else:
        output_format = 'txt'

    print(f"Loading Whisper model: {args.model}")
    start_time = time.time()

    try:
        # Load model
        model = whisper.load_model(args.model, device=args.device)
        load_time = time.time() - start_time
        print(".1f")

        print(f"Transcribing: {audio_path}")
        transcribe_start = time.time()

        # Transcribe
        result = model.transcribe(
            str(audio_path),
            language=args.language if args.language else None,
            verbose=False
        )

        transcribe_time = time.time() - transcribe_start
        duration = result.get('segments', [])[-1]['end'] if result.get('segments') else 0
        speed = duration / transcribe_time if transcribe_time > 0 else 0

        print(".1f")
        print(".2f")
        print(f"Detected language: {result.get('language', 'unknown')}")

        # Generate output
        if output_format == 'srt':
            generate_srt(result, output_path)
        else:
            generate_text(result, output_path)

        print("\nTranscription completed successfully!")

    except Exception as e:
        print(f"Error during transcription: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
