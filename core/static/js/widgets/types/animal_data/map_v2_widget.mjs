import { Widget } from '../../widget.mjs';

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
export class MapV2Widget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType = async () =>{
        this.frame.innerHTML = "";
        const { Map } = await google.maps.importLibrary("maps");
        const { Marker } = await google.maps.importLibrary("marker");
        const { InfoWindow } = await google.maps.importLibrary("streetView");

        let mapContainer = document.createElement("div");
        mapContainer.id = "map_container";
        mapContainer.style = "height:400px;width:100%;"
        this.frame.append(mapContainer);
        const position = { lat: 39.5, lng: -98.35 };

        let map = new Map(document.getElementById("map_container"), {
            zoom: 4,
            center: position,
            mapId: "DEMO_MAP_ID",
            mapTypeId: 'roadmap',
            mapTypeControl: false,
            streetViewControl: false
        });

        let matchTypes = this.frame.getAttribute("data-widget-match-types").split(",");
        let request_object = {params: {types: matchTypes, ljoin_account_links: true}};

        if(this.frame.hasAttribute("data-widget-mode")){
            let mode = this.frame.getAttribute("data-widget-mode");
            if(mode == "associated auction sale account"){
                request_object.type = "matches_by_auction_account";
            }
            else{
                throw "Mode unresolved: " + mode;
            }
        }
        else{
            if(this.frame.hasAttribute("data-widget-account")){
                request_object.type = "matches_by_account";
            }
            else{
                request_object.type = "matches_by_eids";
                request_object.params.eids = [parseInt(this.frame.getAttribute("data-widget-animal"))];
            }
        }

        let matchRowsData = await this.getData("data_request", {request: request_object});
        let matchRows = matchRowsData.result.matches;
        let sectorsIdToNameData = await this.getData("direct/sectors_id_to_name", {});
        let sectorsIDToName = sectorsIdToNameData.sectors_id_to_name;
        console.log(matchRows);
        this.generateMap(map, matchRows, sectorsIDToName, Marker, InfoWindow);
    }

    generateMap = (map, matchRows, sectorsIDToName, Marker, InfoWindow) =>{
        for(const matchRow of matchRows){
            let accountInformationContainer = this.generateAccountInformationContainer(matchRow);
            // let infoWindow = new InfoWindow({
            //    content: accountInformationContainer,
            //    ariaLabel: "Testing"
            //});
            let infoWindow = new InfoWindow();
            let marker = new Marker({
                map: map,
                position: {lat:matchRow["lat"], lng:matchRow["lon"]},
                title: matchRow["account_links.name"] !== null ? matchRow["account_links.name"] : ""
            });
            marker.addListener("click", () => {
                // infoWindow.open({anchor: marker, map,});
                infoWindow.close();
                infoWindow.setContent(accountInformationContainer);
                infoWindow.open(marker.getMap(), marker);
            });
        }
    }

    generateAccountInformationContainer = (matchRow) =>{
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
                let img = document.createElement("img");
                img.src = "/static/images/map_logos/" + imageMap[accountName];
                img.className = "img img-fluid";
                left.append(img);
            }
            let companyName = document.createElement("p");
            companyName.className = "font-weight-bold";
            companyName.textContent = accountName;
            right.append(companyName);
        }
        if("time" in matchRow){
            let sightedContainer = document.createElement("p");
            sightedContainer.textContent = "Sighted on " + matchRow.time;
        }

        accountInformationContainer.append(table);
        return accountInformationContainer;
    }

}