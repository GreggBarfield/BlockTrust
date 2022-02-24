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

            let firstRow = document.createElement("div");
            firstRow.className = "d-flex align-items-end";
            firstRow.appendChild(CreatePrintFlyerButton(data));
            firstRow.appendChild(this.createQRLinkBtn());
            firstRow.appendChild(this.createQRCodeImg());
            this.frame.append(firstRow);

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
        return copyLinkButton;
    }

    createQRCodeImg() {
        let qrImg = document.createElement("img");
        qrImg.src = this.qrSource;
        qrImg.className = "ml-auto";
        qrImg.id = "sales_group_qrcode"
        return qrImg;
    }

    displaySalesGroup() {
        this.salesGroupViewer = new SalesGroupViewer(this.sales_group, this.frame);
    }
}