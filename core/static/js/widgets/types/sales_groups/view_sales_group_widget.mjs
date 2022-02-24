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
        ).then((salesGroup) => {
            let firstRow = document.createElement("div");
            firstRow.className = "d-flex align-items-end";
            firstRow.appendChild(CreatePrintFlyerButton(salesGroup));
            firstRow.appendChild(createQRLinkBtn(this.shareableLink));
            firstRow.appendChild(createQRCodeImg(this.qrSource));
            this.frame.append(firstRow);

            new SalesGroupViewer(salesGroup, this.frame);
        });

        this.onSomeDataLoaded(function () {
            this.frame.innerHTML = "";
        });

    }
}

function createQRLinkBtn(shareableLink) {
    let copyLinkButton = document.createElement("button");
    copyLinkButton.className = "btn btn-outline-primary btn-sm";
    copyLinkButton.innerHTML = "Copy Link";
    copyLinkButton.onclick = function () {
        navigator.clipboard.writeText(shareableLink);
    };
    return copyLinkButton;
}

function createQRCodeImg(qrSource) {
    let qrImg = document.createElement("img");
    qrImg.src = qrSource;
    qrImg.className = "ml-auto";
    qrImg.id = "sales_group_qrcode"
    return qrImg;
}