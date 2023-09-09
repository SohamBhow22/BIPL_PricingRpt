import getdata_v3

import oracledb as ora
import matplotlib.pyplot as mpl_plt
import matplotlib.dates as mpl_dates
import pandas as pd
import datetime as dt

def createviz_fwdprice(data):
    curvedate = pd.to_datetime(data['Curve_Date'], format='%Y%m%d')
    price = data['Price']
    print(curvedate)
    print(price)
    ##print(type(curvedate))
    
    mpl_plt.gca().xaxis.set_major_formatter(mpl_dates.DateFormatter('%d-%m-%Y'))
    #mpl_plt.gca().xaxis.set_major_locator(mpl_dates.DayLocator())
    mpl_plt.gca().xaxis.set_major_locator(mpl_dates.AutoDateLocator())
    mpl_plt.plot_date(curvedate,price)
    mpl_plt.gcf().autofmt_xdate()
    mpl_plt.xlabel("Curve Date") 
    mpl_plt.ylabel("Forward Price (₹)") 
    mpl_plt.title("Forward Pricing Graph for ABC")
    mpl_plt.show()

def createviz_stlprice(data):
    curvedate = pd.to_datetime(data['Curve_Date'], format='%Y%m%d')
    price = data['Price']
    curvename = data['Curve_Name'][0]
    print(curvedate)
    print(price)
    ##print(type(curvedate))
    
    mpl_plt.gca().xaxis.set_major_formatter(mpl_dates.DateFormatter('%d-%m-%Y'))
    #mpl_plt.gca().xaxis.set_major_locator(mpl_dates.DayLocator())
    mpl_plt.gca().xaxis.set_major_locator(mpl_dates.AutoDateLocator())
    mpl_plt.plot_date(curvedate,price)
    mpl_plt.gcf().autofmt_xdate()
    mpl_plt.xlabel("Curve Date")
    ylabel =  curvename
    mpl_plt.ylabel(curvename) 
    mpl_plt.title("Settlement Pricing Graph for ABC")
    mpl_plt.show()


if __name__ == '__main__':
    print()
    ora.init_oracle_client()
    configpath = "C:\oraclexe\app\oracle\product\11.2.0\server\network\ADMIN"
    cs = "Soham-DellG15:1521/XE"
    fwddata = getdata_v3.getData_FwdPrice(cs, configpath) #works
    setldata = getdata_v3.getData_SettPrice(cs, configpath) #works
    #print(fwddata)
    print(setldata)

    createviz_fwdprice(fwddata)
    createviz_stlprice(setldata)

