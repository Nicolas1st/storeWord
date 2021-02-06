let sandwichButton = document.querySelector(".navbar__button")
let links = document.querySelector(".navbar__links")
sandwichButton.addEventListener("click", () => {
    sandwichButton.classList.toggle("navbar__button_open");
    if (links.style.display === "flex") {
        links.style.display = "none";
    } else {
        links.style.display = "flex";
    }
});


let doStuff = document.querySelector("#do-stuff");
doStuff.addEventListener("click", () => {
    let xhr = new XMLHttpRequest();
    xhr.open("GET", 'http://127.0.0.1:5000/word')
    xhr.onload = function() {
        if (this.status == 200) {
            console.log(this.responseText);
        }
    }
    xhr.send();
});
