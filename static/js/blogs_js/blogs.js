const blogsContainer = document.querySelector(".blogs-container");
let blogs = document.querySelectorAll(".masonry_item");
let previousScreenSize = window.innerWidth;
let likeButtons = document.querySelectorAll(".like-button");

function masonryGrid(columns, blogs) {
    let columnWrappers = {};
    for (let i = 0; i < columns; i++) {
        columnWrappers[`column${i}`] = [];
    }

    for (let i = 0; i < blogs.length; i++) {
        const column = i % columns;
        columnWrappers[`column${column}`].push(blogs[i]);
    }

    for (let i = 0; i < columns; i++) {
        let columnBlogs = columnWrappers[`column${i}`];
        let div = document.createElement("div");
        div.classList.add("column");

        columnBlogs.forEach((blog) => {
            div.appendChild(blog);
        });

        blogsContainer.appendChild(div);
    }

    let columnDiv = document.querySelectorAll(".column");

    for (let i = 0; i < columnDiv.length; i++) {
        if (columnDiv[i].childNodes.length === 0) {
            columnDiv[i].remove();
        }
    }
}

window.addEventListener("resize", () => {
    if (window.innerWidth < 600 && previousScreenSize >= 600) {
        masonryGrid(2, blogs);
    } else if (
        window.innerWidth >= 600 &&
        window.innerWidth < 1000 &&
        (previousScreenSize < 600 || previousScreenSize >= 1000)
    ) {
        masonryGrid(3, blogs);
    } else if (
        window.innerWidth >= 1000 &&
        window.innerWidth < 1600 &&
        (previousScreenSize < 1000 || previousScreenSize >= 1600)
    ) {
        masonryGrid(5, blogs);
    } else if (
        window.innerWidth >= 1600 &&
        window.innerWidth <= 1920 &&
        (previousScreenSize < 1600 || previousScreenSize >= 1920)
    ) {
        masonryGrid(6, blogs);
    } else if (window.innerWidth > 1920 && previousScreenSize <= 1920) {
        masonryGrid(7, blogs);
    }

    previousScreenSize = window.innerWidth;
});

function initialMasonry() {
    if (window.innerWidth < 600) {
        masonryGrid(2, blogs);
    } else if (window.innerWidth >= 600 && window.innerWidth < 1000) {
        masonryGrid(3, blogs);
    } else if (window.innerWidth >= 1000 && window.innerWidth < 1600) {
        masonryGrid(5, blogs);
    } else if (window.innerWidth >= 1600 && window.innerWidth <= 1920) {
        masonryGrid(6, blogs);
    } else {
        masonryGrid(7, blogs);
    }
}

initialMasonry()


// Animation on click of a like button

for (let i = 0; i < likeButtons.length; i++) {
    console.log(likeButtons[i])
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
    })
}