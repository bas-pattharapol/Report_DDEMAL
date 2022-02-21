import pandas as pd
import pyodbc

data = pd.read_csv (r'D:\Work\foster\Report_DDEMAL\web\Book.csv')   
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
    postgres_insert_query = 'INSERT INTO SCADA_DB.dbo.Phase_Parameter (PhaseID, PhaseName,Description ,Parameter1, Parameter2, Parameter3, Parameter4, Parameter5, Parameter6, Parameter7) VALUES (?,?,?,?,?,?,?,?,?,?)'
    record_to_insert = (row.Phase_ID, row.Phase_Name,row.Description,row.Parameter1,row.Parameter2,row.Parameter3,row.Parameter4,row.Parameter5,row.Parameter6,row.Parameter7)
    cursor.execute(postgres_insert_query, record_to_insert)
                    
                    
cnxn.commit()
print("OK")