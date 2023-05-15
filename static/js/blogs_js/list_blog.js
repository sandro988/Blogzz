const blogsContainer = document.querySelector(".blogs-container");
const infiniteScrollUrl = "/home/?page=";
let masonryBlogsLoader = document.querySelector(".masonry-blog-loader");
let loadingIndicator = document.querySelector(
    ".masonry-blog-loader-infinite-scroll"
);
let masonry;
let blogThumbnailImages = document.querySelectorAll(".blog-thumbnail-img");
let masonryItems = document.querySelectorAll(".masonry-item");

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
            return blogsContainer.offsetWidth / 7 - paddings - 10;
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

function onAlways() {
    setTimeout(() => {
        loadingIndicator.style.display = "none";
    }, "500");
    masonryBlogsLoader.style.display = "none";
    blogsContainer.classList.remove("is-loading");

    initialMasonryTileSizes();
    masonry = new Masonry(blogsContainer, {
        itemSelector: ".masonry-item",
        horizontalOrder: true,
        fitWidth: true,
        gutter: 20,
        transitionDuration: ".5s",
        columnWidth: initialMasonryColumnSizes(),
        stagger: 30,
    });
}

window.addEventListener("load", () => {
    let loadThumbnails = imagesLoaded(blogThumbnailImages);

    blogsContainer.classList.add("is-loading");
    masonryBlogsLoader.style.display = "flex";
    loadingIndicator.style.display = "none";

    loadThumbnails.on("done", onAlways);
});

document.addEventListener("htmx:beforeRequest", (e) => {
    // In this event listener we are checking if the url where the HTMX request was sent starts with '/home/?page='
    // and if it is we will show the loader and after the masonry is initialized with new blogs we hide the loader.
    let GETRequest = e.target.getAttribute("hx-get");

    if (GETRequest && GETRequest.startsWith(infiniteScrollUrl)) {
        loadingIndicator.style.display = "flex";
    }
});
