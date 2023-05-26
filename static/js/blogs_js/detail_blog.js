let blogOptionsBtn = document.querySelector(".blog-options-div-trigger");

function eventListenerForBlogOptionButtons() {
    blogOptionsBtn.addEventListener("click", function () {
        console.log("yes");
        let blogOptionsDiv = document.querySelector(
            `.options-div-id-${this.classList[1]}`
        );

        blogOptionsDiv.classList.add("blog-options-div-buttons-active");
        console.log(blogOptionsDiv.classList);
    });
}

eventListenerForBlogOptionButtons();
