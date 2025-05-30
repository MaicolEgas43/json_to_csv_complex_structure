"""Custom exceptions for the JSON to CSV converter."""


class JSONCSVConverterError(Exception):
    """Base exception for JSON to CSV conversion errors."""
    
    def __init__(self, message: str, details: str = None) -> None:
        """
        Initialize the exception.
        
        Args:
            message: Error message
            details: Additional error details
        """
        super().__init__(message)
        self.message = message
        self.details = details
    
    def __str__(self) -> str:
        """Return string representation of the exception."""
        if self.details:
            return f"{self.message}: {self.details}"
        return self.message


class InvalidJSONStructureError(JSONCSVConverterError):
    """Raised when JSON structure doesn't match expected format."""
    pass


class FileProcessingError(JSONCSVConverterError):
    """Raised when file operations fail."""
    pass


class ConversionError(JSONCSVConverterError):
    """Raised when data conversion fails."""
    pass 