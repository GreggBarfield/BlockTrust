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
        this.bindHandlers();
    }

    bindHandlers() {
        let that = this;
        this.form.addEventListener("submit", function(e) {
            e.preventDefault();
            that.submit();
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

    submit() {
        if (this.submitting) {
            return;
        }
        this.submitting = true;

        this.clearError();
        this.setStatus(this.loadingMessage);

        let that = this;

        $.post({
            url: this.action,
            data: this.getData()
        })
            .always(function(){
                that.clearStatus();
                that.submitting = false;
            })
            .done(function(data){
                try {
                    if ('error' in data) {
                        that.setError(data.error);
                    }
                    if ('redirect' in data) {
                        if (that.redirectMessage !== undefined) {
                            that.setStatus(that.redirectMessage);
                        }
                        location.replace(data.redirect);
                    }
                    if (that.onFinished !== undefined) {
                        that.onFinished();
                    }
                }
                catch(e) {
                    that.setError("An error occurred: " + e);
                }
            })
            .fail(function(xhr, status){
                that.setError("An error occurred: " + status + ", " + xhr.status + ", " + xhr.responseText);
            });

    }
}