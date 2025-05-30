"""Tests for core utility functions."""

import pytest

from json_csv_converter.core import (
    extract_all_keys,
    flatten_dict,
    get_predefined_column_order,
    organize_columns
)
from json_csv_converter.exceptions import ConversionError


class TestFlattenDict:
    """Test cases for flatten_dict function."""
    
    def test_flatten_simple_dict(self):
        """Test flattening a simple dictionary."""
        data = {"name": "John", "age": 30}
        result = flatten_dict(data)
        
        assert result == {"name": "John", "age": "30"}
    
    def test_flatten_nested_dict(self):
        """Test flattening a nested dictionary."""
        data = {
            "user": {
                "name": "John",
                "contact": {
                    "email": "john@example.com"
                }
            }
        }
        result = flatten_dict(data)
        
        expected = {
            "user__name": "John",
            "user__contact__email": "john@example.com"
        }
        assert result == expected
    
    def test_flatten_dict_with_parent_key(self):
        """Test flattening with parent key."""
        data = {"name": "John", "age": 30}
        result = flatten_dict(data, parent_key="user")
        
        expected = {"user__name": "John", "user__age": "30"}
        assert result == expected
    
    def test_flatten_dict_custom_separator(self):
        """Test flattening with custom separator."""
        data = {"user": {"name": "John"}}
        result = flatten_dict(data, separator=".")
        
        assert result == {"user.name": "John"}
    
    def test_flatten_dict_with_none_values(self):
        """Test flattening with None values."""
        data = {"name": "John", "middle_name": None}
        result = flatten_dict(data)
        
        assert result == {"name": "John", "middle_name": "null"}
    
    def test_flatten_dict_with_boolean_values(self):
        """Test flattening with boolean values."""
        data = {"active": True, "verified": False}
        result = flatten_dict(data)
        
        assert result == {"active": "True", "verified": "False"}
    
    def test_flatten_dict_with_list_values(self):
        """Test flattening with list values."""
        data = {"tags": ["python", "json", "csv"]}
        result = flatten_dict(data)
        
        assert result == {"tags": "['python', 'json', 'csv']"}
    
    def test_flatten_dict_with_numeric_values(self):
        """Test flattening with numeric values."""
        data = {"count": 42, "ratio": 3.14}
        result = flatten_dict(data)
        
        assert result == {"count": "42", "ratio": "3.14"}
    
    def test_flatten_empty_dict(self):
        """Test flattening empty dictionary."""
        result = flatten_dict({})
        assert result == {}


class TestExtractAllKeys:
    """Test cases for extract_all_keys function."""
    
    def test_extract_keys_simple(self):
        """Test extracting keys from simple records."""
        results = [
            {"id": "1", "name": "John"},
            {"id": "2", "name": "Jane", "age": 25}
        ]
        
        keys = extract_all_keys(results)
        expected_keys = ["results__age", "results__id", "results__name"]
        assert sorted(keys) == expected_keys
    
    def test_extract_keys_nested(self):
        """Test extracting keys from nested records."""
        results = [
            {
                "id": "1",
                "user": {
                    "name": "John",
                    "contact": {"email": "john@example.com"}
                }
            }
        ]
        
        keys = extract_all_keys(results)
        expected_keys = [
            "results__id",
            "results__user__contact__email", 
            "results__user__name"
        ]
        assert sorted(keys) == expected_keys
    
    def test_extract_keys_custom_prefix(self):
        """Test extracting keys with custom prefix."""
        results = [{"id": "1", "name": "John"}]
        keys = extract_all_keys(results, prefix="items")
        
        expected_keys = ["items__id", "items__name"]
        assert sorted(keys) == expected_keys
    
    def test_extract_keys_custom_separator(self):
        """Test extracting keys with custom separator."""
        results = [{"id": "1", "user": {"name": "John"}}]
        keys = extract_all_keys(results, separator=".")
        
        expected_keys = ["results.id", "results.user.name"]
        assert sorted(keys) == expected_keys
    
    def test_extract_keys_empty_results(self):
        """Test extracting keys from empty results."""
        keys = extract_all_keys([])
        assert keys == []
    
    def test_extract_keys_with_non_dict_items(self):
        """Test extracting keys when results contain non-dict items."""
        results = [{"id": "1"}, "not a dict", {"name": "John"}]
        keys = extract_all_keys(results)
        
        expected_keys = ["results__id", "results__name"]
        assert sorted(keys) == expected_keys


class TestGetPredefinedColumnOrder:
    """Test cases for get_predefined_column_order function."""
    
    def test_get_predefined_order(self):
        """Test getting predefined column order."""
        columns = get_predefined_column_order()
        
        assert isinstance(columns, list)
        assert len(columns) > 0
        assert "results__id" in columns
        assert "results__user__email" in columns


class TestOrganizeColumns:
    """Test cases for organize_columns function."""
    
    def test_organize_columns_with_predefined(self):
        """Test organizing columns with predefined order."""
        all_keys = [
            "results__name",
            "results__id", 
            "results__user__email",
            "results__custom_field"
        ]
        
        predefined = ["results__id", "results__user__email"]
        result = organize_columns(all_keys, predefined)
        
        # Predefined columns should come first
        assert result[:2] == ["results__id", "results__user__email"]
        # Additional columns should be sorted alphabetically
        assert "results__custom_field" in result
        assert "results__name" in result
    
    def test_organize_columns_default_predefined(self):
        """Test organizing columns with default predefined order."""
        all_keys = ["results__id", "results__custom_field", "results__user__email"]
        result = organize_columns(all_keys)
        
        # Should use default predefined order
        assert isinstance(result, list)
        assert len(result) == len(all_keys)
    
    def test_organize_columns_no_predefined_match(self):
        """Test organizing columns when no predefined columns match."""
        all_keys = ["custom__field1", "custom__field2"]
        predefined = ["results__id", "results__name"]
        
        result = organize_columns(all_keys, predefined)
        
        # Should just return sorted additional columns
        assert result == ["custom__field1", "custom__field2"]
    
    def test_organize_columns_empty_list(self):
        """Test organizing empty column list."""
        result = organize_columns([])
        assert result == [] 