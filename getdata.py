import oracledb as ora
from datetime import datetime 
import pandas as pd
## import db_config

def getData_FwdPrice(cs,configpath, curvenm, rptdt, phyfin):
    #ForwardPricing
    con1 = ora.connect(user="FMS8TEST", password="FMS8TEST", dsn=cs, config_dir=configpath)
    cur1 = con1.cursor()

    """print(curvenm)
    print(rptdt)
    print(phyfin)"""

    #curvename = 'ICE_WIM'

    
    query1 = """Select curve_dd_mm_yr, curve_nm, phys_fin, settle_price, ent_dt 
            from FMS9_FORWARD2_PRICE_DTL 
            where ENT_DT <= to_date('08-05-2023','dd/mm/yyyy') 
            and curve_nm = '"""+curvenm+"""' 
            order by curve_dd_mm_yr asc"""
    #query1 = "Select Distinct curve_nm from FMS9_FORWARD2_PRICE_DTL where ENT_DT = to_date('08-05-2023','dd/mm/yyyy')"

    data = pd.DataFrame(cur1.execute(query1).fetchall())
    #print(data)
    data.rename(columns = {0:'Curve Date', 1:'Curve Name', 2:'Phys_Fin', 
                        3:'Price', 4:'Ent_Date'}, inplace=True)
    print(data)
        
    cur1.close()
    con1.close()

    return data

def getData_SettPrice(cs,configpath) :
    #SettlementPricing
    #con2 = ora.connect(user="FMS8TEST", password="FMS8TEST", dsn=cs, config_dir=configpath)
    con2 = ora.connect(user="fms8", password="fms8", dsn=cs, config_dir=configpath)
    cur2 = con2.cursor()

    curvename = 'PLATTS_JKM'
    query2 = "Select curve_dd_mm_yr, curve_nm, phys_fin, settle_price from FMS9_CURVE2_PRICE_DTL where ENT_DT >= to_date('01-01-2021','dd/mm/yyyy') and CURVE_NM = '"+ curvename + "' order by curve_dd_mm_yr asc"

    data = pd.DataFrame(cur2.execute(query2).fetchall())
    #print(data)
    data.rename(columns = {0:'Curve Date', 1:'Curve Name', 2:'Phys_Fin', 
                        3:'Price'}, inplace=True)
    print(data)
        
    cur2.close()
    con2.close()
    
    return data

def getData_DistinctEntDate(cs, configpath):
    #Distinct ENT_DT from Database
    con3 = ora.connect(user="FMS8TEST", password="FMS8TEST", dsn=cs, config_dir=configpath)
    cur3 = con3.cursor()

    print("Currently within getData_DistinctEntDate function in getdata_v5.py file")

    currdatetime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    print(currdatetime)
    
    query3 = "SELECT DISTINCT ENT_DT FROM FMS9_FORWARD2_PRICE_DTL WHERE ENT_DT <= to_date('08-05-2023','dd/mm/yyyy') ORDER BY ENT_DT desc"
    entdt = pd.DataFrame(cur3.execute(query3).fetchall())
    
    #Adding "None" to the list of Report Dates
    entdt.loc[-1] = ["None"]
    entdt.index = entdt.index + 1  # shifting index
    entdt = entdt.sort_index()  
    print(entdt)

    print("Exiting getData_DistinctEntDate function in getdata_v5.py file")

    return entdt

def getData_DistinctCurveName(cs, configpath):
    #Distinct Curve Name from Database
    con4 = ora.connect(user="FMS8TEST", password="FMS8TEST", dsn=cs, config_dir=configpath)
    cur4 = con4.cursor()

    print("Currently within getData_DistinctCurveName function in getdata_v5.py file") 

    query4 = "SELECT DISTINCT CURVE_NM FROM FMS9_FORWARD2_PRICE_DTL WHERE ENT_DT <= to_date('08-05-2023','dd/mm/yyyy') ORDER BY CURVE_NM asc"
    curvenames = pd.DataFrame(cur4.execute(query4).fetchall()) 
    
    #Adding "All" to the list of Report Dates
    curvenames.loc[-1] = ["All"]
    curvenames.index = curvenames.index + 1  #shifting indexes back to normal #this line can be commented out but we are doing to ensure the index begins from 0 again 
    curvenames = curvenames.sort_index()
    print(curvenames)

    print("Exiting getData_DistinctCurveName function in getdata_v5.py file")

    return curvenames

def getData_DistinctPhysFin(cs, configpath):
    #Distinct Phys_Fin from Database
    con5 = ora.connect(user="FMS8TEST", password="FMS8TEST", dsn=cs, config_dir=configpath)
    cur5 = con5.cursor()

    print("Currently within getData_DistinctPhysFin function in getdata_v5.py file") 

    query5 = "SELECT DISTINCT PHYS_FIN FROM FMS9_FORWARD2_PRICE_DTL WHERE ENT_DT <= to_date('08-05-2023','dd/mm/yyyy') ORDER BY PHYS_FIN asc"
    physfin = pd.DataFrame(cur5.execute(query5).fetchall()) 
    
    #Adding "All" to the list of Report Dates
    physfin.loc[-1] = ["All"]
    physfin.index = physfin.index + 1  #shifting indexes back to normal #this line can be commented out but we are doing to ensure the index begins from 0 again 
    physfin = physfin.sort_index()
    print(physfin)

    print("Exiting getData_DistinctPhysFin function in getdata_v5.py file")

    return physfin


if __name__ == '__main__':
    print("getdata_v6.py script has been called")
    ora.init_oracle_client()
    configpath = "C:\oraclexe\app\oracle\product\11.2.0\server\network\ADMIN"
    cs = "Soham-DellG15:1521/XE"
    #cs = "117.248.251.123:1521/XE"
    fwddata = getData_FwdPrice(cs, configpath, "ICE_WIM", "None", "All")
    #stldata = getData_SettPrice(cs, configpath)
    print(fwddata)
    #print(stldata)
    #getData_DistinctEntDate(cs, configpath)
    print("getdata_v6.py script is running fine")