"""Tests for JSON to CSV converter."""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from json_csv_converter import JSONToCSVConverter
from json_csv_converter.exceptions import (
    FileProcessingError,
    InvalidJSONStructureError
)


class TestJSONToCSVConverter:
    """Test cases for JSONToCSVConverter class."""
    
    @pytest.fixture
    def sample_json_data(self):
        """Sample JSON data for testing."""
        return {
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
                    },
                    "score": 85
                },
                {
                    "id": "456", 
                    "name": "Jane Smith",
                    "user": {
                        "id": "user456",
                        "email": "jane@example.com",
                        "traits": {
                            "FIRST_NAME": "Jane",
                            "LAST_NAME": "Smith"
                        }
                    },
                    "score": 92
                }
            ],
            "next": "https://api.example.com/next"
        }
    
    @pytest.fixture
    def converter(self):
        """Default converter instance."""
        return JSONToCSVConverter()
    
    def test_init_default_settings(self):
        """Test converter initialization with default settings."""
        converter = JSONToCSVConverter()
        assert converter.separator == '__'
        assert converter.quote_all is True
        assert converter.preserve_order is True
        assert converter.encoding == 'utf-8'
    
    def test_init_custom_settings(self):
        """Test converter initialization with custom settings."""
        converter = JSONToCSVConverter(
            separator='.',
            quote_all=False,
            preserve_order=False,
            encoding='latin1'
        )
        assert converter.separator == '.'
        assert converter.quote_all is False
        assert converter.preserve_order is False
        assert converter.encoding == 'latin1'
    
    def test_convert_data_basic(self, converter, sample_json_data):
        """Test basic data conversion."""
        result = converter.convert_data(sample_json_data)
        
        assert len(result) == 2
        assert all(isinstance(record, dict) for record in result)
        
        # Check first record
        first_record = result[0]
        assert first_record['results__id'] == '123'
        assert first_record['results__name'] == 'John Doe'
        assert first_record['results__user__id'] == 'user123'
        assert first_record['results__user__email'] == 'john@example.com'
        assert first_record['results__user__traits__FIRST_NAME'] == 'John'
        assert first_record['results__score'] == '85'
    
    def test_convert_data_with_metadata(self, converter, sample_json_data):
        """Test data conversion including metadata."""
        result = converter.convert_data(sample_json_data, include_metadata=True)
        
        # Check metadata is included
        first_record = result[0]
        assert 'results__next' in first_record
        assert first_record['results__next'] == 'https://api.example.com/next'
    
    def test_convert_data_without_metadata(self, converter, sample_json_data):
        """Test data conversion excluding metadata."""
        result = converter.convert_data(sample_json_data, include_metadata=False)
        
        # Check metadata is not included
        first_record = result[0]
        assert 'results__next' not in first_record
    
    def test_convert_data_custom_separator(self, sample_json_data):
        """Test data conversion with custom separator."""
        converter = JSONToCSVConverter(separator='.')
        result = converter.convert_data(sample_json_data)
        
        first_record = result[0]
        assert 'results.id' in first_record
        assert 'results.user.email' in first_record
        assert 'results.user.traits.FIRST_NAME' in first_record
    
    def test_convert_data_custom_results_key(self, converter):
        """Test data conversion with custom results key."""
        data = {
            "items": [
                {"id": "1", "name": "Test"}
            ]
        }
        
        result = converter.convert_data(data, results_key='items')
        assert len(result) == 1
        assert result[0]['items__id'] == '1'
        assert result[0]['items__name'] == 'Test'
    
    def test_convert_file(self, converter, sample_json_data):
        """Test file conversion."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as json_file:
            json.dump(sample_json_data, json_file)
            json_file_path = json_file.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as csv_file:
            csv_file_path = csv_file.name
        
        try:
            stats = converter.convert_file(json_file_path, csv_file_path)
            
            # Check statistics
            assert stats['records_processed'] == 2
            assert stats['columns_generated'] > 0
            assert stats['output_file'] == csv_file_path
            assert stats['file_size_bytes'] > 0
            
            # Check file exists and has content
            csv_path = Path(csv_file_path)
            assert csv_path.exists()
            assert csv_path.stat().st_size > 0
            
        finally:
            # Clean up
            Path(json_file_path).unlink(missing_ok=True)
            Path(csv_file_path).unlink(missing_ok=True)
    
    def test_validate_json_structure_valid(self, converter, sample_json_data):
        """Test JSON structure validation with valid data."""
        # Should not raise exception
        converter._validate_json_structure(sample_json_data, 'results')
    
    def test_validate_json_structure_missing_results(self, converter):
        """Test JSON structure validation with missing results key."""
        data = {"other_key": []}
        
        with pytest.raises(InvalidJSONStructureError, match="must have a 'results' property"):
            converter._validate_json_structure(data, 'results')
    
    def test_validate_json_structure_invalid_results_type(self, converter):
        """Test JSON structure validation with invalid results type."""
        data = {"results": "not a list"}
        
        with pytest.raises(InvalidJSONStructureError, match="must be a list"):
            converter._validate_json_structure(data, 'results')
    
    def test_validate_json_structure_not_dict(self, converter):
        """Test JSON structure validation with non-dict input."""
        data = []
        
        with pytest.raises(InvalidJSONStructureError, match="JSON must be an object"):
            converter._validate_json_structure(data, 'results')
    
    def test_load_json_file_not_found(self, converter):
        """Test loading non-existent JSON file."""
        with pytest.raises(FileProcessingError, match="Could not find file"):
            converter._load_json('non_existent_file.json')
    
    def test_load_json_invalid_json(self, converter):
        """Test loading invalid JSON file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{"invalid": json}')  # Invalid JSON
            file_path = f.name
        
        try:
            with pytest.raises(FileProcessingError, match="Invalid JSON file"):
                converter._load_json(file_path)
        finally:
            Path(file_path).unlink(missing_ok=True)
    
    def test_extract_metadata_keys(self, converter, sample_json_data):
        """Test metadata key extraction."""
        metadata_keys = converter._extract_metadata_keys(sample_json_data, 'results')
        
        assert 'results__next' in metadata_keys
        assert len(metadata_keys) == 1
    
    def test_convert_data_empty_results(self, converter):
        """Test conversion with empty results."""
        data = {"results": []}
        result = converter.convert_data(data)
        
        assert result == []
    
    def test_convert_data_with_null_values(self, converter):
        """Test conversion with null values."""
        data = {
            "results": [
                {
                    "id": "1",
                    "name": None,
                    "score": 0,
                    "active": False
                }
            ]
        }
        
        result = converter.convert_data(data)
        record = result[0]
        
        assert record['results__name'] == 'null'
        assert record['results__score'] == '0'
        assert record['results__active'] == 'False'
    
    def test_convert_data_with_list_values(self, converter):
        """Test conversion with list values."""
        data = {
            "results": [
                {
                    "id": "1",
                    "tags": ["tag1", "tag2", "tag3"]
                }
            ]
        }
        
        result = converter.convert_data(data)
        record = result[0]
        
        assert record['results__tags'] == "['tag1', 'tag2', 'tag3']" 