import { Widget } from '../../widget.mjs';

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
        // this.generateMapContainer();
        const position = { lat: 39.5, lng: -98.35 };
        let map = new Map(document.getElementById("map_container"), {
            zoom: 3,
            center: position,
            mapId: "DEMO_MAP_ID",
            //mapTypeId: "ROADMAP"
        });
        const marker = new AdvancedMarkerElement({
            map: map,
            position: position,
            title: "Uluru",
        });
    }

}