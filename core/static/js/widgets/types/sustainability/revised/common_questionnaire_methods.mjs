export class CommonQuestionnaireMethods{
    createSelectQuestion = (questionText, options) => {
        let questionContainer = document.createElement("div");
        questionContainer.className = "row px-4 border-bottom"

        let questionTextContainer = document.createElement("div");
        questionTextContainer.className = "col-md-8";
        let label = document.createElement("label");
        label.textContent = questionText;
        questionTextContainer.append(label);

        let questionInputContainer = document.createElement("div");
        questionInputContainer.className = "col-md-4 p-1"
        let input = document.createElement("select");
        input.className = "form-control";
        for(const option of options){
            var inputOption = new Option(option.text, option.score);
            input.appendChild(inputOption);
        }
        questionInputContainer.append(input);

        questionContainer.append(questionTextContainer);
        questionContainer.append(questionInputContainer);
        return questionContainer;
    }
    createInputQuestion = (questionText) =>{
        let questionContainer = document.createElement("div");
        questionContainer.className = "row px-4 border-bottom"

        let questionTextContainer = document.createElement("div");
        questionTextContainer.className = "col-md-8";
        let label = document.createElement("label");
        label.textContent = questionText;
        questionTextContainer.append(label);

        let questionInputContainer = document.createElement("div");
        questionInputContainer.className = "col-md-4 p-1"
        let input = document.createElement("input");
        input.className = "form-control";
        questionInputContainer.append(input);

        questionContainer.append(questionTextContainer);
        questionContainer.append(questionInputContainer);
        return questionContainer;
    }
    createRoundOffInputQuestions = (questionText, score) => {

    }
    createQuestionsSection = (questionsSectionHeaderText) => {
        let section = document.createElement("div");
        section.className = "card col-xl-10";

        let sectionHeader = document.createElement("div");
        sectionHeader.className = "card-header";
        section.append(sectionHeader);

        let sectionHeaderText = document.createElement("div");
        sectionHeaderText.className = "h6";
        sectionHeaderText.textContent = questionsSectionHeaderText;
        sectionHeader.append(sectionHeaderText);
        
        let sectionBody = document.createElement("div");
        sectionBody.className = "card-body";
        section.append(sectionBody);
        return section;
    }
}