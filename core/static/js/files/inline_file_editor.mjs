import {uploadFile} from "./files.mjs";
import {InfoModal} from "../core/info_modal.mjs";
export class InlineFileEditor {
    /**
     *  Creates an inline file editor which uploads a single file to the S3 bucket
     * @param {Element} attach_node The node to which the inline file editor needs to be attached
     * @param {String} fileType  A string which specifies the type of file to be uploaded
     */
    constructor(attach_node=null, fileType = ""){
        this.file = {};
        this.fileType = fileType;
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

        let inputFileNameAndRemoveButtonContainer = document.createElement("div");
        inputFileNameAndRemoveButtonContainer.className = "row m-1";

        this.inputFileNameContainer = document.createElement("div");
        this.inputFileNameContainer.textContent = "No File Uploaded";
        this.inputFileNameContainer.className = "m-1 font-italic";

        let inputFileRemoveButton = document.createElement("button");
        inputFileRemoveButton.textContent = "Remove";
        inputFileRemoveButton.className = "btn btn-sm btn-outline-danger";
        inputFileRemoveButton.type = "button";
        inputFileRemoveButton.onclick = () =>{
            if("input_file" in this.file){
                this.file = {};
                uploadInput.value = "";
                this.inputFileNameContainer.textContent = "No File Uploaded";
            }
        }

        inputFileNameAndRemoveButtonContainer.append(this.inputFileNameContainer);
        inputFileNameAndRemoveButtonContainer.append(inputFileRemoveButton);

        this.uploadContainer.append(uploadButton);
        this.uploadContainer.append(inputFileNameAndRemoveButtonContainer);
        attach_node.append(this.uploadContainer);
    }

    updateUploadContainer = () =>{
        let file = this.file;
        let fileName = "";
        if ("name" in file) {
            fileName = file.name;
        }
        this.inputFileNameContainer.textContent = fileName;
    }

    checkInput = (uploadInput) =>{
        let inputFile = uploadInput.files[0];
        let acceptableFile = true;
        let errorMessage = "";
        if(inputFile.size>10*1000*1000){
            acceptableFile = false;
            errorMessage = "Sorry, " + inputFile.name + " is too big (" + Math.floor(file.size/(1000*1000)) + "MB, the limit is 10MB).";
        }
        if(this.fileType !== "" && inputFile.type !== this.fileType){
            acceptableFile = false;
            errorMessage = "Sorry, "+ inputFile.name + " is not of the right format.";
        }
        if(acceptableFile === true){
            this.file = {
                "name": inputFile.name,
                "input_file": inputFile,
                "uploaded": false
            }
        }
        else{
            this.file = {};
            uploadInput.value = "";
            this.inputFileNameContainer.textContent = "No File Uploaded";
            new InfoModal("File Upload", errorMessage);
        }
        this.updateUploadContainer();
    }

    getFileID = () =>{
        if ("id" in this.file || this.file["id"] !== undefined || this.file["id"] !== null){
            return this.file["id"];
        }
    }

    upload = () =>{
            if(!this.uploadDeclined){
                if(!this.checkForUploadedFile()){return;}

                return uploadFile(false, true, this.file["input_file"], function(perc){})
                .then((id)=>{
                    this.file["uploaded"]= true;
                    this.file["id"] = id;
                    return Promise.resolve(id);
                }); 
            }
            else{
                return Promise.resolve(0);
            }
            
    }

    checkForUploadedFile = () =>{
        if("input_file" in this.file){
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