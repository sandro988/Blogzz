document.addEventListener("htmx:afterRequest", (e) => {
    if (e.target.classList.contains("delete-comment-btn")) {
        // If the HTMX request was initiated by delete button in options container,
        // we add event listeners to 'delete' and 'cancel' buttons in delete form.
        cancelCommentDeletionBtns = document.querySelector(
            ".comment-delete-cancel-btn"
        );
        commentDeleteFormBtns = document.querySelector(
            ".form-comment-delete-btn"
        );

        cancelCommentDeletionBtns.addEventListener("click", function () {
            commentDeleteModalContainer.classList.remove(
                "comment-delete-modal-div-active"
            );
            commentDeleteOverlay.classList.remove(
                "delete-comment-overlay-active"
            );
        });

        commentDeleteFormBtns.addEventListener("click", function () {
            commentDeleteModalContainer.classList.remove(
                "comment-delete-modal-div-active"
            );
            commentDeleteOverlay.classList.remove(
                "delete-comment-overlay-active"
            );
        });
    } else if (e.target.closest(".like-button")) {
        // Handling like button clicks
        let likeBtn = e.target.closest(".like-button");
        likeBtn.classList.toggle("heart-active");
        if (likeBtn.classList.contains("heart-active")) {
            likeBtn.style.animation = "heartActiveAnimation .5s forwards";
        } else {
            likeBtn.style.animation = "none";
        }
        return;
    } else if (e.target.classList.contains("masonry-item")) {
        // Handling infinite scrolling feature on home page.
        masonryItems = document.querySelectorAll(".masonry-item");
        blogThumbnailImages = document.querySelectorAll(".blog-thumbnail-img");
        let loadThumbnails = imagesLoaded(blogThumbnailImages);
        loadThumbnails.on("done", onAlways);
    } else {
        // After the comment is submitted the form has to be emptied
        // and suggestion buttons should become white again.
        commentCreationFormInputField.value = "";
        for (let i = 0; i < commentCreationSuggestionTexts.length; i++) {
            let element = commentCreationSuggestionTexts[i];
            if (element.classList.contains("chosen-suggestion")) {
                element.classList.remove("chosen-suggestion");
            }
        }

        eventListenerForOptionButtons();
        eventListenerForDeleteButtons();
        eventListenerOnEscapeKey();
        eventListenerForCommentShrinkButtons();
    }
});
