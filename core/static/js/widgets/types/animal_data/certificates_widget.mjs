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
            {
                request: {
                    type: 'matches_by_eids',
                    params: {
                        eids: [this.animal],
                        ljoin_account_links: true,
                        types: ["Medical","Weaned","First Birth"]
                    }
                }
            }
        ).then((data)=>
        {
            this.data=data;
            console.log(data)
            this.showPDF();
        })
        
    }
    showPDF(){
        let placeHolder = document.createElement("div");
        placeHolder.style="width: 450px; height: height:400px;"
        placeHolder.style.height= "100%"
        placeHolder.style.width="100%"
        this.frame.append(placeHolder)

        let pdf = document.createElement("embed");
        pdf.id="plugin"
        pdf.type="application/pdf";
        pdf.style.height= "100%"
        pdf.style.width="100%"
        // ="width: 450px; height: height:400px;"
        pdf.src=this.data;
        placeHolder.append(pdf)
    }
}