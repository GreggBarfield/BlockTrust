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

const sectorBasedSectionalTotals = {
    4: {
        air: 5,
        land: 5,
        water: 5,
        animal: 5.5,
        safety: 4.5,
        efficiency: 5.5,
        improvement: 5,
        total: 35.5
    },
    5: {
        water: 5,
        animal: 5,
        safety: 5,
        improvement: 5,
        total: 20
    },
    6: {
        air: 5,
        land: 5,
        water: 5,
        animal: 5,
        safety: 5,
        efficiency: 5,
        improvement: 5,
        total: 35
    },
    7: {
        air: 7.5,
        land: 4.5,
        water: 10,
        animal: 12,
        safety: 7,
        efficiency: 10.5,
        improvement: 5,
        total: 56.5
    },
    10: {
        air: 5,
        land: 5,
        water: 5,
        animal: 5,
        safety: 5,
        efficiency: 5,
        improvement: 5,
        total: 35
    }
}

export {sections, scoringCriteria, questionType, sectorBasedSectionalTotals};