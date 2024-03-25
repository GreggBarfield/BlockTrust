const printContainerById = (containerId) =>{
    let tempWindowForPrint = window.open('', '', 'width=1100,height=900');
    let breakLine = "<hr style='height:2px;background:black'/>"
    tempWindowForPrint.document.write('<html><head><link rel="stylesheet" href="/static/build/build_dashboard_main.min.css"/><link rel="stylesheet" href="/static/css/dashboard/flashable/flash_able_old/plugins/bootstrap/css/bootstrap.min.css"/></head><body>');
    tempWindowForPrint.document.write(breakLine);
    tempWindowForPrint.document.write(document.getElementById(containerId).innerHTML);
    tempWindowForPrint.document.write(breakLine);
    tempWindowForPrint.document.write('</body></html>');
    tempWindowForPrint.document.close();
    tempWindowForPrint.focus();
    tempWindowForPrint.addEventListener("load", (e)=>{
        tempWindowForPrint.print();
    })
}

const printContainer = (container) =>{
    let tempWindowForPrint = window.open('', '', 'width=1100,height=900');
    let breakLine = "<hr style='height:2px;background:black'/>"
    tempWindowForPrint.document.write('<html><head><link rel="stylesheet" href="/static/build/build_dashboard_main.min.css"/><link rel="stylesheet" href="/static/css/dashboard/flashable/flash_able_old/plugins/bootstrap/css/bootstrap.min.css"/></head><body>');
    tempWindowForPrint.document.write(breakLine);
    tempWindowForPrint.document.write(container.innerHTML);
    tempWindowForPrint.document.write(breakLine);
    tempWindowForPrint.document.write('</body></html>');
    tempWindowForPrint.document.close();
    tempWindowForPrint.focus();
    tempWindowForPrint.addEventListener("load", (e)=>{
        tempWindowForPrint.print();
    })
}

export {printContainerById, printContainer}