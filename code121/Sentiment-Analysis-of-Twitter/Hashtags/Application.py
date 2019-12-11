from flask import Flask,jsonify,request
from flask import render_template
import ast
import random
app = Flask(__name__)
analysisdata_array = ['2008 analysis','2009 analysis ','2010 analysis ','2011 analysis ','2012 analysis ','2013 analysis ','2014 analysis ','2015 analysis ','2016 analysis ','2017 analysis ','2018 analysis ','2019 analysis ']
analysisvalues_array = ['500','432','342','743','890','932','735','521','732','213','544','911']
@app.route("/")
def get_chart_page():
        global analysisdata_array,analysisvalues_array
        analysisdata_array = analysisdata_array = ['2008 analysis','2009 analysis ','2010 analysis ','2011 analysis ','2012 analysis ','2013 analysis ','2014 analysis ','2015 analysis ','2016 analysis ','2017 analysis ','2018 analysis ','2019 analysis ']
        analysisvalues_array = []
        for id in range(12):
                analysisvalues_array.append(random.randint(100,1000))
        return render_template('chart.html', analysisvalues_array=analysisvalues_array, analysisdata_array=analysisdata_array)
@app.route('/refreshData')
def refresh_graph_data():
        global analysisdata_array, analysisvalues_array
        analysisvalues_array = []
        for id in range(12):
                analysisvalues_array.append(random.randint(100,1000))
        print("analysisdata_array now: " + str(analysisdata_array))
        print("data now: " + str(analysisvalues_array))
        return jsonify(sLabel=analysisdata_array, sData=analysisvalues_array)
@app.route('/updateData', methods=['POST'])
def update_data():
        global analysisdata_array, analysisvalues_array
        if not request.form or 'data' not in request.form:
          return "error",400
        analysisdata_array = ast.literal_eval(request.form['label'])
        analysisvalues_array = ast.literal_eval(request.form['data'])
        print("analysisdata_array received: " + str(analysisdata_array))
        print("data received: " + str(analysisvalues_array))
        return "success",201
if __name__ == "__main__":
        app.run(port=5001)
#enter your IP address above