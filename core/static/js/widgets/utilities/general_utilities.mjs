const printContainerById = (containerId) =>{
    let tempWindowForPrint = window.open('', '', 'width=1200,height=900');
    let breakLine = "<hr style='height:2px;background:black'/>"
    tempWindowForPrint.document.write('<html><head><link rel="stylesheet" href="/static/build/build_dashboard_main.min.css"/></head><body>');
    tempWindowForPrint.document.write(breakLine);
    tempWindowForPrint.document.write(document.getElementById(containerId).innerHTML);
    tempWindowForPrint.document.write(breakLine);
    tempWindowForPrint.document.write('</body></html>');
    tempWindowForPrint.document.close();
    tempWindowForPrint.focus();
    setTimeout(function() {
        tempWindowForPrint.print();
        tempWindowForPrint.close();
    }, 2000);
}

export {printContainerById}