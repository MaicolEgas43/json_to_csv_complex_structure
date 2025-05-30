"""Main JSON to CSV converter class."""

import csv
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from .core import extract_all_keys, flatten_dict, organize_columns
from .exceptions import (
    ConversionError,
    FileProcessingError, 
    InvalidJSONStructureError
)

logger = logging.getLogger(__name__)


class JSONToCSVConverter:
    """
    A robust JSON to CSV converter that handles complex nested structures.
    
    Features:
    - Configurable field separator for nested keys
    - Maintains column order consistency
    - Handles various data types appropriately
    - Comprehensive error handling
    - Logging support
    """
    
    def __init__(
        self, 
        separator: str = '__',
        quote_all: bool = True,
        preserve_order: bool = True,
        encoding: str = 'utf-8'
    ) -> None:
        """
        Initialize the converter.
        
        Args:
            separator: Separator for nested field names
            quote_all: Whether to quote all CSV fields
            preserve_order: Whether to preserve predefined column order
            encoding: File encoding to use
        """
        self.separator = separator
        self.quote_all = quote_all
        self.preserve_order = preserve_order
        self.encoding = encoding
        
    def convert_file(
        self, 
        json_file_path: Union[str, Path],
        csv_file_path: Union[str, Path],
        results_key: str = 'results',
        include_metadata: bool = True
    ) -> Dict[str, Any]:
        """
        Convert a JSON file to CSV format.
        
        Args:
            json_file_path: Path to input JSON file
            csv_file_path: Path to output CSV file
            results_key: Key containing the array of records
            include_metadata: Whether to include metadata fields like 'next'
            
        Returns:
            Conversion statistics
            
        Raises:
            FileProcessingError: If file operations fail
            InvalidJSONStructureError: If JSON structure is invalid
            ConversionError: If conversion fails
        """
        logger.info(f"Starting conversion: {json_file_path} -> {csv_file_path}")
        
        # Load JSON data
        data = self._load_json(json_file_path)
        
        # Validate structure
        self._validate_json_structure(data, results_key)
        
        # Extract results
        results = data[results_key]
        
        # Get all columns
        all_keys = extract_all_keys(results, results_key, self.separator)
        
        # Organize columns
        if self.preserve_order:
            columns = organize_columns(all_keys)
        else:
            columns = sorted(all_keys)
            
        # Add metadata columns if requested
        if include_metadata:
            metadata_keys = self._extract_metadata_keys(data, results_key)
            columns.extend(metadata_keys)
        
        # Convert to CSV
        stats = self._write_csv(
            data, results, columns, csv_file_path, 
            results_key, include_metadata
        )
        
        logger.info(f"Conversion completed successfully: {stats}")
        return stats
    
    def convert_data(
        self,
        data: Dict[str, Any],
        results_key: str = 'results',
        include_metadata: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Convert JSON data to list of flat dictionaries (CSV-ready format).
        
        Args:
            data: JSON data dictionary
            results_key: Key containing the array of records
            include_metadata: Whether to include metadata fields
            
        Returns:
            List of flattened dictionaries
            
        Raises:
            InvalidJSONStructureError: If JSON structure is invalid
            ConversionError: If conversion fails
        """
        # Validate structure
        self._validate_json_structure(data, results_key)
        
        # Extract results
        results = data[results_key]
        
        # Get all columns
        all_keys = extract_all_keys(results, results_key, self.separator)
        
        # Organize columns
        if self.preserve_order:
            columns = organize_columns(all_keys)
        else:
            columns = sorted(all_keys)
            
        # Add metadata columns if requested
        if include_metadata:
            metadata_keys = self._extract_metadata_keys(data, results_key)
            columns.extend(metadata_keys)
        
        # Convert records
        converted_records = []
        for result in results:
            flattened_result = flatten_dict(result, results_key, self.separator)
            
            # Create row with all columns
            row = {}
            for column in columns:
                if include_metadata and column in metadata_keys:
                    # Add metadata value from root level
                    metadata_key = column.replace(f"{results_key}{self.separator}", "")
                    row[column] = data.get(metadata_key, '')
                else:
                    row[column] = flattened_result.get(column, '')
            
            converted_records.append(row)
        
        return converted_records
    
    def _load_json(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """Load JSON data from file."""
        try:
            file_path = Path(file_path)
            with open(file_path, 'r', encoding=self.encoding) as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileProcessingError(f"Could not find file: {file_path}")
        except json.JSONDecodeError as e:
            raise FileProcessingError(f"Invalid JSON file: {file_path}", str(e))
        except Exception as e:
            raise FileProcessingError(f"Error reading file: {file_path}", str(e))
    
    def _validate_json_structure(
        self, 
        data: Dict[str, Any], 
        results_key: str
    ) -> None:
        """Validate that JSON has expected structure."""
        if not isinstance(data, dict):
            raise InvalidJSONStructureError("JSON must be an object")
        
        if results_key not in data:
            raise InvalidJSONStructureError(f"JSON must have a '{results_key}' property")
        
        results = data[results_key]
        if not isinstance(results, list):
            raise InvalidJSONStructureError(f"The '{results_key}' property must be a list")
    
    def _extract_metadata_keys(
        self, 
        data: Dict[str, Any], 
        results_key: str
    ) -> List[str]:
        """Extract metadata keys from root level."""
        metadata_keys = []
        for key in data.keys():
            if key != results_key:
                metadata_key = f"{results_key}{self.separator}{key}"
                metadata_keys.append(metadata_key)
        return metadata_keys
    
    def _write_csv(
        self,
        data: Dict[str, Any],
        results: List[Dict[str, Any]],
        columns: List[str],
        csv_file_path: Union[str, Path],
        results_key: str,
        include_metadata: bool
    ) -> Dict[str, Any]:
        """Write data to CSV file."""
        try:
            csv_file_path = Path(csv_file_path)
            
            # Ensure output directory exists
            csv_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            quoting = csv.QUOTE_ALL if self.quote_all else csv.QUOTE_MINIMAL
            
            with open(csv_file_path, 'w', newline='', encoding=self.encoding) as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=columns, quoting=quoting)
                
                # Write header
                writer.writeheader()
                
                # Process each record
                for result in results:
                    # Flatten the record
                    flattened_result = flatten_dict(result, results_key, self.separator)
                    
                    # Create row with all columns
                    row = {}
                    for column in columns:
                        if include_metadata and column.startswith(f"{results_key}{self.separator}"):
                            # Check if this is a metadata column
                            metadata_key = column.replace(f"{results_key}{self.separator}", "")
                            if metadata_key in data and metadata_key != results_key:
                                row[column] = data.get(metadata_key, '')
                                continue
                        
                        row[column] = flattened_result.get(column, '')
                    
                    writer.writerow(row)
            
            return {
                'records_processed': len(results),
                'columns_generated': len(columns),
                'output_file': str(csv_file_path),
                'file_size_bytes': csv_file_path.stat().st_size
            }
            
        except Exception as e:
            raise FileProcessingError(f"Error writing CSV file: {csv_file_path}", str(e)) 