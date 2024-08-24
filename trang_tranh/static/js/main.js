const WritingModeSelectorBtn = document.querySelector(".actions__writing-mode-selector");
const WritingModeSelectorDialog = document.querySelector("#writing-mode-selector-dialog");
const CloseWritingModeSelectorDialogBtn = document.querySelector(".close-writing-mode-selector-dialog-btn");
const FormWrapper = document.querySelector(".form-wrapper");
const Form = document.querySelector(".form-wrapper form");
const TextArea = document.querySelector("textarea");
let selectedWritingMode = "h-tb";

const WritingModeChoices = document.querySelectorAll(".writing-mode-choice");

CloseWritingModeSelectorDialogBtn.addEventListener("click", (e) => {
    WritingModeSelectorDialog.close();
})


WritingModeSelectorBtn.addEventListener("click", (e) => {
    WritingModeSelectorDialog.showModal();
})


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
        

        console.log(ChoiceData)
    })
})

TextArea.addEventListener("input", (e) => {
    console.log(TextArea.style.writingMode)
    if (selectedWritingMode == "h-tb") {
        TextArea.style.blockSize = "";
        TextArea.style.blockSize = TextArea.scrollHeight + "px";
    } else {
        TextArea.style.blockSize = "";
        TextArea.style.blockSize = TextArea.scrollWidth + "px";
    }
    
})