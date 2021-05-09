import { Widget } from '../../widget.mjs';

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
         const headers = ["Cow calf base plan", "Enterprise"];
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
         let {price} = await fetch("/stripe/price/basic").then(r => r.json());
         cowCalfFeaturesTD.innerHTML = "1.Feature <br/> 2.Feature <br/> 3.Feature <br/><br/> <h6>Price: " + price + " per year</h6>";
         rowTag.appendChild(cowCalfFeaturesTD);

         let enterpriseFeaturesTD = document.createElement("td");
         let {contactEmail} = await fetch("/outside/contact-email").then(r => r.json());
         enterpriseFeaturesTD.innerHTML = "Please contact us directly at " + contactEmail;
         rowTag.appendChild(enterpriseFeaturesTD);
         
         //2nd row
         rowTag = document.createElement("tr");
         this.mainTableBody.appendChild(rowTag);
         let tdOptions = document.createElement("td");
         rowTag.appendChild(tdOptions);

         let button = document.createElement("a");
         button.className = "btn btn-primary btn-md";
         button.setAttribute("href", "/dashboard/subscribe?price=basic");
         button.textContent = "Select";
         tdOptions.appendChild(button);

         tdOptions = document.createElement("td");
         rowTag.appendChild(tdOptions);
         button = document.createElement("a");
         button.className = "btn btn-info btn-md";
         button.setAttribute("href", "mailto:" + contactEmail);
         button.textContent = "Contact us";
         tdOptions.appendChild(button);
         
         this.frame.append(this.mainTable);
    }
}
