import { Widget } from '../../widget.mjs';
import { SalesGroupViewer } from '../../../sales_groups/view_sales_group.mjs';
import { CreatePrintFlyerButton } from '../../../sales_groups/create_sales_group_flyer.mjs';

export class ViewSalesGroupWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.salesGroupID = parseInt(this.frame.getAttribute("data-widget-sales-group"));
        this.qrSource = this.frame.getAttribute("data-widget-qr-src");
        this.shareableLink = this.frame.getAttribute("data-widget-shareable-link");

        this.getData(
            "sales_group",
            {
                "sales_group": this.salesGroupID
            }
        ).then((data) => {
            this.sales_group = data;
            this.firstRow = document.createElement("div");
            this.firstRow.className = "d-flex align-items-end";
            this.frame.append(this.firstRow);

            this.printFlyerButton = CreatePrintFlyerButton(data);
            this.firstRow.appendChild(this.printFlyerButton);
            this.createQRLinkBtn();
            this.createQRCodeImg();
            this.displaySalesGroup();
        });


        this.onSomeDataLoaded(function () {
            this.frame.innerHTML = "";
        });

    }

    createQRLinkBtn() {
        let copyLinkButton = document.createElement("button");
        copyLinkButton.className = "btn btn-outline-primary btn-sm";
        copyLinkButton.innerHTML = "Copy Link";
        let that = this;
        copyLinkButton.onclick = function () {
            navigator.clipboard.writeText(that.shareableLink);
        };
        this.firstRow.append(copyLinkButton);
    }

    createQRCodeImg() {
        let qrImg = document.createElement("img");
        qrImg.src = this.qrSource;
        qrImg.className = "ml-auto";
        qrImg.id = "sales_group_qrcode"
        this.firstRow.append(qrImg);
    }

    displaySalesGroup() {
        this.salesGroupViewer = new SalesGroupViewer(this.sales_group, this.frame);
    }
}