import { Widget } from '../../widget.mjs';

const MAX_COL_WIDTH = 15;
const Y_SPACING_VAL = 8;

export class CreateSalesGroupFlyer extends Widget {
    constructor(frame) {
        super(frame);
        this.ySpacer = Y_SPACING_VAL;
    }

    initType() {
        this.frame.innerHTML = "";
        this.salesGroupID = parseInt(this.frame.getAttribute("data-widget-sales-group"));

        this.getData(
            "sales_group",
            {
                sales_group: this.salesGroupID
            }
        ).then((data) => {
            this.data = data;

            if (Object.keys(this.data.reported).length !== 0) {
                this.makeFlyerButton();
            }
        });
    }

    makeFlyerButton() {
        let button = document.createElement("button");
        button.className = "btn btn-outline-secondary btn-sm";
        button.textContent = "Create Flyer";

        let widgetObject = this;
        button.addEventListener("click", ()=>{
            widgetObject.makeFlyer();
        });

        this.frame.appendChild(button);
    }

    async makeFlyer() {
        document.body.style.cursor='wait';
        let pdf = new jsPDF("p", "mm");
        
        const pageWidth = pdf.internal.pageSize.getWidth();
        
        let logo = document.querySelector(".b-header-logo-desktop");
        let logoCanvas = await html2canvas(logo, { 
            scale: 1.5 
        });
        let logoData = logoCanvas.toDataURL('image/png', 1);
        pdf.addImage(logoData, 'PNG', (pageWidth / 2) - 40, 10);
        
        this.createHeaderData(pdf);
        this.createAnimalData(pdf);
        this.createMarketData(pdf);
        this.createFooter(pdf, pageWidth);
        
        pdf.save("MarketTrust Sale.pdf");
        document.body.style.cursor='default';
    }

    createHeaderData(pdf) {
        pdf.setFillColor('white');
        pdf.setDrawColor('gray');
        pdf.roundedRect(10, 40, 90, 25, 5, 5);

        pdf.setFontSize(12);
        pdf.text("Sales Group " + this.data.id, 15, 50);
        pdf.setFontSize(10);
        pdf.text("Location: " + this.data.market_location, 15, 57);
        
        pdf.roundedRect(110, 40, 90, 25, 5, 5);
    }

    createAnimalData(pdf) {
        pdf.roundedRect(10, 70, 90, 120, 5, 5);

        pdf.setFontSize(12);
        pdf.text("Animal Data", 15, 77);
        pdf.line(10, 79, 100, 79);

        let xLabelColumn = 15;
        let xDataColumn = 55;
        let yPlacement = 85;

        pdf.setFontSize(10);
        pdf.text("Breed:", xLabelColumn, yPlacement);
        pdf.text(this.checkData(this.data.reported.breeds.join(', ')), xDataColumn, yPlacement);
        yPlacement += this.ySpacer;
        pdf.text("Base Weight:", xLabelColumn, yPlacement);
        pdf.text(this.checkData(this.data.reported.weight.toString()), xDataColumn, yPlacement);
        yPlacement += this.ySpacer;
        pdf.text("Wt. Variance Frame:", xLabelColumn, yPlacement);
        pdf.text(this.checkData(this.data.reported.weight_variance.toString()), xDataColumn, yPlacement);
        yPlacement += this.ySpacer;
        pdf.text("Horns:", xLabelColumn, yPlacement);
        pdf.text(this.checkData(this.data.reported.horns), xDataColumn, yPlacement);
        yPlacement += this.ySpacer;
        pdf.text("Precon Program:", xLabelColumn, yPlacement);
        pdf.text(this.checkData(this.data.reported.preconditioning_program), xDataColumn, yPlacement);
        yPlacement += this.ySpacer;
        pdf.text("Implants:", xLabelColumn, yPlacement);
        pdf.text(this.checkData(this.data.reported.implants.join(', ')), xDataColumn, yPlacement);
        yPlacement += this.ySpacer;
        pdf.text("Castrated:", xLabelColumn, yPlacement);
        pdf.text(this.checkData(this.data.reported.castrated), xDataColumn, yPlacement);
        yPlacement += this.ySpacer;
        pdf.text("Vaccinations:", xLabelColumn, yPlacement);
        pdf.text(this.checkData(this.data.reported.vaccinations.join(', ')), xDataColumn, yPlacement);
        yPlacement += this.ySpacer;
        pdf.text("Feeding Program:", xLabelColumn, yPlacement);
        pdf.text(this.checkData(this.data.reported.feeding_programs.join(', ')), xDataColumn, yPlacement);
        yPlacement += this.ySpacer;
        pdf.text("PVP Program:", xLabelColumn, yPlacement);
        pdf.text(this.checkData(this.data.reported.process_verified_program), xDataColumn, yPlacement);
    }

    createMarketData(pdf) {
        pdf.roundedRect(110, 70, 90, 60, 5, 5)
        
        pdf.setFontSize(12);
        pdf.text("Market Data", 115, 77);
        pdf.line(110, 79, 200, 79);

        let xLabelColumn = 115;
        let xDataColumn = 160;
        let yPlacement = 85;

        pdf.setFontSize(10);
        pdf.text("Total Count:", xLabelColumn, yPlacement);
        pdf.text(this.checkData(this.data.reported.count.toString()), xDataColumn, yPlacement);
        yPlacement += this.ySpacer;
        pdf.text("Delivery Location:", xLabelColumn, yPlacement);
        pdf.text(this.checkData(this.data.delivery_location), xDataColumn, yPlacement);
        yPlacement += this.ySpacer;
        
        let daysRemaining = "--";
        if ("end" in this.data && this.data.end !== null) {
            let currentEpoch = Date.now() / 1000;
            daysRemaining = Math.floor((this.data.end - currentEpoch) / (60 * 60 * 24));
        }
        let salesDate = new Date(this.data.start * 1000);
        
        pdf.text("Sales Date:", xLabelColumn, yPlacement);
        pdf.text(this.checkData(salesDate.toDateString()), xDataColumn, yPlacement);
        yPlacement += this.ySpacer;
        pdf.text("Days Remaining:", xLabelColumn, yPlacement);
        pdf.text(this.checkData(daysRemaining.toString()), xDataColumn, yPlacement);
    }

    createFooter(pdf, pageWidth) {
        const pageHeight = pdf.internal.pageSize.getHeight();

        pdf.setFontSize(8);
        pdf.setDrawColor('black');
        pdf.line(10, pageHeight - 15, pageWidth - 10, pageHeight - 15);
        pdf.text("BlockTrust Network", 15, pageHeight - 10);
        pdf.text("3511 Longmire, College Station, TX 77845", (pageWidth / 2) - 30, pageHeight - 10);
        pdf.text("info@Blocktrustnetwork.com", pageWidth - 50, pageHeight - 10);
    }

    checkData(dataString) {
        if (dataString == null || dataString == "") {
            this.ySpacer = Y_SPACING_VAL;
            return "N/A";
        } else if (dataString.length > MAX_COL_WIDTH) {
            let splitString = dataString.match(/.{15}\w*\W*|.*/g);
            splitString = splitString.filter(el => {
                return el != '' && el != ' ';
            })
            this.ySpacer += ((splitString.length - 1) * 4);
            return splitString.join('\n');
        } else {
            this.ySpacer = Y_SPACING_VAL;
            return dataString;
        }
    }

}

