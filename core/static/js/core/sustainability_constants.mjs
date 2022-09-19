const sections = {
    air: {name: "air", header:"Air & Greenhouse Gas Emissions"},
    land: {name: "land", header:"Land Resources"},
    water: {name: "water", header:"Water Resources"},
    animal: {name: "animal", header:"Animal Health & Well-Being"},
    safety: {name: "safety", header:"Employee Safety & Well-Being"},
    efficiency: {name: "efficiency", header:"Efficiency & Yield"},
    improvement: {name: "improvement", header:"Extra Credit"}
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

const cowCalfQuestionnaireData = {
    [sections.air.name] : [
        {
            id: "air1",
            responseType: questionType.select,
            questionText: "Do you have a Grazing Management Plan (GMP)?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "air2",
            responseType: questionType.select,
            questionText: "Is your grazing management plan written?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5  
        },
        {
            id: "air3",
            responseType: questionType.upload,
            questionText: "Are you willing to share the plan? If so, please upload (PDF only)",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5   
        },
        {
            id: "air4",
            responseType: questionType.select,
            questionText: "Are you actively monitoring and adapting your GMP to ensure continuous progress towards management goals?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5 
        },
        {
            id: "air5",
            responseType: questionType.upload,
            questionText: "Are you willing to share data or information related to that active management? If so, please upload (PDF only)",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.25  
        },
        {
            id: "air6",
            responseType: questionType.select,
            questionText: "Does your GMP include operational success including transition or succession planning? ",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5 
        },
        {
            id: "air7",
            responseType: questionType.select,
            questionText: "Are you actively monitoring your GMP to maintain or improve water quality and cycling? ",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5 
        },
        {
            id: "air8",
            responseType: questionType.upload,
            questionText: "Are you willing to share data or information related to the active management of water resources? If so, please upload (PDF only)",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.25  
        },
        {
            id: "air9",
            responseType: questionType.input,
            questionText: "How many acres are under your grazing management plan?",
            inputType: "number",
            scoringCriteria: scoringCriteria.responsePresent,
            score: 0.5   
        },
        {
            id: "air10",
            responseType: questionType.input,
            questionText: "What percent of your grazing land does this cover?",
            inputType: "number",
            scoringCriteria: scoringCriteria.roundOff
        }
    ],
    [sections.land.name]: [
        {
            id: "land1",
            responseType: questionType.select,
            questionText: "Do you have a Grazing Management Plan (GMP)?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "land2",
            responseType: questionType.select,
            questionText: "Is your grazing management plan written?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5  
        },
        {
            id: "land3",
            responseType: questionType.upload,
            questionText: "Are you willing to share the plan? If so, please upload (PDF only)",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5   
        },
        {
            id: "land4",
            responseType: questionType.select,
            questionText: "Are you actively monitoring and adapting your GMP to ensure continuous progress towards management goals?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5 
        },
        {
            id: "land5",
            responseType: questionType.upload,
            questionText: "Are you willing to share data or information related to that active management? If so, please upload (PDF only)",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.25  
        },
        {
            id: "land6",
            responseType: questionType.select,
            questionText: "Does your GMP include operational success including transition or succession planning? ",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5 
        },
        {
            id: "land7",
            responseType: questionType.select,
            questionText: "Are you actively monitoring your GMP to maintain or improve water quality and cycling? ",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5 
        },
        {
            id: "land8",
            responseType: questionType.upload,
            questionText: "Are you willing to share data or information related to the active management of water resources? If so, please upload (PDF only)",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.25  
        },
        {
            id: "land9",
            responseType: questionType.input,
            questionText: "How many acres are under your grazing management plan?",
            inputType: "number",
            scoringCriteria: scoringCriteria.responsePresent,
            score: 0.5   
        },
        {
            id: "land10",
            responseType: questionType.input,
            questionText: "What percent of your grazing land does this cover?",
            inputType: "number",
            scoringCriteria: scoringCriteria.roundOff
        }
    ],
    [sections.water.name]: [
        {
            id: "water1",
            responseType: questionType.select,
            questionText: "Do you have a Grazing Management Plan (GMP)?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "water2",
            responseType: questionType.select,
            questionText: "Is your grazing management plan written?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5  
        },
        {
            id: "water3",
            responseType: questionType.upload,
            questionText: "Are you willing to share the plan? If so, please upload (PDF only)",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5   
        },
        {
            id: "water4",
            responseType: questionType.select,
            questionText: "Are you actively monitoring and adapting your GMP to ensure continuous progress towards management goals?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5 
        },
        {
            id: "water5",
            responseType: questionType.upload,
            questionText: "Are you willing to share data or information related to that active management? If so, please upload (PDF only)",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.25  
        },
        {
            id: "water6",
            responseType: questionType.select,
            questionText: "Does your GMP include operational success including transition or succession planning? ",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5 
        },
        {
            id: "water7",
            responseType: questionType.select,
            questionText: "Are you actively monitoring your GMP to maintain or improve water quality and cycling? ",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5 
        },
        {
            id: "water8",
            responseType: questionType.upload,
            questionText: "Are you willing to share data or information related to the active management of water resources? If so, please upload (PDF only)",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.25  
        },
        {
            id: "water9",
            responseType: questionType.input,
            questionText: "How many acres are under your grazing management plan?",
            inputType: "number",
            scoringCriteria: scoringCriteria.responsePresent,
            score: 0.5   
        },
        {
            id: "water10",
            responseType: questionType.input,
            questionText: "What percent of your grazing land does this cover?",
            inputType: "number",
            scoringCriteria: scoringCriteria.roundOff
        }
    ],
    [sections.safety.name]: [
        {
            id: "safety1",
            responseType: questionType.select,
            questionText: "Do you conduct stockmanship and/or safety training?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "safety2",
            responseType: questionType.upload,
            questionText: "If yes, what training? Please upload training (PDF only)",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "safety3",
            responseType: questionType.select,
            questionText: "Did you conduct employee safety training in the last 12 months?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "safety4",
            responseType: questionType.select,
            questionText: "Are 100% of your employees stockmanship & safety training annually?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "safety5",
            responseType: questionType.input,
            questionText: "What percentage of your employees have undergone stockmanship &/or safety training?",
            inputType: "number",
            scoringCriteria: scoringCriteria.roundOff
        }
    ],
    [sections.animal.name]: [
        {
            id: "animal1",
            responseType: questionType.select,
            questionText: "Does you operation participate in BQA or equivalent programs?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "animal2",
            responseType: questionType.select,
            questionText: "Is your operation BQA Certified or an equivalent program? Or are you certified?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "animal3",
            responseType: questionType.input,
            questionText: "If yes, what is your BQA certification number? Please upload",
            inputType: "text",
            scoringCriteria: scoringCriteria.responsePresent,
            score: 0.5
        },
        {
            id: "animal4",
            responseType: questionType.select,
            questionText: "Have you conducted a BQA audit?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "animal5",
            responseType: questionType.input,
            questionText: "If yes, what was your score? Please enter",
            inputType: "text",
            scoringCriteria: scoringCriteria.responsePresent,
            score: 0.5
        },
        {
            id: "animal6",
            responseType: questionType.input,
            questionText: "What percentage of your employees are BQA Certified?",
            inputType: "number",
            scoringCriteria: scoringCriteria.roundOff
        }
    ],
    [sections.efficiency.name]: [
        {
            id: "efficiency1",
            responseType: questionType.select,
            questionText: "Have you implemented management strategies to optimize animal productivity through improved nutrition, reproduction, genetics, technologies and practices?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "efficiency2",
            responseType: questionType.select,
            questionText: "Do you individually identify cows and calves? ",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "efficiency3",
            responseType: questionType.select,
            questionText: "Do you measure weaning weight either by individual cow or by unit of land? Neither?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "efficiency4",
            responseType: questionType.select,
            questionText: "Do you track calf weaning percentage per cow exposed?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "efficiency5",
            responseType: questionType.input,
            questionText: "What is your calf weaning percentage per cow exposed?",
            inputType: "number",
            scoringCriteria: scoringCriteria.roundOff
        },
        {
            id: "efficiency6",
            responseType: questionType.select,
            questionText: "Are you/will you making culling decisions based on calf weaning weight or cow reproductive success?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "efficiency7",
            responseType: questionType.select,
            questionText: "Do you consider feed efficiency or calf weaning weight when making breeding or culling decisions?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "efficiency8",
            responseType: questionType.select,
            questionText: "When determing mating decisions are you selecting bulls in considerations of your own cowherds strengths and weaknesses?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "efficiency9",
            responseType: questionType.upload,
            questionText: "Are you willing to share your breeding plan? If so, please upload (PDF only)",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        }
    ],
    [sections.improvement.name]: [
        {
            id: "improvement1",
            responseType: questionType.select,
            questionText: "Have you examined the greenhouse gas footprint of your operation? If yes, what are the units? ",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "improvement2",
            responseType: questionType.input,
            questionText: "What is the most recent year you evaluated your greenhouse gas footprint? ",
            inputType: "text",
            scoringCriteria: scoringCriteria.responsePresent,
            score: 0.5
        },
        {
            id: "improvement3",
            responseType: questionType.input,
            questionText: "What is your most current greenhouse gas footprint? ",
            inputType: "text",
            scoringCriteria: scoringCriteria.responsePresent,
            score: 0.25
        },
        {
            id: "improvement4",
            responseType: questionType.select,
            questionText: "Have you examined the water footprint of your operation? If yes, what are the units? ",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "improvement5",
            responseType: questionType.input,
            questionText: "What is the most recent year you evaluated your water footprint? ",
            inputType: "text",
            scoringCriteria: scoringCriteria.responsePresent,
            score: 0.5
        },
        {
            id: "improvement6",
            responseType: questionType.input,
            questionText: "What is your most current water footprint? ",
            inputType: "text",
            scoringCriteria: scoringCriteria.responsePresent,
            score: 0.25
        },
        {
            id: "improvement7",
            responseType: questionType.select,
            questionText: "Is your operation actively participating in ecosystem service markets or convservation programs (i.e. NRCS, EQUIP, etc.)?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "improvement8",
            responseType: questionType.select,
            questionText: "Do you have a herd health plan developed through a Veterinary-Client Patient Relationship (VCPR)?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "improvement9",
            responseType: questionType.select,
            questionText: "Does your operation actively try to mitigate or remove safety hazards in facilities and equipment?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "improvement10",
            responseType: questionType.select,
            questionText: "Do you utilize RFID or alternative traceability technology?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "improvement11",
            responseType: questionType.select,
            questionText: "Do you track and record your antibiotic use? ",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        }
    ]
}

const feedlotQuestionnaireData = {
    [sections.air.name] : [
        {
            id: "air1",
            responseType: questionType.select,
            questionText: "Are animals sorted into contemporary groups to improve efficiency at the pen level?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "air2",
            responseType: questionType.select,
            questionText: "Are you or are you planning to implement early diagnostic tools to identify and treat sick animals earlier?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "air3",
            responseType: questionType.select,
            questionText: "Are you using feed additives to optimize growth in an effort to reduce emissions?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "air4",
            responseType: questionType.input,
            questionText: "If so, which feed additives?",
            scoringCriteria: scoringCriteria.responsePresent,
            inputType: "text",
            score: 0.5
        },
        {
            id: "air5",
            responseType: questionType.select,
            questionText: "Are energy uses reviewed periodically to identify opportunities to gain efficiencies or reduce usage?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "air6",
            responseType: questionType.input,
            questionText: "What opportunities have you identified?",
            scoringCriteria: scoringCriteria.responsePresent,
            inputType: "text",
            score: 0.5
        }
    ],
    [sections.land.name] : [
        {
            id: "land1",
            responseType: questionType.select,
            questionText: "Do you implement nutrient management BMPs? (ie. manure management, tillage strategies, fertilizer and pesticide applications etc.)",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "land2",
            responseType: questionType.select,
            questionText: "Does the feedyard have applicable state and or federal water and or environmental permits?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "land3",
            responseType: questionType.select,
            questionText: "If yes, are all records required for the permits being properly maintained and reported?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "land4",
            responseType: questionType.select,
            questionText: "Do you have a written nutrient management plan?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "land5",
            responseType: questionType.select,
            questionText: "If yes, do you have SOPs for measuring the required items in the nutrient management plan?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "land6",
            responseType: questionType.upload,
            questionText: "If you have a plan, are you willing to share it?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        }
    ],
    [sections.water.name] : [
        {
            id: "water1",
            responseType: questionType.select,
            questionText: "Do you currently implement water conservation management practices?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "water2",
            responseType: questionType.input,
            questionText: "If so, which practices?",
            scoringCriteria: scoringCriteria.responsePresent,
            inputType: "text",
            score: 0.5
        },
        {
            id: "water3",
            responseType: questionType.select,
            questionText: "Is water use reviewed regularly to improve water use optimization?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "water4",
            responseType: questionType.input,
            questionText: "If so, what practices have you identified?",
            scoringCriteria: scoringCriteria.responsePresent,
            inputType: "text",
            score: 0.25
        },
        {
            id: "water5",
            responseType: questionType.select,
            questionText: "Is water infrastructure properly maintained and upgraded to improve water use efficiency?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "water6",
            responseType: questionType.select,
            questionText: "Do you have a written water management strategy?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "water7",
            responseType: questionType.upload,
            questionText: "If yes, are you willing to share it?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.25
        }
    ],
    [sections.animal.name] : [
        {
            id: "animal1",
            responseType: questionType.select,
            questionText: "Does you operation participate in BQA or equivalent programs?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "animal2",
            responseType: questionType.select,
            questionText: "Is your operation BQA Certified or an equivalent program? Or are you certified?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "animal3",
            responseType: questionType.input,
            questionText: "If yes, what is your BQA certification number? Please upload",
            scoringCriteria: scoringCriteria.roundOff,
            inputType: "number",
            score: 0.5
        },
        {
            id: "animal4",
            responseType: questionType.select,
            questionText: "Have you conducted a BQA audit?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "animal5",
            responseType: questionType.upload,
            questionText: "If yes, what was your score? Please upload",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "animal6",
            responseType: questionType.select,
            questionText: "What percentage of your livestock handling employees are BQA certified?",
            scoringCriteria: scoringCriteria.roundOff,
            score: 1
        },
    ],
    [sections.safety.name] : [
        {
            id: "safety1",
            responseType: questionType.select,
            questionText: "Do you have an employee safety program?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "safety2",
            responseType: questionType.input,
            questionText: "If yes, are you willing to share it?",
            scoringCriteria: scoringCriteria.responsePresent,
            inputType : "text",
            score: 1
        },
        {
            id: "safety3",
            responseType: questionType.select,
            questionText: "Did you conduct employee safety training in the last 12 months?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "safety4",
            responseType: questionType.select,
            questionText: "Do 100% of your employees undergo safety training annually?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "safety5",
            responseType: questionType.input,
            questionText: "What percentage of your employees have undergone safety training?",
            scoringCriteria: scoringCriteria.roundOff
        }
    ],
    [sections.efficiency.name] : [
        {
            id: "efficiency1",
            responseType: questionType.select,
            questionText: "Are closeout metrics and performance tracked and compared over time?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "efficiency2",
            responseType: questionType.select,
            questionText: "Are feed rations formulated to optimize resources and performance?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "efficiency3",
            responseType: questionType.select,
            questionText: "Are feed ingredients stored to prevent or minimize spoilage and is loss prevention practiced?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "efficiency4",
            responseType: questionType.select,
            questionText: "Is feed delivery monitored for efficiency and reviewed for improvements?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "efficiency5",
            responseType: questionType.select,
            questionText: "Is energy consumption measured and is there a process to look for more efficient utilization?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        }
    ],
    [sections.improvement.name] : [
        {
            id: "improvement1",
            responseType: questionType.select,
            questionText: "Have you examined the greenhouse gas footprint of your operation? If yes, what are the units? ",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "improvement2",
            responseType: questionType.input,
            questionText: "What is the most recent year you evaluated your greenhouse gas footprint?  ",
            inputType: "text",
            scoringCriteria: scoringCriteria.responsePresent,
            score: 0.5
        },
        {
            id: "improvement3",
            responseType: questionType.input,
            questionText: "What is your most current greenhouse gas footprint? ",
            inputType: "text",
            scoringCriteria: scoringCriteria.responsePresent,
            score: 0.5
        },
        {
            id: "improvement4",
            responseType: questionType.select,
            questionText: "Have you examined the water footprint of your operation? If yes, what are the units? ",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "improvement5",
            responseType: questionType.input,
            questionText: "What is the most recent year you evaluated your water footprint? ",
            inputType: "text",
            scoringCriteria: scoringCriteria.responsePresent,
            score: 0.5
        },
        {
            id: "improvement6",
            responseType: questionType.input,
            questionText: "What is your most current water footprint? ",
            inputType: "number",
            scoringCriteria: scoringCriteria.responsePresent,
            score: 0.5
        },
        {
            id: "improvement7",
            responseType: questionType.select,
            questionText: "Is your operation actively participating in ecosystem service markets or conservation programs?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "improvement6",
            responseType: questionType.select,
            questionText: "Do you have a herd health plan developed through a Veterinary-Client Patient Relationship (VCPR)?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "improvement8",
            responseType: questionType.select,
            questionText: "Does your operation actively try to mitigate or remove safety hazards in facilities and equipment?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "improvement9",
            responseType: questionType.select,
            questionText: "Do you utilize RFID or alternative traceability technology?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        }
    ]
}

const auctionHouseQuestionnaireData = {
    [sections.water.name] : [
        {
            id: "water1",
            responseType: questionType.select,
            questionText: "If required, does your facility have a waste water permit and is it in compliance with the permit?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "water2",
            responseType: questionType.upload,
            questionText: "If yes, are you willing to share it?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "water3",
            responseType: questionType.select,
            questionText: "Is your facility designed to capture pen runoff and with manure storage areas?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "water4",
            responseType: questionType.select,
            questionText: "Does your facility have a written water or nutrient management plan?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "water5",
            responseType: questionType.upload,
            questionText: "If yes, are you willing to share it?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "water6",
            responseType: questionType.select,
            questionText: "Are employees with environmental responsibilities regularly trained?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        }
    ],
    [sections.safety.name] : [
        {
            id: "safety1",
            responseType: questionType.select,
            questionText: "Do you have an employee safety program in place?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "safety2",
            responseType: questionType.select,
            questionText: "If yes, do is your safety program written?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "safety3",
            responseType: questionType.upload,
            questionText: "If yes, are you willing to share? Please upload training",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "safety4",
            responseType: questionType.input,
            questionText: "What percentage of your employees have undergone stockmanship &/or safety training?",
            inputType: "number",
            scoringCriteria: scoringCriteria.roundOff
        },
        {
            id: "safety5",
            responseType: questionType.select,
            questionText: "Are 100% of your employees stockmanship & safety training upon hiring and at least annually?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        }
    ],
    [sections.animal.name] : [
        {
            id: "animal1",
            responseType: questionType.select,
            questionText: "Does you operation participate in BQA, Livestock marketing association training or equivalent programs?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "animal2",
            responseType: questionType.select,
            questionText: "Is your operation BQA Certified, Livestock marketing association or an equivalent program? Or are you certified?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "animal3",
            responseType: questionType.input,
            questionText: "If yes, what is your BQA certification number? Please upload",
            inputType: "text",
            scoringCriteria: scoringCriteria.responsePresent,
            score: 0.5
        },
        {
            id: "animal4",
            responseType: questionType.select,
            questionText: "Have you conducted a BQA, Livestock marketing association or equivalent audit?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "animal5",
            responseType: questionType.input,
            questionText: "If yes, what was your score? Please enter",
            inputType: "text",
            scoringCriteria: scoringCriteria.responsePresent,
            score: 0.5
        },
        {
            id: "animal6",
            responseType: questionType.input,
            questionText: "What percentage of your animal handling employees are BQA or Livestock Marketing Association trained?",
            inputType: "number",
            scoringCriteria: scoringCriteria.roundOff
        }
    ],
    [sections.improvement.name] : [ 
        {
            id: "improvement1",
            responseType: questionType.select,
            questionText: "Have you or are you planning to examine the environmental impact of your operation? (Water or Greenhouse gas footprint)",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "improvement2",
            responseType: questionType.input,
            questionText: "If yes, what type of assessment have you or are you going to conduct?(Water or Greenhouse)",
            inputType: "text",
            scoringCriteria: scoringCriteria.responsePresent,
            score: 0.5
        },
        {
            id: "improvement3",
            responseType: questionType.input,
            questionText: "If already completed, what was your footprint?",
            inputType: "text",
            scoringCriteria: scoringCriteria.responsePresent,
            score: 0.5
        },
        {
            id: "improvement4",
            responseType: questionType.select,
            questionText: "Do you have a health plan developed through a Veterinary-Client Patient Relationship (VCPR)?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "improvement5",
            responseType: questionType.select,
            questionText: "Does your operation actively try to mitigate or remove safety hazards in facilities and equipment?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "improvement6",
            responseType: questionType.select,
            questionText: "Do you utilize, or facilitate the use of, RFID or alternative traceability technology?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "improvement7",
            responseType: questionType.select,
            questionText: "Are all the proper facilities recommendations implemented at the auction to reduce animal stress and injury?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "improvement8",
            responseType: questionType.select,
            questionText: "Does the auction emphasize the BQA transportation guidelines to its customers?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "improvement9",
            responseType: questionType.select,
            questionText: "Have you or are you planning to install green infrastructure?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "improvement10",
            responseType: questionType.select,
            questionText: "Have you are or you planning to develop on-site habitat restoration?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        }
    ]
}

const packerQuestionnaireData = {
    [sections.air.name] : [
        {
            id: "air1",
            responseType: questionType.select,
            questionText: "Are strategies in place to optimize energy efficiency and reduce greenhouse gas emissions at company facilities?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "air2",
            responseType: questionType.upload,
            questionText: "Report Scope 1 emissions.",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "air3",
            responseType: questionType.upload,
            questionText: "Report Scope 2 emissions.",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "air4",
            responseType: questionType.select,
            questionText: "Does your company calculate carbon dioxide equivalents per head or per mass of finished product?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "air5",
            responseType: questionType.upload,
            questionText: "What is the company's carbon dioxide equivalents per head or per mass of finished product (please specify unit)?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "air6",
            responseType: questionType.select,
            questionText: "Does your company make carbon dioxide equivalents or GHG emissions publicly available?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "air7",
            responseType: questionType.select,
            questionText: "Does your company track air and GHG emissions overtime and set goals for continued improvement? ",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "air8",
            responseType: questionType.input,
            questionText: "What is your GHG reduction goal?",
            scoringCriteria: scoringCriteria.responsePresent,
            inputType: "text",
            score: 0.5
        },
        {
            id: "air9",
            responseType: questionType.select,
            questionText: "Does your company participate in partnerships, initiatives or programs to further GHG reduction and improve air quality? ",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "air10",
            responseType: questionType.select,
            questionText: "Is your Company taking tangible action to achieve an approved science-based target to reduce emissions in line with limiting global temperature increases to well below 2 or, ideally, 1.5 degrees Celsius relative to pre-industrial levels?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        }
    ],
    [sections.land.name] : [
        {
            id: "land1",
            responseType: questionType.select,
            questionText: "Have opportunities relating to mitigating land and biodiversity impacts from company facilities been evaluated by your company? ",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.75
        },
        {
            id: "land2",
            responseType: questionType.upload,
            questionText: "Are you willing to share the opportunities identified by your company? If so, please upload.",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "land3",
            responseType: questionType.select,
            questionText: "Is you company currently involved or exploring involvement in initiatives and programs to mitigate land and biodiversity impacts from company facilities? ",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.75
        },
        {
            id: "land4",
            responseType: questionType.upload,
            questionText: "Are you willing to share current involvement or plans for involvement for your company? If so, please upload.",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "land5",
            responseType: questionType.select,
            questionText: "Do your company's facility construction, renovation or expansion projects will include a plan to mitigate impacts on natural resources by 2025.",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "land6",
            responseType: questionType.upload,
            questionText: "Please share these plans.",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        }
    ],
    [sections.water.name] : [
        {
            id: "water1",
            responseType: questionType.select,
            questionText: "Do all company facilities have a water management plan?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.25
        },
        {
            id: "water2",
            responseType: questionType.upload,
            questionText: "Are you willing to share the plan? If so, please upload.",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "water3",
            responseType: questionType.input,
            questionText: "How many wastewater permit non-compliances has your company had in the previous calendar year?",
            scoringCriteria: scoringCriteria.responsePresent,
            inputType: "text",
            score: 0.25
        },
        {
            id: "water4",
            responseType: questionType.input,
            questionText: "What is the water use in gallons/head/day or gallons/pound of beef processed for your company (please specify unit)?",
            scoringCriteria: scoringCriteria.responsePresent,
            inputType: "text",
            score: 0.25
        },
        {
            id: "water5",
            responseType: questionType.select,
            questionText: "Does the company make water performance efforts public?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.25
        },
        {
            id: "water6",
            responseType: questionType.select,
            questionText: "Does your company track water use year-over-year?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.25
        },
        {
            id: "water7",
            responseType: questionType.upload,
            questionText: "Are you willing to share changes in water use for this year compared to the previous year? If so, please upload.",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "water8",
            responseType: questionType.select,
            questionText: "Does the company have goals for continued improvement in water use?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.25
        },
        {
            id: "water9",
            responseType: questionType.upload,
            questionText: "Are you willing to share these goals and company progress on these goals? Is so, please upload.",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "water10",
            responseType: questionType.select,
            questionText: "Does the company participate in partnerships, initiatives or programs to further advance water resource management?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "water11",
            responseType: questionType.upload,
            questionText: "Are you willing to share details on company involvement in partnerships, initiatives or programs to further advance water resource management? Is so, please upload.",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "water12",
            responseType: questionType.select,
            questionText: "Have you assessed and implemented plans according to a water risk assessment at your facilities ",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "water13",
            responseType: questionType.upload,
            questionText: "Do you work with your beef value chain to encourage adoption of the Beef Industry Sustainability Framework? If so, please share this relevant details of this strategy.",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        }
    ],
    [sections.safety.name] : [
        {
            id: "safety1",
            responseType: questionType.select,
            questionText: "Does your company have a documented employee safety program?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "safety2",
            responseType: questionType.upload,
            questionText: "If yes, please provide specifics on the program. Please upload. ",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "safety3",
            responseType: questionType.select,
            questionText: "Does this program take into consideration employee well-being? ",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "safety4",
            responseType: questionType.select,
            questionText: "Does your company's employee safety program engage front-line employees and leadership? ",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "safety5",
            responseType: questionType.select,
            questionText: "Does the company track Total Recordable Incident Rates (TRIR)? ",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "safety6",
            responseType: questionType.upload,
            questionText: "Are you willing to share your company's TRIR from this year and the previous year?  ",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "safety7",
            responseType: questionType.select,
            questionText: "Does your company track trends for TRIR and reference rates against the NAICS industry standard rate to set goals for the upcoming year? ",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "safety8",
            responseType: questionType.select,
            questionText: "Does the company participate in partnerships, initiatives or programs to further advance employee safety and well-being? ",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "safety9",
            responseType: questionType.upload,
            questionText: "Are you willing to share company involvement in partnerships, initiatives or programs to further advance employee safety and well-being? Is so, please upload. ",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "safety10",
            responseType: questionType.upload,
            questionText: "Is yes, please provide specifics on the program. Please Upload.",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        }
    ],
    [sections.animal.name] : [
        {
            id: "animal1",
            responseType: questionType.select,
            questionText: "Does your company have a comprehensive animal welfare program?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.25
        },
        {
            id: "animal2",
            responseType: questionType.upload,
            questionText: "Are you willing to share details of this program? Is so, please upload.",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.25
        },
        {
            id: "animal3",
            responseType: questionType.select,
            questionText: "Does your company use second -or- third party animal welfare audits to verify policy compliance to at least the packer level?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.25
        },
        {
            id: "animal4",
            responseType: questionType.input,
            questionText: "What percentage of cattle come under a third-party audit? ",
            inputType: "number",
            scoringCriteria: scoringCriteria.responsePresent,
            score: 0.25
        },
        {
            id: "animal5",
            responseType: questionType.input,
            questionText: "What percentage pass on first audit?",
            inputType: "number",
            scoringCriteria: scoringCriteria.responsePresent,
            score: 0.25
        },
        {
            id: "animal6",
            responseType: questionType.select,
            questionText: "Does your company track total number of USDA non-compliance animal welfare violations?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.25
        },
        {
            id: "animal7",
            responseType: questionType.input,
            questionText: "What was your company's total number of USDA non-compliance animal welfare violations per 100,000 head processed in the previous calendar year?",
            inputType: "text",
            scoringCriteria: scoringCriteria.responsePresent,
            score: 0.25
        },
        {
            id: "animal8",
            responseType: questionType.select,
            questionText: "Does your company track animal health and well-being over time and set goals for continued improvement?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.25
        },
        {
            id: "animal9",
            responseType: questionType.upload,
            questionText: "Are you willing to share your company's goals and progress? If yes, please upload.",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.25
        },
        {
            id: "animal10",
            responseType: questionType.select,
            questionText: "Does your company engage its suppliers or participate in partnerships, initiatives or programs and/or engage its suppliers to advance continuous improvement regarding animal health and well-being in the beef value chain?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.25
        },
        {
            id: "animal11",
            responseType: questionType.upload,
            questionText: "Are you willing to provide details on how your company engages its suppliers or participate in partnerships, initiatives or programs and/or engage its suppliers to advance continuous improvement regarding animal health and well-being in the beef value chain? Is yes, please upload. ",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.25
        },
        {
            id: "animal12",
            responseType: questionType.select,
            questionText: "Does your company require suppliers to implement mandatory employee training for animal care?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.25
        },
        {
            id: "animal13",
            responseType: questionType.input,
            questionText: "How frequently are employees of suppliers trained on animal handling and care protocols?",
            inputType: "text",
            scoringCriteria: scoringCriteria.responsePresent,
            score: 0.5
        },
        {
            id: "animal14",
            responseType: questionType.select,
            questionText: "Does your company require suppliers to follow BQA standards for animal care?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.25
        },
        {
            id: "animal15",
            responseType: questionType.input,
            questionText: "What percentage of your suppliers implement mandatory employee training and follow BQA standards for animal care?",
            inputType: "number",
            scoringCriteria: scoringCriteria.responsePresent,
            score: 0.25
        },
        {
            id: "animal16",
            responseType: questionType.select,
            questionText: "Does your company conduct third-party animal transport and handling audits?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.25
        },
        {
            id: "animal17",
            responseType: questionType.input,
            questionText: "What percentage of these audits are passed?",
            inputType: "number",
            scoringCriteria: scoringCriteria.responsePresent,
            score: 0.5
        }
    ],
    [sections.efficiency.name] : [
        {
            id: "efficiency1",
            responseType: questionType.select,
            questionText: "Does your company have a documented waste management plan for all company facilities?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "efficiency2",
            responseType: questionType.upload,
            questionText: "Are you willing to share your waste-management plan? If so, please upload.",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.25
        },
        {
            id: "efficiency3",
            responseType: questionType.select,
            questionText: "Is a program to divert waste from landfills implemented at the facility?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "efficiency4",
            responseType: questionType.input,
            questionText: "How much mass of waste/head or waste/mass of finished product does the company divert from landfill (please specify unit)?",
            inputType: "text",
            scoringCriteria: scoringCriteria.responsePresent,
            score: 0.25
        },
        {
            id: "efficiency5",
            responseType: questionType.select,
            questionText: "Does the company track waste reduction over time and set goals for continued improvement?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "efficiency6",
            responseType: questionType.select,
            questionText: "Are you willing to share your waste reduction goals and progress? Is yes, please upload. ",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.25
        },
        {
            id: "efficiency7",
            responseType: questionType.select,
            questionText: "Does the company participate in partnerships, initiatives or programs to further advance waste reduction strategies?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "efficiency8",
            responseType: questionType.upload,
            questionText: "Are you willing to share your company's engagement in partnerships, initiatives or programs to further advance waste reduction strategies? If yes, please upload.",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.25
        },
        {
            id: "efficiency9",
            responseType: questionType.select,
            questionText: "Does your company have public-facing food waste reduction goal by 2030.",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "efficiency10",
            responseType: questionType.input,
            questionText: "Please share your progress to your company's waste reduction goal(s).",
            inputType: "text",
            scoringCriteria: scoringCriteria.responsePresent,
            score: 0.25
        },
        {
            id: "efficiency11",
            responseType: questionType.select,
            questionText: "Do you have implemented a zero waste to landfill diversion program?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "efficiency12",
            responseType: questionType.select,
            questionText: "Does your company have a zero waste goal?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.25
        },
        {
            id: "efficiency13",
            responseType: questionType.select,
            questionText: "Is your company's zero waste goal(s) audited by an accredited third party to a published standard?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.25
        },
        {
            id: "efficiency14",
            responseType: questionType.upload,
            questionText: "Share the results.",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.25
        }
    ],
    [sections.improvement.name] : [   
        {
            id: "improvement1",
            responseType: questionType.select,
            questionText: "Have you or are you planning to examine the environmental impact of your operation? (greenhouse gas footprint)",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "improvement2",
            responseType: questionType.input,
            questionText: "What was your footprint?",
            inputType: "text",
            scoringCriteria: scoringCriteria.responsePresent,
            score: 0.25
        },
        {
            id: "improvement3",
            responseType: questionType.select,
            questionText: "Have you or are you planning to examine the environmental impact of your operation? (water footprint)",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "improvement4",
            responseType: questionType.input,
            questionText: "What was your footprint?",
            inputType: "text",
            scoringCriteria: scoringCriteria.responsePresent,
            score: 0.25
        },
        {
            id: "improvement5",
            responseType: questionType.select,
            questionText: "Does you company currently report scope 3 emissions?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "improvement6",
            responseType: questionType.input,
            questionText: "Report most current Scope 3 emissions",
            inputType: "text",
            scoringCriteria: scoringCriteria.responsePresent,
            score: 0.25
        },
        {
            id: "improvement7",
            responseType: questionType.select,
            questionText: "Is your operation actively participating in ecosystem service markets or conservation programs?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "improvement8",
            responseType: questionType.select,
            questionText: "Does your operation actively try to mitigate or remove safety hazards in facilities and equipment?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "improvement9",
            responseType: questionType.select,
            questionText: "Have you or are you planning to install green infrastructure?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "improvement10",
            responseType: questionType.input,
            questionText: "What percent of your total energy used is renewable? ",
            inputType: "text",
            scoringCriteria: scoringCriteria.responsePresent,
            score: 0.5
        },
        {
            id: "improvement11",
            responseType: questionType.select,
            questionText: "Have risks relating to mitigating land and biodiversity impacts from company facilities been evaluated by your company? ",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "improvement12",
            responseType: questionType.upload,
            questionText: "Are you willing to share the risks identified by your company? If so, please upload.",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.25
        },
        {
            id: "improvement13",
            responseType: questionType.select,
            questionText: "Does your company perform a water-risk assessment that includes all company facilities?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        }
    ],
}

const stockerBackGrounderQuestionnaireData = {
    [sections.air.name] : [
        {
            id: "air1",
            responseType: questionType.select,
            questionText: "Do you have a Grazing Management Plan (GMP)?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "air2",
            responseType: questionType.select,
            questionText: "Is your grazing management plan written?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1   
        },
        {
            id: "air3",
            responseType: questionType.upload,
            questionText: "Are you willing to share the plan? If so, please upload (PDF only)",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5   
        },
        {
            id: "air4",
            responseType: questionType.select,
            questionText: "Are you actively monitoring and adapting your GMP to ensure continuous progress towards management goals?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1   
        },
        {
            id: "air5",
            responseType: questionType.upload,
            questionText: "Are you willing to share data or information related to that active management? If so, please upload (PDF only)",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5   
        },
        {
            id: "air6",
            responseType: questionType.input,
            questionText: "How many acres are under your grazing management plan?",
            inputType: "number",
            scoringCriteria: scoringCriteria.responsePresent,
            score: 0.5   
        },
        {
            id: "air7",
            responseType: questionType.input,
            questionText: "What percent of your grazing land does this cover?",
            inputType: "number",
            scoringCriteria: scoringCriteria.responsePresent,
            score: 0.5  
        }
    ],
    [sections.land.name] : [
        {
            id: "land1",
            responseType: questionType.select,
            questionText: "Do you have a Grazing Management Plan (GMP)?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "land2",
            responseType: questionType.select,
            questionText: "Is your grazing management plan written?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1   
        },
        {
            id: "land3",
            responseType: questionType.upload,
            questionText: "Are you willing to share the plan? If so, please upload (PDF only)",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5   
        },
        {
            id: "land4",
            responseType: questionType.select,
            questionText: "Are you actively monitoring and adapting your GMP to ensure continuous progress towards management goals?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1   
        },
        {
            id: "land5",
            responseType: questionType.upload,
            questionText: "Are you willing to share data or information related to that active management? If so, please upload (PDF only)",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5   
        },
        {
            id: "land6",
            responseType: questionType.input,
            questionText: "How many acres are under your grazing management plan?",
            inputType: "number",
            scoringCriteria: scoringCriteria.responsePresent,
            score: 0.5   
        },
        {
            id: "land7",
            responseType: questionType.input,
            questionText: "What percent of your grazing land does this cover?",
            inputType: "number",
            scoringCriteria: scoringCriteria.responsePresent,
            score: 0.5  
        }
    ],
    [sections.water.name] : [
        {
            id: "water1",
            responseType: questionType.select,
            questionText: "Do you have a Grazing Management Plan (GMP)?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "water2",
            responseType: questionType.select,
            questionText: "Is your grazing management plan written?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1   
        },
        {
            id: "water3",
            responseType: questionType.upload,
            questionText: "Are you willing to share the plan? If so, please upload (PDF only)",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5   
        },
        {
            id: "water4",
            responseType: questionType.select,
            questionText: "Are you actively monitoring and adapting your GMP to ensure continuous progress towards management goals?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1   
        },
        {
            id: "water5",
            responseType: questionType.upload,
            questionText: "Are you willing to share data or information related to that active management? If so, please upload (PDF only)",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5   
        },
        {
            id: "water6",
            responseType: questionType.input,
            questionText: "How many acres are under your grazing management plan?",
            inputType: "number",
            scoringCriteria: scoringCriteria.responsePresent,
            score: 0.5   
        },
        {
            id: "water7",
            responseType: questionType.input,
            questionText: "What percent of your grazing land does this cover?",
            inputType: "number",
            scoringCriteria: scoringCriteria.responsePresent,
            score: 0.5  
        }
    ],
    [sections.safety.name] : [
        {
            id: "safety1",
            responseType: questionType.select,
            questionText: "Do you conduct stockmanship and/or safety training?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "safety2",
            responseType: questionType.upload,
            questionText: "If yes, what training? Please upload training (PDF only)",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "safety3",
            responseType: questionType.select,
            questionText: "Did you conduct employee safety training in the last 12 months?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "safety4",
            responseType: questionType.select,
            questionText: "Are 100% of your employees stockmanship & safety training annually?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "safety5",
            responseType: questionType.input,
            questionText: "What percentage of your employees have undergone stockmanship &/or safety training?",
            inputType: "number",
            scoringCriteria: scoringCriteria.roundOff
        }
    ],
    [sections.animal.name] : [
        {
            id: "animal1",
            responseType: questionType.select,
            questionText: "Does you operation participate in BQA or equivalent programs?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "animal2",
            responseType: questionType.select,
            questionText: "Is your operation BQA Certified or an equivalent program? Or are you certified?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "animal3",
            responseType: questionType.input,
            questionText: "If yes, what is your BQA certification number? Please upload",
            inputType: "text",
            scoringCriteria: scoringCriteria.responsePresent,
            score: 0.5
        },
        {
            id: "animal4",
            responseType: questionType.select,
            questionText: "Have you conducted a BQA audit?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "animal5",
            responseType: questionType.input,
            questionText: "If yes, what was your score? Please enter",
            inputType: "text",
            scoringCriteria: scoringCriteria.responsePresent,
            score: 1
        },
        {
            id: "animal6",
            responseType: questionType.input,
            questionText: "What percentage of your employees are BQA Certified?",
            inputType: "number",
            scoringCriteria: scoringCriteria.roundOff
        }
    ],
    [sections.efficiency.name] : [
        {
            id: "efficiency1",
            responseType: questionType.select,
            questionText: "Do you measure weaning weight either by individual cow or by unit of land? Neither?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "efficiency2",
            responseType: questionType.select,
            questionText: "Do you track calf weaning percentage per cow exposed?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "efficiency3",
            responseType: questionType.input,
            questionText: "What is your calf weaning percentage per cow exposed?",
            inputType: "number",
            scoringCriteria: scoringCriteria.roundOff
        },
        {
            id: "efficiency4",
            responseType: questionType.select,
            questionText: "Are you/will you making culling decisions based on calf weaning weight or cow reproductive success?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "efficiency5",
            responseType: questionType.select,
            questionText: "When determing mating decisions are you selecting bulls in considerations of your own cowherds strengths and weaknesses?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "efficiency6",
            responseType: questionType.upload,
            questionText: "Are you willing to share your breeding plan? If so, please upload (PDF only)",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
    ],
    [sections.improvement.name] : [
        {
            id: "improvement1",
            responseType: questionType.select,
            questionText: "Have you or are you planning to examine the environmental impact of your operation? (Water footprint)",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "improvement2",
            responseType: questionType.input,
            questionText: "If already completed, what was your footprint?",
            inputType: "text",
            scoringCriteria: scoringCriteria.responsePresent,
            score: 0.5
        },
        {
            id: "improvement3",
            responseType: questionType.select,
            questionText: "Have you or are you planning to examine the environmental impact of your operation? (Greenhouse Gas footprint)",
            scoringCriteria: scoringCriteria.confirmation,
            score: 1
        },
        {
            id: "improvement4",
            responseType: questionType.input,
            questionText: "If already completed, what was your footprint?",
            inputType: "text",
            scoringCriteria: scoringCriteria.responsePresent,
            score: 0.5
        },
        {
            id: "improvement5",
            responseType: questionType.select,
            questionText: "Is your operation actively participating in ecosystem service markets or convservation programs?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "improvement6",
            responseType: questionType.select,
            questionText: "Do you have a herd health plan developed through a Veterinary-Client Patient Relationship (VCPR)?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "improvement7",
            responseType: questionType.select,
            questionText: "Does your operation actively try to mitigate or remove safety hazards in facilities and equipment?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        },
        {
            id: "improvement8",
            responseType: questionType.select,
            questionText: "Do you utilize RFID or alternative traceability technology?",
            scoringCriteria: scoringCriteria.confirmation,
            score: 0.5
        }
    ]
}

const calculateSustainabilityQuestionnaireMaxScores = (sectorsNameToId) => {
    // Calculate the max scores for each sector using the questionnare data
    let sectorBasedSectionalTotals = {
        [sectorsNameToId["Cow-Calf"]] : getSectionalScores(cowCalfQuestionnaireData),
        [sectorsNameToId["Feedlot"]]: getSectionalScores(feedlotQuestionnaireData),
        [sectorsNameToId["Auction House"]]: getSectionalScores(auctionHouseQuestionnaireData),
        [sectorsNameToId["Packer"]]: getSectionalScores(packerQuestionnaireData),
        [sectorsNameToId["Stocker/Backgrounder"]]: getSectionalScores(stockerBackGrounderQuestionnaireData)
    };
    return sectorBasedSectionalTotals;
}

const getSectionalScores = (questionnaireData) => {
    let result = {};
    let totalScore = 0;
    for(const section in questionnaireData){
        let questions = questionnaireData[section];
        let sectionScore = 0;
        for(const question of questions){
            if(question.scoringCriteria == scoringCriteria.roundOff){
                sectionScore += 1;
            }
            else{
                sectionScore += question.score;
            }
        }
        totalScore += sectionScore;
        result[section] = sectionScore;
    }
    result["total"] = totalScore;
    return result;
}

export {
    sections,
    scoringCriteria,
    questionType,
    cowCalfQuestionnaireData,
    auctionHouseQuestionnaireData,
    feedlotQuestionnaireData,
    packerQuestionnaireData,
    stockerBackGrounderQuestionnaireData,
    calculateSustainabilityQuestionnaireMaxScores
};