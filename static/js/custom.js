document.body.addEventListener('htmx:configRequest', (event) => {
    event.detail.headers['X-CSRFToken'] = '{{ csrf_token }}';
})


// On document load event
document.addEventListener('DOMContentLoaded', function () {


    // Text area resize vertically
    let textareaElems = document.querySelectorAll("textarea.auto-expand");

    textareaElems.forEach((textareaElem) => {
        // Add input event listener to each textarea
        textareaElem.addEventListener("input", function () {
            autoExpand(this);
        });

        window.addEventListener("DOMContentLoaded", (event) => {
            autoExpand(textareaElem);
            textareaElem.removeAttribute("x-cloak"); // you can remove x-cloak after adjusting the height
        });
    });


    // Simple toggle element
    const toggleButtons = document.querySelectorAll(".toggle-normal");

    toggleButtons.forEach((button) => {
        button.addEventListener("click", function () {
            const isChecked = this.getAttribute("aria-checked") === "true";

            // Toggle button classes
            if (isChecked) {
                this.classList.add("toggle-unchecked");
                this.classList.remove("toggle-checked");
            } else {
                this.classList.remove("toggle-unchecked");
                this.classList.add("toggle-checked");
            }

            // Toggle span element classes
            const spanElement = this.querySelector('span[aria-hidden="true"]');
            if (isChecked) {
                spanElement.classList.add("translate-x-0");
                spanElement.classList.remove("translate-x-5");
            } else {
                spanElement.classList.remove("translate-x-0");
                spanElement.classList.add("translate-x-5");
            }

            // Update aria-checked attribute
            this.setAttribute("aria-checked", !isChecked);

            // Update the nested input element's value
            const inputElement = this.querySelector(
                `input[aria-labelledby="${this.id}"]`
            );
            inputElement.value = isChecked ? "false" : "true";
        });
    });


    // Toggle with icon
    // All buttons with the class "toggle-with-icon"
    const toggleWithIconButtons = document.querySelectorAll('.toggle-with-icon');

    toggleWithIconButtons.forEach(button => {
        button.addEventListener('click', function () {
            const isChecked = this.getAttribute('aria-checked') === 'true';

            // Toggle button classes
            if (isChecked) {
                this.classList.add('bg-gray-200');
                this.classList.remove('bg-indigo-600');
            } else {
                this.classList.remove('bg-gray-200');
                this.classList.add('bg-indigo-600');
            }

            // Toggle span element classes (for translate)
            const spanElement = this.querySelector('span.translate-x-0, span.translate-x-5');
            if (isChecked) {
                spanElement.classList.add('translate-x-0');
                spanElement.classList.remove('translate-x-5');
            } else {
                spanElement.classList.remove('translate-x-0');
                spanElement.classList.add('translate-x-5');
            }

            // Toggle SVG icons' visibility
            const svgCross = this.querySelector('span > span[aria-hidden="true"]:first-child');
            const svgCheck = this.querySelector('span > span[aria-hidden="true"]:last-child');

            if (isChecked) {
                svgCross.classList.remove('opacity-0', 'duration-100', 'ease-out');
                svgCross.classList.add('opacity-100', 'duration-200', 'ease-in');

                svgCheck.classList.remove('opacity-100', 'duration-200', 'ease-in');
                svgCheck.classList.add('opacity-0', 'duration-100', 'ease-out');
            } else {
                svgCross.classList.add('opacity-0', 'duration-100', 'ease-out');
                svgCross.classList.remove('opacity-100', 'duration-200', 'ease-in');

                svgCheck.classList.add('opacity-100', 'duration-200', 'ease-in');
                svgCheck.classList.remove('opacity-0', 'duration-100', 'ease-out');
            }

            // Update aria-checked attribute
            this.setAttribute('aria-checked', !isChecked);

            // Update the nested input element's value
            const inputElement = this.querySelector(`input[aria-labelledby="${this.id}"]`);
            inputElement.value = isChecked ? 'false' : 'true';
        });
    });


}, false);


function validateForm(formId) {
    console.log('validateForm()')
    const form = document.getElementById(formId);
    return form.checkValidity();
}

function cropperCropImage(cropperContainer, fileSizeByteLimit, aspectRatio) {
    let cropperProfileContainer = document.getElementById(cropperContainer);
    let cropperInputImage = cropperProfileContainer.querySelector('.cropper-input');
    let cropperInputText = cropperProfileContainer.querySelector('.cropper-input-text');
    let cropperInputContainer = cropperProfileContainer.querySelector('.cropper-input-container');
    let cropperEditCropImage = cropperProfileContainer.querySelector('.crop-image');
    let cropperEditContainer = cropperProfileContainer.querySelector('.cropper-edit-container');
    let cropperCroppedPreview = cropperProfileContainer.querySelector('.cropper-cropped-preview');
    let cropperClose = cropperProfileContainer.querySelectorAll('.cropper-close');
    let cropperErrorMessage = cropperProfileContainer.querySelector('.cropper-error-message');

    // Setup cropper
    cropperInputImage.addEventListener('change', e => {
        if (e.target.files.length) {

            // Check file size
            const fileSize = e.target.files[0].size;
            if (fileSize > fileSizeByteLimit) {
                cropperErrorMessage.innerHTML = 'File size must be 1 MByte or less';
                return;
            } else {
                cropperErrorMessage.innerHTML = '';
            }

            $("#modal-cropper").removeClass('hidden');

            // Start file reader
            const reader = new FileReader();
            reader.onload = e => {
                if (e.target.result) {
                    // Create new image
                    let img = document.createElement('img');
                    img.id = 'image';
                    img.src = e.target.result;

                    // Clean result before
                    cropperEditContainer.innerHTML = '';

                    // Append new image
                    cropperEditContainer.appendChild(img);

                    // Initialize cropper
                    cropper = new Cropper(img, {
                        viewMode: 1,
                        aspectRatio: aspectRatio,
                    });
                }
            };
            reader.readAsDataURL(e.target.files[0]);
        }
    });


    // On crop image save event
    cropperEditCropImage.addEventListener('click', e => {
        e.preventDefault();
        // Get result to data url
        let imgSrc = cropper.getCroppedCanvas().toDataURL();
        cropperCroppedPreview.src = imgSrc;

        // Set file input value to name of the image
        cropperInputText.innerHTML = cropperInputImage.files[0]["name"];

        // Get cropped image data
        cropBoxData = cropper.getCropBoxData()
        cropData = cropper.getData();

        $("#cropper-distance-x").val(cropData['x']);
        $("#cropper-distance-y").val(cropData['y']);
        $("#cropper-width").val(cropData['width']);
        $("#cropper-height").val(cropData['height']);

        // Close modal
        $("#modal-cropper").addClass('hidden');
        $("#cropped-image-preview").removeClass('hidden');

        updateProfilePreview(imgSrc, 'test');
    });

    // Close modal on cancel and exit
    // add an event listener to all the cropperClose elements
    cropperClose.forEach(button => {
        button.addEventListener('click', function () {
            // Get all elements with `cropper-modal` class and add `hidden` class to them
            let cropperModals = document.querySelectorAll('.cropper-modal-container');
            cropperModals.forEach(cropperModal => {
                cropperModal.classList.add('hidden');
            });

            cropperInputImage.value = '';
            cropperInputText.innerHTML = 'Upload an image'
        });
    });

    function updateProfilePreview(imgSrc, username) {
        let preview = document.querySelector('.cropper-cropped-preview');

        if (preview) {
            if (imgSrc) { // If image source exists, create or update <img>
                if (preview.tagName === 'IMG') {
                    preview.src = imgSrc;
                } else {
                    let img = document.createElement('img');
                    img.src = imgSrc;
                    img.classList = 'rounded-full w-12 h-12 cropper-cropped-preview';
                    preview.replaceWith(img);
                }
            } else { // Otherwise, create or update <div>
                if (preview.tagName === 'DIV') {
                    preview.innerHTML = username.charAt(0).toUpperCase();
                } else {
                    let div = document.createElement('div');
                    div.className = 'text-gray-800 h-12 w-12 rounded-full bg-gray-200 flex items-center justify-center font-semibold text-2xl cropper-cropped-preview';
                    div.innerHTML = username.charAt(0).toUpperCase();
                    preview.replaceWith(div);
                }
            }
        }
    }


}

// Textarea auto expand height
function autoExpand(textarea) {
    // Temporarily override display property for calculation
    let originalDisplay = getComputedStyle(textarea).display;
    textarea.style.display = "block";

    textarea.style.height = "auto";
    textarea.style.height = textarea.scrollHeight + "px";

    // Reset back to its original display value
    textarea.style.display = originalDisplay;
}


document.addEventListener("DOMContentLoaded", function () {
    const openModalButtons = document.querySelectorAll("[data-modal-target]");
    const closeModalButtons = document.querySelectorAll("[data-modal-close]");

    openModalButtons.forEach(button => {
        button.addEventListener("click", () => {
            const modal = document.querySelector(button.dataset.modalTarget);
            openModal(modal);
        });
    });

    closeModalButtons.forEach(button => {
        button.addEventListener("click", () => {
            const modal = button.closest(".modal");
            closeModal(modal);
        });
    });

    document.addEventListener("keydown", event => {
        if (event.key === "Escape") {
            const modals = document.querySelectorAll(".modal");
            modals.forEach(modal => {
                closeModal(modal);
            });
        }
    });

    function openModal(modal) {
        if (modal == null) return;
        modal.style.display = "block";
    }

    function closeModal(modal) {
        if (modal == null) return;
        modal.style.display = "none";
    }
});


document.querySelectorAll('[data-copy-url]').forEach(button => {
    button.addEventListener('click', () => {
        navigator.clipboard.writeText(window.location.href)
            .then(() => {
                console.log('URL copied to clipboard');
            })
            .catch(err => {
                console.error('Error in copying URL: ', err);
            });
    });
});