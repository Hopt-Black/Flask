const cards = document.querySelectorAll(".card");
// ランダムな動きを適用
cards.forEach((card) => {
  card.style.setProperty("--x", (Math.random() * (0.5 - (-0.5)) + (-0.5)).toFixed(2)); // X方向のランダム位置
  card.style.setProperty("--y", (Math.random() * (0.5 - (-0.5)) + (-0.5)).toFixed(2)); // Y方向のランダム位置
  card.style.setProperty("--r", (Math.random() * (0.5 - (-0.5)) + (-0.5)).toFixed(2)); // 回転のランダム性
  //card.style.zIndex = Math.floor(Math.random() * 10); // 初期z-indexを設定
});

// アニメーション終了後に最後のカードを中央に固定
cards[cards.length - 1].addEventListener("animationend", () => {
  cards.forEach((card) => card.classList.remove("final")); // 他のカードからクラスを外す
  cards[cards.length - 1].classList.add("final"); // 最後のカードにクラスを追加
});

// アニメーション中にランダムにz-indexを更新
// setInterval(() => {
//   cards.forEach((card) => {
//     card.style.zIndex = Math.floor(Math.random() * 10); // ランダムz-index
//   });
// }, 2000); // 0.5秒ごとに更新