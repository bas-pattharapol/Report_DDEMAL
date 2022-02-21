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

#ddddd
app = Flask(__name__)

count = 3
@app.route('/')
@app.route('/batch_report')
def batch_report():
    #cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ host +';DATABASE='+database+';UID='+user+';PWD='+passwd)
    #SQL_Login = cnxn.cursor()
    #SQL_Login.execute("Exec USP_Journal_Rpt '" + Campaign_ID + "','"+ Lot_ID +"','"+ StartOfPeriod_DT + "','"+EndOfPeriod_DT+"'" )
    return render_template('batch_report.html')

@app.route('/report')
def report():
    #cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ host +';DATABASE='+database+';UID='+user+';PWD='+passwd)
    #SQL_Login = cnxn.cursor()
    #SQL_Login.execute("Exec USP_Journal_Rpt '" + Campaign_ID + "','"+ Lot_ID +"','"+ StartOfPeriod_DT + "','"+EndOfPeriod_DT+"'" )
    
    return render_template('report.html')


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


    
    
@app.route('/report/<string:pdOrder>')
def modeReport(pdOrder):
    server = "172.30.2.2"
    port = 5432
    database = "OEE_DB"
    username = "sa"
    password = "p@ssw0rd"
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ server +';DATABASE='+database+';UID='+username+';PWD='+password)
    ST_Report = cnxn.cursor()
    ST_Report.execute("SELECT * FROM SCADA_DB.dbo.Mixing_Report mr  WHERE PhaseID > 200 AND PhaseID < 300 AND PD_ORDER = '" +pdOrder+ "' ORDER BY Start_time ASC")
    
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ server +';DATABASE='+database+';UID='+username+';PWD='+password)
    Phase_Parameter = cnxn.cursor()
    Phase_Parameter.execute("SELECT PhaseID ,Parameter1,Parameter2,Parameter3,Parameter4,Parameter5,Parameter6,Parameter7,Parameter8 FROM SCADA_DB.dbo.Phase_Parameter") 
    
    Phase_Parameter_DIR = Phase_Parameter.fetchall()

    insertObject = []
    columnNames = [column[0] for column in Phase_Parameter.description]
    for record in Phase_Parameter_DIR:
        insertObject.append( dict( zip( columnNames , record ) ) )
    print(insertObject)
    
    return render_template('report.html',pdOrder=pdOrder,Phase_Parameter=insertObject,ST_Report=ST_Report,len=len(Phase_Parameter_DIR))
 
@app.route('/batch_report_API' ,methods=["GET", "POST"])
def batch_report_API():
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
        
    
        payload = []
        content = {}
        for result in batch_report:
            content = {'PD': result[0], 'PD_PLAN_DT': str(result[1]), 'PD_TARGET_QTY': result[2],'PD_UNIT': result[3],'PD_FM_CODE': result[4]+'/'+result[5],'PD_BATCHNO': result[6],'PD_PROC_P_ST': str(result[7]),'PD_PROC_O_ST': str(result[8]),'PD_PROC_M_ST': str(result[9]),'PD_PROC_Q_ED': str(result[10]),'PD_PROC_S_DT': str(result[11]),'PD_STATUS_CODE': str(result[12])}
            payload.append(content)
            content = {}
        #print(payload)
        return json.dumps({"data":payload}, cls = Encoder), 201
         
        
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True ,port=5001)
