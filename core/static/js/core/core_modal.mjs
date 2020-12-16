export class CoreModal {
    constructor() {
        this.visible = false;
        this.modalBackdrop = document.createElement("div");
        this.modalBackdrop.className = "modal-backdrop fade show";
        document.body.append(this.modalBackdrop);

        this.modal = document.createElement("div");
        this.modal.className = "modal fade show";
        this.modal.style = "display:block";
        document.body.append(this.modal);
        
        this.modalDialog = document.createElement("div");
        this.modalDialog.className = "modal-dialog";
        this.modal.append(this.modalDialog);

        this.modalContent = document.createElement("div");
        this.modalContent.className = "modal-content";
        this.modalDialog.append(this.modalContent);

        this.closedPromise = new Promise((resolve)=>{this.closedPromiseResolve=resolve;});
    }

    close() {
        let that = this;
        this.modal.classList.remove("show");
        this.modalBackdrop.classList.remove("show");
        setTimeout(()=>{
            that.modal.remove();
            that.modalBackdrop.remove();
            this.closedPromiseResolve();
        }, 100);
        return this.closedPromise;
    }
}
