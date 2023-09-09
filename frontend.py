import getdata_v4
import createviz_v4

import oracledb as ora
import streamlit as st
import altair as alt
from PIL import Image


st.title("Data Viz")
# Text
st.text("Hello GeeksForGeeks!!!")
tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
ora.init_oracle_client()
#cs = "localhost:1521/XE"
cs = "117.248.251.123:1521/XE"
configpath = "C:\oraclexe\app\oracle\product\11.2.0\server\network\ADMIN"
data = getdata_v4.getData_SettPrice(cs,configpath)
graph_data = data.filter(['Curve Date', 'Price'])
print(graph_data)
#tab1.dataframe(data)
#tab1.line_chart(graph_data)
#tab2.write(graph_data)


with tab1:
    st.line_chart(data=graph_data, x='Curve Date', y='Price', use_container_width=True)
tab2.write(graph_data)
