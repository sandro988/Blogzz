const blogsContainer = document.querySelector(".blogs-container");
let previousScreenSize = window.innerWidth;
let likeButtons = document.querySelectorAll(".like-button");
let searchField = document.querySelector(".search-field");
let searchCancelBtn = document.querySelector(".reset-search");
let searchClearBtn = document.querySelector(".clear-search");

// Masonry layout on home page

window.addEventListener("resize", () => {
    if (window.innerWidth < 600 && previousScreenSize >= 600) {
        blogsContainer.style.columns = "2";
    } else if (
        window.innerWidth >= 600 &&
        window.innerWidth < 1000 &&
        (previousScreenSize < 600 || previousScreenSize >= 1000)
    ) {
        blogsContainer.style.columns = "3";
    } else if (
        window.innerWidth >= 1000 &&
        window.innerWidth < 1600 &&
        (previousScreenSize < 1000 || previousScreenSize >= 1600)
    ) {
        blogsContainer.style.columns = "5";
    } else if (
        window.innerWidth >= 1600 &&
        window.innerWidth <= 1920 &&
        (previousScreenSize < 1600 || previousScreenSize >= 1920)
    ) {
        blogsContainer.style.columns = "6";
    } else if (window.innerWidth > 1920 && previousScreenSize <= 1920) {
        blogsContainer.style.columns = "7";
    }

    previousScreenSize = window.innerWidth;
});

function initialMasonry() {
    if (window.innerWidth < 600) {
        blogsContainer.style.columns = "2";
    } else if (window.innerWidth >= 600 && window.innerWidth < 1000) {
        blogsContainer.style.columns = "3";
    } else if (window.innerWidth >= 1000 && window.innerWidth < 1600) {
        blogsContainer.style.columns = "5";
    } else if (window.innerWidth >= 1600 && window.innerWidth <= 1920) {
        blogsContainer.style.columns = "6";
    } else {
        blogsContainer.style.columns = "7";
    }
}

initialMasonry();

// Animation on click of a like button

for (let i = 0; i < likeButtons.length; i++) {
    likeButtons[i].addEventListener("click", () => {
        let heart = likeButtons[i];
        if (!heart.classList.contains("heart-active")) {
            heart.classList.add("heart-active");
            heart.style.transform = "scale(0.5)";
            setTimeout(() => {
                heart.style.transform = "scale(1.5)";
                setTimeout(() => {
                    heart.style.transform = "scale(1)";
                }, "150");
            }, "150");
        } else {
            heart.classList.remove("heart-active");
        }
    });
}

// 1) Making cancel button active whenever the search field is active
// This works on mobile and tabled devices only
// 2) Making clear button active whenever the search field is active
// This works on every device

searchField.addEventListener("focus", () => {
    searchCancelBtn.classList.add("reset-search-active");
});

searchField.addEventListener("blur", () => {
    searchCancelBtn.classList.remove("reset-search-active");
    searchClearBtn.classList.remove("clear-search-active");
    searchField.value = "";
});

searchField.addEventListener("input", (event) => {
    if (event.target.value !== "") {
        searchClearBtn.classList.add("clear-search-active");
    } else {
        searchClearBtn.classList.remove("clear-search-active");
    }
});

searchClearBtn.addEventListener("click", () => {
    searchField.value = ""
})
