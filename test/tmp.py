from pandas import read_csv, read_excel, isna
import os

def list_folders(directory):
    return [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]

def list_files(folder_path):
    return [f for f in os.listdir(folder_path) if f.endswith(('.csv', '.xlsx'))]

def display_menu_folder(options):
    print("\n [#] List Folder")
    for i, option in enumerate(options):
        if i < 9:
            print(f"     {i + 1}). {option}")
        else:
            print(f"    {i + 1}). {option}")
    print("\n     0). Exit")

def display_menu_file(selected_folder, list_file):
    print(f"\n [#] List File from Folder '{selected_folder}'")
    for i, option in enumerate(list_file):
        if i < 9:
            print(f"     {i + 1}). {option}")
        else:
            print(f"    {i + 1}). {option}")
    print("\n     0). Back")

def read_csv_or_excel(file_path):
    if file_path.endswith('.csv'):
        return read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        return read_excel(file_path)

def main():
    result_folder = "../result"

    while True:
        os.system("cls||clear")
        
        folders = list_folders(result_folder)
        display_menu_folder(folders)

        try:
            choice_folder = int(input("\n [>] Select a folder (enter number): "))
            if choice_folder == 0:
                exit(0)
            elif 1 <= choice_folder <= len(folders):
                os.system("cls||clear")
        
                selected_folder = folders[choice_folder - 1]
                folder_path = os.path.join(result_folder, selected_folder)
                files = list_files(folder_path)
                display_menu_file(selected_folder, files)

                try:
                    choice_file = int(input("\n [>] Select a file (enter number): "))
                    if choice_file == 0:
                        continue
                    elif 1 <= choice_file <= len(files):
                        selected_file = files[choice_file - 1]
                        file_path = os.path.join(folder_path, selected_file)
                        df = read_csv_or_excel(file_path)
                        print(df)
                        input("\n [>] Back to main menu, press [ENTER]")
                    else:
                        print(f"\n [!] Invalid input: Please enter a valid number [{0}..{len(files)}]")
                        input("     Back to main menu, press [ENTER]")
                except ValueError:
                    print("\n [!] Invalid input: Please enter a valid number.")
                    input("     Back to main menu, press [ENTER]")
            else:
                print(f"\n [!] Invalid input: Please enter a valid number [{0}..{len(folders)}]")
                input("     Back to main menu, press [ENTER]")
        except ValueError:
            print("\n [!] Invalid input: Please enter a valid number.")
            input("     Back to main menu, press [ENTER]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n > CTRL + C pressed.")
        exit()