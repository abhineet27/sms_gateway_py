
class Response:
    def __init__(self, message , error):
        self.message = message
        self.error = error

    def get_error(self):
        return self.error
    
    def get_message(self):
        return self.message
