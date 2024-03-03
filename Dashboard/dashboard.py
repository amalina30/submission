import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import datetime

from babel.numbers import format_currency
sns.set(style='dark')

def create_day_df(df):
    df.rename(columns={
        "instant": "no"
    }, inplace=True)

    return df

def create_hour_df(df):
    df.rename(columns={
        "instant": "no"
    }, inplace=True)

    return df

# Load cleaned data
merged_df = pd.read_csv("C:\Lina\Kuliah\Bangkit\Dashboard\merged.csv")

datetime_column = ["dteday"]
for column in datetime_column:
    merged_df[column] = pd.to_datetime(merged_df[column])

min_date = merged_df["dteday"].min()
max_date = merged_df["dteday"].max()

with st.sidebar:
    # Tambah Logo
    st.image("https://raw.githubusercontent.com/amalina30/dashboard/main/resize.png")
    
    tanggal_mulai, tanggal_akhir = st.date_input(
        label='Waktu', min_value=min_date, max_value=max_date, value=[min_date, max_date]
    )

main_df = merged_df[(merged_df["dteday"] >= str(tanggal_mulai)) & (merged_df["dteday"] <= str(tanggal_akhir))]

# Dataframe
day_df = create_day_df(main_df)
hour_df = create_hour_df(main_df)

st.header('Bike Sharing Dataset')

st.subheader("Musim Terbaik Perentalan Sepeda")

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20, 10))

# Membuat plot untuk musim terbaik
colors_best_season = sns.color_palette("viridis", n_colors=len(day_df))
sns.barplot(x="cnt", y="season", data=day_df.sort_values(by="cnt", ascending=False), palette=colors_best_season, ax=ax)
ax.set_ylabel("Musim", fontsize=20)
ax.set_xlabel("Jumlah Rental", fontsize=20)
ax.set_title("Musim Terbaik Perentalan Sepeda", loc="center", fontsize=30)
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', labelsize=15)

# Tampilkan plot menggunakan streamlit
st.pyplot(fig)

# Fungsi untuk mencari penjualan terbanyak
def penjualan_terbanyak(data):
    maksimum = data['cnt'].max()
    bulan_terbanyak = data.loc[data['cnt'] == maksimum, 'no'].values[0]
    return bulan_terbanyak, maksimum

st.subheader("Jumlah Rental Sepeda per Bulan")

# Plotting
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 8))

# Membuat plot untuk jumlah rental sepeda per bulan
sns.barplot(x="no", y="cnt", data=day_df, color='green', alpha=0.8, ax=ax)
ax.set_xlabel('Bulan', fontsize=15)
ax.set_ylabel('Jumlah Rental Sepeda', fontsize=15)
ax.set_title('Jumlah Rental Sepeda per Bulan', fontsize=20)
ax.tick_params(axis='both', labelsize=12)

# Menambahkan garis vertikal untuk menunjukkan bulan dengan rental terbanyak
bulan_terbanyak, _ = penjualan_terbanyak(day_df)
ax.axvline(x=int(bulan_terbanyak), color='blue', linestyle='--', label=f'Bulan dengan Rental Terbanyak ({bulan_terbanyak})')
ax.legend()

# Tampilkan plot menggunakan streamlit
st.pyplot(fig)

baris_terlama = hour_df.nlargest(5, 'hr')

st.subheader("Jumlah Rental Sepeda per Jam")

# Plotting
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 8))

# Membuat plot untuk jumlah rental sepeda per jam
sns.barplot(x="hr", y="cnt", data=hour_df, color='gray', alpha=0.5, label='Lainnya', ax=ax)
sns.barplot(x="hr", y="cnt", data=baris_terlama, color='red', alpha=0.7, label='Teratas', ax=ax)

ax.set_xlabel('Jam', fontsize=15)
ax.set_ylabel('Jumlah Rental Sepeda', fontsize=15)
ax.set_title('Jumlah Rental Sepeda per Jam', fontsize=20)
ax.set_xticks(hour_df['hr'])
ax.legend()

# Tampilkan plot menggunakan streamlit
st.pyplot(fig)

st.subheader("Jumlah Rental Sepeda Berdasarkan Weathersit")

# Buat color palette yang berbeda untuk setip kategori 'Weathersit'
colors = {1: 'blue', 2: 'green', 3: 'orange', 4: 'red'}

# Selectbox untuk memilih weathersit
selected_weathersit = st.selectbox('Pilih Weathersit', list(colors.keys()))

# Filter dataset berdasarkan weathersit yang dipilih
weather_rentals = hour_df[hour_df['weathersit'] == selected_weathersit]

# Plot line chart menggunakan matplotlib
fig, ax = plt.subplots()
ax.plot(weather_rentals['no'], weather_rentals['cnt'], color=colors[selected_weathersit], label=f'Weathersit {selected_weathersit}')
ax.set_xlabel('Instant')
ax.set_ylabel('Jumlah Rental Sepeda')
ax.set_title(f'Rental Sepeda pada Weathersit {selected_weathersit}')
ax.legend()

# Tampilkan plot menggunakan Streamlit
st.pyplot(fig)

# Tampilkan data dalam bentuk tabel
st.dataframe(weather_rentals[['no', 'cnt']])