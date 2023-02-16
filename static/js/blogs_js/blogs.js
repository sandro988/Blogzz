let searchField = document.querySelector(".search-field");
let searchCancelBtn = document.querySelector(".reset-search");
let searchClearBtn = document.querySelector(".clear-search");
let searchDropdown = document.querySelector(".search-dropdown-container");
let searchOverlay = document.querySelector(".search-overlay");
let floatingBoardSearchBtn = document.querySelector(".floating-board-search");
let blogsPageFooter = document.querySelector(".blogs-page-footer");
let navbarDropdownBtn = document.querySelector(".homepage-navbar-dropdown");
let navbarDropdown = document.querySelector(".navbar-dropdown-container");

// search field and floating board related

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
    blogsPageFooter.style.display = "none";

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
        blogsPageFooter.style.display = "none";
        e.stopPropagation();
    } else {
        unLockScroll();
        searchCancelBtn.classList.remove("reset-search-active");
        searchDropdown.classList.remove("search-dropdown-container-active");
        searchOverlay.classList.remove("search-overlay-active");
        navbarDropdown.classList.remove("navbar-dropdown-container-active");
        blogsPageFooter.style.display = "block";
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
