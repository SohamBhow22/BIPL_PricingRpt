import getdata_v3

import oracledb as ora
"""import matplotlib.pyplot as mpl_plt
import matplotlib.dates as mpl_dates"""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def createviz(pricingname, data):
    curvedate = pd.to_datetime(data['Curve Date'], format='%Y%m%d')
    print(curvedate)
    #print(type(curvedate))
    curvename = data['Curve_Name'][0]
    #print(curvename)
    price = data['Price']
    print(price)

    #plt = px.line(data, x='Curve_Date', y='Price', title = pricingname + " Pricing Graph for " + curvename, markers=True).update_layout(xaxis_title="Curve Date", yaxis_title=pricingname + " Price (₹)")
    plt = px.line(data, x='Curve Date', y='Price', title = pricingname + " Pricing Graph for " + curvename, markers=True)
    """plt = go.Figure(data = go.Scatter(x=curvedate, y=price))
    plt.update_xaxes(title_text="Curve Date")
    plt.update_yaxes(title_text=pricingname + " Price (₹)")"""
    
    plt.show()

    
if __name__ == '__main__':
    print()
    ora.init_oracle_client()
    configpath = "C:\oraclexe\app\oracle\product\11.2.0\server\network\ADMIN"
    #cs = "localhost:1521/XE"
    cs = "117.248.251.123:1521/XE"
    fwddata = getdata_v3.getData_FwdPrice(cs, configpath) #works
    setldata = getdata_v3.getData_SettPrice(cs, configpath) #works
    #print(fwddata)
    #print(setldata)
    #pricingname = 'Forward'
    pricingname = 'Settlement'
    #createviz(pricingname, fwddata)
    createviz(pricingname, setldata)

