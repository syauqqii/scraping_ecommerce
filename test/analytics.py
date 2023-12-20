import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
import re
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('vader_lexicon')

# -----------------------------

# Menggunakan Sastrawi untuk menghapus kata-kata umum bahasa Indonesia
stopword_factory = StopWordRemoverFactory()
stopwords_id = set(stopword_factory.get_stop_words())

# Fungsi untuk membersihkan teks
def clean_text(text):
    # Hapus karakter non-alfanumerik
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    # Tokenisasi
    words = word_tokenize(text)

    # Hapus kata-kata stop
    words = [word for word in words if word.lower() not in stopwords_id]

    # Gabungkan kembali kata-kata
    cleaned_text = ' '.join(words)

    return cleaned_text

# -----------------------------

# Ubah path sesuai dengan lokasi file CSV atau sumber data Anda
path_to_csv = "Parfum Wanita Tahan Lama.csv"

# Baca data dari CSV ke dalam DataFrame Pandas
df = pd.read_csv(path_to_csv)

# -----------------------------

# Analisis pengaruh harga terhadap total jumlah rating
sns.scatterplot(x='price', y='total_rating', hue='total_rating', palette='viridis', data=df)

plt.title('Pengaruh Harga Terhadap Total Jumlah Rating')
plt.xlabel('Harga')
plt.ylabel('Total Jumlah Rating')

# Tampilkan grafik
plt.show()

# -----------------------------

# cleaning text
df['cleaned_name'] = df['name'].apply(clean_text)

print(df[['name', 'cleaned_name']])

# -----------------------------

# Analisis sentimen menggunakan NLTK
sid = SentimentIntensityAnalyzer()
df['sentimen'] = df['cleaned_name'].apply(lambda x: sid.polarity_scores(x)['compound'])

# Korelasi dengan penjualan
sns.scatterplot(x='sentimen', y='sold', data=df)
sns.scatterplot(x='liked', y='sold', hue='total_rating', palette='viridis', data=df)

plt.title('Pengaruh Sentimen terhadap Penjualan Produk')
plt.xlabel('Sentimen')
plt.ylabel('Jumlah Terjual')

# Tampilkan grafik
plt.show()

# -----------------------------

# Analisis pengaruh like terhadap total jumlah produk terjual
sns.scatterplot(x='liked', y='sold', hue='total_rating', palette='viridis', data=df)

plt.title('Hubungan Like terhadap Jumlah Produk Terjual')
plt.xlabel('Jumlah Like')
plt.ylabel('Jumlah Terjual')

# Tampilkan grafik
plt.show()

# -----------------------------

# Analisis pengaruh Rating Star terhadap total jumlah produk terjual
sns.scatterplot(x='rating_star', y='sold', hue='total_rating', palette='viridis', data=df)

plt.title('Pengaruh Rating Star terhadap Jumlah Produk Terjual')
plt.xlabel('Rating Star')
plt.ylabel('Jumlah Terjual')

# Tampilkan grafik
plt.show()

# -----------------------------