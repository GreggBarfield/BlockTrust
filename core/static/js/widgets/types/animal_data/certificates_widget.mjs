import { Widget } from '../../widget.mjs';

export class CertificatesWidget extends Widget {
    constructor(frame) {
        super(frame);
    }
    initType() {
        this.animal = parseInt(this.frame.getAttribute("data-widget-animal"));
        this.frame.innerHTML = "";
        this.showPDF()
    }
    showPDF(){
        let placeHolder = document.createElement("div");
        placeHolder.textContent="placeholder";
        this.frame.append(placeHolder)
    }
}