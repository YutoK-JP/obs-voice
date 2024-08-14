import json
import speech_recognition as sr
import pyttsx3

class VoiceRecognizer:
  def __init__(self):
    self.rec = sr.Recognizer()
    self.mic = sr.Microphone()
    self.speech = []

  def grab_audio(self) -> sr.AudioData:
    """マイクで音声を受け取る関数

    Returns:
      speech_recognition.AudioData: 音声認識エンジンで受け取った音声データ
    """
    print("何か話してください...")
    with self.mic as source:
      self.rec.adjust_for_ambient_noise(source)
      audio = self.rec.listen(source)
    return audio

  def recognize_audio(self, audio: sr.AudioData) -> str:
    print ("認識中...")
    try:
      speech = self.rec.recognize_google(audio, language='en-US')
    except sr.UnknownValueError:
      speech = f"#認識できませんでした"
      print(speech)
    except sr.RequestError as e:
      speech = f"#音声認識のリクエストが失敗しました:{e}"
      print(speech)
    return speech

class OBSAssistant:
  def __init__(self, intents_path='intents.json') -> None:
    with open(intents_path) as f:
      raw_intents = json.load(f)
    
    self.wake_words = raw_intents["wakeword"]
    self.intents = raw_intents["intents"]
    print(self.intents)
  
  """def run(self):
    while True:
      audio = self.rec.grab_audio()
      speech = self.rec.recognize_audio(audio)

      if 'hi obs' in speech:
        self.engine.say("hello")
        audio = self.rec.grab_audio()
        cmd = self.rec.recognize_audio(audio)
      else:
        print(speech)"""
        
if __name__ == "__main__":
  assistant = OBSAssistant()