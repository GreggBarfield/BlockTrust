
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

export class MapWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.matchTypes = this.frame.getAttribute("data-widget-match-types").split(",");

        let request_object = {
            params: {
                types: this.matchTypes,
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

        Promise.all([
            
            this.getData(
                "data_request",
                {
                    request: request_object
                }
            ).then((data) => {
                this.match_rows = data.result.matches;
            }),

            this.getData(
                "direct/sectors_id_to_name",
                {}
            ).then((data) => {
                this.sectors_id_to_name = data.sectors_id_to_name;
            })

        ]).then(() => {
            this.frame.innerHTML = "";
            this.makeMap();
        });
    }

    formatDate(epoch) {
        if (epoch == null || epoch <= 0)
            return "--";
        let d = new Date(parseInt(epoch) * 1000);
        return (d.getMonth() + 1) + "/" + d.getDate() + "/" + d.getFullYear();
    }

    makeMap() {

        this.mapFrame = document.createElement("div");
        this.mapFrame.style = "height:100%";
        this.frame.appendChild(this.mapFrame);
        this.mapLegend = document.createElement("div");
        this.mapLegend.innerHTML = '<div style="background-color:#f1f1f1;padding-left:10px;">\
            <div style="float:left; margin-right:15px;"><i class="fas fa-circle f-10 m-r-5" style="color:#900C3F;"></i>Cow Calf</div>\
            <div style="float:left; margin-right:15px;"><i class="fas fa-circle f-10 m-r-5" style="color:#117A65;"></i>Packer</div>\
            <div style="float:left; margin-right:15px;"><i class="fas fa-circle f-10 m-r-5" style="color:#FFFF00;&quot;"></i>Feedlot</div>\
            <div><i class="fas fa-circle f-10 m-r-5" style="color:#FF9800;&quot;"></i>Stocker</div>\
                </div>';
        this.frame.appendChild(this.mapLegend);

        const jvmLineColor = 'rgb(255,0,0)';
        const jvmMapMainName = "us_lcc";
        const jvmImagePreload = true;
        const jvmMapCountyDirectory = "/static/jvm/jquery-jvectormap-us-counties/";
        function jvmMarkerDescription(event, tip, marker_index) {
            let marker = jvmMarkers[marker_index];

            let table = document.createElement("table");
            let tableBody = document.createElement("tbody");
            table.append(tableBody);
            let tr = document.createElement("tr");
            tableBody.append(tr);

            let left = document.createElement("td");
            left.style = "padding:0px;position:relative;";
            tr.append(left);

            // Image
            if (marker.hasOwnProperty('image')) {
                let img = document.createElement("img");
                img.setAttribute("src", marker.image);
                left.append(img);
            }

            let right = document.createElement("td");
            right.style = "vertical-align:top;padding:0px 0px 0px 20px;";
            tr.append(right);

            // Company name

            let pCompany = document.createElement("p");
            pCompany.style = "font-family: verdana; font-size:14px;font-weight:bold;color:#404040";
            pCompany.textContent = marker.name;
            right.append(pCompany);

            // Description
            let pDesc = document.createElement("p");
            pDesc.style = "font-family: verdana; font-size:10px;padding:2px";
            pDesc.textContent = marker.desc;
            right.append(pDesc);

            // Sighted
            let pSighted = document.createElement("p");
            pSighted.style = "font-family: verdana; font-size:12px;padding-top:10px;color:#C0C0C0";
            if ("sighted" in marker)
                pSighted.textContent = "Sighted on " + marker.sighted;
            right.append(pSighted);

            tip.html("");
            tip.append(table);
        }

        // Markers
        // Note: name must be unique!!!
        let jvmMarkers = [];

        // Todo: perform grouping
        for (const match_row of this.match_rows) {
            let im = null;
            let marker = {
                'name': 'Unknown',
                'latLng': [match_row["lat"], match_row["lon"]],
                'company': 'Unknown',
                'desc': '',
                'fill': '#AAAAAA'
            };
            if("time" in match_row) {
                marker.sighted = this.formatDate(match_row["time"])
            }

            let name = match_row["account_links.name"];

            if (name != null) {
                marker['name'] = name;
                if (name in imageMap)
                    im = imageMap[name];
            }

        

            let sector = match_row["account_links.sector"];
            if (sector != null) {
                let sector_name = this.sectors_id_to_name[sector];
                marker['fill'] = colorMap[sector_name];
                if (im == null && sector_name in imageMap) {
                    im = imageMap[sector_name];
                }
            }

        

            if (im != null) {
                marker["image"] = "/static/images/map_logos/" + im;
            }
            jvmMarkers.push(marker);
        }


        // You probably won't have to change anything below this ---------------------

        // Process jvmMarkers
        for (const marker_i in jvmMarkers) {
            let marker = jvmMarkers[marker_i];

            // Convert names to marker indices (need to clean up later)
            if ('lineTo' in marker) {
                let lineTo = [];
                for (const lineTo_i in marker.lineTo) {
                    let otherName = marker.lineTo[lineTo_i];
                    for (const marker_i_other in jvmMarkers) {
                        if (jvmMarkers[marker_i_other].name == otherName) {
                            lineTo.push({
                                'to': parseInt(marker_i_other),
                                'svgs': {}// svgs to line
                            });
                        }
                    }
                }
                marker.lineTo = lineTo;
            }

            // Image pre-loading (set to false to disable)
            if (jvmImagePreload && 'image' in marker) {
                marker._image = new Image();
                marker._image.src = marker.image;
            }
        }

        // Draw arrows
        let arrowsSetup = [];
        function jvmViewportChange(event, scale) {
            let jvmc = event.target;
            let jvmcsvg = $(event.target).find(">svg");
            let g_markers = $(jvmcsvg.find(">g")[2]);

            let alreadySetUp = false;

            for (const as_i in arrowsSetup) {
                if (arrowsSetup[as_i] === jvmc) {
                    alreadySetUp = true;
                }
            }

            if (!alreadySetUp) {
                arrowsSetup.push(jvmc);

                // Set colors
                for (const g_marker_i in jvmMarkers) {
                    $(g_markers.find("circle[data-index='" + g_marker_i + "']")).css('fill', jvmMarkers[g_marker_i].fill);
                }

                // Create line group
                let lineg = document.createElementNS('http://www.w3.org/2000/svg', "g");  // Fixed namespace at line but not here...
                jvmcsvg[0].insertBefore(lineg, g_markers[0]);


                for (const marker_i in jvmMarkers) {
                    let marker = jvmMarkers[marker_i];
                    if ('lineTo' in marker) {
                        for (const lineTo_i in marker.lineTo) {
                            let lineToElement = marker.lineTo[lineTo_i];
                            // Create the line, store in svgs and append to lineg
                            // https://stackoverflow.com/questions/7547117/add-a-new-line-in-svg-bug-cannot-see-the-line
                            let line = document.createElementNS('http://www.w3.org/2000/svg', "line");
                            line.setAttribute('stroke', jvmLineColor);
                            line.setAttribute('stroke-width', '2');
                            line.setAttribute('stroke-opacity', '1');
                            lineToElement.svgs[arrowsSetup.length - 1] = line;
                            lineg.append(line);
                            //Attempted work-around involving editing the html, eventually found that I had missed the SVG namespace two creates above...
                            //let linee_g = document.createElementNS('http://www.w3.org/2000/svg',"g");
                            //lineg.append(linee_g);
                            //linee_g.outerHTML = "<g xmlns=\"http://www.w3.org/2000/svg\">" + line.outerHTML + "</g>";
                            //lineToElement.svgs[jvmc] = $($(lineg).find('>g')[$(lineg).find('>g').length-1]).find('line')[0];
                        }
                    }
                }

            }

            g_markers = $(jvmcsvg.find(">g")[3]);

            let indexJVMC = arrowsSetup.indexOf(jvmc);

            // update cx/cy
            for (const marker_i in jvmMarkers) {
                let marker = jvmMarkers[marker_i];
                if ('lineTo' in marker) {
                    for (const lineTo_i in marker.lineTo) {
                        let toi = marker.lineTo[lineTo_i];
                        let line = $(marker.lineTo[lineTo_i].svgs[indexJVMC]);
                        let originc = $(g_markers.find("circle[data-index='" + marker_i + "']"));
                        let toc = $(g_markers.find("circle[data-index='" + toi.to + "']"));
                        line.attr('x1', originc.attr('cx'));
                        line.attr('x2', toc.attr('cx'));
                        line.attr('y1', originc.attr('cy'));
                        line.attr('y2', toc.attr('cy'));
                    }
                }
            }
        }

        // Uses the configuration above to configure a map
        function generateMapConfig(name) {
            let [initialRadius, hoverRadius] = [7,7];
            if (jvmMarkers.length > 50) {
                initialRadius = initialRadius/2;
            }
            else if (jvmMarkers.length > 10) {
                initialRadius = initialRadius/1.27;
            }
            return {
                map: name,
                markers: jvmMarkers,
                onMarkerTipShow: jvmMarkerDescription,
                onViewportChange: jvmViewportChange,
                markerStyle: {
                    initial: {
                        r: initialRadius
                    },
                    hover: {
                        r: hoverRadius
                    },
                    selected: {

                    },
                    selectedHover: {

                    }
                }
            };
        }

        // Create MultiMap and modify source code
        // Modification of
        // https://github.com/bjornd/jvectormap/blob/1a905c88ff2f19dc9ac01f6611a9ef3384a6049b/src/map.js
        // to remove cull test
        jvm.Map.prototype.latLngToPoint = function (lat, lng) {
            var point,
                proj = jvm.Map.maps[this.params.map].projection,
                centralMeridian = proj.centralMeridian,
                inset,
                bbox;

            if (lng < (-180 + centralMeridian)) {
                lng += 360;
            }

            point = jvm.Proj[proj.type](lat, lng, centralMeridian);

            inset = this.getInsetForPoint(point.x, point.y);
            // This is the code that's been changed
            if (!inset) {
                // Find anything that is real
                var insets = jvm.Map.maps[this.params.map].insets;

                for (let i = 0; i < insets.length; i++) {
                    if (insets[i].width > 0 && insets[i].height > 0) {
                        inset = insets[i];
                        break;
                    }
                }
                if (!inset) {
                    inset = insets[0];
                }
            }
            // End code change
            bbox = inset.bbox;

            point.x = (point.x - bbox[0].x) / (bbox[1].x - bbox[0].x) * inset.width * this.scale;
            point.y = (point.y - bbox[0].y) / (bbox[1].y - bbox[0].y) * inset.height * this.scale;

            return {
                x: point.x + this.transX * this.scale + inset.left * this.scale,
                y: point.y + this.transY * this.scale + inset.top * this.scale
            };
        }


        document.jvmMultiMap = new jvm.MultiMap({
            container: $(this.mapFrame),
            maxLevel: 1,
            main: generateMapConfig(jvmMapMainName),
            mapUrlByCode: function (code, multiMap) {
                return jvmMapCountyDirectory + 'jquery-jvectormap-data-' +
                    code.toLowerCase() + '-' +
                    multiMap.defaultProjection + '-en.js';
            },

        });

        // Modification of
        // https://github.com/bjornd/jvectormap/blob/a0e5497407946cabaad17124021ae70af8722b67/src/multimap.js
        // to allow for custom map config
        document.jvmMultiMap.drillDown = function (name, code) {
            var currentMap = this.history[this.history.length - 1],
                that = this,
                focusPromise = currentMap.setFocus({ region: code, animate: true }),
                downloadPromise = this.downloadMap(code);

            focusPromise.then(function () {
                if (downloadPromise.state() === 'pending') {
                    that.spinner.show();
                }
            });
            downloadPromise.always(function () {
                that.spinner.hide();
            });
            this.drillDownPromise = jvm.$.when(downloadPromise, focusPromise);
            this.drillDownPromise.then(function () {
                currentMap.params.container.hide();
                if (!that.maps[name]) {
                    // This is the code that's been changed
                    let mapConfig = generateMapConfig(name);
                    mapConfig.multiMapLevel = currentMap.params.multiMapLevel + 1;
                    that.addMap(name, mapConfig);
                } else {
                    that.maps[name].params.container.show();
                }
                that.history.push(that.maps[name]);
                that.backButton.show();
            });
        };

    }

}