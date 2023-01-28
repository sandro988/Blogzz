const blogsContainer = document.querySelector(".blogs-container");
let masonry;
let blogThumbnailImages = document.querySelectorAll(".blog-thumbnail-img");
let masonryItems = document.querySelectorAll(".masonry-item");
let searchField = document.querySelector(".search-field");
let searchCancelBtn = document.querySelector(".reset-search");
let searchClearBtn = document.querySelector(".clear-search");
let searchDropdown = document.querySelector(".search-dropdown-container");
let searchOverlay = document.querySelector(".search-overlay");
let floatingBoardSearchBtn = document.querySelector(".floating-board-search");
let homePageFooter = document.querySelector(".home-page-footer");
let navbarDropdownBtn = document.querySelector(".homepage-navbar-dropdown");
let navbarDropdown = document.querySelector(".navbar-dropdown-container");

// masonry related

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
    let loadThumbnails = imagesLoaded(blogThumbnailImages);

    function onAlways() {
        initialMasonryTileSizes();
        masonry = new Masonry(blogsContainer, {
            itemSelector: ".masonry-item",
            horizontalOrder: true,
            fitWidth: true,
            gutter: 15,
            transitionDuration: ".5s",
            columnWidth: initialMasonryColumnSizes(),
            stagger: 30,
        });
    }

    loadThumbnails.on("done", onAlways);
});

document.addEventListener("htmx:afterRequest", (e) => {
    // handling like button clicks
    if (e.target.closest(".like-button")) {
        let likeBtn = e.target.closest(".like-button");
        likeBtn.classList.toggle("heart-active");
        if (likeBtn.classList.contains("heart-active")) {
            likeBtn.style.animation = "heartActiveAnimation .5s forwards";
        } else {
            likeBtn.style.animation = "none";
        }
        return;
    }

    masonryItems = document.querySelectorAll(".masonry-item");
    blogThumbnailImages = document.querySelectorAll(".blog-thumbnail-img");
    let loadThumbnails = imagesLoaded(blogThumbnailImages);

    function onAlways() {
        initialMasonryTileSizes();
        masonry = new Masonry(blogsContainer, {
            itemSelector: ".masonry-item",
            horizontalOrder: true,
            fitWidth: true,
            gutter: 15,
            transitionDuration: ".5s",
            columnWidth: initialMasonryColumnSizes(),
            stagger: 30,
        });
    }

    loadThumbnails.on("done", onAlways);
});

// search field related

function lockScroll() {
    if (window.innerWidth <= 1100) {
        document.body.classList.add("lock-scroll");
    }
}

function unLockScroll() {
    document.body.classList.remove("lock-scroll");
}

searchField.addEventListener("focus", () => {
    lockScroll();
    searchCancelBtn.classList.add("reset-search-active");
    searchDropdown.classList.add("search-dropdown-container-active");
    searchOverlay.classList.add("search-overlay-active");
    homePageFooter.style.display = "none";

    // if the right nav side dropdown is active and user clicks on a search bar
    // we should remove the right nav side dropdown
    if (navbarDropdown.classList.contains("navbar-dropdown-container-active")) {
        navbarDropdown.classList.remove("navbar-dropdown-container-active");
    }
});

searchField.addEventListener("blur", () => {
    searchClearBtn.classList.remove("clear-search-active");
    searchField.value = "";
});

document.addEventListener("mousedown", (e) => {
    // when user clicks anything other than search field, search button
    // on footer and search dropdown container or its child elements the
    // search drop down should be removed.

    if (
        e.target.classList.contains("prevent-propagation-on-search") ||
        e.target.classList.contains("prevent-propagation-nav-dropdown")
    ) {
        lockScroll();
        searchCancelBtn.classList.add("reset-search-active");
        homePageFooter.style.display = "none";
        e.stopPropagation();
    } else {
        unLockScroll();
        searchCancelBtn.classList.remove("reset-search-active");
        searchDropdown.classList.remove("search-dropdown-container-active");
        searchOverlay.classList.remove("search-overlay-active");
        navbarDropdown.classList.remove("navbar-dropdown-container-active");
        homePageFooter.style.display = "block";
    }
});

floatingBoardSearchBtn.addEventListener("click", () => {
    searchField.focus();
    let dropdownIsActive = searchDropdown.classList.contains(
        "search-dropdown-container-active"
    );
    if (!dropdownIsActive) {
        searchDropdown.classList.add("search-dropdown-container-active");
    }
});

searchField.addEventListener("input", (event) => {
    if (event.target.value !== "") {
        searchClearBtn.classList.add("clear-search-active");
        searchDropdown.classList.add("search-dropdown-container-active");
    } else {
        searchClearBtn.classList.remove("clear-search-active");
    }
});

searchClearBtn.addEventListener("click", () => {
    searchField.value = "";
});

// handling homepage navbar dropdown click event

navbarDropdownBtn.addEventListener("click", () => {
    navbarDropdown.classList.toggle("navbar-dropdown-container-active");
});

// remove dropdown containers when user clicks escape button on keyboard,
// it also removes focus from searchfield with blur().

document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
        if (
            navbarDropdown.classList.contains(
                "navbar-dropdown-container-active"
            ) ||
            searchDropdown.classList.contains(
                "search-dropdown-container-active"
            )
        ) {
            navbarDropdown.classList.remove("navbar-dropdown-container-active");
            searchDropdown.classList.remove("search-dropdown-container-active");
            searchOverlay.classList.remove("search-overlay-active");
            searchField.blur();
        }
    }
});
