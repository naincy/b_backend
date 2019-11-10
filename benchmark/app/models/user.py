import json

# User Model Class
class User:

    def __init__(self, name = None, email = None, password = None):
        self.email = email
        self.password = password
        self.name = name
        self.profile = {
            'role' : 'L1',
            'skills' : [],
            'image' : None,
            'interests' : [],
            'devices':[],
            'searchHistory':[]
        }
        
        

    def __str__(self):
        dict = {"name":self.name, "email":self.email}
        return json.dumps(dict)