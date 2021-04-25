from flask import Flask,request,render_template,jsonify
import Login as Login
import IoTEngine as IoTEngine
from datetime import datetime

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

class Display:
    def __init__(self, user):
      self.my_engine = IoTEngine.IoTEngine()
      self.suggestions = []
      self.user = user

    #displays warning in corresponing color for each sensor
    def display_warning(self, speed):
      self.suggestions = self.my_engine.get_suggestion(speed)
      print("Suggestions:", self.suggestions)
      return ",".join(self.suggestions)

    def log(self):
        return self.my_engine.save_log_to_cloud()

    def update(self):
        return self.my_engine.update_iot_engine()

    #renders the login form
    @app.route('/')
    def login():
        return render_template("login.html")

    #sends username and password, validates user
    @app.route("/login", methods=["POST"])
    def request_logon():
        usr = request.form['usr']
        pwd = request.form['pwd']
        my_login = Login.Login(usr,pwd)
        return my_login.login_request()

    #renders operator display view
    @app.route("/operator", methods=["GET"])
    def display_op():
        return render_template("operator.html")

    #allows the operator to start trip
    @app.route("/operator", methods=["POST"])
    def start_trip():
        op_disp.my_engine = IoTEngine.IoTEngine()
        file1 = open("LogFile.txt", "a")  # append mode
        file1.write("New Trip: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n")
        file1.close()
        return str(len(op_disp.my_engine.my_tsnr.RainGauge.value))

    #recieves a recomendation from the IoTEngine and displays on IoTDisplay
    @app.route("/operator/trip", methods=["POST"])
    def get_rec():
        speed = request.form['speed']
        return op_disp.display_warning(speed)

    #renders technician display view
    @app.route("/technician", methods=["GET"])
    def display_tech():
        return render_template("technician.html")

    #renders technician display log
    @app.route("/technician/log", methods=["POST"])
    def tech_log():
        return tech_disp.log()

    #renders technician option to update software
    @app.route("/technician/update", methods=["POST"])
    def tech_update():
        return tech_disp.update()

    
if __name__ == '__main__':
    op_disp = Display("operator")
    tech_disp = Display("technician")
    app.run("0.0.0.0", "3000", debug=True)
