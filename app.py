from flask import Flask, render_template, request
import google.generativeai as genai

app = Flask(__name__)

#google generative AI (gemini API)のAPIキー設定
genai.configure(api_key='YOUR_API_KEY')
#geminiモデルの設定
model = genai.GenerativeModel("gemini-1.5-flash")

# ルーティング
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods = ['POST'])
def return_result():
    #フォームからPOSTデータを受け取る
    user_str = request.form.get('question')
    response = model.generate_content(user_str)
    return render_template('result.html', result = response.text)



if __name__ == '__main__':
    app.run(port=8000, debug=True)