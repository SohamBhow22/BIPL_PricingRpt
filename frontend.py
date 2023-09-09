import getdata_v7
import createviz_v5

import oracledb as ora
import streamlit as st
import altair as alt
import pandas as pd
from PIL import Image


st.title("Pricing Data Visualizations")
#st.text("Hello GeeksForGeeks!!!")
tab1, tab2 = st.tabs(["Forward Pricing", "Settlement Pricing"])

ora.init_oracle_client()
cs = "localhost:1521/XE"
#cs = "117.248.251.123:1521/XE"
configpath = "C:\oraclexe\app\oracle\product\11.2.0\server\network\ADMIN"

dates = getdata_v7.getData_DistinctEntDate(cs, configpath)
cnames = getdata_v7.getData_DistinctCurveName(cs, configpath)
physfin = getdata_v7.getData_DistinctPhysFin(cs, configpath)

"""def fetchfwddata(cs, configpath, curvename, date, physfin):
    data = getdata_v7.getData_FwdPrice(cs, configpath, curvename, date, physfin)
    graph_data = data.filter(['Curve Date', 'Price'])
    print(graph_data)"""


with tab1:
    with st.container():
        curvename = st.selectbox("Curve Names: (mandatory)", cnames)
        st.write("Curve Name selected is: ", curvename)

        date = st.selectbox("Report Date: (mandatory)", dates)
        st.write("Report Date Selected is: ", date)    

        physfin = st.selectbox("Physical_Financial: (not mandatory)", physfin)
        st.write("Physical_Financial Curve Name selected is: ", physfin)

        if (st.button("Generate Graph", key='gengraph1', use_container_width=False)):
            #st.write("Hello")
            if(curvename == "All" and date != "None"):
                st.error("Please select a Curve Name", icon="🚨")
            elif(curvename != "All" and date == "None"):
                st.error("Please select the Date you want the graph to be generated from", icon="🚨")
            elif(curvename == "All" and date == "None"):
                st.error("Please select the Curve Name and the Date you want the graph to be generated from", icon="🚨")
            elif(curvename != "All" and date != "None"):
                st.toast('Graph will be generated soon', icon="ℹ️")
                #st.write("Graph for ", curvename, "Noice")
                data = getdata_v7.getData_SettPrice(cs, configpath, curvename, date, physfin)
                graph_data = data.filter(['Curve Date', 'Price'])
                print(graph_data)
                if not graph_data.empty:
                    st.line_chart(data=graph_data, x='Curve Date', y='Price', use_container_width=True)
                else:
                    st.error("No data available for the selected Curve name and Date", icon="🚨")
                #st.write("getdata_v6.getData_FwdPrice has been called")
                st.toast('This is a success message!', icon="✅")            

with tab2:
    with st.container():
        curvename = st.selectbox("Spot Curve Names: (mandatory)", cnames)
        st.write("Curve Name selected is: ", curvename)

        date = st.selectbox("Settlement Report Date: (mandatory)", dates)
        st.write("Report Date Selected is: ", date)    

        physfin = st.selectbox("Settlement Physical_Financial: (not mandatory)", physfin)
        st.write("Physical_Financial Curve Name selected is: ", physfin)

        if (st.button("Generate Graph", key='gengraph2', use_container_width=False)):
            #st.write("Hello")
            if(curvename == "All" and date != "None"):
                st.error("Please select a Curve Name", icon="🚨")
            elif(curvename != "All" and date == "None"):
                st.error("Please select the Date you want the graph to be generated from", icon="🚨")
            elif(curvename == "All" and date == "None"):
                st.error("Please select the Curve Name and the Date you want the graph to be generated from", icon="🚨")
            elif(curvename != "All" and date != "None"):
                st.toast('Graph will be generated soon', icon="ℹ️")
                #st.write("Graph for ", curvename, "Noice")
                data = getdata_v7.getData_FwdPrice(cs, configpath, curvename, date, physfin)
                graph_data = data.filter(['Curve Date', 'Price'])
                print(graph_data)
                if not graph_data.empty:
                    st.line_chart(data=graph_data, x='Curve Date', y='Price', use_container_width=True)
                else:
                    st.error("No data available for the selected Curve name and Date", icon="🚨")
                #st.write("getdata_v6.getData_FwdPrice has been called")
                st.toast('This is a success message!', icon="✅")            

