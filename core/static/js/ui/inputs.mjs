export class FormGroup {
    /**
     * Constructs FormGroup.
     * 
     * @param {Node} attachTo Where to put the DOM elements
     * @param {string} label The label text
     */
    constructor(attachTo, label) {
        this._form_group = document.createElement("div");
        this._form_group.classList.add("form-group");
        attachTo.appendChild(this._form_group);
        this._input_id = "domuid" + window.DOMUIDNext++;
        this._label = document.createElement("label");
        this._label.htmlFor = this._input_id;
        this._label.textContent = label;
        this._form_group.appendChild(this._label);
    }

    /**
     * Gets the form group DOM node.
     * 
     * @return {Node} The div element with class form-group
     */
    getFormGroup() {
        return this._form_group;
    }
    getFormLabel(){
        return this._label;
    }
}

export class DateFormGroup extends FormGroup {
    /**
     * Constructs DateFormGroup.
     * 
     * @param {Node} attachTo Where to put the DOM elements
     * @param {string} label The label text
     * @param {number} [unixTime] the unix time to default to
     */
    constructor(attachTo, label, input_id, unixTime=null) {
        super(attachTo, label);

        this._input = document.createElement("input");
        this._input.id = input_id;
        this._input.type = "date";
        this._input.className = "form-control";

        if (unixTime !== null && unixTime >= 0) {
            let d = new Date(unixTime * 1000);
            function setWidth(val) {
                if (val < 10)
                    return "0" + val;
                return val;
            }
            this._input.value = d.getFullYear() + "-" + setWidth(d.getMonth() + 1) + "-" + setWidth(d.getDate());
        }

        this._form_group.appendChild(this._input);
    }

    /**
     * Gets the time set.
     * 
     * @return {number|null} The time set or null (for various reasons)
     */
    getTime() {
        if (
            this._input.value === undefined ||
            this._input.value === "" ||
            this._input.value === null
        ) {
            return null;
        }
        let values = this._input.value.split("-");
        let d = new Date(values[0], values[1] - 1, values[2]);
        return Math.floor(d.getTime() / 1000);
    }
}

export class DateRangeFormGroup extends FormGroup {
    /**
     * Constructs DateFormGroup.
     * 
     * @param {Node} attachTo Where to put the DOM elements
     * @param {string} label The label text
     * @param {number} [unixTime] the unix time to default to
     */
    constructor(attachTo, label, startUnixTime=null, endUnixTime=null) {
        super(attachTo, label);
        this._inputGroup = document.createElement("div");
        this._inputGroup.className = "input-group";

        this._startDateInput = document.createElement("input");
        this._startDateInput.id = this._input_id;
        this._startDateInput.type = "date";
        this._startDateInput.className = "form-control col-md-5";

        this._text = document.createElement("p");
        this._text.textContent = "TO";
        this._text.className = "form-control col-md-2";

        this._endDateInput = document.createElement("input");
        this._endDateInput.id = this._input_id;
        this._endDateInput.type = "date";
        this._endDateInput.className = "form-control col-md-5 text-justify";

        this._inputGroup.appendChild(this._startDateInput);
        this._inputGroup.appendChild(this._text);
        this._inputGroup.appendChild(this._endDateInput);

        if (startUnixTime !== null && startUnixTime >= 0) {
            let d = new Date(startUnixTime * 1000);
            function setWidth(val) {
                if (val < 10)
                    return "0" + val;
                return val;
            }
            this._startDateInput.value = d.getFullYear() + "-" + setWidth(d.getMonth() + 1) + "-" + setWidth(d.getDate());
        }
        if (endUnixTime !== null && endUnixTime >= 0) {
            let d = new Date(endUnixTime * 1000);
            function setWidth(val) {
                if (val < 10)
                    return "0" + val;
                return val;
            }
            this._endDateInput.value = d.getFullYear() + "-" + setWidth(d.getMonth() + 1) + "-" + setWidth(d.getDate());
        }

        this._form_group.appendChild(this._inputGroup);
    }

    /**
     * Gets the time set.
     * 
     * @return {number|null} The time set or null (for various reasons)
     */
    getStartTime() {
        if (
            this._startDateInput.value === undefined ||
            this._startDateInput.value === "" ||
            this._startDateInput.value === null
        ) {
            return null;
        }
        let values = this._startDateInput.value.split("-");
        let d = new Date(values[0], values[1] - 1, values[2]);
        return Math.floor(d.getTime() / 1000);
    }
    getEndTime() {
        if (
            this._endDateInput.value === undefined ||
            this._endDateInput.value === "" ||
            this._endDateInput.value === null
        ) {
            return null;
        }
        let values = this._endDateInput.value.split("-");
        let d = new Date(values[0], values[1] - 1, values[2]);
        return Math.floor(d.getTime() / 1000);
    }
}
