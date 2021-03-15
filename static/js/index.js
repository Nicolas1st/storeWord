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
    