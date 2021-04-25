import Sensors as sensors

class TSNR:
  #constructor to declare TSNR attributes
  def __init__(self):
    self.RainGauge = sensors.Sensor("raingauge",4)
    self.Anemometer = sensors.Sensor("anemometer",3)
    self.WheelSlippage = sensors.Sensor("wheelslippage",8)
    self.Radar = sensors.Sensor("radar",9)
    self.Camera = sensors.Sensor("camera",2)

  #sends data from sensors
  def send_data(self):
    return [
        self.RainGauge.get_reading(),
        self.Anemometer.get_reading(),
        self.WheelSlippage.get_reading(),
        self.Radar.get_reading(),
        self.Camera.get_reading()
    ]
