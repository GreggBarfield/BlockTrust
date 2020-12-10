export class ProgressBar {
    constructor (attachTo=null) {
        this.progress = 0;
        this.frame = null;
        this.box = document.createElement("div");
        this.box.className = "progress";
        this.bar = document.createElement("div");
        this.bar.className = "progress-bar";
        this.bar.setAttribute("role", "progressbar");
        this.bar.setAttribute("aria-valuemin", "0");
        this.bar.setAttribute("aria-valuemax", "100");
        this.box.append(this.bar);

        this.setProgress(0);

        if (attachTo !== null) {
            this.attach(attachTo);
        }
    }

    setProgress(currentProgress, lower=0, upper=1) {
        let range = upper - lower;
        if (range == 0) {
            this.progress = 1;
        }
        else if (range < 0) {
            throw "Range is less than 0";
        }
        else {
            this.progress = lower + (currentProgress - lower) / range;
        }
        if (this.progress <= 0) {
            this.progress = 0;
        }
        else if (this.progress >= 1) {
            this.progress = 1;
        }
        this.render();
    }

    render() {
        if (this.frame !== null) {
            let percentProgress = Math.floor(100 * this.progress);
            this.bar.setAttribute("aria-valuenow", percentProgress);
            let percentProgressStr = percentProgress + "%";
            this.bar.style.width = percentProgressStr;
            this.bar.textContent = percentProgressStr;
        }
    }

    show() {
        this.box.style.display = "block";
    }

    hide() {
        this.box.style.display = "none";
    }

    attach(attachTo) {
        if (this.frame !== null) {
            this.detach();
        }
        this.frame = attachTo;
        this.frame.append(this.box);
        this.render();
    }

    detach() {
        if (this.frame !== null) {
            this.box.remove();
        }
        this.frame = null;
    }

    destroy() {
        this.detach();
    }
}
