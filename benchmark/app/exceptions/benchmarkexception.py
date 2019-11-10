# Custom Exception Class
class BenchMarkException(Exception): 
  
    # Constructor or Initializer 
    def __init__(self, message, code): 
        self.message = message 
        self.code = code
  
   