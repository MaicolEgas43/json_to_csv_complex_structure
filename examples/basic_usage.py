#!/usr/bin/env python3
"""
Basic usage example for JSON to CSV converter.

This example demonstrates how to use the JSONToCSVConverter class
to convert JSON data to CSV format programmatically.
"""

import json
from pathlib import Path

from json_csv_converter import JSONToCSVConverter


def main():
    """Demonstrate basic usage of the converter."""
    
    # Sample data
    sample_data = {
        "results": [
            {
                "id": "1",
                "name": "Alice Johnson",
                "user": {
                    "id": "user001",
                    "email": "alice@example.com",
                    "traits": {
                        "FIRST_NAME": "Alice",
                        "LAST_NAME": "Johnson",
                        "DEPARTMENT": "Engineering"
                    }
                },
                "score": 95,
                "active": True
            },
            {
                "id": "2", 
                "name": "Bob Smith",
                "user": {
                    "id": "user002",
                    "email": "bob@example.com",
                    "traits": {
                        "FIRST_NAME": "Bob",
                        "LAST_NAME": "Smith",
                        "DEPARTMENT": "Marketing"
                    }
                },
                "score": 87,
                "active": False
            }
        ],
        "next": "https://api.example.com/page2"
    }
    
    print("🔄 JSON to CSV Converter - Basic Usage Example")
    print("=" * 50)
    
    # Create converter instance
    converter = JSONToCSVConverter()
    
    # Method 1: Convert data in memory
    print("\n📋 Method 1: Converting data in memory")
    converted_records = converter.convert_data(sample_data)
    
    print(f"✅ Converted {len(converted_records)} records")
    print("📊 First record keys:", list(converted_records[0].keys())[:5], "...")
    print("📄 Sample values:")
    for key, value in list(converted_records[0].items())[:3]:
        print(f"   {key}: {value}")
    
    # Method 2: Convert files
    print("\n📁 Method 2: Converting files")
    
    # Create temporary files
    json_file = Path("temp_example.json")
    csv_file = Path("temp_example.csv")
    
    try:
        # Write sample data to JSON file
        with open(json_file, 'w') as f:
            json.dump(sample_data, f, indent=2)
        
        # Convert file
        stats = converter.convert_file(json_file, csv_file)
        
        print(f"✅ File conversion completed:")
        print(f"   📊 Records processed: {stats['records_processed']}")
        print(f"   📋 Columns generated: {stats['columns_generated']}")
        print(f"   📁 Output file: {stats['output_file']}")
        print(f"   📏 File size: {stats['file_size_bytes']:,} bytes")
        
        # Show CSV content preview
        print(f"\n📖 CSV file preview (first 200 characters):")
        with open(csv_file, 'r') as f:
            content = f.read(200)
            print(f"   {content}...")
            
    finally:
        # Clean up temporary files
        json_file.unlink(missing_ok=True)
        csv_file.unlink(missing_ok=True)
    
    # Method 3: Custom configuration
    print("\n⚙️  Method 3: Custom configuration")
    
    custom_converter = JSONToCSVConverter(
        separator='.',  # Use dot separator instead of __
        quote_all=False,  # Minimal quoting
        preserve_order=False  # Alphabetical order
    )
    
    custom_records = custom_converter.convert_data(sample_data)
    print(f"✅ Custom conversion completed")
    print("📊 Sample keys with dot separator:", list(custom_records[0].keys())[:3])
    
    print("\n🎉 All examples completed successfully!")


if __name__ == "__main__":
    main() 