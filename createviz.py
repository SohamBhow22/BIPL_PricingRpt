import getdata_v5

import oracledb as ora
import plotly.express as px
import pandas as pd

def createviz(pricingname, data):
    curvename = data['Curve Name'][0]
    #print(curvename)
    
    plt = px.line(data, x='Curve Date', y='Price', title = pricingname + " Pricing Graph for " + curvename, markers=True)
    plt.show()

    
if __name__ == '__main__':
    #print()
    ora.init_oracle_client()
    cs = "localhost:1521/XE"
    #cs = "117.248.251.123:1521/XE"
    configpath = "C:\oraclexe\app\oracle\product\11.2.0\server\network\ADMIN"
    fwddata = getdata_v5.getData_FwdPrice(cs, configpath) #works
    #setldata = getdata_v5.getData_SettPrice(cs, configpath) #works
    #print(fwddata)
    #print(setldata)
    #dt = getdata_v5.getData_DistinctEntDate(cs, configpath)
    #print(dt)


    #pricingname = 'Forward'
    pricingname = 'Settlement'
    createviz(pricingname, fwddata)
    #createviz(pricingname, setldata)

