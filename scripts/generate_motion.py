import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

def create_frame(index, total_frames, width=1280, height=720):
    # Create a new image with a dark background
    image = Image.new('RGB', (width, height), color=(30, 30, 30))
    draw = ImageDraw.Draw(image)
    
    # Calculate animation parameters
    progress = index / total_frames
    center_x, center_y = width // 2, height // 2
    
    # Draw an animated circle
    radius = 50 + 100 * progress
    draw.ellipse([center_x - radius, center_y - radius, center_x + radius, center_y + radius], 
                 outline=(255, 255, 255), width=5)
    
    # Draw an animated rectangle
    rect_size = 100
    rect_x = (width - rect_size) * progress
    draw.rectangle([rect_x, height - 150, rect_x + rect_size, height - 50], fill=(0, 120, 215))
    
    # Save the frame
    frame_path = f"frame_{index:04d}.png"
    image.save(frame_path)
    return frame_path

def generate_video(output_filename="motion_graphics.mp4", fps=30, duration=3):
    total_frames = fps * duration
    frame_files = []
    
    print(f"Generating {total_frames} frames...")
    for i in range(total_frames):
        frame_files.append(create_frame(i, total_frames))
    
    print("Combining frames into video using FFmpeg...")
    ffmpeg_cmd = [
        'ffmpeg', '-y',
        '-framerate', str(fps),
        '-i', 'frame_%04d.png',
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        output_filename
    ]
    
    try:
        subprocess.run(ffmpeg_cmd, check=True, capture_output=True)
        print(f"Video generated successfully: {output_filename}")
    except subprocess.CalledProcessError as e:
        print(f"Error during video generation: {e.stderr.decode()}")
    finally:
        # Cleanup frames
        for f in frame_files:
            if os.path.exists(f):
                os.remove(f)

if __name__ == "__main__":
    generate_video()
