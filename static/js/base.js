// navbar related
let secondLine = document.querySelector(".hamburger-2");
let thirdLine = document.querySelector(".hamburger-3");
let fourthLine = document.querySelector(".hamburger-4");
let navbar = document.querySelector(".navbar");
let leftNavLinks = document.querySelector(".left-links");
let rightNavLinks = document.querySelector(".right-links");
let primaryNavLinks = document.querySelectorAll(".nav-link-primary");
const hamburgerMenu = document.querySelector(".hamburger-div");

// popular topics section related
let popularTopicsContainer = document.querySelector(".blog-topics-container");
let leftSlider = document.querySelector(".left-slider");
let rightSlider = document.querySelector(".right-slider");

// featured blogs section related
let featureBlogsContainer = document.querySelector(
    ".featured-blogs-container-inner"
);
let mainIndicator = document.querySelector(".main-indicator");
let sliderIndicatorColor = document.querySelector(".indicator-middle-line");
let translateXValue = featureBlogsContainer.children[0].style.transform;
let heartDiv = document.querySelectorAll(".likes-div");
let sliderPosition = 0;

// contact section related
let contactSendBtn = document.querySelector(".ph-plane");
let contactCheckBtn = document.querySelector(".ph-check-contact");
let contactSubmitBtn = document.querySelector(".contact-submit");
let contactName = document.getElementById("id_name");
let email = document.getElementById("id_email");
let message = document.getElementById("id_message");
let emailInput = document.getElementById("id_email");
let emailLabel = document.querySelector(".contact-email-class");

// navbar related

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

function lockScroll() {
    // Function for making body element fixed so it wont scroll in the background
    // when user is in the mobile menu.

    document.body.classList.toggle("lock-scroll");
}

hamburgerMenu.addEventListener("click", function () {
    lockScroll();
    if (navbar.classList.contains("burger-clicked")) {
        unshrinkHamburger();
        navbar.classList.remove("burger-clicked");
        leftNavLinks.classList.remove("increase-font");
        leftNavLinks.classList.add("hidden");
        rightNavLinks.classList.add("hidden");

        leftNavLinks.style.display = "none";
        leftNavLinks.style.fontFamily = '"Poppins", sans-serif';
        rightNavLinks.style.display = "none";
    } else {
        shrinkHamburger();
        navbar.classList.add("burger-clicked");
        leftNavLinks.classList.add("increase-font");
        leftNavLinks.classList.remove("hidden");
        rightNavLinks.classList.remove("hidden");

        leftNavLinks.style.display = "flex";
        leftNavLinks.style.fontFamily = '"Limelight", cursive';
        rightNavLinks.style.display = "flex";
    }
});

window.addEventListener("resize", function () {
    if (window.innerWidth > 1100) {
        unshrinkHamburger();
        navbar.classList.remove("burger-clicked");
        leftNavLinks.classList.remove("hidden");
        rightNavLinks.classList.remove("hidden");
        leftNavLinks.classList.remove("increase-font");
        leftNavLinks.style.display = "flex";
        leftNavLinks.style.fontFamily = '"Poppins", sans-serif';
        rightNavLinks.style.display = "flex";
        document.body.classList.remove("lock-scroll");
    } else {
        if (!navbar.classList.contains("burger-clicked")) {
            navbar.classList.remove("burger-clicked");
            leftNavLinks.classList.add("hidden");
            rightNavLinks.classList.add("hidden");
            leftNavLinks.style.display = "none";
            rightNavLinks.style.display = "none";
        }
    }

    returnToStartingPoint();
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
            document.body.classList.remove("lock-scroll");
        }
    });
}

// popular topics section related

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
        { topic: "Architecture", color: "#d0291d" },
        { topic: "Copyrighting", color: "#7860af" },
        { topic: "Literature", color: "#eeae67" },
        { topic: "Sports", color: "#12257f" },
        { topic: "Fitness", color: "#5ff4f3" },
        { topic: "Productivity", color: "#103f35" },
        { topic: "Creativity", color: "#fcc519" },
        { topic: "Leadership", color: "#d29dbe" },
        { topic: "Traveling", color: "#d0291d" },
        { topic: "Tech Industry", color: "#14af83" },
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
createBlogTopics();

// featured blogs section related

function createGradient(param) {
    let gradient = `linear-gradient(to right, #a5c1f0 ${
        (param + 1) * 12.5
    }%, rgba(0, 0, 0, 0) 10%)`;
    sliderIndicatorColor.style.backgroundImage = gradient;
}

function getXfromTrasnlateXvalue(param) {
    if (param.length === 15) {
        return Number(param.slice(11, 12)) * -1;
    } else if (param.length === 18) {
        return Number(param.slice(11, 15)) * -1;
    } else {
        return Number(param.slice(11, 16)) * -1;
    }
}

function returnToStartingPoint() {
    // returns featured blogs section to its starting position when user resizes webpage

    translateXValue = "";
    for (let i = 0; i < featureBlogsContainer.children.length; i++) {
        featureBlogsContainer.children[i].style.transform = translateXValue;
    }
    sliderPosition = 0;
    mainIndicator.innerText = `0${sliderPosition + 1}`;
    createGradient(sliderPosition);
}

rightSlider.addEventListener("click", function () {
    sliderPosition += 1;
    mainIndicator.innerText = `0${sliderPosition + 1}`;

    let widthOfElement = featureBlogsContainer.children[0].offsetWidth + 20;
    createGradient(sliderPosition);

    if (sliderPosition <= 7) {
        let featureBlogsContainer = document.querySelector(
            ".featured-blogs-container-inner"
        );

        if (translateXValue) {
            if (translateXValue.length === 15) {
                translateXValue = `translateX(${
                    Number(translateXValue.slice(11, 12)) - widthOfElement
                }px)`;
            } else if (translateXValue.length === 18) {
                translateXValue = `translateX(${
                    Number(translateXValue.slice(11, 15)) - widthOfElement
                }px)`;
            } else {
                translateXValue = `translateX(${
                    Number(translateXValue.slice(11, 16)) - widthOfElement
                }px)`;
            }
        } else if (!translateXValue) {
            translateXValue = `translateX(-${widthOfElement}px)`;
        }

        for (let i = 0; i < featureBlogsContainer.children.length; i++) {
            featureBlogsContainer.children[i].style.transform = translateXValue;
        }
    } else {
        returnToStartingPoint();
    }
});

leftSlider.addEventListener("click", function () {
    let widthOfElement = featureBlogsContainer.children[0].offsetWidth + 20;

    if (sliderPosition > 0) {
        sliderPosition -= 1;
        createGradient(sliderPosition);
        mainIndicator.innerText = `0${sliderPosition + 1}`;
        let featureBlogsContainer = document.querySelector(
            ".featured-blogs-container-inner"
        );

        if (translateXValue.length === 15) {
            translateXValue = `translateX(${
                Number(translateXValue.slice(11, 12)) + widthOfElement
            }px)`;
        } else if (translateXValue.length === 18) {
            translateXValue = `translateX(${
                Number(translateXValue.slice(11, 15)) + widthOfElement
            }px)`;
        } else {
            translateXValue = `translateX(${
                Number(translateXValue.slice(11, 16)) + widthOfElement
            }px)`;
        }

        for (let i = 0; i < featureBlogsContainer.children.length; i++) {
            featureBlogsContainer.children[i].style.transform = translateXValue;
        }
    } else if (sliderPosition === 0) {
        translateXValue = "";
    }
});

// Heart button animation

for (let i = 0; i < heartDiv.length; i++) {
    heartDiv[i].addEventListener("click", function () {
        heartReaction(heartDiv[i]);
    });
}

function heartReaction(e) {
    let heart = e.children[0];
    let reactionNumber = e.children[1];

    if (!heart.classList.contains("heart-active")) {
        reactionNumber.innerText = String(Number(reactionNumber.innerText) + 1);
        heart.classList.add("heart-active");
        heart.style.transform = "scale(0.5)";
        setTimeout(() => {
            heart.style.transform = "scale(1.75)";
            setTimeout(() => {
                heart.style.transform = "scale(1)";
            }, "150");
        }, "150");
    } else {
        heart.classList.remove("heart-active");
        reactionNumber.innerText -= 1;
    }
}

// contact section related

function handleDjangoMessagesForContactForm() {
    let djangoMessages = document.querySelectorAll(".messages");

    for (let i = 0; i < djangoMessages.length; i++) {
        if (
            djangoMessages[i].classList.contains(
                "has-to-be-removed-immediately"
            )
        ) {
            djangoMessages[i].remove();
        } else {
            djangoMessages[i].style.animation =
                "fadeMessagesInAndOut 5s forwards";
            setTimeout(() => {
                djangoMessages[i].remove();
            }, "3000");
        }
    }
}

function defineEventListeners() {
    // When user subbmtis contact form, the input fields are replaced with new
    // elements, that have the same id and classes, but they are not the same objects
    // that we initially referenced at the top of this file when creating the variables.
    // because of that when user tries to submit the form for the second time the event listeners
    // for floating labels and subbmit button do not work, to solve this i created this function
    // that will be reexecuted after the htmx request has completed in the event listener that
    // is triggered by htmx:afterRequest event, basically when the HTMX request is completed

    emailInput.addEventListener("input", function () {
        if (emailInput.value) {
            emailLabel.classList.add("floating-label");
        }
    });

    emailInput.addEventListener("focus", function () {
        emailLabel.classList.add("floating-label");
    });

    emailInput.addEventListener("blur", function () {
        if (!emailInput.value) {
            emailLabel.classList.remove("floating-label");
        }
    });

    contactSubmitBtn.addEventListener("click", function () {
        contactName = document.getElementById("id_name");
        email = document.getElementById("id_email");
        message = document.getElementById("id_message");

        if (contactName.value && email.value && message.value) {
            contactSendBtn.style.color = "white";
            contactSendBtn.children[0].style.stroke = "white";
            contactSendBtn.children[1].style.stroke = "white";

            setTimeout(() => {
                contactSendBtn.classList.add("hidden");
                contactCheckBtn.classList.remove("hidden");
                contactCheckBtn.style.backgroundColor = "#afd7b6";
                setTimeout(() => {
                    contactCheckBtn.classList.add("hidden");
                    contactSendBtn.classList.remove("hidden");
                    setTimeout(() => {
                        contactSendBtn.style.backgroundColor = "white";
                        contactSendBtn.children[0].style.stroke = "black";
                        contactSendBtn.children[1].style.stroke = "black";
                    }, "250");
                }, "1000");
            }, "250");
        }
    });

    document.addEventListener("htmx:afterRequest", () => {
        // this event listener will be triggered after an AJAX request has completed
        contactSendBtn = document.querySelector(".ph-plane");
        contactCheckBtn = document.querySelector(".ph-check-contact");
        contactSubmitBtn = document.querySelector(".contact-submit");
        emailInput = document.getElementById("id_email");
        emailLabel = document.querySelector(".contact-email-class");

        handleDjangoMessagesForContactForm()
        defineEventListeners();
    });
}

defineEventListeners();
