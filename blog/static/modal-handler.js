/*
This modal handler will only work with one image per page as it handles them by ID.
Class-level modal handlers may be used to handle multiple images per page
*/
let modal = document.getElementById("modalID");

/*
Get the image, the alt text and use the image as the modal
content and the alt-text as the caption
*/
let img = document.getElementById("modalImg");
let modalImg = document.getElementById("imgID");
let captionText = document.getElementById("caption");
// Trigger event when user clicks on image
img.onclick = function () {
  modal.style.display = "block";
  modalImg.src = this.src;
  captionText.innerHTML = this.alt;
};

// Get the span element that closes the modal
let span = document.getElementsByClassName("close")[0]; // Class type access, just to show how.

// Switch state of modal to none when user clicks on (x)
span.onclick = function () {
  modal.style.display = "none";
};