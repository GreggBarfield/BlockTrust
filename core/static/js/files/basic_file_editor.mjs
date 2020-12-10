import {uploadFile} from "./files.mjs";
import {Table} from "../core/table.mjs";
import {InfoModal} from "../core/info_modal.mjs";

export class BasicFileEditor {
    constructor(restrictions={}, attach_node=null, fileIDs=null, fileAuths=null) {
        let that = this;
        this.files = [];
        this.restrictions = restrictions;
        this.fileAuths = fileAuths;

        if (fileIDs !== null) {
            for (const fileID of fileIDs) {
                let file_obj = {
                    "id": fileID,
                    "uploaded": true
                };
                if (fileID in fileAuths) {
                    file_obj["name"] = fileAuths[fileID]["name"];
                }
                this.files.push(file_obj);
            }
        }

        this.attached = false;
        this.frame = null;
        this.box = document.createElement("div");
        this.input = document.createElement("input");
        this.input.type = "file";
        this.input.multiple = true;
        this.input.style.display = "none";
        document.body.append(this.input);
        this.input.addEventListener("input", () => {
            that.checkInput();
        });

        this.table = new Table();
        this.table.attach(this.box);

        this.table.setHeader(["ID", "Name", "Options"]);

        this.updateTable();

        this.addFilesButton = document.createElement("button");
        this.addFilesButton.className = "btn btn-sm btn-primary";
        this.addFilesButton.textContent = "Add Files"
        this.addFilesButton.type = "button";
        this.addFilesButton.addEventListener("click", function(e) {
            that.input.dispatchEvent(new MouseEvent("click"));
        });
        this.box.append(this.addFilesButton);
        

        if (attach_node !== null) {
            this.attach(attach_node);
        }
    }

    attach(attach_node) {
        this.attached = true;
        this.frame = attach_node;

        this.frame.append(this.box);
    }

    remove(file) {
        if ("removed" in file) {
            file["removed"] = !file["removed"];
        }
        else {
            file["removed"] = true;
        }
        return file["removed"];
    }

    updateTable() {
        for (let file of this.files) {
            let fileID = "Not Uploaded";
            if ("id" in file && file.uploaded == true) {
                fileID = file.id;
            }
            let fileName = "";
            if ("name" in file) {
                fileName = file.name;
            }
            if (!("row" in file)) {
                
                let optionsDiv = document.createElement("div");
                
                let removeButton = document.createElement("button");
                removeButton.textContent = "Remove";
                removeButton.className = "btn btn-sm btn-danger";
                removeButton.type = "button";
                removeButton.addEventListener("click", ()=>{
                    if (this.remove(file)) {
                        removeButton.textContent = "Add";
                    }
                    else {
                        removeButton.textContent = "Remove";
                    }
                    this.updateTable();
                });
                optionsDiv.append(removeButton);
                
                file["row"] = this.table.addRow([fileID, fileName, optionsDiv]);
            }
            this.table.setValue(file["row"], 0, fileID);
            this.table.setValue(file["row"], 1, fileName);

            if ("removed" in file && file["removed"]) {
                file["row"].style.textDecoration = "line-through";
            }
            else {
                file["row"].style.textDecoration = "initial";
            }
        }
    }

    acceptableFile(file) {
        // Just to make it a little less confusing for the users, not for security
        if (file.size > 10 * 1000 * 1000) {
            return "Sorry, " + file.name + " is too big (" + Math.floor(file.size / (1000 * 1000)) + "MB, the limit is 10MB).";
        }
        return null;
    }

    checkInput() {
        let inputFiles = Array.from(this.input.files);
        this.input.value = "";

        for (let file of inputFiles) {
            let r = this.acceptableFile(file);
            if (r === null) {
                this.files.push({
                    "name": file.name,
                    "file": file,
                    "uploaded": false,
                });
            }
            else {
                new InfoModal("File Upload", r);
            }
        }
        this.updateTable();
    }

    getFileIDs() {
        // Gets all uploaded and not removed file IDs
        let result = [];
        for (const file of this.files) {
            if ("removed" in file && file["removed"])
                continue;
            if (!("uploaded" in file)) {
                throw "Uploaded should be in file";
            }
            if (!file["uploaded"])
                continue;
            if (!("id" in file) || file["id"] === undefined || file["id"] === null)
                continue;
            result.push(file["id"]);
        }
        return result;
    }

    upload(progress=null) {
        // Uploads remaining files
        // Returns a Promise

        let filesToBeProcessed = [];

        let totalBytes = 0;

        for (const file of this.files) {
            if (!file["uploaded"] && !("removed" in file && file["removed"])) {
                filesToBeProcessed.push(file);
                totalBytes += file["file"].size;
            }
        }

        if (filesToBeProcessed.length == 0) {
            if (typeof progress == "function") {
                progress(1);
            }
            return Promise.resolve(true);
        }

        let doFile = (itr, bytesSoFar) => {
            if (itr >= filesToBeProcessed.length) {
                return Promise.resolve(true);
            }

            return uploadFile(false, true, filesToBeProcessed[itr]["file"], function(perc) {
                if (totalBytes == 0) {
                    progress(1);
                }
                else if (filesToBeProcessed[itr]["file"].size == 0) {
                    progress(bytesSoFar / totalBytes);
                }
                else {
                    progress(bytesSoFar / totalBytes + perc * filesToBeProcessed[itr]["file"].size / totalBytes);
                }
            })
            .then((id)=>{
                filesToBeProcessed[itr]["uploaded"] = true;
                filesToBeProcessed[itr]["id"] = id;
                this.updateTable();
                return doFile(itr + 1, bytesSoFar + filesToBeProcessed[itr]["file"].size);
            });
        };

        return doFile(0, 0);
    }

}
