from flask import Flask, render_template, request
import joblib
import numpy as np


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
def predictor():
    return render_template('contactus.html')




@app.route('/preventions')
def predictor():
    return render_template('preventions.html')


@app.route('/dataset_info')
def predictor():
    return render_template('dataset_info.html')

@app.route('/predict', methods=['POST'])
def predict():
    temp_array = list()

    if request.method =="POST":
        name = str(request.form["username"])
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
            dieseas = "Sorry , You have Heart Dieseas"
        else:
            dieseas ="You have No Dieseas."
        return render_template('result.html', array1=temp_array,dieseas=dieseas)






if __name__ == '__main__':
    app.run(debug=True)







    	




	