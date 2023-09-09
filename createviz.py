import getdata_v3

import oracledb as ora
import matplotlib.pyplot as mpl_plt
import matplotlib.dates as mpl_dates
import pandas as pd

def createviz(pricingname, data):
    curvedate = pd.to_datetime(data['Curve_Date'], format='%Y%m%d')
    print(curvedate)
    #print(type(curvedate))
    curvename = data['Curve_Name'][0]
    #print(curvename)
    price = data['Price']
    print(price)
        
    mpl_plt.gca().xaxis.set_major_formatter(mpl_dates.DateFormatter('%d-%m-%Y'))
    #mpl_plt.gca().xaxis.set_major_locator(mpl_dates.DayLocator())
    mpl_plt.gca().xaxis.set_major_locator(mpl_dates.AutoDateLocator())
    mpl_plt.plot_date(curvedate,price)
    mpl_plt.gcf().autofmt_xdate()
    mpl_plt.xlabel("Curve Date") 
    mpl_plt.ylabel(pricingname + " Price (₹)") 
    mpl_plt.title(pricingname + " Pricing Graph for " + curvename)
    mpl_plt.show()


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

