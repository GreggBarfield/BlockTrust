const generateMap = async (containerID, mapID, centerPosition, zoomLevel) =>{
    const { Map } = await google.maps.importLibrary("maps");
    const map = new Map(document.getElementById(containerID), {
        zoom: zoomLevel,
        center: centerPosition,
        mapId: mapID
    });
    return map;
}

const generateMapMarker = () =>{

}

export {
    generateMap
}