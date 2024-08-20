info =  {
  "tag": "end",
  "patterns": [
    "(処理|アシスタント|タスク).{0,3}(停止|終了)",
  ],
  "responses": ["execute termination"]
}

def execute():
  return 200