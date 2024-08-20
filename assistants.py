import json
import speech_recognition as sr
import pyttsx3
import random
import re
import importlib, glob

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
  def __init__(self) -> None:
    intents_files = glob.glob("./intents/*.py")
    self.intents = []
    for path in intents_files:
      temp = importlib.import_module(path[2:-3].replace("/", "."))
      temp_dict = temp.info
      temp_dict["execute"] = temp.execute
      self.intents.append(temp_dict)
    
    self.wake_words = ["セルピナ"]
    self.intent_labels = list(map(lambda intent:intent["tag"], self.intents))
    self.methods = [method for method in dir(self) if ( callable(getattr(self, method)) and not(method.startswith("__")) and method!="run"  )]
    print(self.methods)

  
  def find_intent(self, intents, key_str):
    """２つの文字列の配列に共通の単語があるかを返す関数"""
    for target_intent in intents:
      patterns = re.compile('|'.join(target_intent["patterns"]))
      if patterns.search(key_str):
        return target_intent
    return False
    
  def send(self, speech):
    wake_word_query = list(filter(lambda word: word in speech, self.wake_words))
    if wake_word_query:
      #ウェイクワード以降の文字列を抽出]
      word = wake_word_query[0]
      text = speech[speech.find(word)+len(word):]

      #コマンドを検索
      intent_related = self.find_intent(self.intents, text)
      print(intent_related)
      
      #対応するコマンドが見つかった場合
      if intent_related:
        responses = intent_related["responses"]
        res = responses[random.randint(0,len(responses)-1)]
        print(res)
        result = intent_related["execute"]()
        return result

      #非対応のコマンドは記録
      else:
        pass
        
if __name__ == "__main__":
  assistant = OBSAssistant()
  while True:
    res = assistant.send(input("入力 >> "))
    if res==200:
      break