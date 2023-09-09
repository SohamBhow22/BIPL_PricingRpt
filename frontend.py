import getdata_v4
import createviz_v4

import oracledb as ora
import streamlit as st
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
print(type(data))
#tab1.dataframe(data)
tab1.line_chart(data)
tab2.write(data)

"""with tab1:
    tab1.subheader("A tab with a chart")
    tab1.line_chart(data)

with tab2:
    tab2.subheader("A tab with the data")
    tab2.write(data)    """