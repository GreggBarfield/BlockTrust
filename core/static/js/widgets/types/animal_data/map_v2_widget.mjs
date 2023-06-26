import { Widget } from '../../widget.mjs';
import { generateAccountInformationContainer, colorMap } from '../../utilities/map_utlilities.mjs';

export class MapV2Widget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType = async () =>{
        this.frame.innerHTML = "";
        const { Map } = await google.maps.importLibrary("maps");
        const { Marker, AdvancedMarkerElement, PinElement } = await google.maps.importLibrary("marker");
        const { InfoWindow } = await google.maps.importLibrary("streetView");
        const { Polyline } = await google.maps.importLibrary("geometry");

        let mapContainer = document.createElement("div");
        mapContainer.id = "map_container";
        mapContainer.style = "height:400px;width:100%;"
        this.frame.append(mapContainer);
        const position = { lat: 39.5, lng: -98.35 };

        let map = new Map(document.getElementById("map_container"), {
            zoom: 3.75,
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
        this.generateMap(map, matchRows, sectorsIDToName, Marker, AdvancedMarkerElement, PinElement, InfoWindow, Polyline);
    }

    generateMap = (map, matchRows, sectorsIDToName, Marker, AdvancedMarkerElement, PinElement, InfoWindow, Polyline) =>{
        let coordinates = [];
        let infoWindow = new InfoWindow();
        // Generate location markers and info windows on click
        for(const matchRow of matchRows){
            let accountInformationContainer = generateAccountInformationContainer(matchRow, sectorsIDToName);
            let accountSectorID = matchRow["account_links.sector"];
            let accountSectorName = sectorsIDToName[accountSectorID];
            let markerBackground = new PinElement({
                background: colorMap[accountSectorName],
                borderColor: "#137333",
                glyph: ""
            });
            let marker = new AdvancedMarkerElement({
                map,
                position: {lat:matchRow["lat"], lng:matchRow["lon"]},
                content: markerBackground.element
            });
            google.maps.event.addListener(marker, 'click', function(){
                infoWindow.setContent(accountInformationContainer);
                infoWindow.open(marker.map, this);
            })
            coordinates.push({lat:matchRow["lat"], lng:matchRow["lon"]});
        }
        // Generate lines between locations
        let line = new google.maps.Polyline({
            path: coordinates,
            geodesic: true,
            strokeColor: '#000000',
            strokeOpacity: 1.0,
            strokeWeight: 2
        });
        line.setMap(map);
    }
}