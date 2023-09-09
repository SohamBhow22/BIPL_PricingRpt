import oracledb
import datetime
import pandas as pd
## import db_config


def getData_FwdPrice(cs,configpath):
    #ForwardPricing
    con1 = oracledb.connect(user="FMS8TEST", password="FMS8TEST", dsn=cs, config_dir=configpath)
    cur1 = con1.cursor()

    curvename = 'ICE_WIM'
    query1 = "Select * from FMS9_FORWARD2_PRICE_DTL where ENT_DT = to_date('08-05-2023','dd/mm/yyyy') and CURVE_NM = '"+ curvename + "' order by curve_dd_mm_yr asc"
    #query = "Select Distinct curve_nm from FMS9_FORWARD2_PRICE_DTL where ENT_DT = to_date('08-05-2023','dd/mm/yyyy')"

    data = pd.DataFrame(cur1.execute(query1).fetchall())
    data.rename(columns = {0:'Curve_Date', 1:'Curve_Name', 2:'Commodity_Type', 
                        3:'Curve_Type', 4:'Curve_Unit', 5:'Phys_Fin', 
                        6:'Price', 7:'Ent_by', 8:'Ent_Date', 
                        9:'Aprv_by', 10:'Aprv_Date', 11: 'Flag'}, inplace=True)
    #print(data)
    graph_data = data.filter(['Curve_Date', 'Curve_Name', 'Price'])
    print(graph_data)

    cur1.close()
    con1.close()


def getData_SettPrice(cs,configpath) :
    #SettlementPricing
    con2 = oracledb.connect(user="FMS8TEST", password="FMS8TEST", dsn=cs, config_dir=configpath)
    cur2 = con2.cursor()

    curvename = 'DES_WES_INDIA_0_HALFMONTH'
    query2 = "Select * from FMS9_CURVE2_PRICE_DTL where  ENT_DT >= to_date('01-01-2021','dd/mm/yyyy') and CURVE_NM = '"+ curvename + "' order by curve_dd_mm_yr asc"

    data = pd.DataFrame(cur2.execute(query2).fetchall())
    data.rename(columns = {0:'Curve_Date', 1:'Curve_Name', 2:'Commodity_Type', 
                        3:'Curve_Type', 4:'Curve_Unit', 5:'Phys_Fin', 
                        6:'Price', 7:'Ent_by', 8:'Ent_Date', 
                        9:'Aprv_by', 10:'Aprv_Date', 11: 'Flag'}, inplace=True)
    #print(data)

    graph_data = data.filter(['Curve_Date', 'Curve_Name', 'Price'])
    print(graph_data)

    cur2.close()
    con2.close()


if __name__ == '__main__':
    oracledb.init_oracle_client()
    configpath = "C:\oraclexe\app\oracle\product\11.2.0\server\network\ADMIN"
    cs = "Soham-DellG15:1521/XE"
    getData_FwdPrice(cs, configpath)
    getData_SettPrice(cs, configpath)