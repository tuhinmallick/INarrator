class AuthenticationError(Exception):
    """Custom exception class for authentication errors."""
    def __init__(self, message="Authentication failed"):
        self.message = message
        super().__init__(self.message)