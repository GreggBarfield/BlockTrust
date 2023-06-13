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
        const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");
        let mapContainer = document.createElement("div");
        mapContainer.id = "map_container";
        mapContainer.style = "height:400px;width:100%;"
        this.frame.append(mapContainer);
        const position = { lat: 39.5, lng: -98.35 };

        let map = new Map(document.getElementById("map_container"), {
            zoom: 3,
            center: position,
            mapId: "DEMO_MAP_ID"
        });
        const marker = new AdvancedMarkerElement({
            map: map,
            position: position,
            title: "Uluru",
        });

        let matchTypes = this.frame.getAttribute("data-widget-match-types").split(",");
        let request_object = {
            params: {
                types: matchTypes,
                ljoin_account_links: true
            }
        };

        if (this.frame.hasAttribute("data-widget-mode")) {
            let mode = this.frame.getAttribute("data-widget-mode");
            if (mode == "associated auction sale account") {
                request_object.type = "matches_by_auction_account";
            }
            else {
                throw "Mode unresolved: " + mode;
            }
        }
        else {
            if (this.frame.hasAttribute("data-widget-account")) {
                request_object.type = "matches_by_account";
            }
            else {
                request_object.type = "matches_by_eids";
                request_object.params.eids = [parseInt(this.frame.getAttribute("data-widget-animal"))];
            }
        }

        let matchRowsData = await this.getData("data_request", {request: request_object});
        let matchRows = matchRowsData.data;
        let sectorsIdToNameData = await this.getData("direct/sectors_id_to_name", {});
        let sectorsIDToName = sectorsIdToNameData.data;
        this.generateMap(matchRows, sectorsIDToName)
    }

    generateMap = (matchRows, sectorsIDToName) =>{
        let mapMarkers = [];
    }

    generateMapMarkers = 

}