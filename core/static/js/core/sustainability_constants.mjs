const sections = {
    air: {name: "air", header:"Air & Greenhouse Gas Emissions"},
    land: {name: "land", header:"Land Resources"},
    water: {name: "water", header:"Water Resources"},
    animal: {name: "animal", header:"Animal Health & Well-Being"},
    safety: {name: "safety", header:"Employee Safety & Well-Being"},
    efficiency: {name: "efficiency", header:"Efficiency & Yield"},
    improvement: {name: "improvement", header:"Improvement"}
};

const scoringCriteria = {
    confirmation: "confirmation",
    responsePresent: "responsePresent",
    roundOff: "roundOff"
}

const questionType = {
    select: "select",
    input: "input",
    upload: "upload"
}

export {sections, scoringCriteria, questionType};