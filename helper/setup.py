# Import library
from os import getenv
from dotenv import load_dotenv

# Initialize class Setup
class Setup:
    # Constructor function
    def __init__(self, path=".env"):
        self.path = path
        self.loaded = False

    # Load the environment
    def load_env(self):
        if not self.loaded:
            load_dotenv(self.path)
            self.loaded = True

    # Make easier to call variable
    def get_variable(self, variable_name):
        self.load_env()
        return getenv(variable_name)