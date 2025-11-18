# Video Thumbnail Extractor

A Python tool to extract thumbnails from video files, capturing frames from the last 1 second of each video.

**Two versions available:**
- **OpenCV version** (`thumbnail_extractor.py`) - Standard version using OpenCV
- **FFmpeg version** (`thumbnail_extractor_ffmpeg.py`) - **Optimized version** using FFmpeg (recommended for better performance)

## Features

- Extract thumbnail from a single video file
- Batch process entire folders of videos
- Captures frame from the last 1 second of each video
- Supports multiple video formats (MP4, AVI, MOV, MKV, FLV, WMV, WEBM)
- Saves thumbnails as JPEG images
- Creates organized output folder structure

## Requirements

### For OpenCV Version
- Python 3.6+
- OpenCV (cv2)

### For FFmpeg Version (Recommended)
- Python 3.6+
- FFmpeg (system installation required)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd Thumbnail-Extractor
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. **(For FFmpeg version only)** Install FFmpeg:

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download and install from [ffmpeg.org](https://ffmpeg.org/download.html)

## Usage

### Basic Usage

**FFmpeg Version (Recommended - Faster):**

Process a single video:
```bash
python thumbnail_extractor_ffmpeg.py /path/to/video.mp4
```

Process all videos in a folder:
```bash
python thumbnail_extractor_ffmpeg.py /path/to/videos/folder
```

**OpenCV Version:**

Process a single video:
```bash
python thumbnail_extractor.py /path/to/video.mp4
```

Process all videos in a folder:
```bash
python thumbnail_extractor.py /path/to/videos/folder
```

### Advanced Options

**Specify custom output folder:**

FFmpeg version:
```bash
python thumbnail_extractor_ffmpeg.py /path/to/videos -o /path/to/output
```

OpenCV version:
```bash
python thumbnail_extractor.py /path/to/videos -o /path/to/output
```

**FFmpeg version - Control quality (1=best, 31=worst):**
```bash
python thumbnail_extractor_ffmpeg.py /path/to/videos -q 2
```

### Examples

**Using FFmpeg version (recommended):**

1. Extract thumbnail from a single video file:
```bash
python thumbnail_extractor_ffmpeg.py my_video.mp4
```
This creates a `thumbnails` folder with the extracted thumbnail.

2. Process all videos in a folder:
```bash
python thumbnail_extractor_ffmpeg.py ./videos
```
This processes all supported video files in the `videos` folder and saves thumbnails to `./thumbnails`.

3. Use a custom output folder with high quality:
```bash
python thumbnail_extractor_ffmpeg.py ./videos -o ./my_thumbnails -q 1
```

**Using OpenCV version:**

1. Extract thumbnail from a single video file:
```bash
python thumbnail_extractor.py my_video.mp4
```

2. Process all videos in a folder:
```bash
python thumbnail_extractor.py ./videos -o ./my_thumbnails
```

## Output

- Thumbnails are saved as JPEG files
- Naming format: `{original_filename}_thumbnail.jpg`
- Default output folder: `thumbnails` (created automatically if it doesn't exist)

## Supported Video Formats

- MP4 (.mp4)
- AVI (.avi)
- MOV (.mov)
- MKV (.mkv)
- FLV (.flv)
- WMV (.wmv)
- WEBM (.webm)

## Performance Comparison

**FFmpeg Version vs OpenCV Version:**

The FFmpeg version is significantly faster because:
- **Direct seeking**: FFmpeg seeks directly to timestamps without decoding all previous frames
- **Optimized for video processing**: FFmpeg is specifically built for efficient video operations
- **Hardware acceleration**: Can utilize GPU acceleration when available
- **Lower memory usage**: Only loads the specific frame needed

**Recommended use:**
- **FFmpeg version**: Best for batch processing, large files, or when performance matters
- **OpenCV version**: Good for projects already using OpenCV or when FFmpeg is not available

## How It Works

**FFmpeg Version:**
1. Uses ffprobe to get the video duration
2. Calculates timestamp 1 second before the end
3. Uses FFmpeg to seek directly to that timestamp
4. Extracts a single frame and saves it as JPEG

**OpenCV Version:**
1. Opens each video file using OpenCV
2. Calculates the video's total duration and frame rate
3. Seeks to a frame approximately 1 second before the video ends
4. Captures that frame and saves it as a JPEG thumbnail
5. Organizes all thumbnails in the specified output folder

## Error Handling

The tool includes comprehensive error handling for:
- Missing or invalid video files
- Unsupported video formats
- Corrupted video files
- File system permissions issues

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
