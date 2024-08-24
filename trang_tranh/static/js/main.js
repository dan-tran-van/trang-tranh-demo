const WritingModeSelectorBtn = document.querySelector(".actions__writing-mode-selector");
const WritingModeSelectorDialog = document.querySelector("#writing-mode-selector-dialog");
const CloseWritingModeSelectorDialogBtn = document.querySelector(".close-writing-mode-selector-dialog-btn");
const FormWrapper = document.querySelector(".form-wrapper");
const Form = document.querySelector(".form-wrapper form");
const TextArea = document.querySelector("textarea");
const PhotoPreview = document.querySelector(".photo-preview");
const AddPhotoBtn = document.querySelector(".post-media-actions__add-photos-btn");
const FileElem = document.querySelector("#id_media");
const PostBtn = document.querySelector(".actions__post");
const SubmitElement = document.querySelector("#form-submit-element");
const PhotoLimitErrorDialog = document.querySelector("#photo-limit-error-dialog");
const PhotoLimitErrorDialogCloseBtn = document.querySelector("#photo-limit-error-dialog-close-btn");
const validImageTypes = ['image/gif', 'image/jpeg', 'image/png'];
const NotImagesErrorDialog = document.querySelector("#not-images-error-dialog");
const NotImagesErrorDialogCloseBtn = document.querySelector("#not-images-error-dialog-close-btn");

window.addEventListener("load", (e) => {
    TextArea.value = '';
    FileElem.value = '';
})

let selectedWritingMode = "h-tb";

const WritingModeChoices = document.querySelectorAll(".writing-mode-choice");

CloseWritingModeSelectorDialogBtn.addEventListener("click", (e) => {
    WritingModeSelectorDialog.close();
});


WritingModeSelectorBtn.addEventListener("click", (e) => {
    WritingModeSelectorDialog.showModal();
});


WritingModeChoices.forEach((Choice) => {
    Choice.addEventListener("click", (e) => {
        const ChoiceData = Choice.getAttribute("data-writing-mode-choice");

        if (FormWrapper.classList.contains(`form-wrapper--${ChoiceData}`)) {
            WritingModeSelectorDialog.close();
        } else {
            FormWrapper.className = '';
            FormWrapper.classList.add("form-wrapper");
            FormWrapper.classList.add(`form-wrapper--${ChoiceData}`);
            Form.className = '';
            Form.classList.add(`form--${ChoiceData}`)
            WritingModeSelectorDialog.close();
            selectedWritingMode = ChoiceData;
        }
    });
});

TextArea.addEventListener("input", (e) => {
    if (selectedWritingMode == "h-tb") {
        TextArea.style.blockSize = "";
        TextArea.style.blockSize = TextArea.scrollHeight + "px";
    } else {
        TextArea.style.blockSize = "";
        TextArea.style.blockSize = TextArea.scrollWidth + "px";
    }

});

AddPhotoBtn.addEventListener("click", (e) => {
    if (FileElem) {
        FileElem.click();
    }
});

FileElem.addEventListener("change", handleFiles);


function handleFiles() {
    PhotoPreview.textContent = "";
    if (this.files.length) {
        if (this.files.length > 10) {
            PhotoLimitErrorDialog.showModal();
            FileElem.value = '';
        } else {
            for (let i = 0; i < this.files.length; i++) {
                if (!validImageTypes.includes(this.files[i]['type'])) {
                    NotImagesErrorDialog.showModal();
                    FileElem.value = '';
                    PhotoPreview.textContent = '';
                    break;
                }
                const img = document.createElement("img");
                img.src = URL.createObjectURL(this.files[i]);
                img.onload = () => {
                    URL.revokeObjectURL(img.src);
            };
            PhotoPreview.appendChild(img);
            }
        }
    }
}

PhotoLimitErrorDialogCloseBtn.addEventListener("click", (e)=> {
    PhotoLimitErrorDialog.close();
})

NotImagesErrorDialogCloseBtn.addEventListener("click", (e)=> {
    NotImagesErrorDialog.close();
})

PostBtn.addEventListener("click", (e)=>{
    SubmitElement.click();
})