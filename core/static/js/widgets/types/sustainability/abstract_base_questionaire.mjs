import { Widget } from "../../widget.mjs";
import { ProgressBar } from "../../../core/progress_bar.mjs";
import { AsyncForm } from "../../../../global/async_form.mjs";

export class AbstractBaseQuestionaireWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    selectSection = {};
    submitResponse = {};

    generate(formInfo, sections) {
        function createOption(input, value, text) {
            let option = document.createElement("option");
            option.value = value;
            option.textContent = text;
            input.append(option);
            return option;
        }

        function createQuestion(card, id, question, a, b, c) {
            let row = document.createElement("div");
            row.className = "form-row";
            card.append(row);

            let group = document.createElement("div");
            group.className = "form-group col-md-12";
            row.append(group);

            let label = document.createElement("label");
            label.textContent = question;
            group.append(label);

            let input = document.createElement("select");
            input.className = "form-control";
            input.id = id;
            group.append(input);

            createOption(input, "Any", "Please Choose");
            createOption(input, id + "a", a);
            createOption(input, id + "b", b);
            if (c != "") {
                createOption(input, id + "c", c);
            }
            return input;
        }

        function createSection(header, name, form) {
            let card = document.createElement("div");
            card.className = "card";

            let cardHeader = document.createElement("div");
            cardHeader.className = "card-header";
            card.append(cardHeader);

            let cardHeaderText = document.createElement("div");
            cardHeaderText.className = "h4";
            cardHeaderText.textContent = header;
            cardHeader.append(cardHeaderText);

            let cardBody = document.createElement("div");
            cardBody.className = "card-body";
            card.append(cardBody);

            for (var n in that.formInfo["questions"][name]) {
                that.selectSection[name+n]=(createQuestion(
                    cardBody,
                    n,
                    that.formInfo["questions"][name][n],
                    that.formInfo["answers"][name][n + "a"],
                    that.formInfo["answers"][name][n + "b"],
                    that.formInfo["answers"][name][n + "c"]
                ))
            }
            form.append(card);
        }

        this.formInfo = formInfo;
        let that = this;

        let form = document.createElement("form");
        this.frame.append(form);

        for(const key in sections) {
            createSection(sections[key], key, form);
        }

        let submitFormGroup = document.createElement("div");
        submitFormGroup.className = "form-group";
        form.append(submitFormGroup);

        let submitButton = document.createElement("button");
        submitButton.className = "btn btn-primary";
        submitButton.textContent = "Submit";
        submitButton.type = "button";
        submitFormGroup.append(submitButton);

        this.progressBar = new ProgressBar();
        this.progressBar.attach(form);
        this.progressBar.hide();

        let statusMessage = document.createElement("p");
        statusMessage.style.display = "none";
        statusMessage.className = "mt-2 mb-0";
        form.append(statusMessage);

        let errorMessage = document.createElement("p");
        errorMessage.style.display = "none";
        errorMessage.className = "mt-2 mb-0 alert alert-danger";
        form.append(errorMessage);

        this.internalErrorMessage = document.createElement("p");
        this.internalErrorMessage.style.display = "none";
        this.internalErrorMessage.className = "mt-2 mb-0 alert alert-danger";
        form.append(this.internalErrorMessage);

        this.asyncForm = new AsyncForm({
            action: "/widgets/data/save_sustainability",
            form: form,
            status: statusMessage,
            error: errorMessage,
            redirectMessage: "Saved!",
            loadingMessage: "Saving...",
            asJSON: true,
            getData: () => {
                return {
                    response: that.submitResponse,
                    sectorScoreCounter: that.dataCounter
                };
            },
        });

        submitButton.addEventListener("click", () => {
            that.submitResponse={}
            var tempData = []
            var curName=""
            var allAnswered= true
            for (var [i,j] of Object.entries(that.selectSection)) {

                if ( $(j).val()=="Any")
                {
                    allAnswered=false
                    break}
                if( tempData.length==0 && curName==""){
                    curName=i.slice(0,-1)
                }
                
                if(curName!="" && curName!=i.slice(0,-1)){
                    that.submitResponse[curName] = tempData;
                    tempData=[]
                    curName=i.slice(0,-1)
                }
                tempData.push ( $(j).val())
            }

            that.submitResponse[curName] = tempData;
            
            if (allAnswered) {
                this.internalErrorMessage.style.display = "none";
                this.calculateScores();
                this.asyncForm.submit();
            }
            else{
                this.internalErrorMessage.style.display = "block";
                this.internalErrorMessage.textContent =
                    "Please complete the questionnaire";
            }
        });
    }

    calculateScores() {
        let dataCounter = {};

        for(const sectionType in this.submitResponse){
            dataCounter[sectionType] = {
                "excellent": 0, 
                "acceptable": 0,
                "needsWork": 0
            }
            for(const response of this.submitResponse[sectionType]){
                if (response.includes('a')) {
                    dataCounter[sectionType].excellent += 1;
                } else if (response.includes('b')) {
                    dataCounter[sectionType].acceptable += 1;
                } else if (response.includes('c')) {
                    dataCounter[sectionType].needsWork += 1;
                }
            }
        }

        this.dataCounter = JSON.stringify(dataCounter);
    }
}