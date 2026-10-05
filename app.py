import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Delivery Delay - Anu GK", layout="wide")
st.title("Delivery Delay & Operations Analytics - Anu GK")

@st.cache_data
def load_data():
    return pd.read_csv("DataCo_Sample_10k.csv", encoding='latin1')

df = load_data()
df['Delay_Days'] = df['Days for shipping (real)'] - df['Days for shipment (scheduled)']
df['Is_Late'] = (df['Late_delivery_risk']==1).astype(int)

on_time = (1 - df['Is_Late'].mean())*100

c1,c2,c3 = st.columns(3)
c1.metric("Orders", len(df))
c2.metric("On-Time %", f"{on_time:.1f}%")
c3.metric("Avg Delay", f"{df['Delay_Days'].mean():.1f} days")

st.plotly_chart(px.histogram(df, x="Shipping Mode", color="Delivery Status", barmode="group", title="Delay by Shipping Mode"), use_container_width=True)
st.plotly_chart(px.histogram(df, x="Order Region", color="Is_Late", barmode="group", title="Delay by Region"), use_container_width=True)
st.plotly_chart(px.box(df, x="Is_Late", y="Delay_Days", title="Delay Distribution"), use_container_width=True)

hotspot = df.groupby(['Shipping Mode','Order Region'])['Is_Late'].mean().reset_index()
hotspot['Late%'] = hotspot['Is_Late']*100
hotspot = hotspot.sort_values('Late%', ascending=False).head(10)
st.dataframe(hotspot)
st.success("Same Day shipping = Highest late risk. Africa/LatAm = 60%+ late. Action: Increase SLA to 2 days")
