import getdata_v5
import createviz_v5

import oracledb as ora
import streamlit as st
import altair as alt
import pandas as pd
from PIL import Image


st.title("Data Viz")
st.text("Hello GeeksForGeeks!!!")
tab1, tab2 = st.tabs(["Forward Pricing", "🗃 Data"])

ora.init_oracle_client()
cs = "localhost:1521/XE"
#cs = "117.248.251.123:1521/XE"
configpath = "C:\oraclexe\app\oracle\product\11.2.0\server\network\ADMIN"

data = getdata_v5.getData_FwdPrice(cs,configpath)
graph_data = data.filter(['Curve Date', 'Price'])
print(graph_data)

#tab1.dataframe(data)
#tab1.line_chart(graph_data)
#tab2.write(graph_data)
dates = getdata_v5.getData_DistinctEntDate(cs, configpath)
cnames = getdata_v5.getData_DistinctCurveName(cs, configpath)
physfin = getdata_v5.getData_DistinctPhysFin(cs, configpath)


with tab1:
    with st.container():
        date = st.selectbox("Report Date: ", dates)
        # print the selected date
        st.write("Report Date Selected is: ", date)

        curvenames = st.selectbox("Curve Names: ", cnames)
        st.write("Curve Name selected is: ", curvenames)

        physfin = st.selectbox("Physical_Financial: ", physfin)
        st.write("Physical_Financial Curve Name selected is: ", physfin)

        if (st.button("Generate Graph", key = "gengraph", use_container_width=False)):
            st.write("Hello")

        st.write("Graph for ",curvenames,"Noice")

    st.line_chart(data=graph_data, x='Curve Date', y='Price', use_container_width=True)
tab2.write(graph_data)
