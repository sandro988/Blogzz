const blogsContainer = document.querySelector(".blogs-container");
let blogThumbnailImages = document.querySelectorAll(".blog-thumbnail-img")
let masonryItems = document.querySelectorAll(".masonry-item");
let likeButtons = document.querySelectorAll(".like-button");
let searchField = document.querySelector(".search-field");
let searchCancelBtn = document.querySelector(".reset-search");
let searchClearBtn = document.querySelector(".clear-search");
let masonry;

function initialMasonryColumnSizes() {
    const computedStyle = getComputedStyle(blogsContainer);
    const paddings =
        parseFloat(computedStyle.paddingLeft) +
        parseFloat(computedStyle.paddingRight);

    for (let i = 0; i < masonryItems.length; i++) {
        if (window.innerWidth < 600) {
            return blogsContainer.offsetWidth / 2 - paddings;
        } else if (window.innerWidth >= 600 && window.innerWidth < 1000) {
            return blogsContainer.offsetWidth / 3 - paddings;
        } else if (window.innerWidth >= 1000 && window.innerWidth < 1600) {
            return blogsContainer.offsetWidth / 5 - paddings;
        } else if (window.innerWidth >= 1600 && window.innerWidth <= 1920) {
            return blogsContainer.offsetWidth / 6 - paddings;
        } else if (window.innerWidth > 1920) {
            return blogsContainer.offsetWidth / 7 - paddings;
        }
    }
}

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
            }px`;
        }
    }
}

window.addEventListener("load", () => {
    imagesLoaded(blogThumbnailImages, function () {
        initialMasonryTileSizes();
        masonry = new Masonry(blogsContainer, {
            itemSelector: ".masonry-item",
            horizontalOrder: true,
            fitWidth: true,
            gutter: 15,
            transitionDuration: ".5s",
            columnWidth: initialMasonryColumnSizes(),
            stagger: 30
        });
    })
});

document.addEventListener("htmx:afterRequest", () => {
    masonryItems = document.querySelectorAll(".masonry-item");
    initialMasonryTileSizes();
    imagesLoaded(blogThumbnailImages, function () {
        initialMasonryTileSizes();
        masonry = new Masonry(blogsContainer, {
            itemSelector: ".masonry-item",
            horizontalOrder: true,
            fitWidth: true,
            gutter: 15,
            transitionDuration: ".5s",
            columnWidth: initialMasonryColumnSizes(),
            stagger: 30
        });
    })
    
});


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
