import oracledb as ora
from datetime import datetime, date
import pandas as pd


def getOraDBConnection():
    ora.init_oracle_client()
    configpath = "C:\oraclexe\app\oracle\product\11.2.0\server\network\ADMIN"
    #cs = "localhost:1521/XE"
    #cs = "117.248.251.123:1521/XE"
    cs = "Soham-DellG15:1521/XE"
    conn = ora.connect(user = "FMS8TEST", password="FMS8TEST", dsn = cs, config_dir=configpath)
    print("Got the DB Connection")

    return conn

def getData_FwdPrice(curvenm, entdt, physfin):
    #ForwardPricing
    print("Currently within getData_FwdPrice function in getdata_v7.py file")
    con1 = getOraDBConnection()
    #con1 = ora.connect(user="FMS8TEST", password="FMS8TEST", dsn=cs, config_dir=configpath)
    cur1 = con1.cursor()

    if physfin == "All":
        query1 = """Select CURVE_DD_MM_YR, CURVE_NM, PHYS_FIN, SETTLE_PRICE, ENT_DT 
                from FMS9_FORWARD2_PRICE_DTL 
                where ENT_DT = to_date('""" +entdt+ """','dd/mm/yyyy') 
                and CURVE_NM like '"""+curvenm+"""' 
                order by CURVE_NM, ENT_DT, CURVE_DD_MM_YR ASC"""
    else:
        query1 = """Select CURVE_DD_MM_YR, CURVE_NM, PHYS_FIN, SETTLE_PRICE, ENT_DT 
                from FMS9_FORWARD2_PRICE_DTL 
                where ENT_DT = to_date('""" +entdt+ """','dd/mm/yyyy') 
                and CURVE_NM like '"""+curvenm+"""'
                and PHYS_FIN like '"""+physfin+"""'
                order by CURVE_NM, ENT_DT, CURVE_DD_MM_YR ASC"""   
    #query1 = "Select Distinct curve_nm from FMS9_FORWARD2_PRICE_DTL where ENT_DT = to_date('08-05-2023','dd/mm/yyyy')"

    data = pd.DataFrame(cur1.execute(query1).fetchall())
    #print(data)
    data.rename(columns = {0:'Curve Date', 1:'Curve Name', 2:'Phys_Fin', 
                        3:'Price', 4:'Ent_Date'}, inplace=True)
    print(data)
        
    cur1.close()
    con1.close()

    print("Exiting getData_FwdPrice function in getdata_v7.py file")

    return data

def getData_SettPrice(curvename, startdt, enddt, physfin) :
    #SettlementPricing
    print("Currently within getData_SettPrice function in getdata_v8.py file")
    con2 = getOraDBConnection()
    #con2 = ora.connect(user="FMS8TEST", password="FMS8TEST", dsn=cs, config_dir=configpath)
    #con2 = ora.connect(user="fms8", password="fms8", dsn=cs, config_dir=configpath)
    cur2 = con2.cursor()

    #curvename = 'PLATTS_JKM'
    print(physfin)
    if physfin == "All":
        query2 = """Select CURVE_DD_MM_YR, CURVE_NM, PHYS_FIN, SETTLE_PRICE 
                from FMS9_CURVE2_PRICE_DTL 
                where ENT_DT >= to_date('""" +startdt.strftime("%d/%m/%Y")+ """','dd/mm/yyyy')
                and ENT_DT <= to_date('""" +enddt.strftime("%d/%m/%Y")+ """','dd/mm/yyyy') 
                and CURVE_NM like '"""+ curvename + """'
                order by ENT_DT, CURVE_DD_MM_YR desc, CURVE_NM"""
    else:    
        query2 = """Select CURVE_DD_MM_YR, CURVE_NM, PHYS_FIN, SETTLE_PRICE 
                from FMS9_CURVE2_PRICE_DTL 
                where ENT_DT >= to_date('""" +startdt.strftime("%d/%m/%Y")+ """','dd/mm/yyyy')
                and ENT_DT <= to_date('""" +enddt.strftime("%d/%m/%Y")+ """','dd/mm/yyyy') 
                and CURVE_NM like '"""+ curvename + """'
                and PHYS_FIN like '"""+ physfin + """' 
                order by ENT_DT, CURVE_DD_MM_YR desc, CURVE_NM"""

    #print(query2)
    data = pd.DataFrame(cur2.execute(query2).fetchall())
    #print(data)
    data.rename(columns = {0:'Curve Date', 1:'Curve Name', 2:'Phys_Fin', 
                        3:'Price'}, inplace=True)
    print(data)
        
    cur2.close()
    con2.close()
    print("Exiting getData_SettPrice function in getdata_v8.py file")
    
    return data

def getData_DistinctFwdEntDate():
    #Distinct ENT_DT from Database
    con3 = getOraDBConnection()
    #con3 = ora.connect(user="FMS8TEST", password="FMS8TEST", dsn=cs, config_dir=configpath)
    cur3 = con3.cursor()

    print("Currently within getData_DistinctFwdEntDate function in getdata_v8.py file")

    currdatetime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    print(currdatetime)
    
    query3 = """SELECT DISTINCT TO_CHAR((ENT_DT),'DD/MM/YYYY') 
                FROM FMS9_FORWARD2_PRICE_DTL
                WHERE ENT_DT <= SYSDATE
                ORDER BY TO_DATE(TO_CHAR((ENT_DT),'DD/MM/YYYY'),'DD/MM/YYYY') DESC"""
    entdt = pd.DataFrame(cur3.execute(query3).fetchall())
    
    print(entdt)

    cur3.close()
    con3.close()

    print("Exiting getData_DistinctFwdEntDate function in getdata_v8.py file")

    return entdt

def getData_DistinctFwdCurveName():
    #Distinct Forward Curve Name from Database
    con4 = getOraDBConnection()
    #con4 = ora.connect(user="FMS8TEST", password="FMS8TEST", dsn=cs, config_dir=configpath)
    cur4 = con4.cursor()

    print("Currently within getData_DistinctFwdCurveName function in getdata_v8.py file") 

    query4 = """SELECT DISTINCT CURVE_NM 
                FROM FMS9_FORWARD2_PRICE_DTL 
                WHERE ENT_DT <= SYSDATE 
                ORDER BY CURVE_NM asc"""
    fwdcurvenames = pd.DataFrame(cur4.execute(query4).fetchall()) 
    
    #Adding "All" to the list of Report Dates
    fwdcurvenames.loc[-1] = ["All"]
    fwdcurvenames.index = fwdcurvenames.index + 1  #shifting indexes back to normal #this line can be commented out but we are doing to ensure the index begins from 0 again 
    fwdcurvenames = fwdcurvenames.sort_index()
    print(fwdcurvenames)

    cur4.close()
    con4.close()

    print("Exiting getData_DistinctFwdCurveName function in getdata_v8.py file")

    return fwdcurvenames

def getData_DistinctFwdPhysFin():
    #Distinct Phys_Fin from Database
    con5 = getOraDBConnection()
    #con5 = ora.connect(user="FMS8TEST", password="FMS8TEST", dsn=cs, config_dir=configpath)
    cur5 = con5.cursor()

    print("Currently within getData_DistinctFwdPhysFin function in getdata_v8.py file") 

    query5 = """SELECT DISTINCT PHYS_FIN 
                FROM FMS9_FORWARD2_PRICE_DTL 
                WHERE ENT_DT <= SYSDATE
                ORDER BY PHYS_FIN asc"""
    physfin = pd.DataFrame(cur5.execute(query5).fetchall()) 
    
    #Adding "All" to the list of Report Dates
    physfin.loc[-1] = ["All"]
    physfin.index = physfin.index + 1  #shifting indexes back to normal #this line can be commented out but we are doing to ensure the index begins from 0 again 
    physfin = physfin.sort_index()
    print(physfin)

    cur5.close()
    con5.close()

    print("Exiting getData_DistinctFwdPhysFin function in getdata_v8.py file")

    return physfin

def getData_DistinctSpotCurveName():
    #Distinct Spot Curve Name from Database
    con6 = getOraDBConnection()
    #con6 = ora.connect(user="FMS8TEST", password="FMS8TEST", dsn=cs, config_dir=configpath)
    cur6 = con6.cursor()

    print("Currently within getData_DistinctSpotCurveName function in getdata_v8.py file") 

    query6 = """SELECT DISTINCT CURVE_NM
                FROM FMS9_CURVE2_PRICE_DTL
                ORDER BY CURVE_NM ASC"""
    spotcurvenames = pd.DataFrame(cur6.execute(query6).fetchall()) 
    
    #Adding "All" to the list of Report Dates
    spotcurvenames.loc[-1] = ["All"]
    spotcurvenames.index = spotcurvenames.index + 1  #shifting indexes back to normal #this line can be commented out but we are doing to ensure the index begins from 0 again 
    spotcurvenames = spotcurvenames.sort_index()
    print(spotcurvenames)

    cur6.close()
    con6.close()

    print("Exiting getData_DistinctSpotCurveName function in getdata_v8.py file")

    return spotcurvenames

def getData_DistinctSpotFinCurve():
    #Distinct Financial Curve Name from Database
    con7 = getOraDBConnection()
    #con5 = ora.connect(user="FMS8TEST", password="FMS8TEST", dsn=cs, config_dir=configpath)
    cur7 = con7.cursor()

    print("Currently within getData_DistinctSpotFinCurve function in getdata_v8.py file") 

    query7 = """SELECT DISTINCT PHYS_FIN 
                FROM FMS9_CURVE2_PRICE_DTL 
                WHERE ENT_DT <= SYSDATE
                AND PHYS_FIN !='Financial'
                ORDER BY PHYS_FIN asc"""
    physfin = pd.DataFrame(cur7.execute(query7).fetchall()) 
    
    #Adding "All" to the list of Report Dates
    physfin.loc[-1] = ["All"]
    physfin.index = physfin.index + 1  #shifting indexes back to normal #this line can be commented out but we are doing to ensure the index begins from 0 again 
    physfin = physfin.sort_index()
    print(physfin)

    cur7.close()
    con7.close()

    print("Exiting getData_DistinctSpotFinCurve function in getdata_v8.py file")

    return physfin

def getData_SpotStartEndDate():
    #Default Start Date will be 1st of current month and End Date will be today's date
    #We are asking the user to select the date range for which they need the Spot data
    print("Currently within getData_SpotStartEndDate function in getdata_v8.py file") 
    startdate =  date(datetime.now().year, datetime.now().month, 1)
    #startdate =  date(2023, 8, 1)
    print(startdate)
    today = date.today()
    print(today) 

    print("Exiting getData_SpotStartEndDate function in getdata_v8.py file")

    return startdate, today


if __name__ == '__main__':
    print("getdata_v8.py script has been called")
    ora.init_oracle_client()
    configpath = "C:\oraclexe\app\oracle\product\11.2.0\server\network\ADMIN"
    cs = "Soham-DellG15:1521/XE"
    #cs = "117.248.251.123:1521/XE"
    #fwddata = getData_FwdPrice(cs, configpath, "ICE_WIM", "None", "All")
    #stldata = getData_SettPrice(cs, configpath)
    sptcname = getData_DistinctSpotCurveName(cs, configpath)
    #print(fwddata)
    #print(stldata)
    print(sptcname)
    #getData_DistinctEntDate(cs, configpath)
    print("getdata_v8.py script is running fine")