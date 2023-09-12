document.body.addEventListener('htmx:configRequest', (event) => {
    event.detail.headers['X-CSRFToken'] = '{{ csrf_token }}';
})


// Resize textarea along y-axis to fit content
document.addEventListener('DOMContentLoaded', function () {
    let textareas = document.getElementsByClassName('resize-y-auto');

    function resizeTextarea() {
        this.style.height = 'auto';   // Reset the height
        this.style.height = this.scrollHeight + 'px';  // Set it to its scroll height
    }

    // Apply the resize function to all textarea elements
    for (let i = 0; i < textareas.length; i++) {
        // Resize the textarea whenever text is input
        textareas[i].addEventListener('input', resizeTextarea, false);

        // Initial resize
        resizeTextarea.call(textareas[i]);
    }
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