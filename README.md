# json_to_csv_complex_structure
# Nova Datalake

# Folders and their meaning

We have several folders for storing different source code.

## Airbyte
Here we store all data related to airbyte configuration and recovery.

## Dbt
This folder contains all the processes and data structures that constitute the datawarehouse and all other required structures.
By placing .sql files here we can generate views and tables in the worky_consolidated database.

## Docs
Most documentation should be found in ClickUp. However, key technical info and manuals that could help us retrieve the platform's status quo should be placed here.
(Everything should be in markup, and focused on platform recovery, modules or general explanation of how to interact with technology)

## PoCs
Here you will find folders with code, sources, libraries, environments and everything related to a given research.

## Python
Here you will find python sources produced for all data-related tasks.

## Schemas
Scripts required to reconstruct our database structures, datalake or run simple tests during Datalake reconstruction or extraction.
Everything here should be related to schemas and databases.

## sql-scripts
All vanilla scripts that we use for interacting with snowflake, postgres or other databases should be placed here and organized appropriately.

# JSON to CSV Converter

A robust and flexible Python package for converting complex JSON files to CSV format, designed for data processing pipelines and ETL workflows.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 🔄 **Complex Structure Support**: Handles deeply nested JSON objects with automatic flattening
- ⚙️ **Configurable Options**: Customizable separators, quoting, and column ordering
- 📊 **Metadata Preservation**: Optional inclusion of root-level metadata fields
- 🎯 **Type-Safe**: Full type annotations and comprehensive error handling
- 🧪 **Well Tested**: Extensive test suite with high coverage
- 📖 **CLI & API**: Both command-line interface and programmatic API
- 🚀 **Performance**: Efficient processing of large datasets

## Installation

### Development Installation

```bash
# Clone the repository
git clone <repository-url>
cd repo_json_csv

# Install in development mode with all dependencies
pip install -e ".[dev]"

# Or install dependencies manually
pip install -r requirements.txt
```

### Production Installation

```bash
pip install -e .
```

## Quick Start

### Command Line Usage

```bash
# Basic conversion
python -m json_csv_converter.cli data/input.json output.csv

# Custom separator
python -m json_csv_converter.cli data/input.json output.csv --separator "."

# Exclude metadata and use minimal quoting
python -m json_csv_converter.cli data/input.json output.csv --no-metadata --no-quotes

# Show help
python -m json_csv_converter.cli --help
```

### Programmatic Usage

```python
from json_csv_converter import JSONToCSVConverter

# Basic usage
converter = JSONToCSVConverter()
stats = converter.convert_file('input.json', 'output.csv')
print(f"Processed {stats['records_processed']} records")

# Custom configuration
converter = JSONToCSVConverter(
    separator='.',
    quote_all=False,
    preserve_order=False
)

# Convert data in memory
data = {
    "results": [
        {"id": "1", "user": {"name": "John", "email": "john@example.com"}},
        {"id": "2", "user": {"name": "Jane", "email": "jane@example.com"}}
    ],
    "next": "https://api.example.com/page2"
}

records = converter.convert_data(data)
```

## Expected JSON Structure

The converter expects JSON files with the following structure:

```json
{
  "results": [
    {
      "id": "123",
      "name": "John Doe",
      "user": {
        "id": "user123",
        "email": "john@example.com",
        "traits": {
          "FIRST_NAME": "John",
          "LAST_NAME": "Doe"
        }
      }
    }
  ],
  "next": "https://api.example.com/next"
}
```

This will be converted to CSV with flattened column names:
- `results__id`
- `results__name`
- `results__user__id`
- `results__user__email`
- `results__user__traits__FIRST_NAME`
- `results__user__traits__LAST_NAME`
- `results__next` (metadata)

## Project Structure

```
repo_json_csv/
├── json_csv_converter/          # Main package
│   ├── __init__.py             # Package exports
│   ├── converter.py            # Main converter class
│   ├── core.py                 # Core utility functions
│   ├── exceptions.py           # Custom exceptions
│   └── cli.py                  # Command-line interface
├── tests/                      # Test suite
│   ├── test_converter.py       # Converter tests
│   └── test_core.py           # Core function tests
├── examples/                   # Usage examples
│   ├── basic_usage.py         # Programmatic examples
│   └── cli_usage.sh           # CLI examples
├── docs/                      # Documentation
│   └── API.md                 # API documentation
├── data/                      # Sample data files
│   ├── data.json              # Sample JSON input
│   └── data.csv               # Sample CSV output
├── requirements.txt           # Dependencies
├── pyproject.toml            # Project configuration
└── README.md                 # This file
```

## Configuration Options

### JSONToCSVConverter Parameters

- **`separator`** (str, default: `'__'`): Separator for nested field names
- **`quote_all`** (bool, default: `True`): Whether to quote all CSV fields
- **`preserve_order`** (bool, default: `True`): Whether to preserve predefined column order
- **`encoding`** (str, default: `'utf-8'`): File encoding to use

### CLI Options

```bash
python -m json_csv_converter.cli input.json output.csv [OPTIONS]

Options:
  --separator TEXT        Separator for nested field names (default: __)
  --results-key TEXT      Key containing array of records (default: results)
  --no-quotes            Use minimal quoting instead of quoting all fields
  --no-order             Use alphabetical order instead of predefined order
  --no-metadata          Exclude metadata fields from root level
  --encoding TEXT        File encoding (default: utf-8)
  --verbose, -v          Enable verbose logging
  --version              Show version information
  --help                 Show help message
```

## Development

### Setting Up Development Environment

```bash
# Clone and install in development mode
git clone <repository-url>
cd repo_json_csv
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=json_csv_converter

# Run specific test file
pytest tests/test_converter.py
```

### Code Quality

```bash
# Format code
black json_csv_converter/ tests/

# Type checking
mypy json_csv_converter/

# Linting
flake8 json_csv_converter/ tests/
```

### Running Examples

```bash
# Run programmatic examples
python examples/basic_usage.py

# Run CLI examples
chmod +x examples/cli_usage.sh
./examples/cli_usage.sh
```

## Error Handling

The package provides comprehensive error handling with custom exceptions:

- **`JSONCSVConverterError`**: Base exception for all converter errors
- **`InvalidJSONStructureError`**: Invalid JSON structure
- **`FileProcessingError`**: File operation failures
- **`ConversionError`**: Data conversion failures

```python
from json_csv_converter import JSONToCSVConverter
from json_csv_converter.exceptions import JSONCSVConverterError

try:
    converter = JSONToCSVConverter()
    stats = converter.convert_file('input.json', 'output.csv')
except JSONCSVConverterError as e:
    print(f"Conversion failed: {e}")
```

## Nova Datalake Integration

This converter is part of the Nova Datalake ecosystem and integrates with:

- **Airbyte**: Data ingestion and source configuration
- **dbt**: Data warehouse transformations and modeling
- **Python**: Custom data processing scripts
- **SQL Scripts**: Database interactions and queries

### Recommended Workflow

1. **Extract**: Use Airbyte to extract data from sources
2. **Convert**: Use this converter to transform JSON to CSV
3. **Load**: Import CSV data into data warehouse
4. **Transform**: Use dbt for further transformations
5. **Analyze**: Query processed data with SQL scripts

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Format code (`black .`)
7. Commit changes (`git commit -m 'Add amazing feature'`)
8. Push to branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support

For questions, issues, or contributions:

1. Check the [API Documentation](docs/API.md)
2. Review the [examples](examples/)
3. Open an issue on GitHub
4. Contact the Nova Datalake team

---

**Nova Datalake Team** | Building robust data infrastructure
