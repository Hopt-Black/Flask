from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # AIで生成した文章（ここを生成済みの文章に置き換えてもOK）
    ai_generated_text = "こんにちは！これは1文字ずつ表示するデモだよ～💕"
    return render_template('stream.html', text=ai_generated_text)

if __name__ == '__main__':
    app.run(debug=True)