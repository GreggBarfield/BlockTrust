export class SalesGroupViewer {
    constructor(data, attachTo=null) {
        this.frame = null;

        this.box = document.createElement("div");

        if (!"id" in data || !"reported" in data) {
            throw "data incomplete";
        }

        

        if (attachTo !== null)
            this.attach(attachTo);
    }

    attach(frame) {
        if (this.frame !== null) {
            this.detach();
        }
        this.frame = frame;
        this.frame.append(this.box);
    }

    detach() {
        if (this.frame !== null) {
            this.box.remove();
        }
        this.frame = null;
    }


}