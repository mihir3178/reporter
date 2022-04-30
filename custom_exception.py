class CustomException(Exception):
    """
    CustomException

    description - Describe the cause of the error

    status code - Response code to be send to client

    """

    def __init__(self, description, status_code):
        self.description = description
        self.status_code = status_code
