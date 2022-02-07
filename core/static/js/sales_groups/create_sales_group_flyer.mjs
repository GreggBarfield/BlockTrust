
const MAX_COL_WIDTH = 15;
const Y_SPACING_VAL = 8;


export let CreatePrintFlyerButton = (salesData) => {
    let data = salesData;
    let ySpacer = Y_SPACING_VAL;
    let button = null;

    if (Object.keys(data.reported).length !== 0) {
        makeFlyerButton();

        button.addEventListener("click", ()=>{
            makeFlyer();
        });
    }

    return button;

    function makeFlyerButton() {
        button = document.createElement("button");
        button.className = "btn btn-primary btn-sm";
        button.textContent = "Create Flyer";
    }

    async function makeFlyer() {
        document.body.style.cursor='wait';
        let pdf = new jsPDF("p", "mm");
        
        const pageWidth = pdf.internal.pageSize.getWidth();

        let logo = document.querySelector(".b-header-logo-desktop");
        let logoCanvas = await html2canvas(logo, { 
            scale: 1.5 
        });
        let logoData = logoCanvas.toDataURL('image/png', 1);
        pdf.addImage(logoData, 'PNG', (pageWidth / 2) - 40, 10);

            
        let qrcode = document.getElementById('sales_group_qrcode');
        let qrcodeCanvas = await html2canvas(qrcode, { 
            scale: 0.9
        });
        let qrcodeData = qrcodeCanvas.toDataURL('image/png', 1);
        
        createHeaderData(pdf, qrcodeData);
        createAnimalData(pdf);
        createMarketData(pdf);
        createFooter(pdf, pageWidth);
        
        pdf.save("MarketTrust Sale.pdf");
        document.body.style.cursor='default';
    }

    function createHeaderData(pdf, qrcodeData) {
        pdf.setFillColor('white');
        pdf.setDrawColor('gray');
        pdf.roundedRect(10, 40, 90, 25, 5, 5);

        pdf.setFontSize(12);
        pdf.text("Sales Group " + data.id, 15, 50);
        pdf.setFontSize(10);
        pdf.text("Location: " + data.market_location, 15, 57);

        pdf.roundedRect(110, 40, 90, 25, 5, 5);
        pdf.setFontSize(10);

        let sideText="Scan this QR code to get detailed information on each animal and photos.";
        pdf.text(processData(sideText), 125, 47);
        pdf.addImage(qrcodeData, 'PNG', 165, 40.5);
    }

    function createAnimalData(pdf) {
        pdf.roundedRect(10, 70, 90, 120, 5, 5);

        pdf.setFontSize(12);
        pdf.text("Animal Data", 15, 77);
        pdf.line(10, 79, 100, 79);

        let xLabelColumn = 15;
        let xDataColumn = 55;
        let yPlacement = 85;

        pdf.setFontSize(10);
        pdf.text("Breed:", xLabelColumn, yPlacement);
        pdf.text(processData(data.reported.breeds.join(', ')), xDataColumn, yPlacement);
        yPlacement += ySpacer;
        pdf.text("Base Weight:", xLabelColumn, yPlacement);
        pdf.text(processData(data.reported.weight), xDataColumn, yPlacement);
        yPlacement += ySpacer;
        pdf.text("Wt. Variance Frame:", xLabelColumn, yPlacement);
        pdf.text(processData(data.reported.weight_variance), xDataColumn, yPlacement);
        yPlacement += ySpacer;
        pdf.text("Horns:", xLabelColumn, yPlacement);
        pdf.text(processData(data.reported.horns), xDataColumn, yPlacement);
        yPlacement += ySpacer;
        pdf.text("Precon Program:", xLabelColumn, yPlacement);
        pdf.text(processData(data.reported.preconditioning_program), xDataColumn, yPlacement);
        yPlacement += ySpacer;
        pdf.text("Implants:", xLabelColumn, yPlacement);
        pdf.text(processData(data.reported.implants.join(', ')), xDataColumn, yPlacement);
        yPlacement += ySpacer;
        pdf.text("Castrated:", xLabelColumn, yPlacement);
        pdf.text(processData(data.reported.castrated), xDataColumn, yPlacement);
        yPlacement += ySpacer;
        pdf.text("Vaccinations:", xLabelColumn, yPlacement);
        pdf.text(processData(data.reported.vaccinations.join(', ')), xDataColumn, yPlacement);
        yPlacement += ySpacer;
        pdf.text("Feeding Program:", xLabelColumn, yPlacement);
        pdf.text(processData(data.reported.feeding_programs.join(', ')), xDataColumn, yPlacement);
        yPlacement += ySpacer;
        pdf.text("PVP Program:", xLabelColumn, yPlacement);
        pdf.text(processData(data.reported.process_verified_program), xDataColumn, yPlacement);
    }

    function createMarketData(pdf) {
        pdf.roundedRect(110, 70, 90, 60, 5, 5)
        
        pdf.setFontSize(12);
        pdf.text("Market Data", 115, 77);
        pdf.line(110, 79, 200, 79);

        let xLabelColumn = 115;
        let xDataColumn = 160;
        let yPlacement = 85;

        pdf.setFontSize(10);
        pdf.text("Total Count:", xLabelColumn, yPlacement);
        pdf.text(processData(data.reported.count), xDataColumn, yPlacement);
        yPlacement += ySpacer;
        pdf.text("Delivery Location:", xLabelColumn, yPlacement);
        pdf.text(processData(data.delivery_location), xDataColumn, yPlacement);
        yPlacement += ySpacer;
        
        let daysRemaining = "--";
        if ("end" in data && data.end !== null) {
            let currentEpoch = Date.now() / 1000;
            daysRemaining = Math.floor((data.end - currentEpoch) / (60 * 60 * 24));
        }
        let salesDate = new Date(data.start * 1000);
        
        pdf.text("Sales Date:", xLabelColumn, yPlacement);
        pdf.text(processData(salesDate.toDateString()), xDataColumn, yPlacement);
        yPlacement += ySpacer;
        pdf.text("Days Remaining:", xLabelColumn, yPlacement);
        pdf.text(processData(daysRemaining), xDataColumn, yPlacement);
    }

    function createFooter(pdf, pageWidth) {
        const pageHeight = pdf.internal.pageSize.getHeight();

        pdf.setFontSize(8);
        pdf.setDrawColor('black');
        pdf.line(10, pageHeight - 15, pageWidth - 10, pageHeight - 15);
        pdf.text("BlockTrust Network", 15, pageHeight - 10);
        pdf.text("3511 Longmire, College Station, TX 77845", (pageWidth / 2) - 30, pageHeight - 10);
        pdf.text("info@Blocktrustnetwork.com", pageWidth - 50, pageHeight - 10);
    }

    function processData(dataString) {
        if (Number.isInteger(dataString)) {
            dataString = dataString.toString();
        }

        if (dataString == null || dataString == "") {
            ySpacer = Y_SPACING_VAL;
            return "N/A";
        } else if (dataString.length > MAX_COL_WIDTH) {
            // Splits the string by the nearest space if it is longer than 15 characters.
            // Then joins them together with a \n making it a multiline string. 
            let splitString = dataString.match(/.{15}\S*\s|.*/g);
            splitString = splitString.filter(el => {
                return el != '' && el != ' ';
            })
            ySpacer += ((splitString.length - 1) * 4);
            return splitString.join('\n');
        } else {
            ySpacer = Y_SPACING_VAL;
            return dataString;
        }
    }

}

