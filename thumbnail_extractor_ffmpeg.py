#!/usr/bin/env python3
"""
Video Thumbnail Extractor - FFmpeg Optimized Version
Extracts thumbnails from the last 1 second of video files using FFmpeg.
This version is significantly faster than the OpenCV version.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
import json


class FFmpegThumbnailExtractor:
    """Class to extract thumbnails from video files using FFmpeg."""

    SUPPORTED_FORMATS = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm']

    def __init__(self, output_folder='thumbnails'):
        """
        Initialize the FFmpegThumbnailExtractor.

        Args:
            output_folder (str): Path to the folder where thumbnails will be saved
        """
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(parents=True, exist_ok=True)
        self._check_ffmpeg()

    def _check_ffmpeg(self):
        """Check if ffmpeg is available in the system."""
        try:
            subprocess.run(['ffmpeg', '-version'],
                         capture_output=True,
                         check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Error: FFmpeg is not installed or not in PATH")
            print("Please install FFmpeg:")
            print("  Ubuntu/Debian: sudo apt-get install ffmpeg")
            print("  macOS: brew install ffmpeg")
            print("  Windows: Download from https://ffmpeg.org/download.html")
            sys.exit(1)

    def get_video_duration(self, video_path):
        """
        Get the duration of a video file using ffprobe.

        Args:
            video_path (Path): Path to the video file

        Returns:
            float: Duration in seconds, or None if failed
        """
        try:
            cmd = [
                'ffprobe',
                '-v', 'error',
                '-show_entries', 'format=duration',
                '-of', 'json',
                str(video_path)
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)

            if 'format' in data and 'duration' in data['format']:
                return float(data['format']['duration'])

            return None

        except (subprocess.CalledProcessError, json.JSONDecodeError, ValueError) as e:
            print(f"Error getting video duration: {e}")
            return None

    def extract_thumbnail(self, video_path, output_name=None, quality=2):
        """
        Extract a thumbnail from the last 1 second of a video using FFmpeg.

        Args:
            video_path (str or Path): Path to the video file
            output_name (str, optional): Custom name for the output thumbnail
            quality (int): Quality setting (1-31, lower is better, default: 2)

        Returns:
            bool: True if successful, False otherwise
        """
        video_path = Path(video_path)

        if not video_path.exists():
            print(f"Error: Video file not found: {video_path}")
            return False

        if video_path.suffix.lower() not in self.SUPPORTED_FORMATS:
            print(f"Warning: Unsupported format for {video_path.name}")
            return False

        # Get video duration
        duration = self.get_video_duration(video_path)

        if duration is None or duration <= 0:
            print(f"Error: Could not determine video duration for {video_path.name}")
            return False

        # Calculate timestamp for 1 second before the end
        # Use max to ensure we don't go negative
        timestamp = max(0, duration - 1.0)

        # Generate output filename
        if output_name is None:
            output_name = f"{video_path.stem}_thumbnail.jpg"
        elif not output_name.endswith(('.jpg', '.png')):
            output_name = f"{output_name}.jpg"

        output_path = self.output_folder / output_name

        try:
            # FFmpeg command to extract frame at specific timestamp
            # -ss before -i for fast seeking
            # -vframes 1 to extract only one frame
            # -q:v for quality (1-31, lower is better)
            cmd = [
                'ffmpeg',
                '-ss', str(timestamp),  # Seek to timestamp (fast seek before input)
                '-i', str(video_path),  # Input file
                '-vframes', '1',         # Extract only 1 frame
                '-q:v', str(quality),    # Quality setting
                '-y',                    # Overwrite output file
                str(output_path)
            ]

            # Run ffmpeg with suppressed output
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )

            if output_path.exists():
                print(f"✓ Saved thumbnail: {output_path}")
                return True
            else:
                print(f"Error: Thumbnail file was not created for {video_path.name}")
                return False

        except subprocess.CalledProcessError as e:
            print(f"Error processing {video_path.name}: FFmpeg failed")
            if e.stderr:
                print(f"  Details: {e.stderr[:200]}")  # Show first 200 chars of error
            return False
        except Exception as e:
            print(f"Error processing {video_path.name}: {str(e)}")
            return False

    def process_folder(self, folder_path):
        """
        Process all video files in a folder.

        Args:
            folder_path (str or Path): Path to the folder containing videos

        Returns:
            tuple: (successful_count, failed_count)
        """
        folder_path = Path(folder_path)

        if not folder_path.exists():
            print(f"Error: Folder not found: {folder_path}")
            return 0, 0

        if not folder_path.is_dir():
            print(f"Error: Path is not a directory: {folder_path}")
            return 0, 0

        # Find all video files
        video_files = []
        for ext in self.SUPPORTED_FORMATS:
            video_files.extend(folder_path.glob(f"*{ext}"))
            video_files.extend(folder_path.glob(f"*{ext.upper()}"))

        if not video_files:
            print(f"No video files found in {folder_path}")
            return 0, 0

        print(f"\nFound {len(video_files)} video file(s)")
        print(f"Output folder: {self.output_folder.absolute()}\n")

        successful = 0
        failed = 0

        for video_file in video_files:
            print(f"Processing: {video_file.name}")
            if self.extract_thumbnail(video_file):
                successful += 1
            else:
                failed += 1

        return successful, failed


def main():
    """Main function to run the FFmpeg thumbnail extractor."""
    parser = argparse.ArgumentParser(
        description='Extract thumbnails from the last 1 second of video files using FFmpeg (optimized).'
    )
    parser.add_argument(
        'input',
        help='Path to a video file or folder containing videos'
    )
    parser.add_argument(
        '-o', '--output',
        default='thumbnails',
        help='Output folder for thumbnails (default: thumbnails)'
    )
    parser.add_argument(
        '-q', '--quality',
        type=int,
        default=2,
        choices=range(1, 32),
        metavar='[1-31]',
        help='JPEG quality (1=best, 31=worst, default: 2)'
    )

    args = parser.parse_args()

    input_path = Path(args.input)

    if not input_path.exists():
        print(f"Error: Path not found: {input_path}")
        sys.exit(1)

    # Create extractor
    extractor = FFmpegThumbnailExtractor(output_folder=args.output)

    print("=" * 60)
    print("FFmpeg Video Thumbnail Extractor (Optimized)")
    print("=" * 60)

    # Process input
    if input_path.is_file():
        # Single file mode
        print(f"\nProcessing single video: {input_path.name}")
        print(f"Output folder: {extractor.output_folder.absolute()}\n")

        if extractor.extract_thumbnail(input_path, quality=args.quality):
            print("\n✓ Thumbnail extraction completed successfully!")
        else:
            print("\n✗ Thumbnail extraction failed!")
            sys.exit(1)

    elif input_path.is_dir():
        # Folder mode
        successful, failed = extractor.process_folder(input_path)

        print("\n" + "=" * 60)
        print(f"Summary: {successful} successful, {failed} failed")
        print("=" * 60)

        if failed > 0:
            sys.exit(1)

    else:
        print(f"Error: Invalid path: {input_path}")
        sys.exit(1)


if __name__ == '__main__':
    main()
