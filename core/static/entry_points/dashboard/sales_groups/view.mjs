function copyToClipboard() {
    //var aux = document.createElement("input");
    let linkText =  "https://blocktrustnetwork.com/markettrust/"+salesGroupID;
    /*
    aux.setAttribute("value",linkText);
    document.body.appendChild(aux);
    aux.select();
    document.execCommand("copy");
    document.body.removeChild(aux); 
    */
    navigator.clipboard.writeText(linkText)
}