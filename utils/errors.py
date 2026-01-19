class TranscriptError(Exception):
    """Custom exception for transcript-related errors."""
    
    def __init__(self, code, message, status_code=500):
        """
        Initialize a TranscriptError.
        
        Args:
            code (str): Error code identifier
            message (str): Human-readable error message
            status_code (int): HTTP status code (default: 500)
        """
        super().__init__(message)
        self.code = code 
        self.message = message
        self.status_code = status_code