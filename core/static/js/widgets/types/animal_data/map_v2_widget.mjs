import { Widget } from '../../widget.mjs';
import { loadGoogleMapsAPI, generateAccountInformationContainer, generateLegendTable, colorMap, USABounds } from '../../utilities/map_utlilities.mjs';

export class MapV2Widget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType = async () =>{
        this.frame.innerHTML = "";
        await loadGoogleMapsAPI();
        const { Map } = await google.maps.importLibrary("maps");
        const { Marker, AdvancedMarkerElement, PinElement } = await google.maps.importLibrary("marker");
        const { InfoWindow } = await google.maps.importLibrary("streetView");
        const { LatLngBounds } = await google.maps.importLibrary("core");

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
            streetViewControl: false,
            restriction: {latLngBounds: USABounds}
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
        this.generateMap(map, matchRows, sectorsIDToName, Marker, AdvancedMarkerElement, PinElement, InfoWindow, LatLngBounds);
        this.generateMapLegend(map, colorMap)
    }

    generateMap = (map, matchRows, sectorsIDToName, Marker, AdvancedMarkerElement, PinElement, InfoWindow, LatLngBounds) =>{
        let coordinates = [];
        let markers = [];
        let infoWindow = new InfoWindow();
        let bounds = new LatLngBounds();
        // Generate location markers and info windows on click
        for(const matchRow of matchRows){
            if(matchRow["lat"] !==null &&  matchRow["lon"]!== null){
                let accountInformationContainer = generateAccountInformationContainer(matchRow, sectorsIDToName);
                let accountSectorID = matchRow["account_links.sector"];
                let accountSectorName = sectorsIDToName[accountSectorID];
                // Generating custom Pin element and Marker
                let markerBackground = new PinElement({
                    scale: 0.6,
                    background: accountSectorName? colorMap[accountSectorName]: colorMap["Unknown"],
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
                // Updating marker lists for generating lines, clustering and recentering
                markers.push(marker);
                coordinates.push({lat:matchRow["lat"], lng:matchRow["lon"]});
                bounds.extend(marker.position);
            }
        }
        // Generate lines between locations
        let line = new google.maps.Polyline({
            path: coordinates,
            geodesic: true,
            strokeColor: '#000000',
            strokeOpacity: 1.0,
            strokeWeight: 0.5
        });
        line.setMap(map);
        // Adding the marker clusterer script and generating clusters when it is loaded
        let markerClustererScript = document.createElement("script");
        markerClustererScript.src = "https://unpkg.com/@googlemaps/markerclusterer/dist/index.min.js";
        this.frame.append(markerClustererScript);
        markerClustererScript.onload = () =>{
            const markerCluster = new markerClusterer.MarkerClusterer({map, markers});
        }
        // Recentering Map to the cluster of points
        map.fitBounds(bounds);
    }
    
    generateMapLegend = (map, colorMap) =>{
        let legendContainer = document.createElement("div");
        legendContainer.className = "card m-1 p-1";
        let legendContainerBody = document.createElement("div");
        legendContainerBody.className = "card-body col m-2 p-2";
        let legendTable = generateLegendTable(colorMap);
        legendContainerBody.append(legendTable);
        legendContainer.append(legendContainerBody);
        map.controls[google.maps.ControlPosition.LEFT_BOTTOM].push(legendContainer);
    }
}