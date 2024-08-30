# extract_frames

A command-line tool to extract high-quality frames from videos.

## Installation

You can install `extract_frames` directly from PyPI:

```
pip install extract_frames
```

Or, if you've cloned the repository:

```
pip install .
```

## Usage

Basic usage:

```
extract_frames /path/to/video.mp4 /path/to/output/folder
```

This will extract the 10 highest quality frames from the video.

Options:

- `-n, --num-frames`: Specify the number of frames to extract (default: 10)
- `--iframes-only`: Extract only I-frames

Example with options:

```
extract_frames /path/to/video.mp4 /path/to/output/folder -n 20 --iframes-only
```

This will extract up to 20 high-quality I-frames from the video.

## License

This project is licensed under the MIT License.# extract_frames
