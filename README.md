# cli-commons

Reusable CLI utilities for consistent command-line interfaces in Python.

This package provides common building blocks for standardized, professional Python CLI tools:

- Standardized logging (file + console) with verbose/quiet modes
- ANSI color utilities and message formatting templates
- Conventional directory layout helpers
- File operations for batch processing with progress tracking
- Argument parser with a consistent set of flags
- Pure Python (stdlib only)

## Installation

### From PyPI

```bash
pip install cli-commons
```

### Development (editable)

```bash
git clone https://github.com/yourusername/cli-commons.git
cd cli-commons
pip install -e .
```

## Quick Start

Below is a minimal CLI using cli-commons components.

```python
import sys
from pathlib import Path
from cli_commons.parser import create_standard_parser, validate_arguments
from cli_commons.logger import setup_logging
from cli_commons.directories import setup_directories
from cli_commons.colors import MessageFormatter
from cli_commons.file_ops import get_files_recursive, process_batch_files


def process_file(file_path: Path) -> tuple[bool, str]:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            _ = f.read()
        return True, "Processed successfully"
    except Exception as e:
        return False, str(e)


def main() -> int:
    parser = create_standard_parser(
        prog="my-tool",
        description="My awesome CLI tool",
        version="1.0.0",
        epilog="Examples:\n  my-tool ./inputs --output ./outputs",
    )
    args = parser.parse_args()

    errors = validate_arguments(args)
    if errors:
        for error in errors:
            print(MessageFormatter.error(error), file=sys.stderr)
        return 1

    logger = setup_logging(args.log_file, args.verbose, args.quiet)
    dirs = setup_directories(Path.cwd())

    logger.info("Starting my-tool")

    try:
        input_files: list[Path] = []
        for p in args.paths:
            input_files.extend(get_files_recursive(p))

        if not input_files:
            print(MessageFormatter.warning("No files found to process"))
            return 0

        print(MessageFormatter.process(f"Found {len(input_files)} files"))

        stats = process_batch_files(
            input_files,
            process_file,
            dirs,
            logger,
            dry_run=args.dry_run,
        )

        print("\n" + "=" * 70)
        if args.dry_run:
            print(MessageFormatter.dry_run(f"Would process: {stats['processed']} files"))
        else:
            if stats["failed"] > 0:
                print(
                    MessageFormatter.warning(
                        f"Processed: {stats['processed']}, Failed: {stats['failed']}"
                    )
                )
            else:
                print(
                    MessageFormatter.success(
                        f"All {stats['processed']} files processed successfully"
                    )
                )

        print("=" * 70 + "\n")
        if args.log_file:
            print(f"Log file: {args.log_file}")
        return 0

    except KeyboardInterrupt:
        print(MessageFormatter.warning("Interrupted by user"), file=sys.stderr)
        logger.warning("Interrupted by user")
        return 130
    except Exception as e:
        print(MessageFormatter.error(str(e)), file=sys.stderr)
        logger.exception("Fatal error")
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

## Modules

### colors.py

```python
from cli_commons.colors import Colors, MessageFormatter

print(f"{Colors.GREEN}Success{Colors.END}")
print(MessageFormatter.success("Operation completed"))
print(MessageFormatter.error("Something failed"))
print(MessageFormatter.warning("Be careful"))
```

### logger.py

```python
from pathlib import Path
from cli_commons.logger import setup_logging

logger = setup_logging()  # creates ./logs/process_<timestamp>.log
logger = setup_logging(verbose=True)
logger = setup_logging(quiet=True)
logger = setup_logging(log_file=Path("./my.log"))

logger.info("Information message")
logger.debug("Debug message")
logger.warning("Warning message")
logger.error("Error message")
```

### directories.py

```python
from pathlib import Path
from cli_commons.directories import setup_directories, get_timestamped_dir

dirs = setup_directories()  # inputs/, outputs/, inputs/processed/, inputs/failed/, logs/
timestamped = get_timestamped_dir(Path("./outputs"), prefix="run")
```

### file_ops.py

```python
from pathlib import Path
from cli_commons.file_ops import (
    process_batch_files,
    get_files_recursive,
    get_output_filename,
    safe_rename,
)

def process_file(file_path: Path) -> tuple[bool, str]:
    return True, "Success"

files = get_files_recursive(Path("./inputs"), pattern="*.txt")
stats = process_batch_files(files, process_file, dirs, logger, dry_run=False)
output = get_output_filename(Path("file.txt"), suffix="processed")  # file_processed.txt
safe_rename(Path("old.txt"), Path("new.txt"), logger)
```

### parser.py

```python
from cli_commons.parser import (
    create_standard_parser,
    validate_arguments,
    validate_paths,
    validate_output_dir,
)

parser = create_standard_parser(
    prog="my-tool",
    description="What this tool does",
    version="1.0.0",
    epilog="Examples:\n  my-tool ./input",
)
args = parser.parse_args()

errors = validate_arguments(args)
if errors:
    for error in errors:
        print(error)
    sys.exit(1)
```

## Standard Flags

| Flag | Short | Description |
|------|-------|-------------|
| --help | -h | Show help message |
| --version |  | Show version |
| --verbose | -v | Enable verbose output (DEBUG) |
| --quiet | -q | Suppress output (ERROR only) |
| --dry-run | -n | Show what would be done |
| --log-file |  | Save logs to file |
| --output | -o | Output directory (default: ./outputs) |
| --json |  | JSON format output |

## Directory Structure

Created by `setup_directories()`:

```
project/
├── inputs/
├── outputs/
├── inputs/processed/
├── inputs/failed/
└── logs/
```

## Requirements

- Python 3.9 or higher
- No external dependencies (stdlib only)

## License

MIT

## Version History

- 1.0.0 (2025-10-27): Initial release


