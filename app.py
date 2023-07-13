
from flask import Flask , render_template, request
import pickle
import numpy as np

app = Flask(__name__)


@app.route("/" , methods=['POST', 'GET'])
def index():

    with open("model/pricer.pickle" , 'rb') as file:
        model = pickle.load(file)
    price = 0
    if request.method == 'POST':
        ram = request.form['Ram']
        weight = request.form['Weight']
        company = request.form['Company']
        typename = request.form['TypeName']
        opsys = request.form['OpSys']
        cpu = request.form['Cpu_name']
        gpu = request.form['Gpu_name']
        ips = request.form.getlist('IPS')
        touchscreen = request.form.getlist('Touchscreen')
        retina = request.form.getlist('Retina-Display')
        hd = request.form.getlist('Full-HD')
    
        companies = ['Dell', 'Lenovo', 'HP', 'Asus', 'Acer', 'MSI', 'Other', 'Toshiba','Apple']
        typenames = ['Notebook', 'Gaming', 'Ultrabook', '2 in 1 Convertible', 'Workstation','Netbook']
        opsyss = ['Windows', 'other', 'Linux', 'MAC']
        cpu_names = ['Intel Core i7', 'Intel Core i5', 'Others', 'Intel Core i3', 'AMD']
        gpu_names = ['Intel', 'Nvidia', 'AMD', 'Others']

        feature_list = []

        def appender(feature , list) :
            for item in list :
                if item == feature :
                    feature_list.append(1)
                else :
                    feature_list.append(0) 

        appender(company , companies )
        appender(typename , typenames )
        feature_list.append(int(ram))
        appender(opsys , opsyss )
        feature_list.append(float(weight))
        feature_list.append(len(ips))
        feature_list.append(len(touchscreen))
        feature_list.append(len(retina))
        feature_list.append(len(hd))
        appender(cpu , cpu_names )
        appender(gpu , gpu_names )
        pred =  model.predict([feature_list])
        price = np.round(pred[0])
        
    return render_template('index.html' , price = price , lkrprice = np.round(price*294.83) )


 
if __name__ == '__main__':
    app.run(debug=True)