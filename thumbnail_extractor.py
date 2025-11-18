#!/usr/bin/env python3
"""
Video Thumbnail Extractor
Extracts thumbnails from the last 1 second of video files.
"""

import os
import sys
import cv2
import argparse
from pathlib import Path


class ThumbnailExtractor:
    """Class to extract thumbnails from video files."""

    SUPPORTED_FORMATS = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm']

    def __init__(self, output_folder='thumbnails', image_format='jpeg'):
        """
        Initialize the ThumbnailExtractor.

        Args:
            output_folder (str): Path to the folder where thumbnails will be saved
            image_format (str): Output image format ('jpeg' or 'png', default: 'jpeg')
        """
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(parents=True, exist_ok=True)
        self.image_format = image_format.lower()
        if self.image_format not in ['jpeg', 'png']:
            raise ValueError("image_format must be 'jpeg' or 'png'")
        self.file_extension = 'jpg' if self.image_format == 'jpeg' else 'png'

    def extract_thumbnail(self, video_path, output_name=None):
        """
        Extract a thumbnail from the last 1 second of a video.

        Args:
            video_path (str or Path): Path to the video file
            output_name (str, optional): Custom name for the output thumbnail

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

        # Open the video file
        cap = cv2.VideoCapture(str(video_path))

        if not cap.isOpened():
            print(f"Error: Could not open video: {video_path}")
            return False

        try:
            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            if total_frames == 0 or fps == 0:
                print(f"Error: Invalid video properties for {video_path.name}")
                return False

            # Calculate frame position for last 1 second
            # We'll get the frame 1 second before the end
            target_frame = max(0, total_frames - int(fps))

            # Set the position to the target frame
            cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)

            # Read the frame
            ret, frame = cap.read()

            if not ret:
                print(f"Error: Could not read frame from {video_path.name}")
                return False

            # Generate output filename
            if output_name is None:
                output_name = f"{video_path.stem}_thumbnail.{self.file_extension}"
            elif not output_name.endswith(('.jpg', '.jpeg', '.png')):
                output_name = f"{output_name}.{self.file_extension}"

            output_path = self.output_folder / output_name

            # Save the thumbnail with appropriate parameters
            if self.image_format == 'png':
                # PNG compression level (0-9, where 9 is maximum compression)
                cv2.imwrite(str(output_path), frame, [cv2.IMWRITE_PNG_COMPRESSION, 9])
            else:
                # JPEG quality (0-100, where 100 is best quality)
                cv2.imwrite(str(output_path), frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
            print(f"✓ Saved thumbnail: {output_path}")

            return True

        except Exception as e:
            print(f"Error processing {video_path.name}: {str(e)}")
            return False

        finally:
            cap.release()

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
    """Main function to run the thumbnail extractor."""
    parser = argparse.ArgumentParser(
        description='Extract thumbnails from the last 1 second of video files.'
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
        '-f', '--format',
        choices=['jpeg', 'png'],
        default='jpeg',
        help='Output image format (default: jpeg)'
    )

    args = parser.parse_args()

    input_path = Path(args.input)

    if not input_path.exists():
        print(f"Error: Path not found: {input_path}")
        sys.exit(1)

    # Create extractor
    extractor = ThumbnailExtractor(output_folder=args.output, image_format=args.format)

    print("=" * 60)
    print("Video Thumbnail Extractor")
    print("=" * 60)

    # Process input
    if input_path.is_file():
        # Single file mode
        print(f"\nProcessing single video: {input_path.name}")
        print(f"Output folder: {extractor.output_folder.absolute()}\n")

        if extractor.extract_thumbnail(input_path):
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
