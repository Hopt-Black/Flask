function word(){
    var s = document.getElementById("output").value;//HTMLの入力欄に入力された文字を取得する変数sの宣言
    var len = s.length;//入力された文字の変数sの文字数をカウントする変数lenの宣言
    document.getElementById('output_space').innerHTML=s.slice(0,n);//HTMLのoutput_spaceというidの要素に、変数sの０文字目からn文字までのテキストを表示する
    if(n < len){//文字を増やす処理の回数が入力された文字数を超えるまで繰り返す
      n++;
    } else{//文字を増やす処理の回数が入力された文字数を超えた時の処理
      clearInterval(intervalId);//タイマーをリセットする
      s=null;//変数sを空にする
      }
  }
  //↓関数の宣言↓
  function startTimer(){
    n=1;//nの初期値を1とする
    intervalId=setInterval(word,2000);//2000ミリ秒(2.0秒)ごとにword()関数の処理を実行する
  }