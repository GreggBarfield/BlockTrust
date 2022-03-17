const MAX_COL_WIDTH = 15;
const Y_SPACING_VAL = 8;

export let CreatePrintFlyerButton = (salesData) => {
    let button = document.createElement("button");
    button.className = "btn btn-outline-primary btn-sm";
    button.textContent = "Create Flyer";
    button.style.display="none"

    if (Object.keys(salesData.reported).length !== 0) {
        button.style.display = "";
        button.addEventListener("click", ()=>{
            makeFlyer(salesData);
        });
    }

    return button;
}

async function makeFlyer(salesData) {
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
    
    createHeaderData(pdf, qrcodeData, salesData);
    createAnimalData(pdf, salesData);
    createMarketData(pdf, salesData);
    createFooter(pdf, pageWidth);
    
    pdf.save("MarketTrust Sale.pdf");
    document.body.style.cursor='default';
}

function createHeaderData(pdf, qrcodeData, salesData) {
    pdf.setFillColor('white');
    pdf.setDrawColor('gray');
    pdf.roundedRect(10, 40, 90, 25, 5, 5);

    pdf.setFontSize(12);
    pdf.text("Sales Group " + salesData.id, 15, 50);
    pdf.setFontSize(10);
    pdf.text("Location: " + salesData.market_location, 15, 57);

    pdf.roundedRect(110, 40, 90, 25, 5, 5);
    pdf.setFontSize(10);
    let sideText="Scan this QR code to get detailed information on each animal and photos.";
    pdf.text(processData(sideText), 125, 47);
    pdf.addImage(qrcodeData, 'PNG', 165, 40.5);
}

function createAnimalData(pdf, salesData) {
    pdf.roundedRect(10, 70, 90, 120, 5, 5);

    pdf.setFontSize(12);
    pdf.text("Animal Data", 15, 77);
    pdf.line(10, 79, 100, 79);

    let xLabelColumn = 15;
    let xDataColumn = 55;
    let yPlacement = 85;

    pdf.setFontSize(10);
    pdf.text("Breed:", xLabelColumn, yPlacement);
    pdf.text(processData(salesData.reported.breeds.join(', ')), xDataColumn, yPlacement);
    yPlacement += Y_SPACING_VAL;
    pdf.text("Base Weight:", xLabelColumn, yPlacement);
    pdf.text(processData(salesData.reported.weight), xDataColumn, yPlacement);
    yPlacement += Y_SPACING_VAL;
    pdf.text("Wt. Variance Frame:", xLabelColumn, yPlacement);
    pdf.text(processData(salesData.reported.weight_variance), xDataColumn, yPlacement);
    yPlacement += Y_SPACING_VAL;
    pdf.text("Horns:", xLabelColumn, yPlacement);
    pdf.text(processData(salesData.reported.horns), xDataColumn, yPlacement);
    yPlacement += Y_SPACING_VAL;
    pdf.text("Precon Program:", xLabelColumn, yPlacement);
    pdf.text(processData(salesData.reported.preconditioning_program), xDataColumn, yPlacement);
    yPlacement += Y_SPACING_VAL;
    pdf.text("Implants:", xLabelColumn, yPlacement);
    pdf.text(processData(salesData.reported.implants.join(', ')), xDataColumn, yPlacement);
    yPlacement += Y_SPACING_VAL;
    pdf.text("Castrated:", xLabelColumn, yPlacement);
    pdf.text(processData(salesData.reported.castrated), xDataColumn, yPlacement);
    yPlacement += Y_SPACING_VAL;
    pdf.text("Vaccinations:", xLabelColumn, yPlacement);
    pdf.text(processData(salesData.reported.vaccinations.join(', ')), xDataColumn, yPlacement);
    yPlacement += Y_SPACING_VAL;
    pdf.text("Feeding Program:", xLabelColumn, yPlacement);
    pdf.text(processData(salesData.reported.feeding_programs.join(', ')), xDataColumn, yPlacement);
    yPlacement += Y_SPACING_VAL;
    pdf.text("PVP Program:", xLabelColumn, yPlacement);
    pdf.text(processData(salesData.reported.process_verified_program), xDataColumn, yPlacement);
}

function createMarketData(pdf, salesData) {
    pdf.roundedRect(110, 70, 90, 60, 5, 5)
    
    pdf.setFontSize(12);
    pdf.text("Market Data", 115, 77);
    pdf.line(110, 79, 200, 79);

    let xLabelColumn = 115;
    let xDataColumn = 160;
    let yPlacement = 85;

    pdf.setFontSize(10);
    pdf.text("Total Count:", xLabelColumn, yPlacement);
    pdf.text(processData(salesData.reported.count), xDataColumn, yPlacement);
    yPlacement += Y_SPACING_VAL;
    pdf.text("Delivery Location:", xLabelColumn, yPlacement);
    pdf.text(processData(salesData.delivery_location), xDataColumn, yPlacement);
    yPlacement += Y_SPACING_VAL+8;
    
    let daysRemaining = "--";
    if ("end" in salesData && salesData.end !== null) {
        let currentEpoch = Date.now() / 1000;
        daysRemaining = Math.floor((salesData.end - currentEpoch) / (60 * 60 * 24));
    }
    let salesDate = new Date(salesData.start * 1000);
    
    pdf.text("Sales Date:", xLabelColumn, yPlacement);
    pdf.text(processData(salesDate.toDateString()), xDataColumn, yPlacement);
    yPlacement += Y_SPACING_VAL;
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
    let ySpacer = Y_SPACING_VAL;
    if (dataString == null || dataString == "") {
        return "N/A";
    } 
    else if (dataString.length > MAX_COL_WIDTH) {
        // Splits the string by the nearest space if it is longer than 15 characters.
        // Then joins them together with a \n making it a multiline string. 
        let splitString = dataString.match(/.{15}\S*\s|.*/g);
        splitString = splitString.filter(el => {
            return el != '' && el != ' ';
        })
        ySpacer += ((splitString.length - 1) * 4);
        return splitString.join('\n');
    } 
    else {
        ySpacer = Y_SPACING_VAL;
        return dataString;
    }
}

