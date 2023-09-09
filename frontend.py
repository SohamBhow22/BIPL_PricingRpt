import getdata_v6
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

"""data = getdata_v6.getData_FwdPrice(cs,configpath)
graph_data = data.filter(['Curve Date', 'Price'])
print(graph_data)"""

dates = getdata_v6.getData_DistinctEntDate(cs, configpath)
cnames = getdata_v6.getData_DistinctCurveName(cs, configpath)
physfin = getdata_v6.getData_DistinctPhysFin(cs, configpath)


with tab1:
    with st.container():
        curvename = st.selectbox("Curve Names: (mandatory)", cnames)
        st.write("Curve Name selected is: ", curvename)

        date = st.selectbox("Report Date: (mandatory)", dates)
        st.write("Report Date Selected is: ", date)    

        physfin = st.selectbox("Physical_Financial: (not mandatory)", physfin)
        st.write("Physical_Financial Curve Name selected is: ", physfin)

        if (st.button("Generate Graph", key = "gengraph", use_container_width=False)):
            st.write("Hello")
            if(curvename == "All" and date != "None"):
                st.error("Please select a Curve Name", icon="🚨")
            elif(curvename != "All" and date == "None"):
                st.error("Please select the Date you want the graph to be generated from", icon="🚨")
            elif(curvename == "All" and date == "None"):
                st.error("Please select the Curve Name and the Date you want the graph to be generated from", icon="🚨")
            elif(curvename != "All" and date != "None"):
                st.toast('Graph will be generated soon', icon="ℹ️")
                #st.write("Graph for ", curvename, "Noice")
                data = getdata_v6.getData_FwdPrice(cs, configpath, curvename, date, physfin)
                graph_data = data.filter(['Curve Date', 'Price'])
                print(graph_data)
                st.line_chart(data=graph_data, x='Curve Date', y='Price', use_container_width=True)
                st.write("getdata_v6.getData_FwdPrice has been called")
                st.toast('This is a success message!', icon="✅")            

        

    
#tab2.write(graph_data)
