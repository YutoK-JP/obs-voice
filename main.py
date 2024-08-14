import os
import speech_recognition as sr
from datetime import datetime
import pyttsx3
import json
import random

def find_intent(intents, key_str):
  """２つの文字列の配列に共通の単語があるかを返す関数"""
  for target_intent in intents:
    patterns = target_intent["patterns"]
    if key_str in patterns:
      return target_intent
  return False

class SpaakEngine:
  def __init__(self) -> None:
    # 初期化オブジェクト
    self.engine = pyttsx3.init()

    #音声リストの取得
    self.voices = self.engine.getProperty('voices')
    self.engine.setProperty('voice', self.voices[1].id)
    self.engine.setProperty('rate', 150)

  def say(self, text):
    self.engine.say(text)
    self.engine.runAndWait()
        
class VoiceRecognizer:
  def __init__(self):
    self.rec = sr.Recognizer()
    self.mic = sr.Microphone()
    self.speech = []

  def grab_audio(self, mes = "listening...") -> sr.AudioData:
    """マイクで音声を受け取る関数

    Returns:
      speech_recognition.AudioData: 音声認識エンジンで受け取った音声データ
    """
    print(mes)
    with self.mic as source:
      self.rec.adjust_for_ambient_noise(source)
      audio = self.rec.listen(source)
    return audio

  def recognize_audio(self, audio: sr.AudioData, mes = "recognizing...") -> str:
    print (mes)
    try:
      speech = self.rec.recognize_google(audio, language='ja-JP')
    except sr.UnknownValueError:
      speech = f"# recognizeing failed"
    except sr.RequestError as e:
      speech = f"# request failed:{e}"
    print(speech)
    return speech

class OBSAssistant:
  def __init__(self, intents_path) -> None:
    self.rec = VoiceRecognizer()
    self.engine = SpaakEngine()
    with open(intents_path) as f:
      raw_intents = json.load(f)
    
    self.wake_words = raw_intents["wakeword"]
    self.intents = raw_intents["intents"]
    self.intent_labels = list(map(lambda intent:intent["tag"], self.intents))
    self.methods = [method for method in dir(self) if ( callable(getattr(self, method)) and not(method.startswith("__")) and method!="run"  )]
    print(self.methods)
    
  def run(self):
    running = True
    #any([word in speech for word in  self.wake_words])
    while running:
      audio = self.rec.grab_audio()
      speech = self.rec.recognize_audio(audio)
      #ウェイクワード検出時
      if any([word in speech for word in self.wake_words]):
        print("wake up")
        continue
        
        #対応するコマンドが見つかった場合
        intent_related = find_intent(self.intents, speech)
        
        if intent_related:
          intent_tag = intent_related["tag"]
          # 終了コマンドの場合のみループ脱出
          if intent_tag == "end":
            responses = intent_related["responses"]
            res = responses[random.randint(0,len(responses)-1)]
            self.engine.say(res)
            
            break
          
          #未実装コマンドの場合はメッセージ送信のみ 
          elif not(intent_tag in self.methods):
            print("Sorry, this method is not implemented. ")
            
          else:
            pass
        #非対応のコマンドは記録
        else:
          pass
      #ウェイクワード非検出時
      else:
        pass

if __name__ == "__main__":
  assistant = OBSAssistant("intents.json")
  assistant.run()