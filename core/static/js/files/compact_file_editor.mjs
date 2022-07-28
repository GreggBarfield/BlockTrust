import {uploadFile} from "./files.mjs";
import {InfoModal} from "../core/info_modal.mjs";

export class CompactFileEditor {
    constructor(attach_node=null){
        this.file = {};
        this.uploadDeclined = false;

        this.uploadContainer = document.createElement("div");
        this.uploadContainer.className = "row ml-2"
        
        let uploadInput = document.createElement("input");
        uploadInput.type = "file";
        uploadInput.multiple = false;
        uploadInput.style.display = "none";
        uploadInput.addEventListener("input", () => {
            this.checkInput(uploadInput);    
        });

        let uploadButton = document.createElement("button");
        uploadButton.className = "btn btn-sm btn-outline-primary ml-2";
        uploadButton.type = "button";
        uploadButton.textContent = "Upload";
        uploadButton.addEventListener("click", function(e) {
            uploadInput.dispatchEvent(new MouseEvent("click"));
        });

        let uploadedFileDetailsContainer = document.createElement("div");
        uploadedFileDetailsContainer.className = "row m-1";
        this.uploadedFileNameContainer = document.createElement("div");
        this.uploadedFileNameContainer.textContent = "No File Uploaded";
        this.uploadedFileNameContainer.className = "m-1 font-italic";

        let uploadedFileRemoveButton = document.createElement("button");
        uploadedFileRemoveButton.textContent = "Remove";
        uploadedFileRemoveButton.className = "btn btn-sm btn-outline-danger";
        uploadedFileRemoveButton.type = "button";
        uploadedFileRemoveButton.onclick = () =>{
            if(this.file !== {}){
                this.file = {};
                uploadInput.value = "";
                this.uploadedFileNameContainer.textContent = "No File Uploaded";
            }
        }

        uploadedFileDetailsContainer.append(this.uploadedFileNameContainer);
        uploadedFileDetailsContainer.append(uploadedFileRemoveButton);

        this.uploadContainer.append(uploadButton);
        this.uploadContainer.append(uploadedFileDetailsContainer);
        attach_node.append(this.uploadContainer);
    }

    updateUploadContainer = () =>{
        let file = this.file;
        let fileName = "";
        if ("name" in file) {
            fileName = file.name;
        }
        this.uploadedFileNameContainer.textContent = fileName;
    }

    acceptableFile = (file) =>{
        if(file.size>10*1000*1000){
            return "Sorry, " + file.name + " is too big (" + Math.floor(file.size/(1000*1000)) + "MB, the limit is 10MB).";
        }
        if(file.type !== "application/pdf"){
            return "Sorry, "+ file.name + " needs to be in PDF format."
        }
        return null;
    }

    checkInput = (uploadInput) =>{
        let uploadedFile = uploadInput.files[0];
        let acceptableFileCheck = this.acceptableFile(uploadedFile);
        if(acceptableFileCheck === null){
            this.file = {
                "name": uploadedFile.name,
                "file": uploadedFile,
                "uploaded": false
            }
        }
        else{
            new InfoModal("File Upload", acceptableFileCheck);
        }
        this.updateUploadContainer();
    }

    getFileID = () =>{
        if ("id" in this.file || this.file["id"] !== undefined || this.file["id"] !== null){
            return this.file["id"];
        }
    }

    upload = (progress) =>{
            if(!this.uploadDeclined){
                if(!"file" in this.file){return;}

                return uploadFile(false, true, this.file["file"], function(perc){
                    progress(perc);
                })
                .then((id)=>{
                    this.file["uploaded"]= true;
                    this.file["id"] = id;
                    this.updateUploadContainer();
                    return Promise.resolve(id);
                }); 
            }
            else{
                return Promise.resolve(0);
            }
            
    }

    checkForUploadedFile = () =>{
        if("file" in this.file){
            return true;
        }
        return false;
    }

    setUploadDeclined = (value) => {
        this.uploadDeclined = value;
    }

    checkForUploadDeclined = () =>{
        return this.uploadDeclined;
    }
}