# Import library
from os import name, system
from datetime import datetime

# Initialize class Other
class Other:
    # Make function to clear screen console
    @staticmethod
    def clear_screen():
        if name == "nt":
            system("cls")
        elif name == "posix":
            system("clear")
        else:
            pass

    # Make function to return timestamp of now
    @staticmethod
    def get_datetime():
        now = datetime.now()

        # Make optimize code to return timestamp format
        def fnum(number):
            return str(number).zfill(2)

        # return fnum(now.hour), fnum(now.minute), fnum(now.second), fnum(now.day), fnum(now.month), now.year
        return fnum(now.day), fnum(now.month), now.year

    @staticmethod
    def get_banner():
        print("""  __ _
 / _\\ |__   ___  _ __   ___  ___
 \\ \\| '_ \\ / _ \\| '_ \\ / _ \\/ _ \\
 _\\ \\ | | | (_) | |_) |  __/  __/
 \\__/_| |_|\\___/| .__/ \\___|\\___|
                |_|""")