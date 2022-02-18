from flask import Flask, render_template, request, redirect, url_for, jsonify,make_response,session
from flask.sessions import NullSession
from flask_socketio import SocketIO
from flask_login.utils import logout_user
import pandas as pd
import pyodbc
import pprint
import pdfkit
import json
from datetime import datetime, timedelta
import decimal

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal): return float(obj)


app = Flask(__name__)

count = 3
@app.route('/')
@app.route('/batch_report')
def batch_report():
    #cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ host +';DATABASE='+database+';UID='+user+';PWD='+passwd)
    #SQL_Login = cnxn.cursor()
    #SQL_Login.execute("Exec USP_Journal_Rpt '" + Campaign_ID + "','"+ Lot_ID +"','"+ StartOfPeriod_DT + "','"+EndOfPeriod_DT+"'" )
    return render_template('batch_report.html')

@app.route('/Raw_Material/Raw_Material/<string:data>')
def Raw_Material(data):
    return render_template('RawMaterial.html',data=data)

@app.route('/Raw_Material_API/Raw_Material_API/<string:data>')
def Raw_Material_API(data):
    host = "172.30.1.1"
    port = 1433
    database = "managedb"
    user = "sa"
    passwd = "qwerty@2019"
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ host +';DATABASE='+database+';UID='+user+';PWD='+passwd)
    RM = cnxn.cursor()
    RM.execute("SELECT * FROM [dbo].[View_RM_Process_tab] where RM_PD_ORDER = '" + data + "'")
    
    payload = []
    content = {}
    for result in RM:
        
        content = {'RM_RAW_ID': result[1], 'RM_NAME': str(result[2]), 'RM_UNIT': result[3],'PW_NEO_NAME': result[4],'RM_PW_TARGET': result[5],'RM_PW_ACTUAL': str(result[6]),'RM_REQ_DATE': str(result[7]),'RM_INS_DT': str(result[8]),'PW_ITEM_TOTAL': str(result[9]),'RM_PW_EACH_ITEM': str(result[10]),'RM_BARCODE_LIST': str(result[11]),'RM_FFTANK_STATUS': str(result[12]),'RM_FFTANK_1': str(result[13]),'RM_SFTANK_1': str(result[14]),'RM_REF_NO': str(result[15]),'UserDisplayName': str(result[16])}
        payload.append(content)
        content = {}
    #print(payload)
    return json.dumps({"data":payload}, cls = Encoder), 201


    
    
@app.route('/<string:mode>/<string:data>')
def modeReport(mode,data):
    #print(data)
    
    host = "172.30.1.203"
    port = 1433
    database = "BatchHistory"
    user = "sa"
    passwd = "p@ssw0rd"
    Campaign_ID="*"
    Lot_ID="*"
    StartOfPeriod_DT="2/1/2020 12:00:00"
    now  = datetime.now()
    EndOfPeriod_DT= now.strftime("%m/%d/%Y %H:%M:%S")
    print(EndOfPeriod_DT)
    if mode == 'Pre_Mixing_1':
        
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ host +';DATABASE='+database+';UID='+user+';PWD='+passwd)
        USP_Journal_Rpt = cnxn.cursor()
        USP_Journal_Rpt.execute("Exec USP_PM1 '" + Campaign_ID + "','"+ Lot_ID +"','"  + data + "','"+ StartOfPeriod_DT+ "','" + EndOfPeriod_DT+ "'"  )
        
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ host +';DATABASE='+database+';UID='+user+';PWD='+passwd)
        USP_Journal_Rpt1 = cnxn.cursor()
        USP_Journal_Rpt1.execute("Exec USP_PM1 '" + Campaign_ID + "','"+ Lot_ID +"','"  + data + "','"+ StartOfPeriod_DT+ "','" + EndOfPeriod_DT+ "'"  )
        
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ host +';DATABASE='+database+';UID='+user+';PWD='+passwd)
        USP_Journal_Rpt_h = cnxn.cursor()
        USP_Journal_Rpt_h.execute("Exec USP_PM1 '" + Campaign_ID + "','"+ Lot_ID +"','"  + data + "','"+ StartOfPeriod_DT+ "','" + EndOfPeriod_DT+ "'"  )
    
    elif mode == 'Pre_Mixing_2':
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ host +';DATABASE='+database+';UID='+user+';PWD='+passwd)
        USP_Journal_Rpt = cnxn.cursor()
        USP_Journal_Rpt.execute("Exec USP_PM2 '" + Campaign_ID + "','"+ Lot_ID +"','"  + data + "','"+ StartOfPeriod_DT+ "','" + EndOfPeriod_DT+ "'"  )
        
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ host +';DATABASE='+database+';UID='+user+';PWD='+passwd)
        USP_Journal_Rpt1 = cnxn.cursor()
        USP_Journal_Rpt1.execute("Exec USP_PM2 '" + Campaign_ID + "','"+ Lot_ID +"','"  + data + "','"+ StartOfPeriod_DT+ "','" + EndOfPeriod_DT+ "'"  )
        
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ host +';DATABASE='+database+';UID='+user+';PWD='+passwd)
        USP_Journal_Rpt_h = cnxn.cursor()
        USP_Journal_Rpt_h.execute("Exec USP_PM2 '" + Campaign_ID + "','"+ Lot_ID +"','"  + data + "','"+ StartOfPeriod_DT+ "','" + EndOfPeriod_DT+ "'"  )
    
    elif mode == 'Main_Mixing':
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ host +';DATABASE='+database+';UID='+user+';PWD='+passwd)
        USP_Journal_Rpt = cnxn.cursor()
        USP_Journal_Rpt.execute("Exec USP_MM '" + Campaign_ID + "','"+ Lot_ID +"','"  + data + "','"+ StartOfPeriod_DT+ "','" + EndOfPeriod_DT+ "'"  )
        
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ host +';DATABASE='+database+';UID='+user+';PWD='+passwd)
        USP_Journal_Rpt1 = cnxn.cursor()
        USP_Journal_Rpt1.execute("Exec USP_MM '" + Campaign_ID + "','"+ Lot_ID +"','"  + data + "','"+ StartOfPeriod_DT+ "','" + EndOfPeriod_DT+ "'"  )
        
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ host +';DATABASE='+database+';UID='+user+';PWD='+passwd)
        USP_Journal_Rpt_h = cnxn.cursor()
        USP_Journal_Rpt_h.execute("Exec USP_MM '" + Campaign_ID + "','"+ Lot_ID +"','"  + data + "','"+ StartOfPeriod_DT+ "','" + EndOfPeriod_DT+ "'"  )
    
    elif mode == 'Mixing_Storage':
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ host +';DATABASE='+database+';UID='+user+';PWD='+passwd)
        USP_Journal_Rpt = cnxn.cursor()
        USP_Journal_Rpt.execute("Exec USP_ST '" + Campaign_ID + "','"+ Lot_ID +"','"  + data + "','"+ StartOfPeriod_DT+ "','" + EndOfPeriod_DT+ "'"  )
        
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ host +';DATABASE='+database+';UID='+user+';PWD='+passwd)
        USP_Journal_Rpt1 = cnxn.cursor()
        USP_Journal_Rpt1.execute("Exec USP_ST '" + Campaign_ID + "','"+ Lot_ID +"','"  + data + "','"+ StartOfPeriod_DT+ "','" + EndOfPeriod_DT+ "'"  )
        
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ host +';DATABASE='+database+';UID='+user+';PWD='+passwd)
        USP_Journal_Rpt_h = cnxn.cursor()
        USP_Journal_Rpt_h.execute("Exec USP_ST '" + Campaign_ID + "','"+ Lot_ID +"','"  + data + "','"+ StartOfPeriod_DT+ "','" + EndOfPeriod_DT+ "'"  )
    
    elif mode == 'SidePOT_1':
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ host +';DATABASE='+database+';UID='+user+';PWD='+passwd)
        USP_Journal_Rpt = cnxn.cursor()
        USP_Journal_Rpt.execute("Exec USP_SP1 '" + Campaign_ID + "','"+ Lot_ID +"','"  + data + "','"+ StartOfPeriod_DT+ "','" + EndOfPeriod_DT+ "'"  )
        
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ host +';DATABASE='+database+';UID='+user+';PWD='+passwd)
        USP_Journal_Rpt1 = cnxn.cursor()
        USP_Journal_Rpt1.execute("Exec USP_SP1 '" + Campaign_ID + "','"+ Lot_ID +"','"  + data + "','"+ StartOfPeriod_DT+ "','" + EndOfPeriod_DT+ "'"  )
        
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ host +';DATABASE='+database+';UID='+user+';PWD='+passwd)
        USP_Journal_Rpt_h = cnxn.cursor()
        USP_Journal_Rpt_h.execute("Exec USP_SP1 '" + Campaign_ID + "','"+ Lot_ID +"','"  + data + "','"+ StartOfPeriod_DT+ "','" + EndOfPeriod_DT+ "'"  )
    
    elif mode == 'SidePOT_2':
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ host +';DATABASE='+database+';UID='+user+';PWD='+passwd)
        USP_Journal_Rpt = cnxn.cursor()
        USP_Journal_Rpt.execute("Exec USP_SP2 '" + Campaign_ID + "','"+ Lot_ID +"','"  + data + "','"+ StartOfPeriod_DT+ "','" + EndOfPeriod_DT+ "'"  )
        
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ host +';DATABASE='+database+';UID='+user+';PWD='+passwd)
        USP_Journal_Rpt1 = cnxn.cursor()
        USP_Journal_Rpt1.execute("Exec USP_SP2 '" + Campaign_ID + "','"+ Lot_ID +"','"  + data + "','"+ StartOfPeriod_DT+ "','" + EndOfPeriod_DT+ "'"  )
        
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ host +';DATABASE='+database+';UID='+user+';PWD='+passwd)
        USP_Journal_Rpt_h = cnxn.cursor()
        USP_Journal_Rpt_h.execute("Exec USP_SP2 '" + Campaign_ID + "','"+ Lot_ID +"','"  + data + "','"+ StartOfPeriod_DT+ "','" + EndOfPeriod_DT+ "'"  )
    
        
    Campaign_ID = ''
    Lot_ID = ''
    Batch_ID = ''
    Recipe_ID= ''
    Recipe_Version= ''
    recipe_Name= ''
    ApprovalCode= ''
    Batch_Size= ''
    Train_ID= ''
    Log_Close_DT= ''
    
    for u in USP_Journal_Rpt_h:
        Campaign_ID = u[1]
        Lot_ID = u[2]
        Batch_ID = u[3]
        Recipe_ID= u[4]
        Recipe_Version= u[6]
        recipe_Name= u[5]
        ApprovalCode= u[11]
        Batch_Size= u[9]
        Train_ID= u[8]
        Log_Close_DT= u[10]

    section = []
    listans = [15,12,13,14]
    for i in USP_Journal_Rpt :
        p51 = []
        for j in listans:
            p51.append(i[j])
            
        section.append(p51)
       
        
    print(section)
        
    
    Batch_Log_ID = []
    Phase_Instance_ID = []
    
    listPhase = [2,7,9,8,10]
    listrow = []
    row = 0
    details = []
    
   
    for i in USP_Journal_Rpt1:
        Batch_Log_ID.append(i[0])
        Phase_Instance_ID.append(i[16])
        
    list3d = len(Batch_Log_ID)
    MaterialAll = []
   
    listMaterial = [8,10,16,15]

    for i,j in zip(Batch_Log_ID ,Phase_Instance_ID):
        row = 0
        d1 = []
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ host +';DATABASE='+database+';UID='+user+';PWD='+passwd)
        USP_PhaseExecutionEvents_Rpt1 = cnxn.cursor()
        USP_PhaseExecutionEvents_Rpt1.execute("Exec USP_ProcessVar_Rpt '"+ i + "','" + j + "'")
        
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ host +';DATABASE='+database+';UID='+user+';PWD='+passwd)
        USP_PhaseExecutionEvents_Rpt = cnxn.cursor()
        USP_PhaseExecutionEvents_Rpt.execute("Exec USP_ProcessVar_Rpt '"+ i + "','" + j + "'")
        
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ host +';DATABASE='+database+';UID='+user+';PWD='+passwd)
        USP_MaterialInput_Rpt = cnxn.cursor()
        USP_MaterialInput_Rpt.execute("Exec USP_MaterialInput_Rpt '"+ i + "','" + j + "'")
        Material =  []
        for q in USP_MaterialInput_Rpt : 
            for w in listMaterial :
                Material.append(q[w])
            
        MaterialAll.append(Material)
            
        for q in USP_PhaseExecutionEvents_Rpt1:
            row+=1
        listrow.append(row)  
        for q in USP_PhaseExecutionEvents_Rpt:
            d2 = []
            for w in listPhase:
                d2.append(q[w])
            d1.append(d2)
        
        details.append(d1)
           
        
    pprint.pprint(details)
    print("--------------------------")
    
    n = len(section)
   
                
                    
    print("--------------------------")
 
 
    print(n)
    print(listrow)
    #print(details[0][1][0])
    
    return render_template('report.html',section=section,details=details,listrow=listrow,n=n,Campaign_ID=Campaign_ID ,Lot_ID = Lot_ID,Batch_ID =Batch_ID,
        Recipe_ID= Recipe_ID,
        Recipe_Version= Recipe_Version,
        recipe_Name= recipe_Name,
        ApprovalCode=ApprovalCode,
        Batch_Size=Batch_Size,
        Train_ID= Train_ID,
        Log_Close_DT= Log_Close_DT,
        MaterialAll = MaterialAll)
 
@app.route('/batch_report_API' ,methods=["GET", "POST"])
def Report_OEE_API():
    global count
    q = request.args.get('q')
    
    print(q)

    if request.method == "POST":
        count+=1
        return redirect(url_for('ReportOEE'))
    else:
        host = "172.30.1.1"
        port = 1433
        database = "managedb"
        user = "sa"
        passwd = "qwerty@2019"
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ host +';DATABASE='+database+';UID='+user+';PWD='+passwd)
        batch_report = cnxn.cursor()
        batch_report.execute("SELECT PD_ORDER , PD_PLAN_DT , PD_TARGET_QTY ,PD_UNIT , PD_FM_CODE,PD_FM_NAME , PD_BATCHNO ,PD_PROC_P_ST , PD_PROC_O_ST , PD_PROC_M_ST , PD_PROC_Q_ED , PD_PROC_S_DT ,PD_STATUS_CODE FROM [dbo].[PD_ORDER_VIEW_RPT] ")
        
        
        host = "172.30.1.203"
        port = 1433
        database = "BatchHistory"
        user = "sa"
        passwd = "p@ssw0rd"
        Campaign_ID="*"
        Lot_ID="*"
        data ='*'
        StartOfPeriod_DT="1/11/2021 12:00:00"
        now  = datetime.now()
        EndOfPeriod_DT= now.strftime("%m/%d/%Y %H:%M:%S")
        print(EndOfPeriod_DT)
        
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ host +';DATABASE='+database+';UID='+user+';PWD='+passwd)
        USP_Journal_Rpt = cnxn.cursor()
        USP_Journal_Rpt.execute("SELECT distinct Batch_ID From BatchIdLog ")
        Batch_ID = []
        
        for i in USP_Journal_Rpt:
            
            Batch_ID.append(i[0])
    
        payload = []
        content = {}
        for result in batch_report:
            if result[0] in Batch_ID:
                content = {'PD': result[0], 'PD_PLAN_DT': str(result[1]), 'PD_TARGET_QTY': result[2],'PD_UNIT': result[3],'PD_FM_CODE': result[4]+'/'+result[5],'PD_BATCHNO': result[6],'PD_PROC_P_ST': str(result[7]),'PD_PROC_O_ST': str(result[8]),'PD_PROC_M_ST': str(result[9]),'PD_PROC_Q_ED': str(result[10]),'PD_PROC_S_DT': str(result[11]),'PD_STATUS_CODE': str(result[12])}
                payload.append(content)
                content = {}
        #print(payload)
        return json.dumps({"data":payload}, cls = Encoder), 201
         
        
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True ,port=5001)
