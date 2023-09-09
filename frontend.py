#Files to be imported and used
import getdata_v10
#import createviz_v5

#Python Libraries used
import oracledb as ora
import streamlit as st
import altair as alt
import pandas as pd
from PIL import Image


st.title("Pricing Data Visualizations")
tab1, tab2 = st.tabs(["Forward Pricing", "Settlement(Spot) Pricing"])


fwddates = getdata_v10.getData_DistinctFwdEntDate()
fwdcnames = getdata_v10.getData_DistinctFwdCurveName()
fwdphysfin = getdata_v10.getData_DistinctFwdPhysFin()
sptcnames = getdata_v10.getData_DistinctSpotCurveName()
sptfincurve = getdata_v10.getData_DistinctSpotFinCurve()
stdt, enddt = getdata_v10.getData_SpotStartEndDate()


with tab1:
    with st.container():
        fwdcurvename = st.selectbox("Curve Names: (mandatory)", fwdcnames)
        st.write("Curve Name selected is: ", fwdcurvename)

        fwddate = st.selectbox("Report Date: (mandatory)", fwddates)
        st.write("Report Date Selected is: ", fwddate)    

        fphysfin = st.selectbox("Physical_Financial: (not mandatory)", fwdphysfin)
        st.write("Physical_Financial Curve Name selected is: ", fphysfin)

        if (st.button("Generate Graph", key='gengraph1', use_container_width=False)):
            #st.write("Hello")
            if(fwdcurvename == "All" and fwddate != "None"):
                st.error("Please select a Curve Name", icon="🚨")
            elif(fwdcurvename != "All" and fwddate == "None"):
                st.error("Please select the Date you want the graph to be generated from", icon="🚨")
            elif(fwdcurvename == "All" and fwddate == "None"):
                st.error("Please select the Curve Name and the Date you want the graph to be generated from", icon="🚨")
            elif(fwdcurvename != "All" and fwddate != "None"):
                #st.write("Graph for ", fwdcurvename, "Noice")
                data = getdata_v10.getData_FwdPrice(fwdcurvename, fwddate, fphysfin)
                graph_data = data.filter(['Curve Date', 'Price'])
                print(graph_data)
                if not graph_data.empty:
                    st.toast('Graph will be generated soon', icon="ℹ️")
                    st.line_chart(data=graph_data, x='Curve Date', y='Price', use_container_width=True)
                    st.toast('This is a success message!', icon="✅")
                else:
                    st.error("No data available for the selected Curve name and Date", icon="🚨")
                #st.write("getdata_v10.getData_FwdPrice has been called")
   

with tab2:
    with st.container():
        fincurve = st.selectbox("Settlement(Spot) Financial Curve: (mandatory)", sptfincurve)
        #st.write("Physical_Financial Curve Name selected is: ", physfin)

        startdate = st.date_input("Settlement Price Listing Start Date:", stdt)
        #st.write("Report Date Selected is: ", startdate)

        enddate = st.date_input("Settlement Price Listing End Date:", enddt)
        #st.write("Report Date Selected is: ", enddate)     

        #sptcurvename = st.selectbox("Spot Curve Names:", sptcnames)
        #st.write("Curve Name selected is: ", sptcurvename)

        if (st.button("Generate Graph", key='gengraph2', use_container_width=False)):
            if(fincurve == "--Select--"):
                st.error("Please select a Settlement Financial Curve", icon="🚨")
            else:
                data = getdata_v10.getData_SettPrice(startdate, enddate, fincurve)
                graph_data = data.filter(['Curve Date', 'Price'])
                print(graph_data)
                if not graph_data.empty:
                    st.toast('Graph will be generated soon', icon="ℹ️")
                    st.line_chart(data=graph_data, x='Curve Date', y='Price', use_container_width=True)
                    st.toast('This is a success message!', icon="✅") 
                else:
                    st.error("No data available for the selected Curve Name and Date Range", icon="🚨")
                #st.write("getdata_v10.getData_SettPrice has been called")
