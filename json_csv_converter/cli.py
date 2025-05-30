"""Command-line interface for JSON to CSV converter."""

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

from . import __version__
from .converter import JSONToCSVConverter
from .exceptions import JSONCSVConverterError


def setup_logging(verbose: bool = False) -> None:
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    format_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    logging.basicConfig(
        level=level,
        format=format_str,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def create_parser() -> argparse.ArgumentParser:
    """Create command-line argument parser."""
    parser = argparse.ArgumentParser(
        description='Convert complex JSON files to CSV format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s data.json output.csv
  %(prog)s data.json output.csv --separator "." --no-quotes
  %(prog)s data.json output.csv --results-key "items" --no-metadata
  %(prog)s data.json output.csv --verbose
        """
    )
    
    # Positional arguments
    parser.add_argument(
        'json_file',
        type=str,
        help='Input JSON file path'
    )
    
    parser.add_argument(
        'csv_file', 
        type=str,
        help='Output CSV file path'
    )
    
    # Optional arguments
    parser.add_argument(
        '--separator',
        default='__',
        help='Separator for nested field names (default: __)'
    )
    
    parser.add_argument(
        '--results-key',
        default='results',
        help='Key containing the array of records (default: results)'
    )
    
    parser.add_argument(
        '--no-quotes',
        action='store_true',
        help='Do not quote all CSV fields (use minimal quoting)'
    )
    
    parser.add_argument(
        '--no-order',
        action='store_true', 
        help='Do not preserve predefined column order (use alphabetical)'
    )
    
    parser.add_argument(
        '--no-metadata',
        action='store_true',
        help='Do not include metadata fields from root level'
    )
    
    parser.add_argument(
        '--encoding',
        default='utf-8',
        help='File encoding (default: utf-8)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    
    return parser


def validate_arguments(args: argparse.Namespace) -> None:
    """Validate command-line arguments."""
    # Check input file exists
    json_path = Path(args.json_file)
    if not json_path.exists():
        raise FileNotFoundError(f"Input file not found: {json_path}")
    
    if not json_path.is_file():
        raise ValueError(f"Input path is not a file: {json_path}")
    
    # Check output directory is writable
    csv_path = Path(args.csv_file)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Validate separator
    if not args.separator:
        raise ValueError("Separator cannot be empty")


def main() -> int:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    try:
        # Validate arguments
        validate_arguments(args)
        
        # Create converter with configuration
        converter = JSONToCSVConverter(
            separator=args.separator,
            quote_all=not args.no_quotes,
            preserve_order=not args.no_order,
            encoding=args.encoding
        )
        
        # Perform conversion
        logger.info(f"Converting {args.json_file} to {args.csv_file}")
        
        stats = converter.convert_file(
            json_file_path=args.json_file,
            csv_file_path=args.csv_file,
            results_key=args.results_key,
            include_metadata=not args.no_metadata
        )
        
        # Print results
        print("✅ Conversion completed successfully!")
        print(f"📊 Records processed: {stats['records_processed']}")
        print(f"📋 Columns generated: {stats['columns_generated']}")
        print(f"📁 Output file: {stats['output_file']}")
        print(f"📏 File size: {stats['file_size_bytes']:,} bytes")
        
        return 0
        
    except JSONCSVConverterError as e:
        logger.error(f"Conversion error: {e}")
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        print(f"❌ File not found: {e}", file=sys.stderr)
        return 1
        
    except ValueError as e:
        logger.error(f"Invalid argument: {e}")
        print(f"❌ Invalid argument: {e}", file=sys.stderr)
        return 1
        
    except KeyboardInterrupt:
        logger.info("Conversion cancelled by user")
        print("\n⚠️  Conversion cancelled by user", file=sys.stderr)
        return 130
        
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main()) 