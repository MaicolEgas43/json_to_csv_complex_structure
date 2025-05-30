#!/bin/bash
# CLI Usage Examples for JSON to CSV Converter
# This script demonstrates various command-line usage patterns

echo "🔄 JSON to CSV Converter - CLI Usage Examples"
echo "=============================================="

# Make sure we're in the right directory
cd "$(dirname "$0")/.."

echo ""
echo "📋 Example 1: Basic conversion"
echo "Command: python -m json_csv_converter.cli data/data.json output/basic.csv"
mkdir -p output
python -m json_csv_converter.cli data/data.json output/basic.csv

echo ""
echo "📊 Example 2: Custom separator"
echo "Command: python -m json_csv_converter.cli data/data.json output/dot_separated.csv --separator '.'"
python -m json_csv_converter.cli data/data.json output/dot_separated.csv --separator "."

echo ""
echo "⚙️  Example 3: No quotes, no predefined order"
echo "Command: python -m json_csv_converter.cli data/data.json output/minimal.csv --no-quotes --no-order"
python -m json_csv_converter.cli data/data.json output/minimal.csv --no-quotes --no-order

echo ""
echo "🔍 Example 4: Exclude metadata"
echo "Command: python -m json_csv_converter.cli data/data.json output/no_metadata.csv --no-metadata"
python -m json_csv_converter.cli data/data.json output/no_metadata.csv --no-metadata

echo ""
echo "📝 Example 5: Verbose output"
echo "Command: python -m json_csv_converter.cli data/data.json output/verbose.csv --verbose"
python -m json_csv_converter.cli data/data.json output/verbose.csv --verbose

echo ""
echo "ℹ️  Example 6: Show help"
echo "Command: python -m json_csv_converter.cli --help"
python -m json_csv_converter.cli --help

echo ""
echo "📊 Example 7: Show version"
echo "Command: python -m json_csv_converter.cli --version"
python -m json_csv_converter.cli --version

echo ""
echo "📁 Generated files:"
ls -la output/

echo ""
echo "🎉 All CLI examples completed!" 