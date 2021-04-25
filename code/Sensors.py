import csv
import re

class Sensor:
  #constructor to declare attributes of Sensors
  def __init__(self, sensorType, ID):
    self.sensorType = sensorType
    self.ID = ID
    self.value = self.set_value()

  #return sensor type
  def get_sensorType(self):
    return self.sensorType

  #return sensor ID
  def get_ID(self):
    return self.ID

  #returns value from sensor
  def get_value(self):
    return self.value

  #collects sensor readings
  def set_value(self):
    queue = []
    with open('data.csv') as File:
      readFile = csv.reader(File)
      for row in readFile:
        if(self.get_sensorType() == re.sub(r'[^A-Za-z0-9 ]+', '', row[0])):
          queue=row[1:]
    return queue

  #returns most recent sensor reading
  def get_reading(self):
    return self.value.pop(0)


# if __name__ == "__main__":
#   sensor = Sensor("rain_gauge",3)
