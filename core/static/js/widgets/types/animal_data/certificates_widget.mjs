import { Widget } from '../../widget.mjs';

export class CertificatesWidget extends Widget {
    constructor(frame) {
        super(frame);
    }
    initType() {
        this.animal = parseInt(this.frame.getAttribute("data-widget-animal"));
        this.frame.innerHTML = "";
        this.getData(
            "report",
            {
                eid:this.animal
            }
        ).then((data)=>
        {
            this.data=data;
            this.showPDF();
        })
        
    }
    showPDF(){
        let placeHolder = document.createElement("div");
        placeHolder.textContent="placeholder";
        this.frame.append(placeHolder)

        let pdf = document.createElement("embed");
        pdf.type="application/pdf";
        pdf.src="test_output.pdf";
        placeHolder.append(pdf)
    }
}