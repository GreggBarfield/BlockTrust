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

        let pdf = document.createElement("embed");
        pdf.type="application/x-google-chrome-pdf"
        pdf.src=""
        this.frame.append(pdf)
    }
}