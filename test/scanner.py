# proses import library yang dibutuhkan (pandas, matplotlib, seaborn, nltk, Sastrawi, requests)
from pandas import read_csv, read_excel, isna
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from re import sub, IGNORECASE
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import os

nltk.download(['stopwords', 'punkt', 'vader_lexicon'])

def list_folders(directory):
    return [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]

def list_files(folder_path):
    return [f for f in os.listdir(folder_path) if f.endswith(('.csv', '.xlsx'))]

def display_menu_folder(options):
    print("\n # List Folder")
    for i, option in enumerate(options):
        if i < 9:
            print(f"    {i + 1}. {option}")
        else:
            print(f"   {i + 1}. {option}")
    print("\n    0. Exit")

def display_menu_file(options):
    print("\n # List File")
    for i, option in enumerate(options):
        if i < 9:
            print(f"    {i + 1}. {option}")
        else:
            print(f"   {i + 1}. {option}")
    print("\n    0. Back")

def read_csv_or_excel(file_path):
    if file_path.endswith('.csv'):
        return read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        return read_excel(file_path)

def clean_text(text):
    # Hapus karakter non-alfanumerik (hapus selain alphabet [kapital / nonkapital] + numeric)
    text = sub(r'[^a-zA-Z0-9\s]', '', text)

    # Tokenisasi (memisahkan setiap kata)
    words = word_tokenize(text)

    # Hapus kata-kata yang terdapat di kamus stopwords_id variable dari library sastrawi
    words = [word for word in words if word.lower() not in stopwords_id]

    # Gabungkan kembali kata-kata yang telah dipisah menjadi kalimat awal
    cleaned_text = ' '.join(words)

    # Mengembalikan kalimat yang telah dibersihkan
    return cleaned_text

def main():
    stopword_factory = StopWordRemoverFactory()
    stopwords_id = set(stopword_factory.get_stop_words())

    result_folder = "result"

    while True:
        os.system("cls||clear")

        folders = list_folders(result_folder)
        display_menu_folder(folders)

        try:
            choice_folder = int(input("\n > Select a folder (enter number): "))
            if choice_folder == 0:
                exit(0)
            elif 1 <= choice_folder <= len(folders):
                selected_folder = folders[choice_folder - 1]
                folder_path = os.path.join(result_folder, selected_folder)
                files = list_files(folder_path)
                display_menu_file(files)

                try:
                    choice_file = int(input("\n > Select a file (enter number): "))
                    if choice_file == 0:
                        continue
                    elif 1 <= choice_file <= len(files):
                        selected_file = files[choice_file - 1]
                        file_path = os.path.join(folder_path, selected_file)
                        df = read_csv_or_excel(file_path)
                        print(f"\n > Total data: {len(df)}")
                        # Analisis pengaruh harga terhadap total jumlah rating + set pengaturan grafik
                        sns.scatterplot(x='price', y='total_rating', hue='total_rating', palette='viridis', data=df)

                        # Set pengaturan grafik
                        plt.title('Pengaruh Harga Terhadap Total Jumlah Rating')
                        plt.xlabel('Harga')
                        plt.ylabel('Total Jumlah Rating')

                        # Tampilkan grafik
                        plt.show()
                        # print("\n # File Contents:")
                        # print(df)
                        input("\n > Back to main menu, press [ENTER]")
                except ValueError:
                    print("\n ! Invalid input: Please enter a valid number.")
        except ValueError:
            print("\n ! Invalid input: Please enter a valid number.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n > CTRL + C pressed.")
        exit()