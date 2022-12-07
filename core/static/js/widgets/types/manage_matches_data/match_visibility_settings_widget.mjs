import { Widget } from '../../widget.mjs';
import { Switch } from '../../../ui/switch.mjs';
import { ajax } from '../../../core/network.mjs';

export class MatchVisibilitySettingsWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        Promise.all([
            this.getData(
                "get_account_type_visibilities",
                {},
            ).then((data)=>{
                this.type_visibilities = data.type_visibilities;
            }),

            this.getData(
                "direct/match_types_id_to_name",
                {}
            ).then((data) => {
                this.match_types_id_to_name = data.match_types_id_to_name;
            }),
        ]).then(() => {
            this.frame.innerHTML = "";

            this.type_visibilities_local = {};
            this.typeSwitches = {};

            for (const match_type_id in this.match_types_id_to_name) {
                this.type_visibilities_local[match_type_id] = false;
            }

            for (const type_visibility of this.type_visibilities) {
                if (type_visibility.visibility) {
                    this.type_visibilities_local[type_visibility.type] = true;
                }
            }

            this.render();
        });
    }

    /**
     * Generates the UI and attaches actions.
     */
    render() {
        
        const match_descriptions = {
            "Sighting": "Cow was sighted",
            "Born": "Cow was born",
            "Died": "Cow died",
            "Sold": "Cow was sold",
            "Medical": "Cow had medicine applied",
            "Packer": "Cow was packed by this packer",

        };

        let form = document.createElement("form");
        let itemsFormGroup = document.createElement("div");
        itemsFormGroup.className = "form-group";
        {
            let itemsLabel = document.createElement("label");
            itemsLabel.textContent = "Match type block controls:";
            itemsFormGroup.append(itemsLabel);


            let items = document.createElement("div");
            items.className = "form-row match-types-privacy-panel";
            itemsFormGroup.append(items);
    
            for (const match_type_id in this.match_types_id_to_name) {
                const match_type_name = this.match_types_id_to_name[match_type_id];
    
                let item = document.createElement("div");
                item.className = "col-md-3";
    
                let itemc = document.createElement("div");
                item.append(itemc);
    
                let top_section = document.createElement("top-section");
                {
                    let header = document.createElement("header");
                    header.textContent = match_type_name;
                    top_section.append(header);
        
                    let element_id = document.createElement("id");
                    element_id.textContent = match_type_id;
                    top_section.append(element_id);
        
                    if (match_type_name in match_descriptions) {
                        let description = document.createElement("description");
                        description.textContent = match_descriptions[match_type_name];
                        top_section.append(description);
                    }
                }
                itemc.append(top_section);
    
                let warning = document.createElement("warning");
                itemc.append(warning);
    
                let warning_span = document.createElement("span");
                warning_span.textContent = "Block all public access: ";
                warning.append(warning_span);
    
                this.typeSwitches[match_type_id] = new Switch(
                    warning,
                    !this.type_visibilities_local[match_type_id],
                    "danger"
                );
    
                items.append(item);
            }
        }
        form.append(itemsFormGroup);

        let submitFormGroup = document.createElement("div");
        submitFormGroup.className = "form-group";
        {
            let submit = document.createElement('button');
            submit.type = "button";
            submit.className = "btn btn-primary";
            submit.textContent = "Update Block Settings";
            submit.addEventListener("click", ()=>{this.submit();});
            this.submitButton = submit;
            submitFormGroup.append(submit);
        }
        form.append(submitFormGroup);

        this.frame.append(form);
    }

    submit() {
        let visibilitySettings = {};

        for (const match_type_id in this.typeSwitches) {
            visibilitySettings[this.match_types_id_to_name[match_type_id]] =
                !this.typeSwitches[match_type_id].isChecked();
        }

        this.submitButton.disabled = true;
        this.submitButton.textContent = "Saving...";

        ajax({
            method: 'POST',
            url: '/widgets/data/update_match_visibility_settings',
            contentType: 'application/json',
            data: JSON.stringify({
                'visibility_settings': visibilitySettings
            }),
        })
        .then(() => {
            let alert = document.createElement("div");
            alert.className = "alert alert-success";
            alert.textContent = "Settings saved!";
            this.frame.append(alert);

            this.submitButton.textContent = "Saved";
        })
        .catch((err) => {
            let alert = document.createElement("div");
            alert.className = "alert alert-danger";
            alert.textContent = err;
            this.frame.append(alert);
            this.submitButton.textContent = "Save failed";
        })
        .finally(()=>{
            this.submitButton.disabled = false;
        });
    }

}
