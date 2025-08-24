# Remove The BG




<img width="1584" height="396" alt="Junk (2)-modified" src="https://github.com/user-attachments/assets/88978f11-7378-4da6-819c-0567df443b15" />

A self-contained Python package for removing backgrounds from images with no external dependencies.

## Features

- **Zero Dependencies**: Everything is bundled - just `pip install remove-the-bg` and you're ready to go
- **Simple CLI**: Just run `rem /path/to/your/images`
- **Batch Processing**: Processes entire folders of images
- **Multiple Formats**: Supports PNG, JPG, JPEG image formats
- **AI-Powered**: Uses advanced machine learning models for accurate background removal

## Installation

```bash
pip install remove-the-bg
```

## Usage

### Command Line

Remove backgrounds from all images in a folder:
```bash
rem /path/to/your/images
```

Remove background from a single image:
```bash
rem /path/to/image.jpg
```

### Python API

```python
from remove_the_bg import remove_background

# Remove background from a single image
remove_background('input.jpg', 'output.png')

# Process a folder
from remove_the_bg.cli import process_folder
process_folder('/path/to/images')
```

## How it Works

This package includes all necessary dependencies (rembg, Pillow) bundled within the package itself, so you don't need to worry about installing additional dependencies or dealing with version conflicts.

## License

MIT License - see LICENSE file for details.
