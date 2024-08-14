import numpy as np
import pyaudio

# パラメータ設定
samplingrate = 44100  # サンプリングレート（Hz）
freq = 440.0          # 音の周波数（Hz）
duration = 2.0        # 音の長さ（秒）

# 正弦波生成
t = np.linspace(0, duration, int(samplingrate * duration), endpoint=False)
wave = 0.5 * np.sin(2 * np.pi * freq * t)

# PyAudioの設定
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=samplingrate,
                output=True)

# 音を流す
stream.write(wave.astype(np.float32).tobytes())

# ストリームの終了とPyAudioの終了
stream.stop_stream()
stream.close()
p.terminate()
