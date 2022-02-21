import pandas as pd
import pyodbc

data = pd.read_csv (r'D:\Work\foster\Report_DDEMAL\web\test.csv')   
df = pd.DataFrame(data)

print(df)
server = "172.30.2.2"
port = 5432
database = "OEE_DB"
username = "sa"
password = "p@ssw0rd"
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ server +';DATABASE='+database+';UID='+username+';PWD='+password)
cursor = cnxn.cursor()
for row in df.itertuples():
    postgres_insert_query = 'INSERT INTO SCADA_DB.dbo.Phase_Parameter (PhaseID, PhaseName,Description ,Parameter1, Parameter2, Parameter3, Parameter4, Parameter5, Parameter6, Parameter7,Parameter8) VALUES (?,?,?,?,?,?,?,?,?,?,?)'
    record_to_insert = (int(row.Phase_ID), str(row.Phase_Name),str(row.Description),str(row.Parameter1),str(row.Parameter2),str(row.Parameter3),str(row.Parameter4),str(row.Parameter5),str(row.Parameter6),str(row.Parameter7),str(row.Parameter8))
    cursor.execute(postgres_insert_query, record_to_insert)
                    
                    
cnxn.commit()
print("OK")