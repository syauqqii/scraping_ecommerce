# Import library
from os import makedirs, path
from pandas import DataFrame

# Initialize class Export
class Export:
    # Make function to check directory existence
    def is_directory_exists(self, dir_name):
        if path.exists(dir_name):
            return True
        else:
            return False

    # Make function to make directory
    def make_directory(self, dir_name):
        if not self.is_directory_exists(dir_name):
            try:
                makedirs(dir_name)
            except OSError:
                # Exception handling if cant make directory
                print("\n > Error: Cannot make directory\n   [DEBUG: make_directory() => (helper/other.py)]")
                exit()
        else:
            pass

     # Make function to check file existence
    def is_file_exists(self, directory, filename):
        file_path = path.join(directory, filename)
        return path.exists(file_path)

    # Make function to make file
    def make_file(self, directory, filename, data):
        if self.is_directory_exists(directory):
            with open(f"{directory}/{filename}", "w") as file:
                file.write(data)
        else:
            self.make_directory(directory)
            with open(f"{directory}/{filename}", "w") as file:
                file.write(data)

    # Make function to make file .csv or .xlsx
    def export_file(self, directory, filename, dataframe, config=1):
        if self.is_directory_exists(directory):
            try:
                if int(config) == 1:
                    dataframe.to_csv(f"{directory}/{filename}", index=False)
                else:
                    dataframe.to_excel(f"{directory}/{filename}", index=False)
            except Exception as e:
                # Exception handling if cant make directory
                print("\n > Error: Cannot make file\n   [DEBUG: export_file() => (helper/export.py)]")
                # print(f"\n > Error: Cannot make file\n   [DEBUG: export_file() => (helper/export.py)]\n\n > ERROR: {e}")
                exit()
        else:
            self.make_directory(directory)
            try:
                if int(config) == 1:
                    dataframe.to_csv(f"{directory}/{filename}", index=False)
                else:
                    dataframe.to_excel(f"{directory}/{filename}", index=False)
            except Exception as e:
                # Exception handling if cant make directory
                print("\n > Error: Cannot make file\n   [DEBUG: export_file() => (helper/export.py)]")
                # print(f"\n > Error: Cannot make file\n   [DEBUG: export_file() => (helper/export.py)]\n\n > ERROR: {e}")
                exit()