const blogsContainer = document.querySelector(".blogs-container");
let masonryItems = document.querySelectorAll(".masonry-item");
let previousScreenSize = window.innerWidth;
let likeButtons = document.querySelectorAll(".like-button");
let searchField = document.querySelector(".search-field");
let searchCancelBtn = document.querySelector(".reset-search");
let searchClearBtn = document.querySelector(".clear-search");

// Masonry layout on home page
// window.onload = () => {
//     const grid = document.querySelector(".grid");
//     const masonry = new Masonry(grid, {
//         itemSelector: ".masonry-item",
//         horizontalOrder: true,
//         fitWidth: true,
//         gutter: 15,
//         transitionDuration: ".5s",
//     });
// };

window.addEventListener("load", () => {
    const masonry = new Masonry(blogsContainer, {
        itemSelector: ".masonry-item",
        horizontalOrder: true,
        fitWidth: true,
        gutter: 15,
        transitionDuration: ".5s",
    });
})

window.addEventListener("resize", () => {
    const computedStyle = getComputedStyle(blogsContainer);
    const paddings =
        parseFloat(computedStyle.paddingLeft) +
        parseFloat(computedStyle.paddingRight);

    if (window.innerWidth < 600 && previousScreenSize >= 600) {
        masonryItems[i].style.width = `${
            blogsContainer.offsetWidth / 2 - paddings
        }px`;
    } else if (
        window.innerWidth >= 600 &&
        window.innerWidth < 1000 &&
        (previousScreenSize < 600 || previousScreenSize >= 1000)
    ) {
        masonryItems[i].style.width = `${
            blogsContainer.offsetWidth / 3 - paddings
        }px`;
    } else if (
        window.innerWidth >= 1000 &&
        window.innerWidth < 1600 &&
        (previousScreenSize < 1000 || previousScreenSize >= 1600)
    ) {
        masonryItems[i].style.width = `${
            blogsContainer.offsetWidth / 5 - paddings
        }px`;
    } else if (
        window.innerWidth >= 1600 &&
        window.innerWidth <= 1920 &&
        (previousScreenSize < 1600 || previousScreenSize >= 1920)
    ) {
        masonryItems[i].style.width = `${
            blogsContainer.offsetWidth / 6 - paddings
        }px`;
    } else {
        masonryItems[i].style.width = `${
            blogsContainer.offsetWidth / 7 - paddings
        }px`
    }

    previousScreenSize = window.innerWidth;
});

function initialMasonryTileSizes() {
    const computedStyle = getComputedStyle(blogsContainer);
    const paddings =
        parseFloat(computedStyle.paddingLeft) +
        parseFloat(computedStyle.paddingRight);

    for (let i = 0; i < masonryItems.length; i++) {
        if (window.innerWidth < 600) {
            masonryItems[i].style.width = `${
                blogsContainer.offsetWidth / 2 - paddings
            }px`;
        } else if (window.innerWidth >= 600 && window.innerWidth < 1000) {
            masonryItems[i].style.width = `${
                blogsContainer.offsetWidth / 3 - paddings
            }px`;
        } else if (window.innerWidth >= 1000 && window.innerWidth < 1600) {
            masonryItems[i].style.width = `${
                blogsContainer.offsetWidth / 5 - paddings
            }px`;
        } else if (window.innerWidth >= 1600 && window.innerWidth <= 1920) {
            masonryItems[i].style.width = `${
                blogsContainer.offsetWidth / 6 - paddings
            }px`;
        } else if (window.innerWidth > 1920) {
            masonryItems[i].style.width = `${
                blogsContainer.offsetWidth / 7 - paddings
            }px`
        }
    }
}

initialMasonryTileSizes();

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
    searchField.value = "";
});
