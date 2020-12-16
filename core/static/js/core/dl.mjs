export class DL {
    constructor(asCols, attachTo) {
        this.asCols = asCols;
        this.dl = document.createElement("dl");
        attachTo.append(this.dl);

        if (this.asCols) {
            this.dl.className = "row";
        }
    }

    add(key, value) {
        let dt = document.createElement("dt");
        let dd = document.createElement("dd");
        dt.textContent = key;
        dd.textContent = value;
        if (this.asCols) {
            dt.className = "col-12 col-md-6";
            dd.className = "col-12 col-md-6";
        }
        this.dl.append(dt);
        this.dl.append(dd);
    }
}
