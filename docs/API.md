# API Documentation

## JSONToCSVConverter Class

The main class for converting JSON data to CSV format.

### Constructor

```python
JSONToCSVConverter(
    separator: str = '__',
    quote_all: bool = True,
    preserve_order: bool = True,
    encoding: str = 'utf-8'
)
```

**Parameters:**
- `separator` (str): Separator for nested field names. Default: `'__'`
- `quote_all` (bool): Whether to quote all CSV fields. Default: `True`
- `preserve_order` (bool): Whether to preserve predefined column order. Default: `True`
- `encoding` (str): File encoding to use. Default: `'utf-8'`

### Methods

#### convert_file()

Convert a JSON file to CSV format.

```python
convert_file(
    json_file_path: Union[str, Path],
    csv_file_path: Union[str, Path],
    results_key: str = 'results',
    include_metadata: bool = True
) -> Dict[str, Any]
```

**Parameters:**
- `json_file_path`: Path to input JSON file
- `csv_file_path`: Path to output CSV file
- `results_key`: Key containing the array of records
- `include_metadata`: Whether to include metadata fields like 'next'

**Returns:**
Dictionary with conversion statistics:
- `records_processed`: Number of records processed
- `columns_generated`: Number of columns generated
- `output_file`: Path to output file
- `file_size_bytes`: Size of output file in bytes

**Raises:**
- `FileProcessingError`: If file operations fail
- `InvalidJSONStructureError`: If JSON structure is invalid
- `ConversionError`: If conversion fails

#### convert_data()

Convert JSON data to list of flat dictionaries (CSV-ready format).

```python
convert_data(
    data: Dict[str, Any],
    results_key: str = 'results',
    include_metadata: bool = True
) -> List[Dict[str, Any]]
```

**Parameters:**
- `data`: JSON data dictionary
- `results_key`: Key containing the array of records
- `include_metadata`: Whether to include metadata fields

**Returns:**
List of flattened dictionaries ready for CSV writing

**Raises:**
- `InvalidJSONStructureError`: If JSON structure is invalid
- `ConversionError`: If conversion fails

## Core Functions

### flatten_dict()

Flattens a nested dictionary using a separator for hierarchical keys.

```python
flatten_dict(
    data: Dict[str, Any], 
    parent_key: str = '', 
    separator: str = '__'
) -> Dict[str, Any]
```

**Parameters:**
- `data`: Dictionary to flatten
- `parent_key`: Parent key to build hierarchy
- `separator`: Separator for nested keys

**Returns:**
Flattened dictionary

### extract_all_keys()

Extracts all possible keys from all records.

```python
extract_all_keys(
    results: List[Dict[str, Any]], 
    prefix: str = 'results',
    separator: str = '__'
) -> List[str]
```

**Parameters:**
- `results`: List of records from JSON
- `prefix`: Prefix to add to keys
- `separator`: Separator for nested keys

**Returns:**
Sorted list of all unique keys

### organize_columns()

Organizes columns with predefined order first, then additional columns.

```python
organize_columns(
    all_keys: List[str], 
    predefined_order: List[str] = None
) -> List[str]
```

**Parameters:**
- `all_keys`: All available column keys
- `predefined_order`: Predefined column order

**Returns:**
Organized list of columns

## Exceptions

### JSONCSVConverterError

Base exception for JSON to CSV conversion errors.

```python
class JSONCSVConverterError(Exception):
    def __init__(self, message: str, details: str = None) -> None:
        ...
```

### InvalidJSONStructureError

Raised when JSON structure doesn't match expected format.

### FileProcessingError

Raised when file operations fail.

### ConversionError

Raised when data conversion fails.

## Usage Examples

### Basic Usage

```python
from json_csv_converter import JSONToCSVConverter

# Create converter
converter = JSONToCSVConverter()

# Convert file
stats = converter.convert_file('input.json', 'output.csv')
print(f"Processed {stats['records_processed']} records")
```

### Custom Configuration

```python
# Custom separator and settings
converter = JSONToCSVConverter(
    separator='.',
    quote_all=False,
    preserve_order=False
)

# Convert data in memory
data = {"results": [{"id": "1", "user": {"name": "John"}}]}
records = converter.convert_data(data)
```

### Error Handling

```python
from json_csv_converter import JSONToCSVConverter
from json_csv_converter.exceptions import JSONCSVConverterError

try:
    converter = JSONToCSVConverter()
    stats = converter.convert_file('input.json', 'output.csv')
except JSONCSVConverterError as e:
    print(f"Conversion failed: {e}") 