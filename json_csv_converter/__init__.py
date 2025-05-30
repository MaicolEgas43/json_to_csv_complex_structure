"""
JSON to CSV Converter Package

A robust JSON to CSV converter that handles complex nested structures,
maintaining data hierarchy using configurable separators.
"""

from .converter import JSONToCSVConverter
from .core import flatten_dict, extract_all_keys
from .exceptions import JSONCSVConverterError, InvalidJSONStructureError

__version__ = "1.0.0"
__author__ = "Nova Datalake Team"
__email__ = "team@example.com"

__all__ = [
    "JSONToCSVConverter",
    "flatten_dict", 
    "extract_all_keys",
    "JSONCSVConverterError",
    "InvalidJSONStructureError",
] 