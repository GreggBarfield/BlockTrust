const loadGoogleMapsAPI = () =>{
    // Google Maps JavaScript API Script Link: https://developers.google.com/maps/documentation/javascript/load-maps-js-api
    // Use the 'v' parameter to indicate the version to use (weekly, beta, alpha, etc.).
    // Add other bootstrap parameters as needed, using camel case.
    (g=>{
        var h,a,k,p="The Google Maps JavaScript API",c="google",l="importLibrary",q="__ib__",m=document,b=window;
        b=b[c]||(b[c]={});
        var d=b.maps||(b.maps={}),r=new Set,e=new URLSearchParams,u=()=>h||(h=new Promise(async(f,n)=>{await (a=m.createElement("script"));
        e.set("libraries",[...r]+"");for(k in g)e.set(k.replace(/[A-Z]/g,t=>"_"+t[0].toLowerCase()),g[k]);
        e.set("callback",c+".maps."+q);
        a.src=`https://maps.${c}apis.com/maps/api/js?`+e;
        d[q]=f;a.onerror=()=>h=n(Error(p+" could not load."));a.nonce=m.querySelector("script[nonce]")?.nonce||"";
        m.head.append(a)}));
        d[l]?console.warn(p+" only loads once. Ignoring:",g):d[l]=(f,...n)=>r.add(f)&&u().then(()=>d[l](f,...n))
    })
    ({
        key: "AIzaSyB6DmYwUZ7ZFhlojy-nH8klsBwsziZR8SM",
        v: "weekly",
    });
}

const imageMap = {
    "Bounty County Feeders": "barton_county_map_logo.png",
    "Dillwyn Feedyard": "dillwyn_map_logo.png",
    "Great Bend Feeding": "great_bend_map_logo.png",
    "Knight Feedlot": "knight_map_logo.png",
    "Lewis Feedlot": "lewis_map_logo.png",
    "McClymot Feedlot": "mcclymont_map_logo.png",
    "Mid America Feeding": "mid_america_map_logo.png",
    "Roberts Cattle Co.": "roberts_map_logo.png",
    "Tyson": "tyson_map_logo.png",
    "Tyson Meats": "tyson_map_logo.png",
    "Ward Feedyard": "ward_map_logo.png",
    "Cow-Calf": "cowcalf_map_logo.png",
    "Feedlot": "generic_feedyard_map_logo.png"
};

const colorMap = {
    "Cow-Calf": "#900C3F",
    "Packer": "#117A65",
    "Feedlot": "#FFFF00",
    "Stocker": "#FF9800"
};

const generateAccountInformationContainer = (matchRow, sectorsIDToName) =>{
    let accountInformationContainer = document.createElement("div");
    accountInformationContainer.className = "p-1 m-1";
    let table = document.createElement("table");
    let tableBody = document.createElement("tbody");
    table.append(tableBody);

    let tableRow = document.createElement("tr");
    tableBody.append(tableRow);
    let left = document.createElement("td");
    left.className = "p-0";
    tableRow.append(left);
    let right = document.createElement("td");
    right.className = "p-0";
    tableRow.append(right);

    if("account_links.name" in matchRow){
        let accountName = matchRow["account_links.name"];
        if(accountName in imageMap){
            let img = generateImageElement(imageMap[accountName]);
            left.append(img);
        }
        else{
            if("account_links.sector" in matchRow){
                let sectorID = matchRow["account_links.sector"];
                let sectorName = sectorsIDToName[sectorID];
                if(sectorName in imageMap){
                    let img = generateImageElement(imageMap[sectorName]);
                    left.append(img);
                }
            }
        }
        let companyName = document.createElement("p");
        companyName.className = "font-weight-bold";
        companyName.textContent = accountName;
        right.append(companyName);
    }
    if("time" in matchRow){
        let sightedContainer = document.createElement("p");
        sightedContainer.textContent = "Sighted on " + formatDate(matchRow.time);
    }
    accountInformationContainer.append(table);
    return accountInformationContainer;
}

const generateImageElement = (imageName) =>{  
    let img = document.createElement("img");
    img.src = "/static/images/map_logos/" + imageName;
    img.className = "img img-fluid";
    return img;
}

const formatDate = (epoch) =>{
    if (epoch == null || epoch <= 0)
        return "--";
    let d = new Date(parseInt(epoch) * 1000);
    return (d.getMonth() + 1) + "/" + d.getDate() + "/" + d.getFullYear();
}

export {
    loadGoogleMapsAPI,
    generateAccountInformationContainer,
    colorMap
}