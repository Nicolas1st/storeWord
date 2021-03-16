const form = document.getElementById("form");
const wordList = document.querySelector("#word-list");


form.addEventListener("submit", (e) => {
    e.preventDefault();
    sentData = new FormData(form);
    if (sentData.get("word") === "") {
      return;
    }
    fetch('http://127.0.0.1:5000/words/' , {
        method: "POST",
        body: sentData,
    })
  .then(response => response.json())
  .then(data => {
      if (data["result"] === "Success") {
        const div = document.createElement("div");

        const word = document.createElement("p");
        word.setAttribute("class", "word__word");
        word.innerHTML = sentData.get("word");
        word.setAttribute("data-id", `${data["wordId"]}`);

        const button = document.createElement("button");
        button.innerHTML = "Remove";
        button.classList.add("word-item__remove-button");

        div.appendChild(word);
        div.appendChild(button);
        div.classList.add("word-item");
        
        wordList.appendChild(div);

        document.querySelector(".form__input").value = "";
      } else {
        console.log("Failure");
      }
  });
})


wordList.addEventListener("click", event => {
  if (event.target.classList.contains("word-item__remove-button")) {
    const wordId = +event.target.parentElement.querySelector(".word__word").getAttribute("data-id");
    fetch(`http://127.0.0.1:5000/words/${wordId}`, {method: "DELETE"})
    .then(response => response.json())
    .then(data => {
      console.log(data["result"]);
      if (data["result"] === "Success") {
        wordList.removeChild(event.target.parentElement);
        console.log("Success");
      } else {
        console.log("Failure");
      }
    })
  }
});
