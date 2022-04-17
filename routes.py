
from functools import wraps
from flask import Flask, flash, request, redirect, url_for, current_app,send_from_directory,render_template, session    ,jsonify, after_this_request
from itsdangerous import json
import json
import pandas as pd
import mysql.connector
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from datetime import datetime
import cv2
import numpy as np
# from redis.commands.json.path import Path
from pathlib import Path
from dotenv import load_dotenv
import os

from flask.wrappers import Response
from flask_apscheduler import APScheduler

app = Flask(__name__)
scheduler = APScheduler() 


env_path = Path('.') / 'project.env'
load_dotenv(dotenv_path=env_path)

###########################################3
with app.app_context():
    # within this block, current_app points to app.
    print(current_app.name)
UPLOAD_FOLDER = './static/assets/uploaders'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.secret_key = 'super secret key'
#############################################3
try:
    mydb = mysql.connector.connect(
        host="hypegenai.com",
        user="hypegena",
        password="aZ5xjXf133",
        database="hypegena_dashboard"
    )
   
except Exception as e:
    print(e)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for("login"))

    return decorated_function
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session["yetki"]==1:
            return f(*args, **kwargs)
        else:
            return render_template("./index.html")

    return decorated_function







@app.route('/api/file', methods=['POST'])
def eventPost():
    global count
    global r
    count =1 
    d = request.files.to_dict()
    content = request.form.to_dict()
    image = request.files['screen_image'].read()
    
    jpg_as_np = np.frombuffer(image, dtype=np.uint8)
    img_decode = cv2.imdecode(jpg_as_np, cv2.IMREAD_COLOR)
    image = img_decode.reshape(480, 848, 3)
    
    cv2.imwrite("./static/assets/api_image/api_image.jpg",image)
    api_image_path = "./static/assets/api_image/api_image.jpg"




    json_re = {
        'screen_image': image,
        'module_name': content['module_name'],
        'notification_no': content['notification_no'],
        'proffer':content["proffer"],
        "cam_no":content['cam_no'],
        "date":content['date'],
        "status":content['status']

    }






    with open("./static/assets/popup/data.json", 'w') as file:
        file.write("""
        {
    "hype_module_list": "Super Hero Emre YILDIZ",
    "activity": "Factory",
    "design_date": 2020,
    "secret_key": "coKhjsPmTtSejyHqOjo64grxzgBnQzJd",
    "active": true,
    "notification_list": [
      {
        "name": "Equipment Control",
        "notification_no": 12123,
        "Proffer" : "m-101",
        "image" : "image-101",
        "cam_no" : "6",
        "Date":"02.04.2022 17:25",
        "Status": "Appro",
        "image_path" : """ +'"'+str(api_image_path)+'"'+ """
        
      }
     
     
    ]
  }

  
        
        """)
   
    
    return """0k"""
    
@app.route('/seq')
def scheduleTask():
    pass


@app.route('/remove', methods=['GET','POST'])
def remove():
    if request.method == 'POST':
        
        file_name = request.form.get('data') 
        print("file_name",file_name)
        try:
            os.remove("./static/assets/popup/"+str(file_name)+".json")
        except Exception as e:
            print(e)


        return """ok"""



@app.route('/')
@login_required
def index():
    print("ss")
    header_information_array=[]
    with open('./static/assets/json_files/header_information.json') as json_file:
        header_information = json.load(json_file)
    

        header_information_array.append(header_information['header_list'][0]['total_cam'])
        header_information_array.append(header_information['header_list'][0]['total_module'])
        header_information_array.append(header_information['header_list'][0]['total_users'])
        header_information_array.append(header_information['header_list'][0]['total_cam']*header_information['header_list'][0]['total_module']*8)
        
         

    module_list_array = []
    with open('./static/assets/json_files/module.json') as json_file:
        data = json.load(json_file)
    

        for list_array in data['module_list']:
            module_list_array.append(list_array['name'])
    information_name = []
    information_path = []
    information_risk = []

    with open('./static/assets/json_files/information.json') as json_file:
        data_information = json.load(json_file)
    

        for value in data_information['information_list']:
            information_name.append(value["file_name"])
            information_path.append(value["file_path"])


    with open('./static/assets/json_files/bank_MOCK_DATA (2).json') as json_file:
        data_notification = json.load(json_file)
        dataframe_notification = pd.DataFrame.from_dict(data_notification)
        dataframe_notification=dataframe_notification.dropna()
        
        dataframe_notification.sort_values(by=["date"],inplace=True, ascending=False)
        dataframe_notification=dataframe_notification.reset_index()
        orginal_notification = dataframe_notification
        



        
        # Fire Detection
        # Area Violation
        today_date = datetime.today()
        one_month_ago = today_date - relativedelta(months=1)
        
        orginal_notification['date'] = pd.to_datetime(orginal_notification['date'])  
        mask = (orginal_notification['date'] > one_month_ago) & (orginal_notification['date'] <= today_date)
        month_notification = orginal_notification.loc[mask]
        




        information_risk.append(len(orginal_notification['name'].unique())*4) #uniq name baktık ve her modül için 4 önerimiz var
        information_risk.append(len(orginal_notification)) # toplam risk sayısını atadık
        information_risk.append(len(month_notification)) #1 aylık risk tablosu

        # area=(orginal_notification.groupby('name')['index'].nunique())
        area=(orginal_notification['name'].value_counts())
        
        area=(area.sort_values(ascending=True))
        risk_mana = area.to_frame().reset_index()
        
        
        first_data=dataframe_notification[:10]
        
        # print(first_data)



       
    
    return render_template("index.html",module_list_array=module_list_array,information_name=information_name,information_path=information_path,first_data=first_data,orginal_notification=orginal_notification,information_risk=information_risk,
    header_information_array=header_information_array,risk_mana=risk_mana)



    

@app.route('/notifications')
@login_required
def notifications():

    with open('./static/assets/json_files/bank_MOCK_DATA (2).json') as json_file:
        data_notification = json.load(json_file)
        dataframe_notification = pd.DataFrame.from_dict(data_notification)
        dataframe_notification=dataframe_notification.dropna()
        
        dataframe_notification.sort_values(by=["date"],inplace=True, ascending=False)
        dataframe_notification=dataframe_notification.reset_index()
        orginal_notification = dataframe_notification

        first_data=orginal_notification[:100]
        area=(orginal_notification['name'].value_counts())
        
        area=(area.sort_values(ascending=True))
        risk_mana = area.to_frame().reset_index()
        

    return render_template("./pages/tables/basic-table.html",first_data=first_data,risk_mana=risk_mana)
video = cv2.VideoCapture("rtsp://admin:Password@192.168.1.108/cam/realmonitor?channel=1&subtype=1.")

def gen(video):
    while True:
        try:
            _, image = video.read()
        except Exception as e:
            print(e)

        _, jpeg = cv2.imencode('.jpg', image)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
@app.route('/video_feed')
def video_feed():
    global video
    return Response(gen(video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')






@app.route('/banka')
# @login_required
def banka():
    print("ss")
    header_information_array=[]
    with open('./static/assets/json_files/bank_header_information.json') as json_file:
        header_information = json.load(json_file)
    

        header_information_array.append(header_information['header_list'][0]['gunluk_musteri'])
        header_information_array.append(header_information['header_list'][0]['banka_icerisindeki_musteri_sayisi'])
        header_information_array.append(header_information['header_list'][0]['gise_musteri_sayisi'])
    
    
        header_information_array.append(header_information['header_list'][0]['bekleyen_musteri_sayisi'])
        
         

    module_list_array = []
    with open('./static/assets/json_files/bank_module.json') as json_file:
        data = json.load(json_file)
    

        for list_array in data['module_list']:
            module_list_array.append(list_array['name'])
    information_name = []
    information_path = []
    information_risk = []

    with open('./static/assets/json_files/information.json') as json_file:
        data_information = json.load(json_file)
    

        for value in data_information['information_list']:
            information_name.append(value["file_name"])
            information_path.append(value["file_path"])


    with open('./static/assets/json_files/MOCK_DATA (2).json') as json_file:
        data_notification = json.load(json_file)
        dataframe_notification = pd.DataFrame.from_dict(data_notification)
        dataframe_notification=dataframe_notification.dropna()
        
        dataframe_notification.sort_values(by=["date"],inplace=True, ascending=False)
        dataframe_notification=dataframe_notification.reset_index()
        orginal_notification = dataframe_notification
        



        
        # Fire Detection
        # Area Violation
        today_date = datetime.today()
        one_month_ago = today_date - relativedelta(months=1)
        
        orginal_notification['date'] = pd.to_datetime(orginal_notification['date'])  
        mask = (orginal_notification['date'] > one_month_ago) & (orginal_notification['date'] <= today_date)
        month_notification = orginal_notification.loc[mask]
        




        information_risk.append(len(orginal_notification['name'].unique())*4) #uniq name baktık ve her modül için 4 önerimiz var
        information_risk.append(len(orginal_notification)) # toplam risk sayısını atadık
        information_risk.append(len(month_notification)) #1 aylık risk tablosu

        # area=(orginal_notification.groupby('name')['index'].nunique())
        area=(orginal_notification['name'].value_counts())
        
        area=(area.sort_values(ascending=True))
        risk_mana = area.to_frame().reset_index()
        
        
        first_data=dataframe_notification[:10]
        
        # print(first_data)



       
    
    return render_template("bank_index.html",module_list_array=module_list_array,information_name=information_name,information_path=information_path,first_data=first_data,orginal_notification=orginal_notification,information_risk=information_risk,
    header_information_array=header_information_array,risk_mana=risk_mana)



@app.route('/chart')
@login_required
def chart():


    with open('./static/assets/json_files/bank_MOCK_DATA (2).json') as json_file:
        data = json.load(json_file)

    dataframe = pd.DataFrame.from_dict(data)
    dataframe=dataframe.dropna()
    dataframe=dataframe.reset_index()
    
    for i in range(len(dataframe)):
        (dataframe['date'].loc[i])=(dataframe['date'].loc[i])[0:10]


    #########LİNE CHART
    line_dataframe=dataframe.sort_values(by='date', ascending=False)
    el=(line_dataframe['date'].value_counts())
    df = el.to_frame()
    df=df.reset_index()
    df=df.sort_values(by='index', ascending=False)
    df=df.reset_index()

    line_index_array = []
    line_value_array = []
    df=df[:30]
    for i in range(len(df)):
        line_index_array.append(df['index'].iloc[i])
        line_value_array.append(df['date'].iloc[i])
    
    ######BOX CHART
    for i in range(len(dataframe)):
        (dataframe['date'].loc[i])=(dataframe['date'].loc[i])[0:7]

    box_dataframe=dataframe.sort_values(by='date', ascending=False)
    box=(box_dataframe['date'].value_counts())
    df_box = box.to_frame()
    df_box=df_box.reset_index()
    df_box=df_box.sort_values(by='index', ascending=False)
    df_box=df_box.reset_index()
    df_box=(df_box[0:12])
    dfbox_index_array = []
    dfbox_value_array = []

    for i in range(len(df_box)):
        dfbox_index_array.append(df_box['index'].iloc[i])
        dfbox_value_array.append(df_box['date'].iloc[i])
    #AREAAA CHART

    area_dataframe=dataframe.sort_values(by='cam_no', ascending=False)
    area_dataframe=(area_dataframe['cam_no'].value_counts())

    area_dataframe = area_dataframe.to_frame()
    area_dataframe=area_dataframe.reset_index()
    area_dataframe=area_dataframe.sort_values(by='index', ascending=False)
    area_dataframe=area_dataframe.reset_index()
    area_index_array = []
    area_value_array = []
    for i in range(len(area_dataframe)):
        area_index_array.append(area_dataframe['index'].iloc[i])
        area_value_array.append(area_dataframe['cam_no'].iloc[i])
   #DOUGHNUTTT CHARTTT

    doughnut_dataframe=dataframe.sort_values(by='name', ascending=False)
    doughnut_dataframe=(doughnut_dataframe['name'].value_counts())
    doughnut_dataframe = doughnut_dataframe.to_frame()
    doughnut_dataframe=doughnut_dataframe.reset_index()
    doughnut_dataframe=doughnut_dataframe.sort_values(by='index', ascending=False)
    doughnut_dataframe=doughnut_dataframe.reset_index()
    doughnut_index_array = []
    doughnut_value_array = []
    for i in range(len(doughnut_dataframe)):
        doughnut_index_array.append(doughnut_dataframe['index'].iloc[i])
        doughnut_value_array.append(doughnut_dataframe['name'].iloc[i])





    with open("./static/assets/js/chart.js", 'w') as file:
        file.write("""
    $(function() {
    /* ChartJS
    * -------
    * Data and config for chartjs
    */
    'use strict';
    var data = {
        labels: """+str(line_index_array)+""",
        datasets: [{
        label: '# of Votes',
        data: """+str(line_value_array)+""",
        backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)',
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)',
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)',
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)',
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)',
        ],
        borderColor: [
            'rgba(255,99,132,1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)',
            'rgba(255,99,132,1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)',
            'rgba(255,99,132,1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)',
            'rgba(255,99,132,1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)',
            'rgba(255,99,132,1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)',
            
        ],
        borderWidth: 1,
        fill: false
        }]
    };
    var data_bar = {
        labels: """+str(dfbox_index_array)+""",
        datasets: [{
        label: '# of Votes',
        data: """+str(dfbox_value_array) +""",
        backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)',
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)'
        ],
        borderColor: [
            'rgba(255,99,132,1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)',
            'rgba(255,99,132,1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)',
            
        ],
        borderWidth: 1,
        fill: false
        }]
    };

    var options = {
        scales: {
        yAxes: [{
            ticks: {
            beginAtZero: true
            },
            gridLines: {
            color: "rgba(204, 204, 204,0.1)"
            }
        }],
        xAxes: [{
            gridLines: {
            color: "rgba(204, 204, 204,0.1)"
            }
        }]
        },
        legend: {
        display: false
        },
        elements: {
        point: {
            radius: 0
        }
        }
    };
    var doughnutPieData = {
        datasets: [{
        data: """+str(doughnut_value_array)+""",
        backgroundColor: [
            'rgba(255, 99, 132, 0.5)',
            'rgba(54, 162, 235, 0.5)',
            'rgba(255, 206, 86, 0.5)',
            'rgba(75, 192, 192, 0.5)',
            'rgba(153, 102, 255, 0.5)',
            'rgba(255, 159, 64, 0.5)'
        ],
        borderColor: [
            'rgba(255,99,132,1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)'
        ],
        }],

        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: """+str(doughnut_index_array)+"""
    };

    var doughnutPieOptions = {
        responsive: true,
        animation: {
        animateScale: true,
        animateRotate: true
        }
    };

    var areaData = {
        labels: """+str(area_index_array)+""",
        datasets: [{
        label: '# of Votes',
        data: """+str(area_value_array)+""",
        backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)'
        ],
        borderColor: [
            'rgba(255,99,132,1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)'
        ],
        borderWidth: 1,
        fill: true, // 3: no fill
        }]
    };

    var areaOptions = {
        plugins: {
        filler: {
            propagate: true
        }
        },
        scales: {
        yAxes: [{
            gridLines: {
            color: "rgba(204, 204, 204,0.1)"
            }
        }],
        xAxes: [{
            gridLines: {
            color: "rgba(204, 204, 204,0.1)"
            }
        }]
        }
    }

    // Get context with jQuery - using jQuery's .get() method.
    if ($("#barChart").length) {
        var barChartCanvas = $("#barChart").get(0).getContext("2d");
        // This will get the first returned node in the jQuery collection.
        var barChart = new Chart(barChartCanvas, {
        type: 'bar',
        data: data_bar,
        options: options
        });
    }

    if ($("#lineChart").length) {
        var lineChartCanvas = $("#lineChart").get(0).getContext("2d");
        var lineChart = new Chart(lineChartCanvas, {
        type: 'line',
        data: data,
        options: options
        });
    }

    


    if ($("#doughnutChart").length) {
        var doughnutChartCanvas = $("#doughnutChart").get(0).getContext("2d");
        var doughnutChart = new Chart(doughnutChartCanvas, {
        type: 'doughnut',
        data: doughnutPieData,
        options: doughnutPieOptions
        });
    }

    

    if ($("#areaChart").length) {
        var areaChartCanvas = $("#areaChart").get(0).getContext("2d");
        var areaChart = new Chart(areaChartCanvas, {
        type: 'line',
        data: areaData,
        options: areaOptions
        });
    }

    
    });
    """.strip())




    return render_template("./pages/charts/chartjs.html")

@app.route('/setting',methods=['GET', 'POST'])
@login_required
def setting():
    if request.method == 'POST':


        if request.form.get("button1") == "value1":
            password_current=request.form.get("password_current")
            password=request.form.get("password")
            password_confirmation=request.form.get("password_confirmation")
            print(password_current)
            print(password)
            print(password_confirmation)

            username = session["username"]

            mycursor = mydb.cursor(buffered=True)
            mycursor.execute("select*from users where username='" +
                            str(username)+"' and password='"+str(password_current)+"'")
            myresult = mycursor.fetchall()
            mycursor.close()
            if myresult:
                if password==password_confirmation:
                    mycursor = mydb.cursor(buffered=True)
                    mycursor.execute("update users SET password='" +
                                  password_confirmation+"' where username='"+username+"'")
                    mycursor.close()
                    mydb.commit()
                    flash("Şifre Değiştirildi",'info')
                else:
                    flash("Şifre Değiştirilemedi Lütfen Daha Sonra Tekrar Deneyin",'info')




    return render_template("./pages/tables/setting.html")


@app.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == 'POST':


        if request.form.get("button") == "login_btn":
            username=request.form.get("username")
            password=request.form.get("pass")
            print(username,password)
            mycursor = mydb.cursor(buffered=True)
            mycursor.execute("select*from users where username='" +
                            username+"' and password='"+password+"'")
            myresult = mycursor.fetchall()
            mycursor.close()
            if myresult:
                print(myresult)
                for i in myresult:
                    session["username"]=i[1]
                    session["company_id"]=i[3]
                    session["mail"]=i[4]
                    session["auth"]=i[5]
                    session["title"]=i[6]
                    session["name_surname"]=i[7]
                    session['logo_path']=i[8]
                    session['reg_date']=i[9]
                session["logged_in"] = True

                return redirect(url_for("index"))
                # return render_template("./index.html")

            else:

                return render_template("./pages/samples/login.html")

    return render_template("./pages/samples/login.html")
@app.route("/logout")
def logout():
    session.clear()
    print("Cikis Yapildi")

    return redirect(url_for("login"))

@app.route("/form", methods=['GET', 'POST'])
@login_required
def form():
    if request.method == 'POST':


        if request.form.get("button") == "form_btn":
            name=request.form.get("name")
            email=request.form.get("email")
            city=request.form.get("city")
            textarea=request.form.get("textarea")
            print(name,email,city,textarea)
            flash("Message Sent",'info')
    

    return render_template("./pages/forms/basic_elements.html")
@app.errorhandler(500)
def page_not_found(error):
    return render_template('./pages/samples/error-500.html'), 500


@app.errorhandler(404)
def page_not_found(error):
    return render_template('./pages/samples/error-404.html'), 404





    return decorated_function
if __name__ == '__main__':
    scheduler.add_job(id = 'Scheduled Task', func=scheduleTask, trigger="interval", minutes=0.01)
    scheduler.start()

    # run() method of Flask class runs the application
    # on the local development server.
    app.run()