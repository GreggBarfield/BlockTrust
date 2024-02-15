import {AsyncForm} from '/static/global/async_form.mjs';

document.addEventListener('DOMContentLoaded', function() {
    let breedsList = [];
    for(let breed of breeds){
        breedsList.push({id: breed.value, text:breed.value});
    }
    $("#animal-breed").select2({data: breedsList, placeholder: "Select Breed"});
    $("#genetics-kit-breed").select2({data: breedsList, placeholder: "Select Breed"});
});

let geneticsForm = $("#genetics-form");
let eid = geneticsForm.find("#eid");
let geneticsUid = geneticsForm.find("#genetics-uid");
let animalBreed = geneticsForm.find("#animal-breed");
let geneticsKitBreed = geneticsForm.find("#genetics-kit-breed");
let statusMessage = geneticsForm.find("#status_message");
let errorMessage = geneticsForm.find("#error_message");


let form = new AsyncForm({
    action: window.location.href,
    form: geneticsForm[0],
    status: statusMessage[0],
    error: errorMessage[0],
    redirectMessage: "Uploaded Data!",
    loadingMessage: "Uploading...",
    getData: () => {
        return {
            eid: eid.val(),
            genetics_uid: geneticsUid.val(),
            animal_breed: animalBreed.val(),
            genetics_kit_breed: geneticsKitBreed.val()
        };
    }
});