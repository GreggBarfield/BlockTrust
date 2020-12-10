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
                    progress(perc);
                }
            }, false);
            return x;
        },
        data: formData
    })
    .done(function(data, status){
        if (typeof progress == "function") {
            progress(1);
        }
        return Promise.resolve(true);
    })
    .fail(function(xhr, status, err){
        if (typeof fail == "function") {
            throw "error during post: " + status + " " + err + "<br>" + 
                "The specific error returned was: " + xhr.responseText;
        }
    });
}

export function uploadFile(userOwns, accountOwns, file, progress=null) {
    let dataResult = null;
    return $.ajax({
        url: "/widgets/data",
        data: JSON.stringify({
            "action": "get_upload_config",
            "params": {
                "user_owns": userOwns === true,
                "account_owns": accountOwns === true,
                "file_name": file.name
            }
        }),
        contentType: 'application/json',
        method: "POST"
    })
        .done(function (data) {
            dataResult = data;
            return uploadFileToS3(data["config"], file, progress);
        })
        .fail(function (jqXHR, textStatus) {
            throw "HTTP error " + jqXHR.status + " " + textStatus + ": " + jqXHR.responseText;
        })
        .then(function(){
            return Promise.resolve(dataResult["id"]);
        });
}
