# import display as display

class Login:
    def __init__(self, id, password):
        self.id = id
        self.password = password
        
    #accepts a login request with user id and password and validates or rejects user
    def login_request(self):
      if(self.id=="operator" and self.password=="cs347"):
        return "operator"
      elif (self.id=="technician" and self.password=="cs347"): 
        return "technician"
      else:
        return "Login Failed. Please Try Again."
        

        
