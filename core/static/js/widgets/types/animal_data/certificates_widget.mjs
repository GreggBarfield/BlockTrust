import { Widget } from '../../widget.mjs';

export class CertificatesWidget extends Widget {
    constructor(frame) {
        super(frame);
    }
    initType() {
        this.animal = parseInt(this.frame.getAttribute("data-widget-animal"));
        this.frame.innerHTML = "";
        this.getData(
            "update_certificates",
            {}
        ).then((data)=>
        {
            this.data=data;
            console.log(data)
            this.showPDF();
        })
        
    }
    showPDF(){
        let placeHolder = document.createElement("div");
        placeHolder.textContent="placeholder";
        this.frame.append(placeHolder)

        let pdf = document.createElement("embed");
        pdf.type="application/pdf";
        pdf.src=this.data;
        placeHolder.append(pdf)
    }
}