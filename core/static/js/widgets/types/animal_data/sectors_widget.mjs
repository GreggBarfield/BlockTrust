import { Widget } from '../../widget.mjs';

export class SectorsWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.animal = parseInt(this.frame.getAttribute("data-widget-animal"));

        this.getData(
            "matches",
            {
                animal: this.animal,
                ljoin_data_str: true,
                ljoin_account_links: true
            },
            (data) => {
                this.match_rows = data.match_rows;
            }
        );
        this.getData(
            "sectors_by_id",
            {},
            (data) => {
                this.sectors_by_id = data.sectors_by_id;
            }
        );
        this.getData(
            "sectors_by_name",
            {},
            (data) => {
                this.sectors_by_name = data.sectors_by_name;
            }
        );
        this.getData(
            "match_types_by_id",
            {},
            (data) => {
                this.match_types_by_id = data.match_types_by_id;
            }
        );
        this.getData(
            "match_types_by_name",
            {},
            (data) => {
                this.match_types_by_name = data.match_types_by_name;
            }
        );


        this.onAllDataLoaded(function () {
            this.frame.innerHTML = "";
            this.prepData();
            this.makeBoxes();
        });

    }

    formatDate(epoch) {
        if (epoch == null || epoch <= 0)
            return "--";
        let d = new Date(parseInt(epoch) * 1000);
        return (d.getMonth() + 1) + "/" + d.getDate() + "/" + d.getFullYear();
    }

    prepData() {
        let match_types_by_name=this.match_types_by_name;
        let sectors_by_name=this.sectors_by_name;
        let match_rows=this.match_rows;
        let formatDate = this.formatDate;

        let sectors = [];
        this.sectors = sectors;

        function addSector(sectorName) {
            sectors.push({ "name": sectorName, "tabs": [] });
        }

        let displaySectors = ["Cow-Calf", "Auction House", "Feedlot", "Packer"];

        let uniqueTabID = 0;

        function addData(sectorName, tabName, dataLabel, data) {
            let good = false;
            for (const sector of sectors) {
                if (sector.name == sectorName) {
                    for (const tab of sector.tabs) {
                        if (tab.name == tabName) {
                            good = true;
                            tab.pairs.push([dataLabel, data]);
                        }
                    }
                    if (!good) {
                        good = true;
                        sector.tabs.push({ "name": tabName, "id": uniqueTabID++, "pairs": [[dataLabel, data]], "element": null, "target": null });
                    }
                }
            }
            if (!good) {
                throw "Failed to add data to sector " + sector;
            }
        }

        function convAsIs(v) {
            return v;
        }

        function convDate(v) {
            return formatDate(v);
        }

        function useDataString(converter=convAsIs) {
            return function (row) {
                return converter(row.data_str);
            }
        }

        function useAccountLinkCompany(converter=convAsIs) {
            return function (row) {
                return converter(row["account_links.company"]);
            }
        }
        
        function useDataValue(converter=convAsIs) {
            return function (row) {
                return converter(row.data);
            }
        }
        
        function useTime(converter=convDate) {
            return function (row) {
                return converter(row.time);
            }
        }

        function filterMatchTypeDataValue(matchTypeStr, dataValue) {
            return function (row) {
                return row.type === match_types_by_name[matchTypeStr] && row.data === dataValue;
            }
        }

        function filterMatchTypeAccountLinkSector(matchTypeStr, sectorName) {
            return function (row) {
                return row.type === match_types_by_name[matchTypeStr] && row["account_links.sector"] === sectors_by_name[sectorName];
            }
        }

        function filterMatchType(matchTypeStr) {
            return function (row) {
                return row.type === match_types_by_name[matchTypeStr];
            }
        }

        function filterAll() {
            return function (row) {
                return true;
            }
        }
        
        function useDataJson(property, converter=convAsIs) {
            return function (row) {
                let jObj = null;
                try {
                    jObj = JSON.parse(row.data_str);
                }
                catch {}
                if (jObj != null && jObj.hasOwnProperty(property)) {
                    return converter(jObj[property])
                }
                return null;
            }
        }

        function addField(sectorName, tabName, dataLabel, __filter=null, __use=null, combined=null) {
            let numAdded = 0;
            if (combined === null) {
                combined = [[__filter, __use]];
            }
            for (const match_row of match_rows) {
                for (const pair of combined) {
                    const filter = pair[0];
                    const use = pair[1];
                    if (filter(match_row)) {
                        let res = use(match_row);
                        if (res === null) {
                            res = "--";
                        }
                        addData(sectorName, tabName, dataLabel, res);
                        numAdded += 1;
                    }
                }
            }
            if (numAdded == 0) {
                addData(sectorName, tabName, dataLabel, "");
            }
        }

        // Shared
        for (const displaySector of displaySectors) {
            addSector(displaySector);
            addField(displaySector, "Demographics", displaySector + " Company", filterMatchTypeAccountLinkSector("Sighting", displaySector), useAccountLinkCompany());
            addField(displaySector, "Demographics", "Sighted", filterMatchTypeAccountLinkSector("Sighting", displaySector), useTime());
        }

        // Cow-Calf info
        addField("Cow-Calf", "Demographics", "Born", filterMatchType("Born"), useTime());
        addField("Cow-Calf", "Demographics", "Visual Tag", null, null, [[filterMatchType("Visual ID"), useDataValue()], [filterMatchType("Visual ID Complex"), useDataString()]]);
        addField("Cow-Calf", "Demographics", "Weaned", filterMatchType("Weaned"), useTime());
        addField("Cow-Calf", "Demographics", "Weaned At", filterMatchType("Weaned"), useDataJson("at"));

        // Cow-Calf Feed
        addField("Cow-Calf", "Feed", "Creepfeed", filterMatchType("Weaned"), useDataJson("creep_feed"));
        addField("Cow-Calf", "Feed", "Feed Type days 1-14 after weaning", filterMatchType("Weaned"), useDataJson("first_14_feed"));
        addField("Cow-Calf", "Feed", "Feeding method days 1-14", filterMatchType("Weaned"), useDataJson("first_14_method"));
        addField("Cow-Calf", "Feed", "Feed Type days 15-45 after weaning", filterMatchType("Weaned"), useDataJson("second_31_feed"));
        addField("Cow-Calf", "Feed", "Feeding method days 15-45", filterMatchType("Weaned"), useDataJson("second_31_method"));

        // Cow-Calf Market
        addField("Cow-Calf", "Market", "Sold", filterMatchType("Sold"), useTime());
        addField("Cow-Calf", "Market", "Method", filterMatchType("Sold"), useDataJson("method"));
        addField("Cow-Calf", "Market", "At", filterMatchType("Sold"), useDataJson("location"));
        addField("Cow-Calf", "Market", "Group Size", filterMatchType("Sold"), useDataJson("group_size"));

        // Packer Quality
        addField("Packer", "Quality", "Hot Weight", filterMatchType("Hot Weight"), useDataValue());
        addField("Packer", "Quality", "USDA Quality Grade", filterMatchType("USDA Quality Grade"), useDataString());
        addField("Packer", "Quality", "USDA Yield Grade", filterMatchType("USDA Yield Grade"), useDataValue());
        addData("Packer", "Quality", "Ribeye Area", "");
        addData("Packer", "Quality", "Marbling Score", "");
        addData("Packer", "Quality", "Fat Thickness", "");
    }

    selectTab(tab, sector) {
        for (const t of sector.tabs) {
            $(t.target).removeClass("show");
            $(t.target).removeClass("active");
            $(t.element).removeClass("active");
        }
        
        $(tab.target).addClass("show");
        $(tab.target).addClass("active");
        $(tab.element).addClass("active");

    }

    makeBoxes() {

        for (const sector of this.sectors) {
            let box = document.createElement("div");
            box.className = "col-md-6";
            this.frame.append(box);

            let card = document.createElement("div");
            card.className = "card";
            box.append(card);

            let cardHeader = document.createElement("div");
            cardHeader.className = "card-header";
            card.append(cardHeader);

            let ulHeader = document.createElement("ul");
            ulHeader.className = "nav nav-tabs card-header-tabs";
            ulHeader.style = "margin: 0px 0px -20px;";
            cardHeader.append(ulHeader);

            let liSector = document.createElement("li");
            liSector.className = "nav-item";
            liSector.style = "flex-grow: 1;";
            ulHeader.append(liSector);

            let h5Sector = document.createElement("h5");
            h5Sector.style = "padding-top:0px;padding-bottom:0px;border:none;";
            h5Sector.textContent = sector.name;
            liSector.append(h5Sector);

            // Tab selectors

            for (const tab of sector.tabs) {
                let liTab = document.createElement("li");
                liTab.className = "nav-item";
                ulHeader.append(liTab);

                let aTab = document.createElement("a");
                aTab.className = "nav-link ";
                aTab.style="cursor:pointer";
                aTab.textContent = tab.name;
                liTab.append(aTab);

                let that = this;

                $(liTab).click(function(){
                    that.selectTab(tab, sector);
                });
                tab.element = aTab;
            }

            let cardBody = document.createElement("div");
            cardBody.className = "card-body tab-content";
            card.append(cardBody);

            if (sector.tabs.length == 0) {
                let noData = document.createElement("div");
                noData.style = "text-align:center;padding:10px;width:100%;";
                noData.textContent = "No information is available.";
                cardBody.append(noData);

                h5Sector.style.paddingBottom = "20px";
            }
            else {

                for (const tab of sector.tabs) {
                    let tabPane = document.createElement("div");
                    tabPane.className = "tab-pane fade";
                    cardBody.append(tabPane);
                    tab.target = tabPane;

                    let tabInside = document.createElement("div");
                    tabInside.className = "col-sm-12";
                    tabPane.append(tabInside);

                    let dl = document.createElement("dl");
                    dl.className = "dl-horizontal row";
                    tabInside.append(dl);
                    for (const pair of tab.pairs) {
                        let dt = document.createElement("dt");
                        dt.textContent = pair[0];
                        dt.className = "col-sm-4";
                        dl.append(dt);
                        let dd = document.createElement("dd");
                        dd.textContent = pair[1];
                        dd.className = "col-sm-8";
                        dl.append(dd);
                    }
                }
            }

            $(sector.tabs[0].element).click();
        }

        
    }
}