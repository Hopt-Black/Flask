import random
import google.generativeai as genai

#google generative AI (gemini API)のAPIキー設定
genai.configure(api_key='YOUR_API_KEY')
#geminiモデルの設定
model = genai.GenerativeModel("gemini-1.5-flash")

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

#正位置、逆位置をランダムに選ぶ
def draw_tarot_cards():
    selected_cards = []
    #３枚のカードを引く
    for _ in range(3):
        #１枚目
        position = random.choice(['正位置', '逆位置'])

        #正位置か逆位置を選び、そのカードの意味を選択
        if position == '正位置':
            card_index = random.choice(range(22))
            selected_cards.append((tarot_cards[card_index], '正位置'))
        else:
            card_index = random.choice(range(22))
            selected_cards.append((tarot_cards_reversed[card_index], '逆位置'))
    return selected_cards

# 3枚のカードを引く
selected_cards = draw_tarot_cards()

# 選ばれたカードを表示
print("タロットカード選択の結果:")
for i, (card, position) in enumerate(selected_cards):
    print(f"カード{i+1}: {card} ({position})")

# 現状、アドバイス、最終結果の解釈
current_card = selected_cards[0][0]  # 現状
advice_card = selected_cards[1][0]   # アドバイス
future_card = selected_cards[2][0]   # 最終結果

# プロンプトを作成
prompt = f"転職をすべきかどうかを、現状：'{current_card}'、アドバイスや取るべき行動：'{advice_card}'、最終的な結果や未来の展望：'{future_card}' の解釈で回答してください。"

# AIによる占い結果の生成
response = model.generate_content(prompt)

# 結果を表示
print("占い結果:")
print(response.text)