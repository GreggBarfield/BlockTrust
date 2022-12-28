import {saveAndUploadFile} from "./files.mjs";
import {InfoModal} from "../core/info_modal.mjs";
export class FileUploader {
    /**
     *  Creates an inline file editor which uploads a single file to the S3 bucket
     * @param {Element} parentNode The node to which the inline file editor needs to be attached
     * @param {String} acceptFileTypes  A string which specifies the type of file to be uploaded
     */
    constructor(parentNode=null, acceptFileTypes = []){
        this.file = null;
        this.fileName = "";
        this.fileID = 0;
        this.uploaded = false;
        this.removed = false;
        this.acceptFileTypes = acceptFileTypes;
        this.uploadDeclinedByUser = false;

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

        let inputFileNameAndRemoveButtonContainer = document.createElement("div");
        inputFileNameAndRemoveButtonContainer.className = "row m-1";

        this.inputFileNameContainer = document.createElement("div");
        this.inputFileNameContainer.textContent = "No File Uploaded";
        this.inputFileNameContainer.className = "m-1 font-italic";

        let inputFileRemoveButton = document.createElement("button");
        inputFileRemoveButton.textContent = "Remove";
        inputFileRemoveButton.className = "btn btn-sm btn-outline-danger ml-2";
        inputFileRemoveButton.type = "button";
        inputFileRemoveButton.onclick = () =>{
            if(this.file !== null){  
                this.file = null;
                this.removed = true;
                this.fileName = "";
                uploadInput.value = "";
                this.inputFileNameContainer.className = "m-1 font-italic";
                this.inputFileNameContainer.textContent = "No File Uploaded";
            }
        }

        inputFileNameAndRemoveButtonContainer.append(this.inputFileNameContainer);
        inputFileNameAndRemoveButtonContainer.append(inputFileRemoveButton);

        this.uploadContainer.append(uploadButton);
        this.uploadContainer.append(inputFileNameAndRemoveButtonContainer);
        parentNode.append(this.uploadContainer);
    }

    checkInput = (uploadInput) =>{
        let inputFile = uploadInput.files[0];
        let acceptableFile = true;
        let errorMessage = "";
        if(inputFile.size>10*1000*1000){
            acceptableFile = false;
            errorMessage = "Sorry, " + inputFile.name + " is too big (" + Math.floor(file.size/(1000*1000)) + "MB, the limit is 10MB).";
        }
        if(this.acceptFileTypes !== [] && !this.acceptFileTypes.includes(inputFile.type)){
            acceptableFile = false;
            errorMessage = "Sorry, "+ inputFile.name + " must be PDF";
        }
        if(acceptableFile === true){
            this.file = inputFile;
            this.fileName = inputFile.name;
            this.uploaded = false;
            this.inputFileNameContainer.innerHTML = `<strong>${this.fileName}</strong> (queued for upload)`;
        }
        else{
            this.file = null;
            this.fileName = "";
            uploadInput.value = "";
            this.inputFileNameContainer.textContent = "No File Uploaded";
            new InfoModal("File Upload", errorMessage);
        }
    }

    upload = (questionId=null) =>{
        //Returns a promise
        return saveAndUploadFile(true, true, this.file, null, questionId)
        .then((id)=>{
            this.uploaded= true;
            this.inputFileNameContainer.className = "m-1 font-italic text-success";
            this.inputFileNameContainer.textContent = this.fileName + " (Uploaded)";
            return Promise.resolve(id);
        });      
    }

    isFileAttached = () =>{
        if(this.file !== null){
            return true;
        }
        return false;
    }

    updateContainer = (customClassName, customTextContent) => {
        this.inputFileNameContainer.className = customClassName;
        this.inputFileNameContainer.textContent = customTextContent;
    }
}