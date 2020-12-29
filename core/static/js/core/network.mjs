class NetworkResult {
    constructor(data, jqXHR) {
        this.data = data;
        this.jqXHR = jqXHR;
    }
}

/**
 * Represents a network error.
 */
export class NetworkError extends Error {
    constructor(jqXHR) {
        super();
        this.jqXHR = jqXHR;
        this.message = this.getHumanReadable();
    }

    getHumanReadable() {
        let error = "HTTP " + this.jqXHR.status + ":";

        try {

            let contentType = this.jqXHR.getResponseHeader("Content-Type");
            if (contentType === null) {
                contentType = "";
            }

            if (contentType.includes("json")) {
                let o = JSON.parse(this.jqXHR.responseText);

                if ('short' in o) {
                    error += " " + o.short;
                }

                error += " (full error: " + this.jqXHR.responseText + ")";
            }
            else if (contentType.includes("html")) {
                error += " Uncommon error. Contact us to get help. \
                    (Additional debugging in console)";
                let token = "displayLastError";
                let func = () => {
                    let iframe = document.createElement("iframe");
                    iframe.style = "position:fixed;left:20px;top:20px;\
                        width:calc(100% - 40px);height:calc(100% - 40px);\
                        background-color:white;z-index:10001;";
                    document.body.append(iframe);
                    let cd = iframe.contentDocument;
                    cd.open();
                    cd.writeln(this.jqXHR.responseText);
                    cd.close();
                    let closeDiv = document.createElement("div");
                    closeDiv.style = "position:fixed;left:0px;top:0px;\
                        width:100%;height:100%;z-index:10000";
                    closeDiv.addEventListener("click", ()=>{
                        closeDiv.remove();
                        iframe.remove();
                    });
                    document.body.append(closeDiv);
                }
                window[token] = func;
                console.log("Call window." + token + " to see error GUI");
            }
            else {
                error += " " + this.jqXHR.responseText;
            }
        }
        catch(e) {
            error += " " + this.jqXHR.responseText;
            error += " (additionally, an error occurred while generating this: " + e + ") ";
        }

        return error;
    }
}

/**
 * Calls jQuery ajax with the passed parameters. Wraps results with a true Promise.
 * 
 * @param {object} settings Passed to jQuery.ajax
 * @returns {Promise} A true Promise
 */
export let ajax = (settings) => {
    return new Promise((resolve, reject) => {
        $.ajax(settings)
            .done((data, textStatus, jqXHR) => {
                resolve(new NetworkResult(data, jqXHR));
            })
            .fail((jqXHR, textStatus, errorThrown) => {
                reject(new NetworkError(jqXHR));
            });
    });
}
