let commentCreationFormInputField = document.querySelector(".comment-input"); // Main comment form
let commentCreationSuggestionTexts = document.querySelectorAll(".suggestion");
let floatingBoard = document.querySelector(".blogs-page-footer");
let commentOptionsBtn;
let commentDeleteModalContainer = document.querySelector(
    ".comment-delete-modal-div"
);
let commentDeleteBtns; // Delete buttons in options container
let cancelCommentDeletionBtns;
let commentDeleteFormBtns; // Delete buttons in delete form
let commentDeleteOverlay;
let commentShrinkBtns;
let commentShrinkButtonsListenerAdded = false;

// In the comment section there are few suggestion comments, they are just buttons
// that users can click on, after they click them, value of a clicked button
// will be inputted in the comment form and users can submit this new comment,
// basically this suggestions are like shortcuts for creating comments.

commentCreationSuggestionTexts.forEach(function (suggestion) {
    suggestion.addEventListener("click", function () {
        for (let i = 0; i < commentCreationSuggestionTexts.length; i++) {
            let element = commentCreationSuggestionTexts[i];
            if (
                element.classList.contains("chosen-suggestion") &&
                element != suggestion
            ) {
                element.classList.remove("chosen-suggestion");
            }
        }

        // If user has already clicked on a suggestion we
        // should make it white again instead of black and
        // clear the form input.
        // If user clicks on another suggestion or this is their
        // first suggestion choice than we just make the button black and populate the form
        if (suggestion.classList.contains("chosen-suggestion")) {
            suggestion.classList.remove("chosen-suggestion");
            commentCreationFormInputField.value = "";
        } else {
            suggestion.classList.add("chosen-suggestion");
            commentCreationFormInputField.value = suggestion.value;
        }
    });
});

// In comment section there is three dot SVG on each comment, by clicking that user gets a
// container with edit and delete buttons and in this function i am adding event listeners
// to all those SVG's, this function will also be rerun after the successful HTMX request(
// when users edit their comments, delete them, reply and etc).

function eventListenerForOptionButtons() {
    commentOptionsBtn = document.querySelectorAll(
        ".comment-options-div-trigger"
    );

    commentOptionsBtn.forEach(function (btn) {
        btn.addEventListener("click", function () {
            let optionsDiv = document.querySelector(
                `.options-div-id-${this.classList[1]}`
            );
            optionsDiv.classList.add("comment-options-div-buttons-active");
        });
    });
}

// if the container for delete and edit buttons is visible, it should disappear if user clicks
// on any other container on a page other than the ones that have classname of "prevent-propagation"

document.addEventListener("mousedown", (e) => {
    // For comment options container

    if (e.target.classList.contains("prevent-propagation")) {
        e.stopPropagation();
    } else {
        let activeOptions = document.querySelectorAll(
            ".comment-options-div-buttons-active"
        );

        activeOptions.forEach(function (optionDiv) {
            optionDiv.classList.remove("comment-options-div-buttons-active");
        });
    }

    // For comment delete modal

    if (
        e.target.classList.contains("prevent-propagation-for-comment-deletion")
    ) {
        e.stopPropagation();
    } else {
        commentDeleteModalContainer = document.querySelector(
            ".comment-delete-modal-div"
        );

        if (
            commentDeleteModalContainer.classList.contains(
                "comment-delete-modal-div-active"
            )
        ) {
            commentDeleteModalContainer.classList.remove(
                "comment-delete-modal-div-active"
            );
            commentDeleteOverlay.classList.remove(
                "delete-comment-overlay-active"
            );
        }
        commentDeleteModalContainer.replaceChildren();
    }

    // For comment sorting options

    if (
        e.target.classList.contains(
            "prevent-propagation-for-comment-sort-options"
        )
    ) {
        e.stopPropagation;
    } else {
        let commentSortOptions = document.querySelector(".sort-by-form");
        commentSortOptions.classList.remove("sort-by-form-active");
    }
});

function eventListenerForDeleteButtons() {
    commentDeleteModalContainer = document.querySelector(
        ".comment-delete-modal-div"
    );
    commentDeleteBtns = document.querySelectorAll(".delete-comment-btn");
    commentDeleteOverlay = document.querySelector(".delete-comment-overlay");

    commentDeleteBtns.forEach(function (btn) {
        btn.addEventListener("click", function () {
            commentDeleteModalContainer.classList.add(
                "comment-delete-modal-div-active"
            );

            commentDeleteOverlay.classList.add("delete-comment-overlay-active");
        });
    });
}

function eventListenerOnEscapeKey() {
    document.addEventListener("keydown", function (e) {
        if (e.key === "Escape") {
            commentDeleteModalContainer = document.querySelector(
                ".comment-delete-modal-div"
            );

            if (
                commentDeleteModalContainer.classList.contains(
                    "comment-delete-modal-div-active"
                )
            ) {
                commentDeleteModalContainer.classList.remove(
                    "comment-delete-modal-div-active"
                );
                commentDeleteOverlay.classList.remove(
                    "delete-comment-overlay-active"
                );
            }
            commentDeleteModalContainer.replaceChildren();
        }
    });
}

function eventListenerForCommentSortButton() {
    let commentSortBtn = document.querySelector(".sort-by-btn");
    let sortOptions = document.querySelector(".sort-by-form");

    commentSortBtn.addEventListener("click", function () {
        sortOptions = document.querySelector(".sort-by-form");
        sortOptions.classList.toggle("sort-by-form-active");
    });
}

function eventListenerForCommentShrinkButtons() {
    commentShrinkBtns = document.querySelectorAll(".comment-shrink-btn");
    commentShrinkBtns.forEach(function (btn) {
        btn.addEventListener("click", handleCommentShrinkButtonClick);
    });

    commentShrinkButtonsListenerAdded = true;
}

function handleCommentShrinkButtonClick() {
    let comment = this.closest(".reply");
    let childReply = comment.querySelectorAll(".inner-reply");
    let commentMain = comment.querySelector(".comment-main");
    let commentFooter = comment.querySelector(".comment-footer");

    comment.classList.toggle("comment-shrink-btn-active");

    if (childReply) {
        childReply.forEach(function (reply) {
            // Hiding every child replies, a comment can have multiple
            // nested replies, so we should hide all of them if user clicks
            // on the shrink button, not just the first one.
            reply.style.display =
                reply.style.display === "none" ? "block" : "none";
        });
    }

    // Hiding the body of a comment and upvote/downvote/reply buttons
    commentMain.style.display =
        commentMain.style.display === "none" ? "block" : "none";
    commentFooter.style.display =
        commentFooter.style.display === "none" ? "flex" : "none";
}

eventListenerForOptionButtons();
eventListenerForDeleteButtons();
eventListenerOnEscapeKey();
eventListenerForCommentSortButton();
eventListenerForCommentShrinkButtons();
