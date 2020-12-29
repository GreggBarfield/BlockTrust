export class SwitchFormGroup {
    /**
     * Constructs SwitchFormGroup.
     * 
     * @param {Node} attachTo Where to place DOM elements
     * @param {string} label A label for the switch
     * @param {boolean|number} checked Whether the switch is checked
     */
    constructor(attachTo, label, checked) {
        let publishFormGroup = document.createElement("div");
        publishFormGroup.className = "form-group";
        attachTo.append(publishFormGroup);

        let publishSwitchRegion = document.createElement("div");
        publishSwitchRegion.className = "switch switch-success d-inline m-r-10";
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