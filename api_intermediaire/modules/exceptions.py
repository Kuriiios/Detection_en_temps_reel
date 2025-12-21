class Unauthorized(Exception):
    """Exception raised for 401 Unauthorized errors."""
    def __init__(self, message="Unauthorized"):
        self.message = message
        self.status_code = 401
        super().__init__(self.message)