"use strict";

let secondLine = document.querySelector(".hamburger-2");
let thirdLine = document.querySelector(".hamburger-3");
let fourthLine = document.querySelector(".hamburger-4");
let navbar = document.querySelector(".navbar");
let leftNavLinks = document.querySelector(".left-links");
let rightNavLinks = document.querySelector(".right-links");
let primaryNavLinks = document.querySelectorAll(".nav-link-primary");
let popularTopicsContainer = document.querySelector(".blog-topics-container");
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
    primaryNavLinks[i].addEventListener("click", function () {
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

function createBlogTopics() {
    const topicsAndColors = [
        { topic: "Python", color: "#390099" },
        { topic: "JavaScript", color: "#0466C8" },
        { topic: "Self Development", color: "#FF0054" },
        { topic: "UI/UX", color: "#FFBD00" },
        { topic: "Interior Design", color: "#0EAD69" },
        { topic: "Development", color: "#CEC2FF" },
        { topic: "Psychology", color: "#FF5400" },
        { topic: "Science", color: "#09BC8A" },
        { topic: "Rlationships", color: "#FF99C8" },
        { topic: "Music", color: "#70D6FF" },
        { topic: "Artificial Inteligence", color: "#7678ED" },
        { topic: "Finances", color: "#D00000" },
        { topic: "Politics", color: "#2EC6BD" },
        { topic: "Music", color: "#afd7b3" },
        { topic: "History", color: "#a5c1f0" },
        { topic: "Health", color: "#b42f83" },
        { topic: "Art", color: "#fbc5c4" },
        { topic: "Physics", color: "#fce440" },
        { topic: "Networking", color: "#0000b5" },
        { topic: "Education", color: "#b1aae6" },
    ];

    for (let i = 0; i < topicsAndColors.length; i++) {
        let topicContainer = document.createElement("div");
        let colorDiv = document.createElement("div");
        let topicDiv = document.createElement("p");

        topicContainer.classList.add(`topic-container`);
        colorDiv.classList.add("topic-color");
        topicDiv.classList.add("topic-name");

        colorDiv.style.backgroundColor = topicsAndColors[i].color;
        topicDiv.innerText = topicsAndColors[i].topic;

        topicContainer.appendChild(colorDiv);
        topicContainer.appendChild(topicDiv);
        popularTopicsContainer.appendChild(topicContainer);
    }
}

console.log(popularTopicsContainer);
createBlogTopics();
