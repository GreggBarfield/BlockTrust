import { Widget } from '../../../widget.mjs';

export class PlansWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    async initType() {
        this.frame.innerHTML = "";

        this.inputs = {};

        await this.generate();
    }

    async generate() {
        this.mainTable = document.createElement("table");
        this.mainTable.className = "table table-bordered nowrap";

        // Header
        this.mainTableHead = document.createElement("thead");
        this.mainTable.appendChild(this.mainTableHead);

        this.mainTableHeadRow0 = document.createElement("tr");
        this.mainTableHead.appendChild(this.mainTableHeadRow0);
        const headers = ["Cow-Calf Base Plan", "Cow-Calf Premium Plan", "Enterprise Plan"];
        for (const headerText of headers) {
            let th = document.createElement("th");
            th.textContent = headerText;
            th.setAttribute("scope", "col");
            th.style.width = "50%";
            this.mainTableHeadRow0.appendChild(th);
        }

        this.mainTableBody = document.createElement("tbody");
        this.mainTable.appendChild(this.mainTableBody);

        //1st row
        let rowTag = document.createElement("tr");
        this.mainTableBody.appendChild(rowTag);
        let cowCalfFeaturesTD = document.createElement("td");
        cowCalfFeaturesTD.innerHTML = "a. Carcass Data<br/>b. Access to In-Network Feeders and Auction Markets<br/>c. Secure Messaging in Network<br/><br/> <h6>Price: FREE</h6>";
        rowTag.appendChild(cowCalfFeaturesTD);

        let cowCalfFeaturesPremium = document.createElement("td");
        let { price } = await fetch("/stripe/price/basic").then(r => r.json());
        cowCalfFeaturesPremium.innerHTML = "a. Carcass Data<br/>b. Access to In-Network Feeders and Auction Markets<br/>c. Secure Messaging in Network<br/>d. Access to MarketTrust Cattle Sales System<br/>e. Access to Real-time Market Prices and Futures Prices<br/><br/> <h6>Price: $9.95 per month (billed annually)</h6>";
        rowTag.appendChild(cowCalfFeaturesPremium);

        let enterpriseFeaturesTD = document.createElement("td");
        enterpriseFeaturesTD.innerHTML = "Please contact us.";
        rowTag.appendChild(enterpriseFeaturesTD);

        //2nd row
        rowTag = document.createElement("tr");
        this.mainTableBody.appendChild(rowTag);
        let tdOptions = document.createElement("td");
        rowTag.appendChild(tdOptions);

        let button = document.createElement("a");
        button.className = "btn btn-primary btn-md";
        button.setAttribute("href", "");
        button.textContent = "Select";
        tdOptions.appendChild(button);

        tdOptions = document.createElement("td");
        rowTag.appendChild(tdOptions);
        button = document.createElement("a");
        button.className = "btn btn-primary btn-md";
        button.setAttribute("href", "/dashboard/subscribe?price=basic");
        button.textContent = "Select";
        tdOptions.appendChild(button);

        tdOptions = document.createElement("td");
        rowTag.appendChild(tdOptions);
        button = document.createElement("a");
        button.className = "btn btn-info btn-md";
        let { contactEmail } = await fetch("/outside/contact-email").then(r => r.json());
        button.setAttribute("href", "mailto:" + contactEmail);
        button.textContent = "Contact us";
        tdOptions.appendChild(button);

        this.frame.append(this.mainTable);
    }
}
