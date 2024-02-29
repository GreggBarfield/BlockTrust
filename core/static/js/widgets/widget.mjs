import { ajax, NetworkError } from '../core/network.mjs';
import { spinner } from '../ui/spinner.mjs';

// onAllDataLoaded removed and onSomeDataLoaded deprecated;
// use https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/any
// or the all (or allSettled) versions

export class Widget {
    constructor(frame) {
        this.frame = frame;
        this.totalDataLoaded = 0;
        this.totalDataRequested = 0;
        this.queuedDataRequests = [];
        this.instantProcessDataRequests = false;
        //this.type = frame.getAttribute("data-widget-type");
        this.frame.innerHTML = spinner;
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
            const promiseResolve = dataRequest.promiseResolve;
            const promiseError = dataRequest.promiseError;
            const suppressErrors = dataRequest.suppressErrors;
            const method = dataRequest.method;
            let that = this;
            let requestParams = {
                url: "/widgets/data/" + action,
                contentType: 'application/json',
                method: method
            };
            if(["POST", "PUT"].includes(method)){
                requestParams.data = JSON.stringify(params);
            }
            else{
                for(let p of params){
                    requestParams.url += `/${p}`
                }
            }
            ajax(requestParams)
                .then((networkResult) => {
                    if ('onSomeDataLoaded_bind' in that && that.onSomeDataLoaded_bind) {
                        that.onSomeDataLoaded_bind();
                        that.onSomeDataLoaded_bind = null;
                    }
                    that.totalDataLoaded += 1;
                    promiseResolve(networkResult.data);
                })
                .catch((error) => {
                    let errorMessage = error.toString();
                    if (!suppressErrors) {
                        that.displayError(errorMessage);
                    }
                    promiseError(error);
                });
        }
        this.queuedDataRequests = [];
    }

    getData(action, params={}, suppressErrors=false, method="POST") {
        this.totalDataRequested += 1;
        let promiseResolve, promiseError;
        let promise = new Promise((resolve, error)=>{
            promiseResolve = resolve;
            promiseError = error;
        });
        this.queuedDataRequests.push({
            action: action,
            params: params,
            promiseResolve: promiseResolve,
            promiseError: promiseError,
            suppressErrors: suppressErrors,
            method: method
        });
        if (this.instantProcessDataRequests) {
            this.processQueuedDataRequests();
        }
        return promise;
    }

    onSomeDataLoaded(callback) {
        if (this.totalDataLoaded > 0) {
            callback();
        }
        else {
            this.onSomeDataLoaded_bind = callback;
        }
    }
}
