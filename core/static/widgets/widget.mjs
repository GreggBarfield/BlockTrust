export class Widget {
    constructor(frame) {
        this.frame = frame;
        this.totalDataLoaded = 0;
        this.totalDataRequested = 0;
        this.queuedDataRequests = [];
        this.instantProcessDataRequests = false;
        this.type = frame.getAttribute("data-widget-type");

        this.frame.innerHTML = '\
            <div class="d-flex justify-content-center">\
                <div class="spinner-border" role="status">\
                    <span class="sr-only">Loading...</span>\
                </div>\
            </div>';
    }

    init() {
        try {
            this.initType();
            this.processQueuedDataRequests();
            this.instantProcessDataRequests = true;
        }
        catch (err) {
            this.displayError("in initType, error: " + err);
            console.log(err);
        }
    }

    displayError(message) {
        this.frame.innerHTML = '';
        let errorElement = document.createElement("div");
        errorElement.setAttribute("class", "alert alert-danger");
        errorElement.appendChild(document.createTextNode(
            "Error in widget: " + message
        ));
        this.frame.appendChild(errorElement);
    }

    processQueuedDataRequests() {
        for (const dataRequest of this.queuedDataRequests) {
            const action = dataRequest.action;
            const params = dataRequest.params;
            const callback = dataRequest.callback;
            let that = this;
            let data = {
                action: action,
                params: params
            };
            $.ajax({
                url: "/widgets/data",
                data: JSON.stringify(data),
                contentType: 'application/json',
                method: "POST"
            })
                .done(function (data) {
                    if ('onSomeDataLoaded_bind' in that && that.onSomeDataLoaded_bind) {
                        that.onSomeDataLoaded_bind();
                        that.onSomeDataLoaded_bind = null;
                    }
                    that.totalDataLoaded += 1;
                    callback(data);
                    if ('onAllDataLoaded_bind' in that && that.onAllDataLoaded_bind && that.totalDataLoaded == that.totalDataRequested) {
                        that.onAllDataLoaded_bind();  // Make sure to set this at the VERY END of all data requests
                        that.onAllDataLoaded_bind = null;
                    }
                })
                .fail(function (jqXHR, textStatus) {
                    that.displayError("HTTP error " + jqXHR.status + " " + textStatus + ": " + jqXHR.responseText);
                });
        }
        this.queuedDataRequests = [];
    }

    getData(action, params, callback) {
        this.totalDataRequested += 1;
        this.queuedDataRequests.push({
            action: action,
            params: params,
            callback: callback
        });
        if (this.instantProcessDataRequests) {
            this.processQueuedDataRequests();
        }
    }

    onSomeDataLoaded(callback) {
        if (this.totalDataLoaded > 0) {
            callback();
        }
        else {
            this.onSomeDataLoaded_bind = callback;
        }
    }

    onAllDataLoaded(callback) {
        if (this.totalDataLoaded == this.totalDataRequested) {
            callback();
        }
        else {
            this.onAllDataLoaded_bind = callback;
        }
    }
}
