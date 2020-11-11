from flask import Flask,Response,render_template,request,redirect,url_for,send_file, jsonify


app = Flask(__name__)

@app.route('/user-data', methods=['post', 'get'])
def user_data():
	emai_id = request.form["email-id"]
	return render_template("company.html")

@app.route('/', methods=['post', 'get'])
def home():
    return render_template("company.html")


if __name__ == '__main__':
    app.run(host = "127.0.0.1", port= "5566",debug=True)
    # app.run(host = appIp, port= appPort ,debug=True)
