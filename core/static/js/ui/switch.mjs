export class Switch {
    /**
     * Construct Switch.
     * 
     * @param {Node} attachTo Where to place DOM elements
     * @param {boolean|number} checked Whether the switch is checked
     * @param {string} [switch_class] The style class (default success)
     */
    constructor(attachTo, checked, switch_class="success") {

        let publishSwitchRegion = document.createElement("div");
        publishSwitchRegion.className = "switch switch-" + switch_class + " d-inline";
        attachTo.append(publishSwitchRegion);

        let publishSwitchInput = document.createElement("input");
        publishSwitchInput.className = "";
        publishSwitchInput.type = "checkbox";
        publishSwitchInput.id = "sw" + (window.DOMUIDNext++);
        let checkedSafe = false;
        if (typeof checked == "number") {
            checkedSafe = checked !== 0;
        }
        else if (typeof checked == "boolean") {
            checkedSafe = checked;
        }
        else {
            throw "Unable to decipher whether to check checkbox";
        }
        publishSwitchInput.checked = checkedSafe;
        publishSwitchRegion.append(publishSwitchInput);

        let publishSwitchLabel = document.createElement("label");
        publishSwitchLabel.className = "cr";
        publishSwitchLabel.htmlFor = publishSwitchInput.id;
        publishSwitchRegion.append(publishSwitchLabel);
    
        this._input = publishSwitchInput;
    }

    isChecked() {
        return this._input.checked;
    }
}


export class SwitchFormGroup {
    /**
     * Constructs SwitchFormGroup.
     * 
     * @param {Node} attachTo Where to place DOM elements
     * @param {string} label A label for the switch
     * @param {boolean|number} checked Whether the switch is checked
     * @param {string} [switch_class] The style class (default success)
     */
    constructor(attachTo, label, checked, switch_class="success") {
        let publishFormGroup = document.createElement("div");
        publishFormGroup.className = "form-group";
        attachTo.append(publishFormGroup);

        let publishSwitchRegion = document.createElement("div");
        publishSwitchRegion.className = "switch switch-" + switch_class + " d-inline m-r-10";
        publishFormGroup.append(publishSwitchRegion);

        let publishSwitchInput = document.createElement("input");
        publishSwitchInput.className = "";
        publishSwitchInput.type = "checkbox";
        publishSwitchInput.id = "sw" + (window.DOMUIDNext++);
        let checkedSafe = false;
        if (typeof checked == "number") {
            checkedSafe = checked !== 0;
        }
        else if (typeof checked == "boolean") {
            checkedSafe = checked;
        }
        else {
            throw "Unable to decipher whether to check checkbox";
        }
        publishSwitchInput.checked = checkedSafe;
        publishSwitchRegion.append(publishSwitchInput);

        let publishSwitchLabel = document.createElement("label");
        publishSwitchLabel.className = "cr";
        publishSwitchLabel.htmlFor = publishSwitchInput.id;
        publishSwitchRegion.append(publishSwitchLabel);

        let publishSwitchLabelLabel = document.createElement("label");
        publishSwitchLabelLabel.htmlFor = publishSwitchInput.id;
        publishSwitchLabelLabel.textContent = label;
        publishFormGroup.append(publishSwitchLabelLabel);

        this._input = publishSwitchInput;
    }

    isChecked() {
        return this._input.checked;
    }
}