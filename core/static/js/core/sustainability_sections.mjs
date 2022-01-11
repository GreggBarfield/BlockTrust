const sections = {
    "air": "Air & Greenhouse Gas Emissions",
    "land": "Land Resources",
    "water": "Water Resources",
    "animal": "Animal Health & Well-Being",
    "safety": "Employee Safety & Well-Being",
    "efficiency": "Efficiency & Yield"
};

export function getSustainabilitySections(neededSections=null) {
    if (neededSections == null) {
        return sections;
    } else {
        let resultSections = {};
        for (const sectionType of neededSections) {
            resultSections[sectionType] = sections[sectionType];
        }
        return resultSections;
    }
}