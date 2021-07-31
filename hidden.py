import os
from dotenv import load_dotenv

class Hidden:
    def token(self):
        load_dotenv()
        
        token = os.getenv('TOKEN')
        return token
