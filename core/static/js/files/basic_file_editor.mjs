import {uploadFile} from "./files.mjs";
import {Table} from "../core/table.mjs";
import {InfoModal} from "../core/info_modal.mjs";
import {promptURLBox  } from "./video_links.mjs";
export class BasicFileEditor {
    constructor(restrictions={}, attach_node=null, fileIDs=null, fileDes=null, fileAuths=null) {
        let that = this;
        this.files = [];
        //this.restrictions is a dictionary which has following items supported:
        //1. filetype: this is a list which can contain by the type of the file. For example: 'image'
        this.restrictions = restrictions;
        this.fileAuths = fileAuths;

        if (fileIDs !== null) {
            for (const fileID of fileIDs) {
                const curDes = fileDes[fileIDs.indexOf(fileID)]
                let file_obj = {
                    "id": fileID,
                    "description": curDes,
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
        this.ImageBox = document.createElement("div");
        this.ImageInput = document.createElement("input");
        this.ImageInput.type = "file";
        this.ImageInput.multiple = true;
        this.ImageInput.style.display = "none";
        document.body.append(this.ImageInput);
        this.ImageInput.addEventListener("input", () => {
            that.checkInput();
        });

        this.table = new Table();
        this.table.attach(this.ImageBox);

        this.table.setHeader(["ID", "Name", "Options","Description"]);

        this.updateTable();

        this.addImageButton = document.createElement("button");
        this.addImageButton.className = "btn btn-sm btn-primary";
        this.addImageButton.textContent = "Add Files"
        this.addImageButton.type = "button";
        this.addImageButton.addEventListener("click", function(e) {
            that.ImageInput.dispatchEvent(new MouseEvent("click"));
        });
        this.ImageBox.append(this.addImageButton);

        if (attach_node !== null) {
            this.attach(attach_node);
        }
        
    }

    attach(attach_node) {
        this.attached = true;
        this.frame = attach_node;
        this.frame.append(this.ImageBox);
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
                console.log("fileID:", fileID)
            }
            let fileName = "";
            if ("name" in file) {
                fileName = file.name;
            }
            let fileDes = document.createElement("input");
            fileDes.type = "text";
            fileDes.className = "form-control";
            fileDes.id = this.files.indexOf(file);
            console.log("filedes:",  this.files.indexOf(file));
            if("description" in file){
                
                fileDes.value = file.description;
                
            }
            if (!("row" in file)) {
                
                let optionsDiv = document.createElement("div");
                
                let removeButton = document.createElement("button");
                removeButton.textContent = "Remove";
                removeButton.textContent.fontcolor("green");
                removeButton.style.borderColor="black";
                removeButton.className = "btn btn-sm btn-danger";
                removeButton.type = "button";
                removeButton.style.backgroundColor="rgb(168, 87, 34)";
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
                
                file["row"] = this.table.addRow([fileID, fileName, optionsDiv,fileDes]);
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

    acceptableFile(file, restrictions={}) {
        // Just to make it a little less confusing for the users, not for security
        if (file.size > 10 * 1000 * 1000) {
            return "Sorry, " + file.name + " is too big (" + Math.floor(file.size / (1000 * 1000)) + "MB, the limit is 10MB).";
        }

        const {error, message} = this.checkFileType(file, restrictions);
        if(error)
            return message;

        return null;
    }

    checkFileType(file, restrictions) {
        if('filetype' in restrictions) {
            let result = {error: true, message:""};
            if(restrictions.filetype.includes("image"))
            {
                const  fileType = file['type'];
                const validImageTypes = ['image/gif','image/jpg', 'image/jpeg', 'image/png'];
                if (!validImageTypes.includes(fileType)) {
                    // invalid file type code goes here.
                    result.error = true;
                    result.message = "Sorry, the file " + file.name + " is not in .jpg, .jpeg, .png, or .gif format.";
                }
                else {
                    result.error = false;
                    result.message = "";
                }
            }
            return result;           
        }
    }

    checkInput() {
        let inputFiles = Array.from(this.ImageInput.files);
        this.ImageInput.value = "";

        for (let file of inputFiles) {
            let r = this.acceptableFile(file, this.restrictions);
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
    getDes(){
        let result = [];
        let i=0;
        for (const file of this.files) {
            if ("removed" in file && file["removed"]){
                i+=1;
                continue;
            }
                
            if (!("uploaded" in file)) {
                throw "Uploaded should be in file";
            }
            if (!file["uploaded"])
                continue;
            if (!("id" in file) || file["id"] === undefined || file["id"] === null)
                continue;
            result.push(document.getElementById(i).value);
            i+=1;
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