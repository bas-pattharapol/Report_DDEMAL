import pandas as pd
import pyodbc

data = pd.read_csv (r'D:\Work\foster\Report_DDEMAL\web\report.csv')   
df = pd.DataFrame(data)

print(df)
server = "172.30.2.2"
port = 5432
database = "OEE_DB"
username = "sa"
password = "p@ssw0rd"
def Phase_Parameter():
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ server +';DATABASE='+database+';UID='+username+';PWD='+password)
    cursor = cnxn.cursor()
    for row in df.itertuples():
        postgres_insert_query = 'INSERT INTO SCADA_DB.dbo.Phase_Parameter (PhaseID, PhaseName,Description ,Parameter1, Parameter2, Parameter3, Parameter4, Parameter5, Parameter6, Parameter7,Parameter8) VALUES (?,?,?,?,?,?,?,?,?,?,?)'
        record_to_insert = (int(row.Phase_ID), str(row.Phase_Name),str(row.Description),str(row.Parameter1),str(row.Parameter2),str(row.Parameter3),str(row.Parameter4),str(row.Parameter5),str(row.Parameter6),str(row.Parameter7),str(row.Parameter8))
        cursor.execute(postgres_insert_query, record_to_insert)
                                         
    cnxn.commit()
    print("OK")
    
def Mixing_Report():
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ server +';DATABASE='+database+';UID='+username+';PWD='+password)
    cursor = cnxn.cursor()
    for row in df.itertuples():
        postgres_insert_query = 'INSERT INTO SCADA_DB.dbo.Mixing_Report (PD_ORDER,PhaseID,  Status, Start_time, End_Time, SetPoint1, Actual1, SetPoint2, Actual2, SetPoint3, Actual3, SetPoint4, Actual4, SetPoint5, Actual5, SetPoint6, Actual6, SetPoint7, Actual7, SetPoint8, Actual8, User_Mixing) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        record_to_insert = (str(row.PD_ORDER),int(row.PHASE_ID), str(row.Status),str(row.StartDT),str(row.EndDT),str(row.SetPoint1),str(row.Actual1),
                            str(row.SetPoint2),str(row.Actual2),str(row.SetPoint3),str(row.Actual3),str(row.SetPoint4),str(row.Actual4),
                            str(row.SetPoint5),str(row.Actual5),str(row.SetPoint6),str(row.Actual6),str(row.SetPoint7),str(row.Actual7),
                            str(row.SetPoint8),str(row.Actual8),str(row.User_Mixing))
        cursor.execute(postgres_insert_query, record_to_insert)
                                         
    cnxn.commit()
    print("OK")
    
if __name__ =="__main__":
    Mixing_Report()