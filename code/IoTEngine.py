import TSNR as tsnr
from urllib.request import urlopen, URLError
import time

class IoTEngine:
  #constructor to declare attributes of IoTEngine
  def __init__(self):
    self.recs = []
    self.my_tsnr = tsnr.TSNR()
    self.prev_obj_pos = 0
    self.prev_obj_spd = -1

  #Logic that determines display message for rain gauge
  def rain_gauge_rec(self, reading, speed):
    speed = int(speed)
    reading = float(reading)
    if(speed <= 20):
      return ['ok', 'no hazard detected']
    elif(speed > 20 and speed <= 40):
      if(reading < 0.6):
        return ['ok', 'no hazard detected']
      else:
        return ['warning', 'reduce speed to 20 MPH']
    else:
      if(reading < 0.3):
        return  ['ok', 'no hazard detected']
      elif(reading < 0.6):
        return ['hazard', 'reduce speed to 40 MPH']
      else:
        return ['warning', 'reduce speed to 20 MPH']

  #Logic that determines display message for anemometer readings
  def anemometer_rec(self, reading, speed):
    speed = int(speed)
    reading = float(reading)
    if(speed <= 20):
      return ['ok', 'no hazard detected']
    elif(speed > 20 and speed <= 40):
      if(reading < 65):
        return ['ok', 'no hazard detected']
      else:
        return ['warning', 'reduce speed to 20 MPH']
    else:
      if(reading < 45):
        return ['ok', 'no hazard detected']
      elif(reading < 65):
        return ['hazard', 'reduce speed to 40 MPH']
      else:
        return ['warning', 'reduce speed to 20 MPH']

  #Logic that determines display message for wheel slippage
  def wheel_slip_rec(self, reading, speed):
    speed = int(speed)
    reading = float(reading)
    if(speed <= 20):
      return ['ok', 'no hazard detected']
    elif(speed > 20 and speed <= 40):
      if(reading < 50):
        return ['ok', 'no hazard detected']
      else:
        return ['warning', 'reduce speed to 20 MPH']
    else:
      if(reading < 20):
        return ['ok', 'no hazard detected']
      elif(reading < 50):
        return ['hazard', 'reduce speed to 40 MPH']
      else:
        return ['warning', 'reduce speed to 20 MPH']

  #Logic that determines display message for detection of a moving/stat object
  def moving_stat_obj_rec(self, reading, speed):
    speed = int(speed)
    reading = float(reading)
    if(reading <= 0):
      self.prev_obj_spd = -1
      self.prev_obj_pos = 0
      return ['ok', 'no hazard detected', 'ok', 'no hazard detected']
    if(self.prev_obj_pos == 0):
      self.prev_obj_pos = reading
      return ['hazard', 'potential hazard detected', 'hazard', 'potential hazard detected']
    if(self.prev_obj_spd == -1):
      self.prev_obj_spd = self.prev_obj_pos - reading
      self.prev_obj_pos = reading
      return ['hazard', 'potential hazard detected', 'hazard', 'potential hazard detected']
    if(speed != 0):
      if(self.prev_obj_pos == reading):
        self.prev_obj_spd = self.prev_obj_pos - reading
        self.prev_obj_pos = reading
        return ['warning', 'moving object detected', 'ok', 'no hazard detected']
      self.prev_obj_spd = self.prev_obj_pos - reading
      self.prev_obj_pos = reading
      return ['ok', 'no hazard detected', 'warning', 'stationary object detected']
    if(reading != self.prev_obj_pos):
      self.prev_obj_spd = self.prev_obj_pos - reading
      self.prev_obj_pos = reading
      return ['warning', 'moving object detected', 'ok', 'no hazard detected']
    self.prev_obj_spd = self.prev_obj_pos - reading
    self.prev_obj_pos = reading
    return ['ok', 'no hazard detected', 'warning', 'stationary object detected']

  #Logic that determines display message for an open/closed gate
  def gate_rec(self, reading, speed):
    speed = int(speed)
    reading = float(reading)
    if(reading == 0):
      return ['ok', 'no hazard detected']
    if(reading < 0):
      return ['hazard', 'Honk the horn']
    return['warning', 'Stop the train! Reduce speed to 0 MPH'] 

  #Logic that determines display message
  def rec_to_display(self, speed):
    speed = int(speed)
    if(self.recs[11] == "hazard"):
      return ["0", "Honk the Horn!"]
    if(speed == 0 and self.recs[11] == "warning"):
      return ["0", "Honk the Horn!"]
    if(speed > 0 and (self.recs[7] == "warning" or self.recs[9] == "warning" or self.recs[11] == "warning")):
      return ["0", "Stop the train"]
    if(speed > 20 and (self.recs[1] == "warning" or self.recs[3] == "warning" or self.recs[5] == "warning")):
      return ["20", "Slow the train to 20 MPH or less"]
    if(speed > 40 and (self.recs[1] == "hazard" or self.recs[3] == "hazard" or self.recs[5] == "hazard")):
      return ["40", "Slow the train to 40 MPH or less"]
    
    return ["0", "---No Suggestion---"]

  #Collects suggestions from prior functions
  def get_suggestion(self, speed):
    data = self.my_tsnr.send_data()
    # data = values for the following sensors [rain,wind,wheel,radar,camera]
    self.recs = [speed] + \
      self.rain_gauge_rec(data[0], speed) + \
      self.anemometer_rec(data[1], speed) + \
      self.wheel_slip_rec(data[2], speed) + \
      self.moving_stat_obj_rec(data[3], speed) + \
      self.gate_rec(data[4], speed) + \
      data
    self.recs += self.rec_to_display(speed)
    file1 = open("LogFile.txt", "a")  # append mode
    file1.write(str(self.recs)+ "\n")
    file1.close()
    return self.recs

  #check if internet connection is available
  def internet_available(self):
    try:
        urlopen('http://216.58.192.142', timeout=1)
        return True
    except URLError as err: 
        return False

  #sends sensor data to log file
  def save_log_to_cloud(self):
    if(self.internet_available()):
      f = open('LogFile.txt', 'r+')
      g = open('CloudLog.txt', 'a')
      g.write(f.read())
      f.truncate(0)
      f.close()
      g.close()
      return "Successfully uploaded to Cloud Log."
    return "No Internet Connection. Cannot upload to Cloud Log."

  #updates IoT engine
  def update_iot_engine(self):
    if(self.internet_available()):
      time.sleep(3)
      return "IoT Engine up to date."
    return "No Internet Connection. Cannot update IoT Engine."

if __name__ == "__main__":
  pass
