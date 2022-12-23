function uploadFileToS3(config, file, progress=null) {
    let formData = new FormData();

    for (const fieldName in config["fields"]) {
        formData.append(fieldName, config["fields"][fieldName]);
    }

    formData.append("file", file);

    return $.ajax({
        type: "POST",
        url: config["url"],
        contentType: false,
        processData: false,
        xhr: function() {
            let x = new XMLHttpRequest();
            x.upload.addEventListener("progress", function(e){
                if (e.lengthComputable) {
                    let perc = 1;
                    if (e.total != 0) {
                        perc = e.loaded / e.total;
                    }
                    if (perc > 0.98) {
                        perc = 0.98;
                    }
                    if (progress != null) {
                        progress(perc);
                    }
                }
            }, false);
            return x;
        },
        data: formData
    })
    .fail(function(xhr, status, err){
        if (typeof fail == "function") {
            throw "error during post: " + status + " " + err + "<br>" + 
                "The specific error returned was: " + xhr.responseText;
        }
    })
    .then(function(data, status){
        if (typeof progress == "function") {
            progress(1);
        }
        return Promise.resolve(true);
    });
}

export function saveAndUploadFile(userOwns, accountOwns, file, questionId=null, progress=null) {
    let dataResult = null;
    return $.ajax({
        url: "/widgets/data/save_file_and_get_upload_config",
        data: JSON.stringify({
            "user_owns": userOwns === true,
            "account_owns": accountOwns === true,
            "file_name": file.name,
            "question_id": questionId
        }),
        contentType: 'application/json',
        method: "POST"
    })
        .fail(function (jqXHR, textStatus) {
            throw "HTTP error " + jqXHR.status + " " + textStatus + ": " + jqXHR.responseText;
        })
        .then(function (data) {//note: done() and then() are NOT even close to similar, done() does not respect returned promises
            dataResult = data;
            return uploadFileToS3(data["config"], file, progress);
        })
        .then(function(){
            return Promise.resolve(dataResult["id"]);
        });
}
