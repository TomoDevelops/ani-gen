UIFromRanking = document.getElementById("from_ranking");
UINotFromRanking = document.getElementById("not_from_ranking");
UISelect = document.getElementById("my-ranking-select");
UISelectLabel = document.querySelector("label.my-ranking-select");

function remove_hide() {
  UISelect.classList.remove("hide");
  UISelectLabel.classList.remove("hide");
}

function add_hide() {
  UISelect.classList.add("hide");
  UISelectLabel.classList.add("hide");
}

UIFromRanking.addEventListener("click", remove_hide);
UINotFromRanking.addEventListener("click", add_hide);
