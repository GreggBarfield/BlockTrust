import {uploadFile} from "./files.mjs";
import {Table} from "../core/table.mjs";
import {InfoModal} from "../core/info_modal.mjs";
export class VideoSession{
    constructor(restrictions={}, attach_node=null, linkIDs=null, linkAuths=null) {
        let that = this;
        this.links = [];
        this.restrictions = restrictions;
        this.linkAuths = linkAuths;

        if (linkIDs !== null) {
            for (const linkID of linkIDs) {
                let link_obj = {
                    "id": linkID,
                    "name": linkID,
                    "uploaded": true
                };
                if (linkID in linkAuths) {
                    link_obj["name"] = linkAuths[linkID]["name"];
                }
                this.links.push(link_obj);
            }
        }

        this.attached = false;

        this.linkBox = document.createElement("div");

        this.table = new Table();
        this.table.attach(this.linkBox);

        this.table.setHeader(["ID", "Link", "Options"]);
        
        this.updateTable();
        this.addURLButton = document.createElement("button");
        this.addURLButton.className = "btn btn-sm btn-primary";
        this.addURLButton.textContent = "Add Youtube/Vimeo link"
        this.addURLButton.type = "button";
        this.addURLButton.addEventListener("click", ()=> {
           
            this.promptURLBox(this.links,"23456");

        });

        this.linkBox.append(this.addURLButton);

        if (attach_node !== null) {
            this.attach(attach_node);
        }

    }
    getLinks() {
        // Gets all uploaded and not removed file IDs
        let result = [];
        for (const link of this.links) {
            // if ("removed" in link && link["removed"])
            //     continue;
            // if (!("uploaded" in link)) {
            //     throw "Uploaded link already exist";
            // }
            // if (!link["uploaded"])
            //     continue;
            // // if (!("id" in link) || link["id"] === undefined || link["id"] === null)
            // //     continue;
            // console.log(link);
            result.push(link["name"]);
        }
        return result;
    }
    attach(attach_node) {
        this.attached = true;
        this.frame = attach_node;
        this.frame.append(this.linkBox);
    }
    remove(link) {
        if ("removed" in link) {
            link["removed"] = !link["removed"];
        }
        else {
            link["removed"] = true;
        }
        return link["removed"];
    }
    updateTable() {
        for (let link of this.links) {
            let linkID = "Not Uploaded";
            if ("id" in link && link.uploaded == true) {
                linkID = link.id;
            }
            let linkName = "";
            if ("name" in link) {
                linkName = link.name;
            }
            if (!("row" in link)) {
                
                let optionsDiv = document.createElement("div");
                
                let removeButton = document.createElement("button");
                removeButton.textContent = "Remove";
                removeButton.className = "btn btn-sm btn-danger";
                removeButton.type = "button";
                removeButton.addEventListener("click", ()=>{
                    if (this.remove(link)) {
                        removeButton.textContent = "Add";
                    }
                    else {
                        removeButton.textContent = "Remove";
                    }
                    this.updateTable();
                });
                optionsDiv.append(removeButton);
                
                link["row"] = this.table.addRow([linkID, linkName, optionsDiv]);
            }
            this.table.setValue(link["row"], 0, linkID);
            this.table.setValue(link["row"], 1, linkName);

            if ("removed" in link && link["removed"]) {
                link["row"].style.textDecoration = "line-through";
            }
            else {
                link["row"].style.textDecoration = "initial";
            }
        }
    }
    promptURLBox(files, id=null){

        // let toStr = toAccountName;

        // if (toStr === null || toStr == undefined) {
        //     if (typeof toAccount === "number") {
        //         toStr = "Account ID " + toAccount;
        //     }
        //     else {
        //         throw "Needs to know who to send the message to";
        //     }
        // }

        let infoModal = new InfoModal("Adding video link(s) ");
        let modalBody = infoModal.getBody();

        let form = document.createElement("form");
        modalBody.append(form);

        let formGroup = document.createElement("div");
        formGroup.className = "form-group";
        form.append(formGroup);

        let label = document.createElement("label");
        label.textContent = "Link(s):";
        formGroup.append(label);

        let textArea = document.createElement("textarea");
        textArea.className = "form-control";
        textArea.setAttribute("maxlength", 1000);
        formGroup.append(textArea);

        let submitButton = document.createElement("button");
        submitButton.textContent = "Submit";
        submitButton.className = "btn btn-primary";
        infoModal.getFooter().append(submitButton);

        submitButton.addEventListener("click", ()=>{
            let file_obj = {
                "id": id,
                "name": textArea.value,
                "uploaded": false
            };
            files.push(file_obj);
            console.log(files);
        
            // obj.updateTable();
            infoModal.close();
            this.updateTable();
        
        });
        
    }
}