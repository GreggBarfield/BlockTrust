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
    constructor(attachTo, label, unixTime=null) {
        super(attachTo, label);

        this._input = document.createElement("input");
        this._input.id = this._input_id;
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
