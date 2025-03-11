import numpy as np
import seaborn as sns 
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from babel.numbers import format_currency 
sns.set(style='dark')


# def fungsi

def create_daily_orders_df(df):
    daily_orders_df = df.resample(
        rule='D',
        on='order_purchase_timestamp'
    ).agg({
        'order_id': 'nunique',
        'total_price': 'sum'
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        'order_id': 'order_count',
        'total_price': 'revenue'
    }, inplace=True)
    
    return daily_orders_df 

def create_sum_order_items_df(df):
    sum_order_items_df = df.groupby(by='product_category_name_english').order_item_id.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df 

def create_rfm_df(df):
    rfm_df = df.groupby(by='customer_unique_id', as_index=False).agg({
        'order_purchase_timestamp': 'max',
        'order_id': 'nunique',
        'total_price': 'sum'
    })
    rfm_df.columns = ['customer_id','max_order_timestamp', 'frequency', 'monetary']
    
    rfm_df['max_order_timestamp'] = rfm_df['max_order_timestamp'].dt.date
    recent_date = df['order_purchase_timestamp'].dt.date.max()
    rfm_df['recency'] = rfm_df['max_order_timestamp'].apply(lambda x: (recent_date-x).days)
    rfm_df.drop('max_order_timestamp', axis=1, inplace=True)
    rfm_df['customer_id_short'] = '...' + rfm_df['customer_id'].astype(str).str[-5:] # lima digit terakhir

    return rfm_df 

all_df = pd.read_csv('https://raw.githubusercontent.com/wildan-wicaksono/brazilian_e-commerce/refs/heads/main/dashboard/all_data_proyek.csv')

all_df['order_purchase_timestamp'] = pd.to_datetime(all_df['order_purchase_timestamp'])
print(all_df.info())

min_date = all_df['order_purchase_timestamp'].min()
max_date = all_df['order_purchase_timestamp'].max()

with st.sidebar:
    st.image("https://cdn.brandfetch.io/idvSn4Org5/w/1200/h/1200/theme/dark/icon.jpeg?c=1dxbfHSJFAPEGdCLU4o5B")
    start_date, end_date = st.date_input(
    label='Rentang Waktu',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
    )
    st.markdown('© 2025 Wildan Bagus Wicaksono')

main_df = all_df[(all_df['order_purchase_timestamp'].dt.date >= (start_date))
                 & (all_df['order_purchase_timestamp'].dt.date <= (end_date))]

daily_orders_df = create_daily_orders_df(main_df)
sum_order_items_df = create_sum_order_items_df(main_df)
rfm_df = create_rfm_df(main_df)
print(rfm_df)


#================================================================================= MEMANGGIL SEBAGIAN DATA

# menampilkan kategori produk yang terjual dengan order terbanyak-tersedikit, dan rata-rata review_score masing-masing (pertanyaan 1-2)
category_orders_df = all_df.groupby(by='product_category_name_english').agg({
    'order_id': 'nunique',
    'total_price': 'sum',
    'review_score': 'mean'
})
category_orders_df.rename(columns={
    'order_id': 'order_count',
    'total_price': 'revenue'
}, inplace=True)
#category_orders_df.sort_values(by='order_count', ascending=False, inplace=True)


customer_review = all_df.groupby('customer_unique_id').agg({
    'order_id': 'nunique',
    'review_score': 'mean'
})
customer_review.rename(columns={
    'order_id': 'order_count',
    'review_score': 'avg_review_score'
}, inplace=True)
customer_review.sort_values(by='order_count', ascending=False, inplace=True)

corr_review_OrderCount = customer_review['order_count'].corr(customer_review['avg_review_score'])

# df order dan pendapatan tahun 2016
all_df_2016 = all_df[all_df['order_purchase_timestamp'].dt.year == 2016]
monthly_orders_df_2016 = all_df_2016.resample(rule='M', on='order_purchase_timestamp').agg({
    'order_id': 'nunique',  # menghitung banyak order
  'total_price': 'sum'      # menghitung pendapatan
})

# format bulan
monthly_orders_df_2016.index = monthly_orders_df_2016.index.strftime('%B')
monthly_orders_df_2016 = monthly_orders_df_2016.reset_index()

# rename nama kolom
monthly_orders_df_2016.rename(columns={
    'order_id': 'order_count',
    'total_price': 'revenue'
}, inplace=True)

# df order dan pendapatan tahun 2017
all_df_2017 = all_df[all_df['order_purchase_timestamp'].dt.year == 2017]
monthly_orders_df_2017 = all_df_2017.resample(rule='M', on='order_purchase_timestamp').agg({
    'order_id': 'nunique',  # menghitung banyak order
  'total_price': 'sum'      # menghitung pendapatan
})

# format bulan
monthly_orders_df_2017.index = monthly_orders_df_2017.index.strftime('%B')
monthly_orders_df_2017 = monthly_orders_df_2017.reset_index()

# rename nama kolom
monthly_orders_df_2017.rename(columns={
    'order_id': 'order_count',
    'total_price': 'revenue'
}, inplace=True)

# df order dan pendapatan tahun 2018
all_df_2018 = all_df[all_df['order_purchase_timestamp'].dt.year == 2018]
monthly_orders_df_2018 = all_df_2018.resample(rule='M', on='order_purchase_timestamp').agg({
    'order_id': 'nunique',  # banyak pesanan
  'total_price': 'sum'      # total pendapatan
})

# format bulanan
monthly_orders_df_2018.index = monthly_orders_df_2018.index.strftime('%B')
monthly_orders_df_2018 = monthly_orders_df_2018.reset_index()

# rename nama kolom
monthly_orders_df_2018.rename(columns={
    'order_id': 'order_count',
    'total_price': 'revenue'
}, inplace=True)

all_df_sold_revenue = all_df.groupby('product_category_name').agg({
    'order_id': 'nunique',
    'total_price': 'sum',
    'review_score': 'mean'
})
all_df_sold_revenue.rename(columns={
    'order_id': 'order_count',
    'total_price': 'revenue',
    'review_score': 'avg_review_score'
}, inplace=True)


#==================================================================================== PEMBUATAN DASHBOARD

st.title('Analisis E-Commerce Olist')

## Sec1: Pesanan Harian dan Total Pendapatan

st.header('Pesanan Harian dan Total Pendapatan')

col1, col2 = st.columns(2) 
with col1:
    total_orders = daily_orders_df.order_count.sum()
    st.metric('Total Pesanan', value=total_orders)
with col2:
    total_revenue = format_currency(daily_orders_df.revenue.sum(), 'BRL', locale='es_CO')
    st.metric('Total Pendapatan', value=total_revenue)

tab1, tab2 = st.tabs(['Pesanan Harian', 'Pendapatan Harian'])
with tab1:
    fig, ax = plt.subplots(figsize=(16,8))
    ax.plot(
        daily_orders_df['order_purchase_timestamp'],
        daily_orders_df['order_count'],
        marker='o',
        linewidth=2,
        color='#90CAF9'
    )
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    st.pyplot(fig)
with tab2:
    fig, ax = plt.subplots(figsize=(16,8))
    ax.plot(
        daily_orders_df['order_purchase_timestamp'],
        daily_orders_df['revenue'],
        marker='o',
        linewidth=2,
        color='#90CAF9'
    )
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    st.pyplot(fig)

st.markdown(
    """
Pemesanan harian pada tahun 2016 sangat rendah, namun sempat menaik pada awal bulan Oktober dan mulai menurun saat memasuki pertengahan Oktober. 
Pada tahun 2016 penjualan harian mulai relatif menaik dan puncaknya terjadi pada bulan November secara signifikan dan turun kembali secara signifikan.
Pada tahun 2017 pemesanan yang dilakukan relatif konsisten, namun pada bulan Agustus mulai terjadi penurunan. Pola yang serupa untuk pendapatan harian.
    """
)

# Sec 2: Pemesanan dan Kateogori Produk

st.header('Produk dan Pelanggan')

colors =  ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

## 2.1 : Pemesanan Per Bulan

st.subheader('Banyak Pesanan dan Total Pendapatan Per Bulan')

tab1, tab2, tab3 = st.tabs(['2016', '2017', '2018'])
with tab1:
    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(24,20))

    # objek 1
    sns.lineplot(x='order_purchase_timestamp', y='order_count', data=monthly_orders_df_2016, palette=colors, ax=ax[0],
            marker='o',linewidth=4,markersize=15)
    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("Total Pemesanan", loc="center", fontsize=22)
    ax[0].tick_params(axis='x', labelsize=20)
    ax[0].tick_params(axis ='y', labelsize=20)
    ax[0].grid()

    # objek 2
    sns.lineplot(x="order_purchase_timestamp", y="revenue", data=monthly_orders_df_2016, palette=colors, ax=ax[1],
            marker='o',linewidth=4,markersize=15)
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].yaxis.set_label_position("right")
    ax[1].set_title("Total Pendapatan", loc="center", fontsize=22)
    ax[1].tick_params(axis='x', labelsize=20)
    ax[1].tick_params(axis='y', labelsize=20)
    ax[1].grid()

    # judul
    plt.suptitle("Banyak Pesanan dan Total Pendapatan Per Bulan (2016)", fontsize=25,y=.92)
    st.pyplot(fig)
with tab2:
    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(24,20))
# objek 1
    sns.lineplot(x='order_purchase_timestamp', y='order_count', data=monthly_orders_df_2017, palette=colors, ax=ax[0],
            marker='o',linewidth=4,markersize=15)
    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("Total Pemesanan", loc="center", fontsize=22)
    ax[0].tick_params(axis='x', labelsize=20, rotation=40)
    ax[0].tick_params(axis ='y', labelsize=20)
    ax[0].grid()

    # objek 2
    sns.lineplot(x="order_purchase_timestamp", y="revenue", data=monthly_orders_df_2017, palette=colors, ax=ax[1],
            marker='o',linewidth=4,markersize=15)
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].yaxis.set_label_position("right")
    ax[1].set_title("Total Pendapatan", loc="center", fontsize=22)
    ax[1].tick_params(axis='x', labelsize=20, rotation=40)
    ax[1].tick_params(axis='y', labelsize=20)
    ax[1].grid()

    # judul
    plt.suptitle("Banyak Pesanan dan Total Pendapatan Per Bulan (2017)", fontsize=25,y=.92)

    st.pyplot(fig)
with tab3:
    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(24,20))

# objek 1
    sns.lineplot(x='order_purchase_timestamp', y='order_count', data=monthly_orders_df_2018, palette=colors, ax=ax[0],
          marker='o',linewidth=4,markersize=15)
    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("Total Pemesanan", loc="center", fontsize=22)
    ax[0].tick_params(axis='x', labelsize=20, rotation=40)
    ax[0].tick_params(axis ='y', labelsize=20)
    ax[0].grid()

    # objek 2
    sns.lineplot(x="order_purchase_timestamp", y="revenue", data=monthly_orders_df_2018, palette=colors, ax=ax[1],
            marker='o',linewidth=4,markersize=15)
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].yaxis.set_label_position("right")
    ax[1].set_title("Total Pendapatan", loc="center", fontsize=22)
    ax[1].tick_params(axis='x', labelsize=20, rotation=40)
    ax[1].tick_params(axis='y', labelsize=20)
    ax[1].grid()

    # judul
    plt.suptitle("Banyak Pesanan dan Total Pendapatan Per Bulan (2018)", fontsize=25,y=.92)

    st.pyplot(fig)

st.markdown("""**Pertanyaan 1: Berapa jumlah order dan pendapatan yang diperoleh dalam beberapa bulan terakhir?**""")

st.markdown("""Jumlah pesanan dan total pendapatan yang diperoleh pada masing-masing bulan tertera pada diagram di atas.
            Banyaknya pemesanan berbanding lurus dengan total pendapatan yang diperoleh sehingga memiliki pola yang sama.""")
            
st.markdown("""Pada tahun 2016, total pesanan sempat menaik pada September-Oktober dan mulai menurun secara konstan pada hingga
            November. Sedangkan, pada November-Desember tidak ada pesanan. 
            Jumlah pesanan pada tahun 2017 pada Januari-November jumlah pesanannya relatif naik. Kenaikan signifikan terjadi
            pada Oktober-November dan selanjutnya menurun hingga Desember. 
            Jumlah pesanan pada tahun 2018 pada Januari-Agustus relatif konstan, namun mulai menurun secara signifikan pada
            Agustus-September.""")

# 2.2 : Banyak Pesanan, Kesetiaan Pelanggan, dan Skor Review

st.subheader("Banyak Pesanan, Kesetiaan Pelanggan, dan Skor Review")

col1, col2 = st.columns(2)

with col1:
    # Korelasi order_count-review_score (pertanyaan 2)
    corr_sold_review_score = round(all_df_sold_revenue['order_count'].corr(all_df_sold_revenue['avg_review_score']),3)
    st.metric('Korelasi Banyak Pesanan dan Skor Review', value=corr_sold_review_score)
with col2:
    corr_review_OrderCount = round(customer_review['order_count'].corr(customer_review['avg_review_score']),3)
    st.metric('Korelasi Banyak Pembelian Customer dan Skor Review', value=corr_review_OrderCount)

tab1, tab2 = st.tabs(['Banyak Pesanan', 'Skor Review'])
with tab1:
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35,15))
    # objek 1
    sns.barplot(x='order_count', y='product_category_name_english', data=category_orders_df.sort_values(by="order_count", ascending=False).head(5), palette=colors, ax=ax[0])
    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("Kategori Terbaik", loc="center", fontsize=35)
    ax[0].tick_params(axis ='y', labelsize=30)
    ax[0].tick_params(axis='x', labelsize=30)

    # objek 2
    sns.barplot(x="order_count", y="product_category_name_english", data=category_orders_df.sort_values(by="order_count", ascending=True).head(5), palette=colors, ax=ax[1])
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].invert_xaxis()
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].set_title("Kategori Terburuk", loc="center", fontsize=35)
    ax[1].tick_params(axis='y', labelsize=30)
    ax[1].tick_params(axis='x', labelsize=30)
    # judul
    
    plt.suptitle("Kategori Produk Terbaik dan Terburuk Berdasarkan Banyak Pembelian", fontsize=40)
    st.pyplot(fig)

with tab2:
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35,15))
    sns.barplot(x='review_score', y='product_category_name_english', data=category_orders_df.sort_values(by='review_score', ascending=False).head(5), palette=colors, ax=ax[0])
    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("Kategori Terbaik", loc="center", fontsize=35)
    ax[0].tick_params(axis ='y', labelsize=30)
    ax[0].tick_params(axis='x', labelsize=30)

    # objek 2
    sns.barplot(x="review_score", y="product_category_name_english", data=category_orders_df.sort_values(by="review_score", ascending=True).head(5), palette=colors, ax=ax[1])
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].set_xlim(0,5)
    ax[1].invert_xaxis()
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].set_title("Kategori Terburuk", loc="center", fontsize=35)
    ax[1].tick_params(axis='y', labelsize=30)
    ax[1].tick_params(axis='x', labelsize=30)

    plt.suptitle("Kategori Produk Terbaik dan Terburuk Berdasarkan Skor Review", fontsize=40)
    st.pyplot(fig)

fig, ax = plt.subplots(figsize=(10, 6))
sns.regplot(x=customer_review['order_count'], y=customer_review['avg_review_score'],scatter_kws={'alpha':0.3}, line_kws={'color':'red'})
ax.set_title('Distribusi Frekuensi Pembelian Pelanggan dan Rata-Rata Skor Review')
ax.set_xlabel('Frekuensi Pembelian')
ax.set_ylabel('Rata-Rata Skor Review')
ax.grid()

st.pyplot(fig)

st.markdown("**Pertanyaan 2: Bagaimana perbandingan kategori produk berdasarkan banyak pemesanan dan rata-rata skor review? Apakah ada hubungan diantara keduanya?**")

st.markdown("""Perhatikan diagram pertama mengenai perbandingan kategori produk terbaik dan terburuk berdasarkan banyak pemesanan dan review skor.
            Dari September 2016 hingga September 2018, diperoleh:
- Berdasarkan banyaknya pemesanan, lima kategori produk terbaik diduduki oleh bed bath table, health beauty, sports leisure, computers accessories, dan funniture decor. Sedangkan, lima kategori terburuk diduduki oleh security and services, fashion childres clothes, cds dvds musicals, la cuisine, dan art and craftmanship.
- Berdasarkan review skor, lima kategori produk terbaik diduduki oleh cds dvds musicals, fashion childres clothes, books general interest, books imported, construcion tool tools. Sedangkan, kategori terburuk diduduki oleh security and services, dispers and hygiene, office furniture, home comfort 2, dan fashion male clothing.

Dari sini dapat ditunjukkan bahwa security and services mendapatkan kategori terburuk dari segi banyak pemesanan dan review skor. Setelah ditinjau korelasi antara banyaknya pemesanan dan skor review hasilnya hanyalah sekitar 3%. Artinya, hampir tidak ada hubungan sama sekali diantara keduanya.
""")

st.markdown("**Pertanyaan 3: Apakah ada hubungan antara banyak pemesanan pelanggan dengan skor review yang diberikan?**")

st.markdown("""Perhatikan diagram pertama mengenai hubungan rata-rata skor review yang diperoleh dengan frekuensi pembelian oleh seorang pelanggan.
            Sebagian besar pelanggan hanya melakukan pembelian sebanyak 1 hingga 3 kali walau memberikan review skor yang baik. Sebagian
            besar pelanggan melakukan pembelian lebih dari tiga kali apabila rating yang diperoleh 3 hingga 5. Setelah ditinjau nilai korelasi diantara
            kedua hal tersebut, ternayta hasil yang diperoleh mendekati 0 sehingga hampir tidak menunjukkan adanya hubungan diantara keduanya.""")


# SEC 3:

st.subheader('Pelanggan Terbaik Berdasaran Parameter RFM')

col1, col2, col3 = st.columns(3)

with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric('Rata-Rata Kehadiran (hari)', value=avg_recency)
with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric('Rata-Rata Frekuensi', value=avg_frequency)
with col3:
    avg_monetary = format_currency(rfm_df.monetary.mean(), "BRL", locale='es_CO') 
    st.metric("Rata-Rata Moneter", value=avg_monetary)

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))
colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]


sns.barplot(y="recency", x="customer_id_short", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0]).set_ylim(bottom=0)
ax[0].set_ylabel(None)
ax[0].set_xlabel("customer_id (lima karakter terakhir)", fontsize=30)
ax[0].set_title("Berdasarkan Kehadiran (hari)", loc="center", fontsize=40)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=30, rotation=45)
 
sns.barplot(y="frequency", x="customer_id_short", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("customer_id (lima karakter terakhir)", fontsize=30)
ax[1].set_title("Berdasarkan Frekuensi", loc="center", fontsize=40)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=30, rotation=45)
 
sns.barplot(y="monetary", x="customer_id_short", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel("customer_id (lima karakter terakhir)", fontsize=30)
ax[2].set_title("Berdasarkan Moneter", loc="center", fontsize=40)
ax[2].tick_params(axis='y', labelsize=30)
ax[2].tick_params(axis='x', labelsize=30, rotation=45)
 
st.pyplot(fig)

st.markdown("""**Pertanyaan 4: Kapan terakhir pembeli membeli produk?**""")

st.markdown("Pelanggan yang terakhir kali melakukan pembelian tepat pada 3 Oktober 2018, kemudian 4 pelanggan selanjutnya melakukan pembelian 5 hari sebelumnya.")

st.markdown("**Pertanyaan 5: Berapa kali pelanggan melakukan pembelian dalam periode tertentu?**")

st.markdown("Dua pelanggan teratas telah melakukan pembelian sebanyak 25 kali, kemudian dilanjutkan 3 pelanggan yang melakukan pembelian berturut-turut 21, 20, dan 20 kali.")

st.markdown("**Pertanyaan 6: Berapa rata-rata uang yang dikeluarkan pelanggan dalam pembelian pada periode tertentu?**")

st.markdown("Pelanggan teratas yang mengeluarkan uang untuk pembelian memiliki perbedaan yang signifikan dengan orang ke-2.")

st.header("Kesimpulan")

st.markdown("""Banyaknya pemesanan mulai menunjukkan hasil pada tahun 2017 karena memiliki kenaikan yang dilanjutkan pada tahun 2018 menjadi relatif konstan. 
    Hasil review yang diberikan pelanggan tidak menunjukkan adanya hubungan antara banyaknya produk yang dibeli setiap pelanggan atau secara total dalam per kategorinya.
    Kemungkinan pembeli melakukan pembelian berdasarkan kebutuhan yang ada, terutama pada kebutuhan pribadi yang ditunjukkan tingginya pemesanan kategori "bed bath table".
    Berdasarkan kesetiaan pelanggan menggunakan analisa RFM, pelanggan terakhir baru saja melakukan transaksi dalam waktu yang hampir bersamaan. Pelanggan dengan ID berakhir
    "... c8455" merupakan pelanggan teraktif dan pelanggan dengan ID berakhir "... 7bc16" memiliki kontribusi finansial terbesar. Karena pelanggan dengan ID berakhir
    "...46268", "...f1782", dan "...95f33" memiliki metrik yang rendah di frekuensi maupun moneter, maka diperlukan perhatian khusus agar tetap loyal. Demikian juga pada produk
            dengan pembelian rendah diperlukan perhatian khusus agar tetap menjadi mitra Olist. Pelanggan yang lumayan aktif diberikan hak-hak tertentu agar tertarik untuk menambah frekuensi pembelian.
""")
