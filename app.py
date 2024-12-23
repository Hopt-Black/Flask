from flask import Flask, render_template, request, session, jsonify, send_from_directory
import google.generativeai as genai
import random
import define
# タロットカード一覧とその意味
tarot_cards = [
    "愚者: 新しい始まり、自由、未知への挑戦",
    "魔術師: チャンスの到来、可能性、自己実現",
    "女教皇: 直感、内なる声、秘密",
    "女帝: 豊かさ、成長、育む",
    "皇帝: 安定、支配、秩序",
    "法王: 伝統、助言、精神的成長",
    "恋人: 選択、愛、人間関係",
    "戦車: 勝利、意志力、前進",
    "力: 忍耐、強さ、困難の克服",
    "隠者: 内省、探求、孤独",
    "運命の輪: 運命、転機、チャンス",
    "正義: 公平、バランス、正しい判断",
    "吊るされた男: 忍耐、犠牲、視点の転換",
    "死神: 終わり、新しい始まり、変化",
    "節制: 調和、バランス、穏やかな進展",
    "悪魔: 欲望、束縛、執着",
    "塔: 崩壊、変化、衝撃的な出来事",
    "星: 希望、ひらめき、癒し",
    "月: 不安、迷い、隠された真実",
    "太陽: 幸福、成功、明るい未来",
    "審判: 復活、決断、過去からの解放",
    "世界: 完成、達成、統合"
]

# タロットカード一覧とその意味（逆位置）
tarot_cards_reversed = [
    "愚者: 無計画、軽率、リスク回避",
    "魔術師: 能力不足、未発達、過信",
    "女教皇: 秘密、隠された真実、直感不足",
    "女帝: 不足、成長の停滞、依存",
    "皇帝: 支配過剰、権威主義、安定欠如",
    "法王: 従順すぎる、精神的閉塞、保守的",
    "恋人: 選択の誤り、関係の破綻、愛情不足",
    "戦車: 衝動的、方向感覚の欠如、競争心",
    "力: 弱さ、忍耐不足、感情の乱れ",
    "隠者: 孤立、無視、内省不足",
    "運命の輪: 運命の逆行、チャンスの喪失、混乱",
    "正義: 不公平、バランス欠如、不正",
    "吊るされた男: 無駄な犠牲、視点の欠如、方向転換不足",
    "死神: 変化の拒絶、停滞、過去の囚われ",
    "節制: 不調和、過度な欲望、過剰",
    "悪魔: 自由の欠如、依存、誘惑",
    "塔: 崩壊、ショック、不安定",
    "星: 絶望、期待外れ、夢の喪失",
    "月: 不安、混乱、誤解",
    "太陽: 悲しみ、失敗、迷い",
    "審判: 後悔、過去にとらわれる、再生の欠如",
    "世界: 不完全な達成、進展の停止、結びつきの欠如"
]

app = Flask(__name__, static_folder="./static/")

#セッション用のシークレットキーを設定
app.secret_key = define.APP_SECRET_KEY

#google generative AI (gemini API)のAPIキー設定
genai.configure(api_key=define.YOUR_API_KEY)
#geminiモデルの設定
model = genai.GenerativeModel("gemini-1.5-flash")

# ルーティング
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tarot', methods = ['POST'])
def tarot_select():
    #フォームから相談内容を受け取る
    user_consultation = request.form.get('consultation')
    #セッションスコープに保存
    session['user_consultation'] = user_consultation

    #次のタロットカードのシャッフルの前に1回シャッフルを済ませておく
    generated_numbers = random.sample(range(22), 3)
    #セッションスコープに保存
    session['generated_numbers'] = generated_numbers

    return render_template('tarotSelect.html')

@app.route('/generateTarots')
def generate_tarots():
    generated_numbers = random.sample(range(22), 3)
    session['generated_numbers'] = generated_numbers
    return render_template('tarotSelect.html')

@app.route('/getTarots', methods=['GET'])
def get_tarots():
    consultation_number = session['user_consultation']
    generated_numbers = session['generated_numbers']
    if generated_numbers is not None:
        selected_cards = []
        # 生成された乱数を使ってカードとその意味を取得
        for num in generated_numbers:
            position = random.choice(['正位置', '逆位置'])  # 正位置 or 逆位置をランダムに選択
            if position == '正位置':
                selected_cards.append({"card": tarot_cards[num], "position": "正位置"})
            else:
                selected_cards.append({"card": tarot_cards_reversed[num], "position": "逆位置"})

        # 現状、アドバイス、最終結果の解釈
        current_card = selected_cards[0]["card"]  # 現状
        advice_card = selected_cards[1]["card"]  # アドバイス
        future_card = selected_cards[2]["card"]  # 最終結果

        #格納されているデータ確認
        #t = type(selected_cards[0]["card"])
        #print(t)


        # プロンプトを作成
        #prompt = f"転職をすべきかどうかを、現状：{current_card}、アドバイスや取るべき行動：'{advice_card}'、最終的な結果や未来の展望：'{future_card}' の解釈で回答し、最後にまとめてください（カードの正位置逆位置を明示）。また、各解釈の区切りには<br>を２回、まとめの前には<br>を3回入力してください"
        determine_personality = f"あなたは優しい占い師です"

        if consultation_number == '1':
            prompt_current = f"転職すべきかどうかを、現状を{current_card}の解釈で回答してください。段落ごとに改行を<br>で、200文字程度で"
        elif consultation_number == '2':
            prompt_current = f"職業訓練を受けるべきかどうかを、現状を{current_card}の解釈で回答してください。段落ごとに改行を<br>で、200文字程度で"
        else:
            prompt_current = f"今日の運勢を、現状を{current_card}の解釈で回答してください。段落ごとに改行を<br>で、200文字程度で"

        prompt_advice = f"先ほどの回答を踏まえて、アドバイスや取るべき行動を{advice_card}の解釈で回答してください。段落ごとに改行を<br>で、200文字程度で"
        prompt_future = f"先ほどまでの回答を踏まえて、最終的な結果や未来の展望を{future_card}の解釈で回答してください。段落ごとに改行を<br>で、200文字程度で"

        # AIによる占い結果の生成（履歴保存式）
        #response = model.generate_content(prompt)

        #AIによる占い結果の生成（履歴保存）
        chat = model.start_chat(history=[])
        response_first = chat.send_message(determine_personality)
        response_current = chat.send_message(prompt_current)
        response_advice = chat.send_message(prompt_advice)
        response_future = chat.send_message(prompt_future)

        return render_template('result.html', text_current = response_current.text, text_advice = response_advice.text, text_future = response_future.text, selected_cards = selected_cards)
    else:
        print('乱数が生成されていません')
        return None

if __name__ == '__main__':
    app.run(port=8000, debug=True)