import { Widget } from '../../widget.mjs';


export class CertificatesWidget extends Widget {
    constructor(frame) {
        super(frame);
    }
    initType() {
        this.animal = parseInt(this.frame.getAttribute("data-widget-animal"));
        this.frame.innerHTML = "";
        this.getData(
            "update_certificates",
            {
                request: {
                    type: 'matches_by_eids',
                    params: {
                        eids: [this.animal],
                        ljoin_account_links: true,
                        types: ["Weaned","First Birth","Medical"]
                    }
                }
            }
        ).then((data)=>
        {
            this.match_rows=[]
            this.wean_data=""
            this.first_born=""
            for ( const match of data.result.matches)
            {
                if (match.type==20){this.match_rows.push(match)}
                else if(match.type==11){this.wean_data=match;
                console.log("what is ",match)}
                else if(match.type==12){this.first_born=match}
            }
            // this.wean_data=data.result.matches[0];
            // this.match_rows = data.result.matches;
            // this.match_rows.shift();
            console.log("this.wean_data",this.wean_data)


            console.log("this.match_rows",this.match_rows)
            this.createDisplay();
        })
        
    }
    formatDate(epoch) {
        if (epoch == null || epoch <= 0)
            return "--";
        let d = new Date(parseInt(epoch) * 1000);
        return (d.getMonth() + 1) + "/" + d.getDate() + "/" + d.getFullYear();
    }
    createDisplay(){
        function addInfo(){

        }

        // let placeHolder = document.createElement("div");
        // placeHolder.style="width: 450px; height: height:400px;"
        // placeHolder.style.height= "100%"
        // placeHolder.style.width="100%"
        let certHeader = document.createElement("h2");
        certHeader.style="text-align: center;margin-top: 10px;"
        certHeader.textContent= "MFA Health Track Processing and Feed Report"
        this.frame.append(certHeader)

        let row =  document.createElement("div");
        row.className= "row"
        row.style="margin: auto;padding-left:20px"
        this.frame.append(row);

        let appNo =document.createElement("div");
        appNo.className = "col-md-4";
        appNo.textContent="App No:"
        row.append(appNo)

        let prodName =document.createElement("div");
        prodName.className = "col-md-4";
        prodName.textContent="Producer Name: "+ this.wean_data["account_links.uid"]
        row.append(prodName)
        let tagRange =document.createElement("div");
        tagRange.className = "col-md-4";
        tagRange.textContent="Tag Range: "+this.wean_data["eid"]
        row.append(tagRange)
        let firstBD =document.createElement("div");
        firstBD.className = "col-md-4";
        firstBD.textContent="First Birth Date: "+ ((this.first_born!="")? this.formatDate(this.first_born.time):" ")
        row.append(firstBD)
        let weanDate =document.createElement("div");
        weanDate.className = "col-md-4";
        weanDate.textContent="Wean Date: "+ this.formatDate(this.wean_data.time)
        row.append(weanDate)
        let firstMD =document.createElement("div");
        firstMD.className = "col-md-4";
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


        //table
        this.divTableResponsive = document.createElement("div");
        this.divTableResponsive.className = "table-responsive";
        this.divTableResponsive.style = "margin: auto;padding:10px;width:100%;";

        this.mainTable = document.createElement("table");
        this.mainTable.className = "table table-xs";
        this.divTableResponsive.appendChild(this.mainTable);

        // Header

        this.headers = ["Date", "Product Name", "Location", "Admin Route"];

        this.mainTableHead = document.createElement("thead");
        this.mainTableHead.className = "thead-light";
        this.mainTable.appendChild(this.mainTableHead);

        this.mainTableHeadRow0 = document.createElement("tr");
        this.mainTableHead.appendChild(this.mainTableHeadRow0);

        for (const header of this.headers) {
            let th = document.createElement("th");
            th.textContent = header;
            this.mainTableHeadRow0.appendChild(th);
        }

        this.rows = [];
        this.wean_dataHeader=["date","product","location","route"]
        for (const match_row of this.match_rows) {
            let data_obj = match_row["data"];
            data_obj.date = this.formatDate(match_row.time);
            let row = [];
            // for (const header in data_obj) {
            //     if (this.headers.indexOf(header) == -1) {
            //         this.headers.push(header);
            //     }
            // }
            for (const header of this.wean_dataHeader) {
                if (header in data_obj) {
                    row.push(data_obj[header]);
                }
                else {
                    row.push("");
                }
            }
            this.rows.push(row);
        }

        // Body

        this.mainTableBody = document.createElement("tbody");
        this.mainTable.appendChild(this.mainTableBody);

        if (this.rows.length == 0) {
            let noData = document.createElement("div");
            noData.style = "text-align:center;padding:10px;width:100%;";
            noData.textContent = "No health data is available for this animal.";
            this.divTableResponsive.append(noData);
        }
        else {
            for (const row of this.rows) {
                let tr = document.createElement("tr");
                this.mainTableBody.append(tr);

                for (const cell of row) {
                    let td = document.createElement("td");
                    tr.append(td);
                    td.textContent = cell;
                }
            }
        }

        // Put HTML in frame

        this.frame.appendChild(this.divTableResponsive);
        
    }
        
    
}