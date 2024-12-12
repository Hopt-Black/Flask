from flask import Flask, request, render_template

app = Flask(__name__)

# login処理
@app.route('/', methods = ['GET', 'POST'])
def form():
    #2回目以降データが送られてきた時の処理
    if request.method == 'POST':
        print('POSTされたIDは？' + str(request.form['id']))
        print('POSTされたPASSWORDは？' + str(request.form['pwd']))
        return render_template('form.html')
    #１回目のデータが何も送られてこなかった時の処理
    else:
        return render_template('form.html')

#アプリケーションを動かすための
if __name__ == '__main__':
    app.run(port = 8000, debug = True)