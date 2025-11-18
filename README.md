# Video Thumbnail Extractor

A Python tool to extract thumbnails from video files, capturing frames from the last 1 second of each video.

## Features

- Extract thumbnail from a single video file
- Batch process entire folders of videos
- Captures frame from the last 1 second of each video
- Supports multiple video formats (MP4, AVI, MOV, MKV, FLV, WMV, WEBM)
- Saves thumbnails as JPEG images
- Creates organized output folder structure

## Requirements

- Python 3.6+
- OpenCV (cv2)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd Thumbnail-Extractor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

**Process a single video:**
```bash
python thumbnail_extractor.py /path/to/video.mp4
```

**Process all videos in a folder:**
```bash
python thumbnail_extractor.py /path/to/videos/folder
```

### Advanced Options

**Specify custom output folder:**
```bash
python thumbnail_extractor.py /path/to/videos -o /path/to/output
```

or

```bash
python thumbnail_extractor.py /path/to/videos --output /path/to/output
```

### Examples

1. Extract thumbnail from a single video file:
```bash
python thumbnail_extractor.py my_video.mp4
```
This creates a `thumbnails` folder with the extracted thumbnail.

2. Process all videos in a folder:
```bash
python thumbnail_extractor.py ./videos
```
This processes all supported video files in the `videos` folder and saves thumbnails to `./thumbnails`.

3. Use a custom output folder:
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

## How It Works

1. The tool opens each video file using OpenCV
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
