const WritingModeSelectorBtn = document.querySelector(".actions__writing-mode-selector");
const WritingModeSelectorDialog = document.querySelector("#writing-mode-selector-dialog");
const CloseWritingModeSelectorDialogBtn = document.querySelector(".close-writing-mode-selector-dialog-btn");


CloseWritingModeSelectorDialogBtn.addEventListener("click", (e)=> {
    WritingModeSelectorDialog.close();
})


WritingModeSelectorBtn.addEventListener("click", (e) => {
    WritingModeSelectorDialog.showModal();
})