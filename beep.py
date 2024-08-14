import numpy as np
import pyaudio
import matplotlib.pyplot as plt

class BeepEngine:
  def __init__(self, samplingrate=44100, duration = 1/3, freq = 1000) -> None:   
    period = 1.0 / freq
    total_time = int(np.ceil(duration / period)) * period 
    t = np.linspace(0, total_time, int(samplingrate * total_time), endpoint=False)
    
    self.wave = 0.5 * np.sin(2 * np.pi * freq * t)
    self.calm = np.zeros(t.size)
    
    plt.plot(self.wave)
    plt.show()
    
    p = pyaudio.PyAudio()
    self.stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=samplingrate,
                output=True)
  
  def close(self):
    self.stream.close()
  
  def __call__(self, code=".-."):
    for char in code:
      if char ==  ".":
        self.stream.write(self.wave.astype(np.float32).tobytes())
        self.stream.write(self.calm.astype(np.float32).tobytes())
      if char ==  "-":
        self.stream.write(self.wave.astype(np.float32).tobytes())
        self.stream.write(self.wave.astype(np.float32).tobytes())
        self.stream.write(self.wave.astype(np.float32).tobytes())
        self.stream.write(self.calm.astype(np.float32).tobytes())
  
if __name__ == "__main__":
  engine = BeepEngine(duration=1/12, freq=320)
  engine(".-.")
  engine.close()
  