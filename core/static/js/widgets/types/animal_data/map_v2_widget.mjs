import { Widget } from '../../widget.mjs';
import { generateAccountInformationContainer, closeOtherInfoWindows } from '../../utilities/map_utlilities.mjs';

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
            zoom: 3.6,
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
        //console.log(matchRows);
        this.generateMap(map, matchRows, sectorsIDToName, Marker, InfoWindow);
    }

    generateMap = (map, matchRows, sectorsIDToName, Marker, InfoWindow) =>{
        for(const matchRow of matchRows){
            let accountInformationContainer = generateAccountInformationContainer(matchRow, sectorsIDToName);
            let infoWindow = new InfoWindow();
            let infoWindowElementsList = [];
            let marker = new Marker({
                map: map,
                position: {lat:matchRow["lat"], lng:matchRow["lon"]},
                title: matchRow["account_links.name"] !== null ? matchRow["account_links.name"] : ""
            });
            marker.addListener("mouseover", () => {
                // infoWindow.open({anchor: marker, map,});
                infoWindowElementsList = closeOtherInfoWindows(infoWindowElementsList);
                // infoWindow.close();
                infoWindow.setContent(accountInformationContainer);
                infoWindowElementsList[0] = infoWindow;
                infoWindow.open(marker.getMap(), marker);
            });
            marker.addListener("mouseout", () =>{
                infoWindowElementsList = closeOtherInfoWindows(infoWindowElementsList);
                infoWindow.close();
                infoWindowElementsList[0] = infoWindow;
            });
        }
    }
}