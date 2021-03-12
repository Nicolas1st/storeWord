const form = document.getElementById("form");
const wordList = document.querySelector("#word-list");

// form.addEventListener("submit", function(e) {
//     e.preventDefault();

//     const formData = new FormData(this);
//     fetch("/words/", {
//         method: "post",
//         body: formData,
//     }).then(response => {
//         return response.text();
//     }).then(text => {
//         console.log(text);
//     }).catch( function(error) {
//         console.log(error);
//     })
// }


form.addEventListener("submit", (e) => {
    e.preventDefault();
    sentData = new FormData(form);
    fetch('http://127.0.0.1:5000/words/' , {
        method: "POST",
        body: sentData,
    })
  .then(response => response.json())
  .then(data => {
      if (data["result"] === "Success") {
        const word = document.createElement("p");
        console.log("Success");
        word.innerHTML = sentData.get("word");
        wordList.appendChild(word);
      } else {
        console.log("Failure");
      }
  });
})