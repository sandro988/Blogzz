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
let commentSortBtn = document.querySelector(".sort-by-btn");
let sortOptions = document.querySelector(".sort-by-form");

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

// After the comment is submitted the form has to be emptied
// and suggestion buttons should become white again.
document.addEventListener("htmx:afterRequest", (e) => {
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

    // If the HTMX request was initiated by delete button in options container,
    // we add event listeners to delete and cancel buttons in delete form.
    if (e.target.classList.contains("delete-comment-btn")) {
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
    }
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
    commentSortBtn = document.querySelector(".sort-by-btn");
    commentSortBtn.addEventListener("click", function () {
        sortOptions = document.querySelector(".sort-by-form");
        sortOptions.classList.toggle("sort-by-form-active");
    });
}

eventListenerForOptionButtons();
eventListenerForDeleteButtons();
eventListenerOnEscapeKey();
eventListenerForCommentSortButton();
