const form = document.querySelector(".add-word-form");
const wordList = document.querySelector(".words-container");


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

        const word = document.createElement("p");
        word.setAttribute("class", "words-container__word-text");
        word.innerHTML = sentData.get("word");
        word.setAttribute("data-id", `${data["wordId"]}`);

        const buttons = document.getElementById("buttons").cloneNode(true);
        buttons.setAttribute("style", "");

        const translation = document.createElement("p");
        translation.setAttribute("class", "words-container__word-translation");
        translation.innerHTML = data["translation"];

        const div = document.createElement("div");
        div.setAttribute("class", "words-container__word");
        div.appendChild(word);
        div.appendChild(translation);
        div.appendChild(buttons);
        
        wordList.appendChild(div);

        document.querySelector(".add-word-form__input").value = "";

      } else {
        console.log("Failure");
      }
  });
})


wordList.addEventListener("click", event => {
  console.log("hello")
  console.log(event.target)
  if (event.target.classList.contains("words-container__svg-remove")) {
    console.log("works");
    console.log(event.target.parentElement)
    const wordId = +event.target.parentElement.parentElement.parentElement.querySelector(".words-container__word-text").getAttribute("data-id");
    fetch(`http://127.0.0.1:5000/words/${wordId}`, {method: "DELETE"})
    .then(response => response.json())
    .then(data => {
      console.log(data["result"]);
      if (data["result"] === "Success") {
        wordList.removeChild(event.target.parentElement.parentElement.parentElement);
        console.log("Success");
      } else {
        console.log("Failure");
      }
    })
  }
});
