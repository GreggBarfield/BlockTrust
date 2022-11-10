export class AsyncForm {
    constructor(options) {
        this.form = options.form;
        this.error = options.error;
        this.status = options.status;
        this.loadingMessage = options.loadingMessage;
        this.action = options.action;
        this.redirectMessage = options.redirectMessage;
        this.submitting = false;
        this.onFinished = options.onFinished;
        this.getData = options.getData;
        this.asJSON = options.asJSON;
        this.requestRedirectTo = options.requestRedirectTo;
        this.reCaptcha =  "reCaptcha" in options? options.reCaptcha : false;
        this.reCaptchaAction = "reCaptchaAction" in options? options.reCaptchaAction : "submit";
        this.reCaptchaSiteKey = "reCaptchaSiteKey" in options? options.reCaptchaSiteKey: "";
        this.bindHandlers();
    }

    bindHandlers() {
        let that = this;
        this.form.addEventListener("submit", function(e) {
            e.preventDefault();       
            if (that.reCaptcha) {
                grecaptcha.ready(function() {
                    grecaptcha.execute(that.reCaptchaSiteKey, {action: that.reCaptchaAction}).then(function(token) {
                        that.submit(token);
                    });
                  });
            }
            else {
                that.submit();
            }
        });
    }

    clearStatus() {
        this.status.style.display = "none";
    }

    setStatus(message) {
        this.status.style.display = "block";
        this.status.textContent = message;
    }

    clearError() {
        this.error.style.display = "none";

    }

    setError(message) {
        this.error.style.display = "block";
        this.error.textContent = message;
    }

    submit(token="") {
        if (this.submitting) {
            return;
        }
        this.submitting = true;

        this.clearError();
        this.setStatus(this.loadingMessage);

        let that = this;

        let postOptions = {
            url: this.action,
            data: undefined
        };

        try {
            postOptions.data = this.getData();
            if (token != "") {
                postOptions.data.token = token
            }
        }
        catch(e) {
            console.log(e);
            this.clearStatus();
            this.setError("An error occurred before submitting data: " + e + " (" + e.message + ")");
            return;
        }

        
        if (this.asJSON !== undefined && this.asJSON) {
            postOptions.data = JSON.stringify(postOptions.data);
            postOptions.contentType = "application/json";
        }

        if (this.requestRedirectTo) {
            postOptions.data.requestRedirectTo = this.requestRedirectTo;
        }

        let csrfTokenElement = this.form.querySelector("#csrf_token");
        if (csrfTokenElement !== null) {
            postOptions.headers = {"X-CSRFToken": csrfTokenElement.value}
        }

        $.post(postOptions)
            .always(function(){
                that.clearStatus();
                that.submitting = false;
            })
            .done(function(data){
                try {
                    if ('error' in data) {
                        that.setStatus(data.error);
                    }
                    if ('redirect' in data) {
                        if (that.redirectMessage !== undefined) {
                            that.setStatus(that.redirectMessage);
                        }
                        location.replace(data.redirect);
                    }
                    if (that.onFinished !== undefined) {
                        that.onFinished(data);
                    }
                }
                catch(e) {
                    that.setError("An error occurred: " + e);
                }
            })
            .fail(function(xhr, status){
                try {
                    let data = JSON.parse(xhr.responseText);
                    if ("error" in data) {
                        that.setError(data.error);
                    }
                    else {
                        throw "Nope";
                    }
                }
                catch {
                    that.setError("An error occurred: " + status + ", " + xhr.status + ", " + xhr.responseText);
                }
            });

    }
}