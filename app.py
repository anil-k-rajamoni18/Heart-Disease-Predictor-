from flask import Flask, render_template, request
import joblib
import numpy as np



import csv

import smtplib 

from email.message import EmailMessage

from string import Template

from pathlib import Path

MY_ADDRESS,PASSWORD='hello.hell3096@gmail.com','Hello.hell#3096'




# Load from file
# Load the Random Forest CLassifier model
filename = 'models/heart_diesease_RandomForest.sav'
model = joblib.load(filename)

app = Flask(__name__)

@app.route("/")
def home():
	return render_template('index.html')



@app.route('/predictor')
def predictor():
    return render_template('predictor.html')



@app.route('/contactus')
def contactus():
    return render_template('contact.html')





@app.route('/preventions')
def preventions():
    return render_template('preventions.html')


@app.route('/dataset_info')
def dataset_info():
    return render_template('dataset_info.html')



@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
  
    if request.method=="POST" or request.method=="GET":
        try:
            data=request.form.to_dict()
            # print(data)
            send_mail_user(data)
           
            
            
            return render_template('/thankyou.html',name=data['username'])
        except Exception as e:
            # print(e)
            return f"did not save to database {e}"
    else:
        return "something went wrong" 






def write_to_file(data):
    with open(r'database.txt',mode='a') as db:
        email=data['email']
        name=data['username']
        dieseas = data["dieseas"]
        accuracy = data["accuracy"]

        file=db.write(f'\n {name} ,{email},{dieseas},{accuracy}')



def write_to_csv(data):
 
    with open(r'database2.csv',mode='a',newline='') as db2:
        email=data['email']
        name=data['username']
        dieseas = data["dieseas"]
        accuracy = data["accuracy"]
        csv_writer = csv.writer(db2,delimiter=',', quotechar='"',quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([name,email,dieseas,accuracy])
        print(csv_writer)


def send_mail(data):
   
    email=EmailMessage()
     
    email['from'] = 'Heart Predictor WebApp'
    email['to'] = data["email"]
    email['subject'] = "Hey Your Results Are "
    data["message"] = f' {data["dieseas"]} With   {data["accuracy"]} \n Please Visit our website for More Details'
    msg=f" \t From Heat Predictor WebApp \n Name:{data['username']} \n EMAIL : {data['email']} \n SUBJECT : Heart Prediction Test Details \n MESSAGE : {data['message']}"


    email.set_content(msg)


    with smtplib.SMTP('smtp.gmail.com:587') as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(MY_ADDRESS,PASSWORD)
        smtp.send_message(email)
        print('all good boss')



def send_mail_user(data):
   
    email=EmailMessage()
     
    email['from'] = 'Heart Predictor WebApp'
    email['to'] = "rajamonianil0909@gmail.com"
    email['subject'] = " Hey ! AK You Have New Response From Heart Predictor Web App "
    msg=f" \t From Heat Predictor WebApp \n Name:{data['username']} \n EMAIL : {data['email']} \n SUBJECT : {data['subject']} \n MESSAGE : {data['message']}"


    email.set_content(msg)


    with smtplib.SMTP('smtp.gmail.com:587') as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(MY_ADDRESS,PASSWORD)
        smtp.send_message(email)
        print('all good boss')










@app.route('/predict', methods=['POST'])
def predict():
    temp_array = list()

    if request.method =="POST":
        name = str(request.form["username"])

        email =str(request.form["email"])
        age  = int(request.form["age"])
        sex = int(request.form["Gender"])
        resting_blood_pressure = int(request.form["resting_blood_pressure"])
        cholesterol = int(request.form["cholestrol"])
        fasting_blood_Pressure = int(request.form["fasting_blood_sugar"])
        max_heart_rate = int(request.form["max_heart_rate"])
        exercise_induced_angina = int(request.form["exang"])
        st_depression =  float(request.form["st_depression"])
        num_major_vessels = int(request.form["no_vessels"])

        temp_array +=[age, sex , resting_blood_pressure, cholesterol, fasting_blood_Pressure, max_heart_rate,exercise_induced_angina,st_depression,num_major_vessels]


        chest_pain_type = int(request.form["chest_pain"])

        if chest_pain_type==0:
            temp_array = temp_array +[1,0,0,0]
        elif chest_pain_type == 1:
            temp_array = temp_array +[0,1,0,0]
        elif chest_pain_type ==2:
            temp_array = temp_array +[0,0,1,0]
        else:
            temp_array = temp_array +[0,0,0,1]

        restecg = int(request.form["rest_ecg_type"])

        if restecg == 0:
            temp_array+=[1,0,0]
        elif restecg==1:
            themp_array+=[0,1,0]
        else:
            temp_array+=[0,0,1] 

        slope = int(request.form["st_slope"])
        if slope ==0:
            temp_array = temp_array+[1,0,0]
        elif slope==1:
            temp_array = temp_array+[0,1,0]
        else:
            temp_array = temp_array+[0,0,1]

        thal  = int (request.form["thalassemia"])


        if thal ==0:
            temp_array+=[0,0,0,1]
        elif thal==1:
            temp_array+=[1,0,0,0]
        elif thal==2:
            temp_array+=[0,1,0,0]
        else:
            temp_array+=[0,0,1,0]

        #reshaping 
        temp_array =np.array(temp_array)
        temp_array = temp_array.reshape(1,-1)


        print(temp_array.shape,temp_array )

        #predicting 
        pred=model.predict(temp_array)
        if pred ==1:
            dieseas = "Yes , Heart Dieseas"
        else:
            dieseas ="No Dieseas."


        data = request.form.to_dict()
        data["dieseas"] = dieseas
        data["accuracy"] = 87
        write_to_csv(data)
        send_mail(data)
        write_to_file(data)
        print(data)
        return render_template('result.html', test_result=dieseas)
    else:
        return "Something went wrong"






if __name__ == '__main__':
    app.run(debug=True)







    	




	