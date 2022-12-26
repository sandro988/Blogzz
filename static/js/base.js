"use strict";

let secondLine = document.querySelector(".hamburger-2");
let thirdLine = document.querySelector(".hamburger-3");
let fourthLine = document.querySelector(".hamburger-4");
let navbar = document.querySelector(".navbar");
let leftNavLinks = document.querySelector(".left-links");
let rightNavLinks = document.querySelector(".right-links");
let primaryNavLinks = document.querySelectorAll(".nav-link-primary");
const hamburgerMenu = document.querySelector(".hamburger-div");

function shrinkHamburger() {
    secondLine.classList.add("shrink-second-line");
    thirdLine.classList.add("shrink-third-line");
    fourthLine.classList.add("shrink-fourth-line");
}
function unshrinkHamburger() {
    secondLine.classList.remove("shrink-second-line");
    thirdLine.classList.remove("shrink-third-line");
    fourthLine.classList.remove("shrink-fourth-line");
}
hamburgerMenu.addEventListener("click", function () {
    if (navbar.classList.contains("burger-clicked")) {
        unshrinkHamburger();
        navbar.classList.remove("burger-clicked");
        leftNavLinks.classList.add("hidden");
        rightNavLinks.classList.add("hidden");

        leftNavLinks.style.display = "none";
        rightNavLinks.style.display = "none";
    } else {
        shrinkHamburger();
        navbar.classList.add("burger-clicked");
        leftNavLinks.classList.remove("hidden");
        rightNavLinks.classList.remove("hidden");

        leftNavLinks.style.display = "flex";
        rightNavLinks.style.display = "flex";
    }
});

window.addEventListener("resize", function () {
    if (window.innerWidth > 1100) {
        unshrinkHamburger();
        navbar.classList.remove("burger-clicked");
        leftNavLinks.classList.remove("hidden");
        rightNavLinks.classList.remove("hidden");
        leftNavLinks.style.display = "flex";
        rightNavLinks.style.display = "flex";
    } else {
        if (!navbar.classList.contains("burger-clicked")) {
            navbar.classList.remove("burger-clicked");
            leftNavLinks.classList.add("hidden");
            rightNavLinks.classList.add("hidden");
            leftNavLinks.style.display = "none";
            rightNavLinks.style.display = "none";
        }
    }
});

for (let i = 0; i < 3; i++) {
    primaryNavLinks[i].addEventListener('click', function () {
        if (navbar.classList.contains("burger-clicked")) {
            unshrinkHamburger();
            navbar.classList.remove("burger-clicked");
            leftNavLinks.classList.add("hidden");
            rightNavLinks.classList.add("hidden");
    
            leftNavLinks.style.display = "none";
            rightNavLinks.style.display = "none";
        } 
    });
}
