const NavCreate = document.querySelector(".nav__create");
const body = document.querySelector("body");

NavCreate.addEventListener("click", () => {
    const CreateDialog = document.querySelector(".create-dialog");

    const CloseCreateDialogBtn = document.querySelector(".create-dialog__close-btn");

    CreateDialog.showModal();

    CloseCreateDialogBtn.addEventListener("click", ()=> {
        CreateDialog.close();
    })
})