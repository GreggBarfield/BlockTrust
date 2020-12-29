export class CoreModal {
    /**
     * Constructs the core modal.
     * 
     * @param {boolean} [wide] Whether to make the modal wide. Default false
     */
    constructor(wide=false) {
        this.visible = false;
        this.modalBackdrop = document.createElement("div");
        this.modalBackdrop.className = "modal-backdrop fade show";
        document.body.append(this.modalBackdrop);

        this.modal = document.createElement("div");
        this.modal.className = "modal fade show";
        this.modal.style = "display:block";
        this.modal.style.overflowY = "scroll";
        document.body.append(this.modal);

        // Todo: implement wide
        
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
