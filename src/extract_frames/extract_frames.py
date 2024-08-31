import os
from typing import Tuple

import click
import cv2
import numpy as np


def calculate_metrics(frame: np.ndarray) -> Tuple[float, float, float, float]:
    """Calculate image quality metrics for a given frame."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Sharpness
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    sharpness = np.var(laplacian)

    # Contrast
    contrast = np.std(gray)

    # Exposure (average pixel intensity)
    exposure = np.mean(gray)

    # Feature density
    orb = cv2.ORB_create()
    keypoints = orb.detect(gray, None)
    feature_density = len(keypoints)

    return sharpness, contrast, exposure, feature_density


def is_iframe(cap: cv2.VideoCapture, frame_count: int) -> bool:
    """Check if the current frame is an I-frame."""
    return cap.get(cv2.CAP_PROP_POS_FRAMES) == frame_count


def extract_frames(
    video_path: str, output_folder: str, num_frames: int, iframes_only: bool
) -> None:
    """Extract frames from the video."""
    cap = cv2.VideoCapture(video_path)

    frames = []
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if not iframes_only or is_iframe(cap, frame_count):
            metrics = calculate_metrics(frame)
            frames.append((frame_count, frame, metrics))

        frame_count += 1

        # Print progress
        if frame_count % 100 == 0:
            click.echo(f"Processed {frame_count} frames...")

    cap.release()

    click.echo(f"Total frames processed: {frame_count}")
    click.echo(f"Frames meeting criteria: {len(frames)}")

    # Sort frames by sharpness (first metric)
    frames.sort(key=lambda x: x[2][0], reverse=True)

    # Save top N frames
    for i, (original_count, frame, metrics) in enumerate(frames[:num_frames]):
        output_path = os.path.join(
            output_folder, f"frame_{i+1:03d}_original_{original_count:05d}.jpg"
        )
        cv2.imwrite(output_path, frame)
        click.echo(f"Saved frame {i+1}: {output_path}")
        click.echo(
            f"  Metrics - Sharpness: {metrics[0]:.2f}, Contrast: {metrics[1]:.2f}, "
            f"Exposure: {metrics[2]:.2f}, Feature Density: {metrics[3]:.2f}"
        )


@click.command()
@click.argument("video_path", type=click.Path(exists=True))
@click.argument("output_folder", type=click.Path())
@click.option(
    "-n", "--num-frames", default=10, help="Number of frames to extract (default: 10)"
)
@click.option("--iframes-only", is_flag=True, help="Extract only I-frames")
def main(
    video_path: str, output_folder: str, num_frames: int, iframes_only: bool
) -> None:
    """Extract high-quality frames from a video."""
    click.echo(f"Extracting frames from: {video_path}")
    click.echo(f"Output folder: {output_folder}")
    click.echo(f"Number of frames to extract: {num_frames}")
    click.echo(f"I-frames only: {'Yes' if iframes_only else 'No'}")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        click.echo(f"Created output folder: {output_folder}")

    extract_frames(video_path, output_folder, num_frames, iframes_only)

    click.echo("Frame extraction completed successfully!")


if __name__ == "__main__":
    main()
