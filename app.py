from flask import Flask , render_template , request , redirect , url_for
app = Flask(__name__)

_code = ""


@app.route("/index", methods=["GET","POST"])
def main():
		return render_template('index.html')


@app.route("/analyse", methods=["POST"])
def analyse():
	if(request.method == "POST"):
		import pandas as pd
		import numpy as np
		# import os
		data = pd.read_excel("data.xlsx")
		
		data['N'] =  data.N.astype(float)
		data['P'] =  data.P.astype(float)
		data['K'] =  data.K.astype(float)
		data['TEMPERATURE'] =  data.TEMPERATURE.astype(float)
		X =  data.drop("CLASS",axis=1)
		y =  data.CLASS

		from sklearn.neighbors import KNeighborsClassifier
		clf = KNeighborsClassifier(n_neighbors=3)
		clf.fit(X,y)

		print(request.form.get('Potassium'))
		
		
		potassium = request.form.get('Potassium')
		phosphorous = request.form.get('Phosphorous')
		nitrogen = request.form.get('Nitrogen') 
		pH = request.form.get('pH')
		temperature = request.form.get('Temperature')

		columns = ['N','P','K','pH','TEMPERATURE'] 
		values = np.array([ nitrogen ,phosphorous ,potassium ,   pH , temperature])
		pred = pd.DataFrame(values.reshape(-1, len(values)),columns=columns)
			# print(pred.dtype)
		print(pred)

		prediction = clf.predict(pred)
		print(prediction)

		data =  data[ data['CLASS'] != prediction[0]]
		X =  data.drop("CLASS",axis=1)
		y =  data.CLASS
		clf = KNeighborsClassifier(n_neighbors=3)
		clf.fit(X,y)
		prediction1 = clf.predict(pred)
		print(prediction1)


		data =  data[ data['CLASS'] != prediction1[0]]
		X =  data.drop("CLASS",axis=1)
		y =  data.CLASS
		clf = KNeighborsClassifier(n_neighbors=3)
		clf.fit(X,y)
		prediction2 = clf.predict(pred)
		print(prediction2)

		p1 = prediction1[0]
		p2 = prediction2[0]
		p1 = p1 -1
		p2 = p2 -1
			# print()

		if(prediction == 7):
			return render_template('crops.html' , crop="TOMATO" , crop1=prediction1[0] , crop2=prediction2[0] ) 
		elif(prediction == 1):
			return render_template('crops.html' , crop="GARLIC" , crop1=prediction1[0] , crop2=prediction2[0] )
		elif(prediction == 2):
			return render_template('crops.html' , crop="ONION" , crop1=prediction1[0] , crop2=prediction2[0] )
		elif(prediction == 3):
			return render_template('crops.html' , crop="ORANGE" , crop1=prediction1[0] , crop2=prediction2[0])
		elif(prediction == 4):
			return render_template('crops.html' , crop="PEAS" , crop1=prediction1[0] , crop2=prediction2[0] )
		elif(prediction == 5):
			return render_template('crops.html' , crop="POTATO" , crop1=prediction1[0] , crop2=prediction2[0] )
		elif(prediction == 6):
			return render_template('crops.html' , crop="RICE" , crop1=prediction1[0] , crop2=prediction2[0] )
		elif(prediction == 8):
			return render_template('crops.html' , crop="SUGARCANE" , crop1=prediction1[0] , crop2=prediction2[0])		
		else:
			return "no"
	# render_template('index.html')
	else:
		return render_template('index.html')


		 
		

		
if (__name__ == "__main__"):	
	app.run(debug=True)
