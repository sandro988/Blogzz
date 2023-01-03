import {
    map,
    lerp,
    getMousePos,
    calcWinsize,
    getRandomNumber,
} from "../account_js/utils.js";

let winsize = calcWinsize();

window.addEventListener("resize", () => (winsize = calcWinsize()));

// The height of a div with class name "left-side-div" on bigger devices is set to 100vh,
// but on the phone devices when user clicks on the input the height of the entire container
// is calculated by the area that is left above the keyboard, this causes user to not see what they are writing
// so with the code below i set the height of that element to the height of the device, this way the problem 
// mentioned above is solved.
let mobileAuthContainerHeight = document.querySelector(".left-side-div")
mobileAuthContainerHeight.style.height = `${winsize.height}px`

let mousepos = { x: winsize.width / 2, y: winsize.height / 2 };
window.addEventListener("mousemove", (ev) => (mousepos = getMousePos(ev)));

class GridItem {
    constructor(el) {
        this.DOM = { el: el };
        this.move();
    }
    move() {
        let translationVals = { tx: 0, ty: 0, r: 0 };
        const xstart = getRandomNumber(15, 60);
        const ystart = getRandomNumber(30, 90);
        const randR = getRandomNumber(-15, 15);

        const render = () => {
            translationVals.tx = lerp(
                translationVals.tx,
                map(mousepos.x, 0, winsize.width, -xstart, xstart),
                0.07
            );
            translationVals.ty = lerp(
                translationVals.ty,
                map(mousepos.y, 0, winsize.height, -ystart, ystart),
                0.07
            );
            translationVals.r = lerp(
                translationVals.r,
                map(mousepos.x, 0, winsize.width, -randR, randR),
                0.07
            );

            gsap.set(this.DOM.el, {
                x: translationVals.tx,
                y: translationVals.ty,
                rotation: translationVals.r,
            });
            requestAnimationFrame(render);
        };
        requestAnimationFrame(render);
    }
}

export default class Grid {
    constructor(el) {
        this.DOM = { el: el };
        this.gridItems = [];
        this.items = [...this.DOM.el.querySelectorAll(".grid__item")];
        this.items.forEach((item) => this.gridItems.push(new GridItem(item)));

        this.showItems();
    }

    showItems() {
        gsap.timeline()
            .set(this.items, { scale: 0.7, opacity: 0 }, 0)
            .to(
                this.items,
                {
                    duration: 2,
                    ease: "Expo.easeOut",
                    scale: 1,
                    stagger: { amount: 0.6, grid: "auto", from: "center" },
                },
                0
            )
            .to(
                this.items,
                {
                    duration: 3,
                    ease: "Power1.easeOut",
                    opacity: 0.7,
                    stagger: { amount: 0.6, grid: "auto", from: "center" },
                },
                0
            );
    }
}

const grid = new Grid(document.querySelector(".grid"));

// Function for showing alert messages, adding a close button in them and 
// handling the click action on that close button
function alertMessageCloseBtn() {
    let alertMessage = document.querySelectorAll(".errorlist");
    let formFooter = document.querySelector(".form-footer");
    if (alertMessage) {
        for (let i = 0; i < alertMessage.length; i++) {
            // creating button
            let closeBtn = document.createElement("p");

            // adding text and classnames
            closeBtn.textContent = "Close";
            closeBtn.classList.add("form-close-btn");
            formFooter.classList.add("form-footer-relative")

            // appending it to the alert container
            alertMessage[i].appendChild(closeBtn);

            // handling click event on close button
            closeBtn.addEventListener("click", function () {
                alertMessage[i].style.display = "none";
                formFooter.classList.remove("form-footer-relative")
            });
        }
    }
}

alertMessageCloseBtn();
