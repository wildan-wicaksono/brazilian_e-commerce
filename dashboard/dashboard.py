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
    rfm_df = df.groupby(by='customer_id', as_index=False).agg({
        'order_purchase_timestamp': 'max',
        'order_id': 'count',
        'total_price': 'sum'
    })
    rfm_df.columns = ['customer_id','max_order_timestamp', 'frequency', 'monetary']
    
    rfm_df['max_order_timestamp'] = rfm_df['max_order_timestamp'].dt.date
    recent_date = df['order_purchase_timestamp'].dt.date.max()
    rfm_df['recency'] = rfm_df['max_order_timestamp'].apply(lambda x: (recent_date-x).days/30)
    rfm_df.drop('max_order_timestamp', axis=1, inplace=True)
    rfm_df['customer_id_short'] = '...' + rfm_df['customer_id'].astype(str).str[-5:] # lima digit terakhir

    return rfm_df 

all_df = pd.read_csv('all_data_proyek.csv')

all_df['order_purchase_timestamp'] = pd.to_datetime(all_df['order_purchase_timestamp'])
print(all_df.info())

min_date = all_df['order_purchase_timestamp'].min()
max_date = all_df['order_purchase_timestamp'].max()

with st.sidebar:
    st.image("https://cdn.brandfetch.io/idvSn4Org5/w/1200/h/1200/theme/dark/icon.jpeg?c=1dxbfHSJFAPEGdCLU4o5B")
    start_date, end_date = st.date_input(
    label='Time Span',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
    )

main_df = all_df[(all_df['order_purchase_timestamp'] >= str(start_date))
                 & (all_df['order_purchase_timestamp'] <= str(end_date))]

daily_orders_df = create_daily_orders_df(main_df)
sum_order_items_df = create_sum_order_items_df(main_df)
rfm_df = create_rfm_df(main_df)
print(rfm_df)

st.header('Olist Cllection Dashboard')
st.subheader('Daily Orders')

col1, col2 = st.columns(2) 
with col1:
    total_orders = daily_orders_df.order_count.sum()
    st.metric('Total orders', value=total_orders)
with col2:
    total_revenue = format_currency(daily_orders_df.revenue.sum(), 'BRL', locale='es_CO')
    st.metric('Total Revenue', value=total_revenue)

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

st.subheader('Best and Worst Product Categories by Number of Purchases')

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35,15))
colors =  ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x='order_item_id', y='product_category_name_english', data=sum_order_items_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Best Product Categories", loc="center", fontsize=50)
ax[0].tick_params(axis ='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(x="order_item_id", y="product_category_name_english", data=sum_order_items_df.sort_values(by="order_item_id", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Product Categories", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)
st.subheader('Best Customer Based on RFM Parameters')

col1, col2, col3 = st.columns(3)

with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric('Average Recency (days)', value=avg_recency)
with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric('Average Frequency', value=avg_frequency)
with col3:
    avg_monetary = format_currency(rfm_df.monetary.mean(), "BRL", locale='es_CO') 
    st.metric("Average Monetary", value=avg_monetary)

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))
colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]

#print(rfm_df.sort_values(by="recency", ascending=True).head(5))

sns.barplot(y="recency", x="customer_id_short", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("customer_id (last five digits)", fontsize=30)
ax[0].set_title("By Recency (days)", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=30, rotation=45)
 
sns.barplot(y="frequency", x="customer_id_short", data=rfm_df.sort_values(by="recency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("customer_id (last five digits)", fontsize=30)
ax[1].set_title("By Frequency", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=30, rotation=45)
 
sns.barplot(y="monetary", x="customer_id_short", data=rfm_df.sort_values(by="recency", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel("customers_id (last five digits)", fontsize=30)
ax[2].set_title("By Monetary", loc="center", fontsize=50)
ax[2].tick_params(axis='y', labelsize=30)
ax[2].tick_params(axis='x', labelsize=30, rotation=45)
 
st.pyplot(fig)
