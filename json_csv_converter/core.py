"""Core utility functions for JSON to CSV conversion."""

from typing import Any, Dict, List, Set, Union
from .exceptions import ConversionError


def flatten_dict(
    data: Dict[str, Any], 
    parent_key: str = '', 
    separator: str = '__'
) -> Dict[str, Any]:
    """
    Flattens a nested dictionary using a separator for hierarchical keys.
    
    Args:
        data: Dictionary to flatten
        parent_key: Parent key to build hierarchy
        separator: Separator for nested keys
        
    Returns:
        Flattened dictionary
        
    Raises:
        ConversionError: If data conversion fails
    """
    try:
        items = []
        
        for key, value in data.items():
            # Build new key
            new_key = f"{parent_key}{separator}{key}" if parent_key else key
            
            # If value is a dictionary, apply recursion
            if isinstance(value, dict):
                items.extend(flatten_dict(value, new_key, separator).items())
            elif isinstance(value, list):
                # Handle lists by converting to string representation
                items.append((new_key, str(value)))
            else:
                # Convert special values for CSV consistency
                converted_value = _convert_value(value)
                items.append((new_key, converted_value))
        
        return dict(items)
    
    except Exception as e:
        raise ConversionError(f"Failed to flatten dictionary", str(e))


def _convert_value(value: Any) -> str:
    """
    Convert various data types to appropriate string representation for CSV.
    
    Args:
        value: Value to convert
        
    Returns:
        String representation of the value
    """
    if value is None:
        return "null"
    elif isinstance(value, bool):
        return str(value)
    elif isinstance(value, (int, float)):
        return str(value)
    else:
        return str(value)


def extract_all_keys(
    results: List[Dict[str, Any]], 
    prefix: str = 'results',
    separator: str = '__'
) -> List[str]:
    """
    Extracts all possible keys from all records.
    
    Args:
        results: List of records from JSON
        prefix: Prefix to add to keys
        separator: Separator for nested keys
        
    Returns:
        Sorted list of all unique keys
        
    Raises:
        ConversionError: If key extraction fails
    """
    try:
        all_keys: Set[str] = set()
        
        for result in results:
            if not isinstance(result, dict):
                continue
                
            flattened = flatten_dict(result, prefix, separator)
            all_keys.update(flattened.keys())
        
        return sorted(all_keys)
    
    except Exception as e:
        raise ConversionError(f"Failed to extract keys", str(e))


def get_predefined_column_order() -> List[str]:
    """
    Returns predefined column order for consistency.
    
    This can be customized based on your specific data structure needs.
    
    Returns:
        Ordered list of expected columns
    """
    return [
        "results__id",
        "results__createdAt", 
        "results__updatedAt",
        "results__externalId",
        "results__userId",
        "results__user__id",
        "results__user__createdAt",
        "results__user__updatedAt",
        "results__user__externalId",
        "results__user__name",
        "results__user__email",
        "results__user__avatar",
        "results__user__traits__ID",
        "results__user__traits__name",
        "results__user__traits__EMAIL", 
        "results__user__traits__email",
        "results__user__traits__ROLE_HR",
        "results__user__traits__LAST_NAME",
        "results__user__traits__createdAt",
        "results__user__traits__CREATED_AT",
        "results__user__traits__FIRST_NAME",
        "results__user__firstKnown",
        "results__user__lastSeenTimestamp",
        "results__user__lastInboundMessageTimestamp",
        "results__user__lastOutboundMessageTimestamp",
        "results__user__npsLastScore",
        "results__user__npsLastFeedback",
        "results__user__npsLastRespondedAt",
        "results__user__unsubscribedFromConversations",
        "results__user__unsubscribedFromConversationsAt",
        "results__user__deactivatedAt",
        "results__user__joinDate",
        "results__dismissedAt",
        "results__respondedAt",
        "results__score",
        "results__feedback",
        "results__createdByService",
        "results__outboundMessageId",
        "results__surveyResponseId",
    ]


def organize_columns(
    all_keys: List[str], 
    predefined_order: List[str] = None
) -> List[str]:
    """
    Organizes columns with predefined order first, then additional columns.
    
    Args:
        all_keys: All available column keys
        predefined_order: Predefined column order
        
    Returns:
        Organized list of columns
    """
    if predefined_order is None:
        predefined_order = get_predefined_column_order()
    
    # Start with predefined columns that exist in data
    organized_columns = [col for col in predefined_order if col in all_keys]
    
    # Add any additional columns not in predefined order
    additional_columns = [key for key in sorted(all_keys) 
                         if key not in predefined_order]
    organized_columns.extend(additional_columns)
    
    return organized_columns 