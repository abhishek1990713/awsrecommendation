
from flask import Flask, request, jsonify,render_template
import os
from flask_cors import CORS, cross_origin
from matrix3 import abhi


application = Flask(__name__)


@application.route("/")
@cross_origin()
def home():
    return render_template('index.html')

@application.route("/recommendations", methods=['GET','POST'])
@cross_origin()
def predictRoute():
    if request.method == 'POST':

        cu_d = request.args.get('customerId')
        print((cu_d))
        recommended_products, rmse = abhi(int(cu_d), 5)

        print("Recommended products:", recommended_products)

        return jsonify({"products": recommended_products})

if __name__=="__main__":
    application.run(host="0.0.0.0")