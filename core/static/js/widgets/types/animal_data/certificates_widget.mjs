import { Widget } from '../../widget.mjs';
import { formatDate } from "../../../core/time.mjs";

export class CertificatesWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.eid = parseInt(this.frame.getAttribute("data-widget-animal"));
        this.company = this.frame.getAttribute("data-widget-company");
        this.frame.innerHTML = "";
        this.getData(
            "direct/match_types_by_name",
            {}
        ).then((data) => {

            this.matchTypes = data.match_types_by_name;
            this.getData(
                "data_request",
                {
                    request: {
                        type: 'matches_by_eids',
                        params: {
                            eids: [this.eid],
                            ljoin_account_links: false,
                            types: ["Weaned","First Birth","Medical"]
                        }
                    }
                }
            ).then((data)=>
            {
                this.medical_rows=[];
                this.wean_data=null;
                this.first_born=null;
                for ( const match of data.result.matches)
                {
                    if (match.type == this.matchTypes["Medical"]){
                        this.medical_rows.push(match)
                    }
                    else if(match.type == this.matchTypes["Weaned"]){
                        this.wean_data=match;
                    }
                    else if(match.type == this.matchTypes["First Birth"]){
                        this.first_born=match
                    }
                }
                this.createDisplay();
            })
            
        });
    }

    createDisplay(){

        let certHeader = document.createElement("h2");
        certHeader.style="text-align: center;margin-top: 10px; font-size:20px"
        certHeader.textContent= "MFA Health Track Processing and Feed Report"
        this.frame.append(certHeader)

        let row =  document.createElement("div");
        row.className= "row"
        row.style="margin: auto;padding-left:20px ;font-weight: bold;"
        this.frame.append(row);

        let appNo =document.createElement("div");
        appNo.className = "col-md-4";
        appNo.textContent="App No:"+ ((this.wean_data["grouping_id"]!==null)? this.wean_data["grouping_id"]: "N/A");
        row.append(appNo)

        let prodName =document.createElement("div");
        prodName.className = "col-md-4";
        prodName.textContent="Producer Name: "+ this.company
        row.append(prodName)
        let tagRange =document.createElement("div");
        tagRange.className = "col-md-4";
        tagRange.textContent="Tag Range: "+this.eid
        row.append(tagRange)
        let firstBD =document.createElement("div");
        firstBD.className = "col-md-4";
        firstBD.textContent="First Birth Date: "+ ((this.first_born!==null)? formatDate(this.first_born.time):" ")
        row.append(firstBD)
        let weanDate =document.createElement("div");
        weanDate.className = "col-md-4";
        weanDate.textContent="Wean Date: "+ ((this.wean_data!==null)? formatDate(this.wean_data.time):" ")
        row.append(weanDate)
        let firstMD =document.createElement("div");
        firstMD.className = "col-md-4";
        if (this.wean_data !== null) {
            firstMD.textContent="First Eligible Movement Date: "+ (("first_14_date" in this.wean_data["data"])? this.wean_data["data"]["first_14_date"]:" ")
            row.append(firstMD)
            let creepFeed =document.createElement("div");
            creepFeed.className = "col-md-4";
            creepFeed.textContent="Creep Feed: "+ (("creep_feed" in this.wean_data["data"])? this.wean_data["data"]["creep_feed"]:" ")
            row.append(creepFeed)
            let first14DF =document.createElement("div");
            first14DF.className = "col-md-4";
            first14DF.textContent="First 14 Day Feed: "+ (("first_14_feed" in this.wean_data["data"])? this.wean_data["data"]["first_14_feed"]:" ")
            row.append(first14DF)
        }

        //table
        this.divTableResponsive = document.createElement("div");
        this.divTableResponsive.className = "table-responsive";
        this.divTableResponsive.style = "margin: auto;width:100%;padding-top:10px;padding-bottom:0px;";

        this.mainTable = document.createElement("table");
        this.mainTable.className = "table";
        this.mainTable.style ="padding:0px;padding-bottom:0px;margin-top:0px;margin-bottom:0px"
        this.divTableResponsive.appendChild(this.mainTable);

        // Header

        this.headers = ["Date", "Product Name", "Location"];

        this.mainTableHead = document.createElement("thead");
        this.mainTableHead.className = "thead-light";
        this.mainTable.appendChild(this.mainTableHead);

        this.mainTableHeadRow0 = document.createElement("tr");
        this.mainTableHeadRow0.style ="font-size:15px;padding:0px;padding-bottom:0px;margin-top:0px;margin-bottom:0px"
        this.mainTableHead.appendChild(this.mainTableHeadRow0);

        for (const header of this.headers) {
            let th = document.createElement("th");
            th.textContent = header;
            th.style =" background-color:#e83c3c;color: black;font-weight: bold;font-size:15px;padding-top:0px;padding:0px;margin-top:0px;margin-bottom:0px"
            this.mainTableHeadRow0.appendChild(th);
        }

        this.displayRows = [];
        this.weanDataHeader=["date","product","location"]
        for (const medical_row of this.medical_rows) {
            let data_obj = medical_row["data"];
            data_obj.date = formatDate(medical_row.time);
            let row = [];
            for (const header of this.weanDataHeader) {
                if (header in data_obj) {
                    row.push(data_obj[header]);
                }
                else {
                    row.push("");
                }
            }
            this.displayRows.push(row);
        }

        // Body

        this.mainTableBody = document.createElement("tbody");
        this.mainTableBody.style="padding-top:0px;padding:0px;margin-top:0px;margin-bottom:0px"

        this.mainTable.appendChild(this.mainTableBody);

        if (this.displayRows.length == 0) {
            let noData = document.createElement("div");
            noData.style = "text-align:center;padding:10px;width:100%;";
            noData.textContent = "No health data is available for this animal.";
            this.divTableResponsive.append(noData);
        }
        else {
            for (const row of this.displayRows) {
                let tr = document.createElement("tr");
                tr.style="height:2px; font-size:13px;padding:0px;padding-bottom:0px"
                this.mainTableBody.append(tr);

                for (const cell of row) {
                    let td = document.createElement("td");
                    td.style="font-size:13px;padding-top:0px;padding:0px;margin-top:0px;margin-bottom:0px"
                    tr.append(td);
                    td.textContent = cell;
                }
            }
        }

        // Put HTML in frame
        this.frame.appendChild(this.divTableResponsive);
        
    }
        
    
}