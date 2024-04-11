import { InfoModal } from "../../../core/info_modal.mjs";

export class UploadEIDsForSalesGroupWidget{
    constructor() {
        this.eids = [];
        this.infoModal = null;
        this.eidCountLimit = 0;
    }

    createModalLink = () =>{
        let linkContainer = document.createElement("div");
        linkContainer.className = `d-flex justify-content-center align-items-center`;
        this.link = document.createElement("a");
        this.link.className = "h6";
        this.link.href="#";
        this.link.textContent = "Upload EIDs for Sales Group";
        this.link.onclick = () =>{
            if(this.eidCountLimit == 0){
                this.generateModalWithMessage("Upload EIDs for Sales Group", "Please provide the Total Head Count under Characteristics to start uploading EIDs.");
            }
            else{
                this.displayModal();
            }
        }
        linkContainer.append(this.link);
        return linkContainer;
    }

    updateModalLinkText = (updatedLinkText) =>{
        this.link.textContent = updatedLinkText;
    }


    displayModal = () =>{
        if(this.infoModal == null){
            let infoModal = new InfoModal("Upload EIDs for Sales Group", null, true);
            this.infoModal = infoModal;
            let eidsUploadersContainer = this.generateEidsUploadContainer();
            this.infoModal.getBody().append(eidsUploadersContainer);
        }
        else{
            this.infoModal.display();
            this.updateEidLimitMessage();
        }
    }

    generateEidsUploadContainer = () =>{
        let eidsUploadContainer = document.createElement("div");

        let requiredMessage = document.createElement("h6");
        requiredMessage.className = "col-md-12 text-primary font-italic";
        requiredMessage.textContent = "*Please select how you would like to upload the EIDs";
        eidsUploadContainer.append(requiredMessage);

        let eidLimitMessage = document.createElement("h6");
        eidLimitMessage.className = "col-md-12 text-primary font-italic";
        eidLimitMessage.id = "eid-limit-message";
        eidLimitMessage.textContent = "*Please provide at most " + this.getEidCountLimit() + " EIDs";
        eidsUploadContainer.append(eidLimitMessage);

        let uploadEidsManuallyCheckboxRow = document.createElement("div");
        uploadEidsManuallyCheckboxRow.className = "row d-flex m-2 p-2";
        let uploadEidsManuallyCheckbox = document.createElement("input");
        uploadEidsManuallyCheckbox.className = "checkbox m-1 p-1";
        uploadEidsManuallyCheckbox.type = "checkbox";
        uploadEidsManuallyCheckbox.id = "upload-eids-manually";
        uploadEidsManuallyCheckboxRow.append(uploadEidsManuallyCheckbox);
        let uploadEidsManuallyCheckboxText = document.createElement("label");
        uploadEidsManuallyCheckboxText.className = "m-1 p-1 text-primary";
        uploadEidsManuallyCheckboxText.htmlFor = "upload-eids-manually";
        uploadEidsManuallyCheckboxText.textContent = "Upload EIDs Manually";
        uploadEidsManuallyCheckboxRow.append(uploadEidsManuallyCheckboxText);
        eidsUploadContainer.append(uploadEidsManuallyCheckboxRow);

        let manualUploadInput = this.generateManualUploadInput();
        eidsUploadContainer.append(manualUploadInput);

        let enterEidSequenceCheckboxRow = document.createElement("div");
        enterEidSequenceCheckboxRow.className = "row d-flex m-2 p-2";
        let enterEidSequenceCheckbox = document.createElement("input");
        enterEidSequenceCheckbox.className = "checkbox m-1 p-1";
        enterEidSequenceCheckbox.type = "checkbox";
        enterEidSequenceCheckbox.id = "enter-eid-sequence";
        enterEidSequenceCheckboxRow.append(enterEidSequenceCheckbox);
        let enterEidSequenceCheckboxText = document.createElement("label");
        enterEidSequenceCheckboxText.className = "m-1 p-1 text-primary";
        enterEidSequenceCheckboxText.htmlFor = "enter-eid-sequence";
        enterEidSequenceCheckboxText.textContent = "Enter EID Tags Start and End Sequence Numbers";
        enterEidSequenceCheckboxRow.append(enterEidSequenceCheckboxText);
        eidsUploadContainer.append(enterEidSequenceCheckboxRow); 

        let eidSequenceUploadInput = this.generateEIDSequenceUploadInput();
        eidsUploadContainer.append(eidSequenceUploadInput);

        uploadEidsManuallyCheckbox.onchange = () =>{
            if(uploadEidsManuallyCheckbox.checked){
                enterEidSequenceCheckbox.checked = false;
                this.manualUploadInput.disabled = false;
                this.startSequenceInput.disabled = true;
                this.endSequenceInput.disabled = true;
            }
            else{
                this.manualUploadInput.disabled = true;
            }
        }

        enterEidSequenceCheckbox.onchange = () =>{
            if(enterEidSequenceCheckbox.checked){
                uploadEidsManuallyCheckbox.checked = false;
                this.startSequenceInput.disabled = false;
                this.endSequenceInput.disabled = false;
                this.manualUploadInput.disabled = true;
            }
            else{
                this.startSequenceInput.disabled = true;
                this.endSequenceInput.disabled = true;
            }
        }

        uploadEidsManuallyCheckbox.checked = true;
        $(uploadEidsManuallyCheckbox).trigger('change');

        this.statusMessage = document.createElement("p");
        this.statusMessage.style.display = "none";
        this.statusMessage.className = "mt-2 mb-0";
        eidsUploadContainer.append(this.statusMessage);
        this.errorMessage = document.createElement("p");
        this.errorMessage.style.display = "none";
        this.errorMessage.className = "mt-2 mb-0 alert alert-danger";
        eidsUploadContainer.append(this.errorMessage);

        let modalFooter = this.infoModal.getFooter();


        let resetButton = document.createElement("button");
        resetButton.className = "btn btn-secondary";
        resetButton.textContent = "Reset";
        resetButton.addEventListener("click", (e)=>{
            this.resetAllInputs();
        });
        modalFooter.prepend(resetButton);
    
        let submitButton = document.createElement("button");
        submitButton.className = "btn btn-primary";
        submitButton.textContent = "Save";
        submitButton.addEventListener("click", (e)=>{
            if(uploadEidsManuallyCheckbox.checked){
                this.saveManuallyUploadedEids(this.manualUploadInput.value);
            }
            else if(enterEidSequenceCheckbox.checked){
                this.saveEidsbySequence(this.startSequenceInput.value, this.endSequenceInput.value);
            }
        });
        modalFooter.prepend(submitButton);

        return eidsUploadContainer;
    }

    updateEidLimitMessage = () =>{
        let eidLimitMessage = document.getElementById("eid-limit-message");
        eidLimitMessage.textContent = "*Please provide at most " + this.getEidCountLimit() + " EIDs";
    }

    generateManualUploadInput = () =>{
        let manualUploadContainer = document.createElement("div");
        manualUploadContainer.className = "card m-2 p-2";

        let manualUploadContainerHeader = document.createElement("h6");
        manualUploadContainerHeader.className = "card-header m-1 p-1";
        manualUploadContainerHeader.textContent = "Please enter EIDs separated by commas";
        manualUploadContainer.append(manualUploadContainerHeader);

        let manualUploadContainerBody = document.createElement("div");
        manualUploadContainerBody.className = "card-body";
        this.manualUploadInput = document.createElement("textarea");
        this.manualUploadInput.rows = 7;
        this.manualUploadInput.cols = 100;
        this.manualUploadInput.className = "form-control d-block max-textarea";
        manualUploadContainerBody.append(this.manualUploadInput)
        manualUploadContainer.append(manualUploadContainerBody);
        return manualUploadContainer;
    }

    generateEIDSequenceUploadInput = () =>{
        let eidSequenceContainer = document.createElement("div");
        eidSequenceContainer.className = "card m-2 p-2";

        let eidSequenceContainerHeader = document.createElement("h6");
        eidSequenceContainerHeader.className = " card-header m-1 p-1";
        eidSequenceContainerHeader.textContent = "Please enter the Starting and Ending EID Tag Numbers";
        eidSequenceContainer.append(eidSequenceContainerHeader);

        let eidSequenceContainerBody = document.createElement("div");
        eidSequenceContainerBody.className = "card-body row";

        let startSequenceContainer = document.createElement("div");
        startSequenceContainer.className = "col-md-6 d-block";
        let startSequenceText = document.createElement("h6");
        startSequenceText.textContent = "Starting EID";
        startSequenceContainer.append(startSequenceText);
        this.startSequenceInput = document.createElement("input");
        this.startSequenceInput.className = "form-control";
        this.startSequenceInput.type = "number";
        this.startSequenceInput.min = 0;
        startSequenceContainer.append(this.startSequenceInput);
        eidSequenceContainerBody.append(startSequenceContainer);

        let endSequenceContainer = document.createElement("div");
        endSequenceContainer.className = "col-md-6 d-block";
        let endSequenceText = document.createElement("h6");
        endSequenceText.textContent = "Ending EID";
        endSequenceContainer.append(endSequenceText);
        this.endSequenceInput = document.createElement("input");
        this.endSequenceInput.className = "form-control";
        this.endSequenceInput.type = "number";
        this.endSequenceInput.min = 0;
        endSequenceContainer.append(this.endSequenceInput);
        eidSequenceContainerBody.append(endSequenceContainer);

        eidSequenceContainer.append(eidSequenceContainerBody);
        return eidSequenceContainer;
    }

    saveManuallyUploadedEids = (eids) =>{
        this.resetUploadedEids();
        let validList = true;
        if(eids.replace(/\s/g, '').length == 0){
            this.updateErrorMessage("Please provide EIDs to be uploaded", "d-block mt-2 mb-0 alert alert-danger");
            return;
        }
        let eidsList = eids.split(',');
        for(const eidString of eidsList){
            let formattedEidString = eidString.replace(/\s/g, '');
            if(formattedEidString.length < 15 || ! /^\d+$/.test(formattedEidString)){
                this.updateErrorMessage("Invalid EID format detected. Please check the uploaded EIDs", "d-block mt-2 mb-0 alert alert-danger");
                validList = false;
            }
        }
        if(validList && this.validateEidUploadCount(eidsList.length)){
            for(let eidString of eidsList){
                let formattedEidString = eidString.replace(/\s/g, '');
                this.eids.push(parseInt(formattedEidString));
                this.updateErrorMessage("", "d-none");
                this.updateModalLinkText("Uploaded " + this.eids.length + " EID(s)");
                this.closeEidUploadModal();
            }
        }
    }

    saveEidsbySequence = (start, end) =>{
        this.resetUploadedEids();
        if(start.length < 15 || ! /^\d+$/.test(start) || end.length < 15 || ! /^\d+$/.test(end)){
            this.updateErrorMessage("Invalid format for Start or End Tag Number","d-block mt-2 mb-0 alert alert-danger");
        }
        else{
            let startNumber = parseInt(start.replace(/\s/g, ''));
            let endNumber = parseInt(end.replace(/\s/g, ''));
            if(startNumber > endNumber){
                this.updateErrorMessage("Start Number cannot be greater than End Number", "d-block mt-2 mb-0 alert alert-danger");
            }
            else if(this.validateEidUploadCount(endNumber - startNumber + 1)){
                while(startNumber <= endNumber){
                    this.eids.push(startNumber);
                    startNumber++;
                }
                this.updateErrorMessage("", "d-none");
                this.updateModalLinkText("Uploaded " + this.eids.length + "EID(s)");
                this.closeEidUploadModal();
            }
        }
    }

    setEidCountLimit = (eidCountLimit) =>{
        this.eidCountLimit = eidCountLimit;
    }

    getEidCountLimit = () =>{
        return this.eidCountLimit;
    }

    displayEidUploadModal = () =>{
        this.infoModal.display();
    }

    closeEidUploadModal = () =>{
        this.infoModal.close();
    }

    getUploadedEids = () =>{
        return this.eids;
    }

    resetUploadedEids = () =>{
        this.eids = [];
    }

    resetAllInputs = () =>{
        this.manualUploadInput.value = "";
        this.startSequenceInput.value = "";
        this.endSequenceInput.value = "";
        this.eids = [];
        this.updateErrorMessage("", "d-none");
        this.updateModalLinkText("Upload EIDs for Sales Group");
    }

    updateErrorMessage = (errorMessageText, errorMessageClass) =>{
        this.errorMessage.textContent = errorMessageText;
        this.errorMessage.className = errorMessageClass;
    }

    generateModalWithMessage = (modalHeader, messageText) =>{
        let messageModal = new InfoModal(modalHeader, null, true)
        let messageContainer = document.createElement("div");
        let message = document.createElement("h6");
        message.textContent = messageText;
        messageContainer.append(message);
        messageModal.getBody().append(messageContainer);
    }

    validateEidUploadCount = (uploadedEidsCount) =>{
        if(uploadedEidsCount > parseInt(this.getEidCountLimit())){
            this.updateErrorMessage("Please provide upto " + this.getEidCountLimit() + " EIDs. Current EID count is " + uploadedEidsCount, "d-block mt-2 mb-0 alert alert-danger");
            return false;
        }
        if(uploadedEidsCount < parseInt(this.getEidCountLimit())){
            this.generateModalWithMessage("EID Upload", "You have uploaded " + uploadedEidsCount + " EIDs. " + (this.getEidCountLimit() - uploadedEidsCount) + " head(s) of cattle will remain untracked.");
            return true;
        }
        return true;
    }
}