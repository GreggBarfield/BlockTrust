// /<\s*[a-zA-Z\s/=\"0-9]*>\s*/g
// ([a-z0-9A-Z])""
// $1",
// \t"
let commonBreedNames = [
    "Amerifax",
	"Angus",
	"Angus Cross",
	"Angus F1",
	"Angus Plus",
	"Aubrac",
	"Balancer",
	"Barzona",
	"Beef Friesian",
	"Beefalo",
	"Beefmaster",
	"Beefmaster Cross",
	"Belgian Blue",
	"Belted Galloway",
	"Black Angus",
	"Black Hereford",
	"Black Simmental",
	"Blonde d' Aquitaine",
	"Braford",
	"Brahman",
	"Brahman Cross",
	"Brahman F1",
	"Brahmousin",
	"Brangus",
	"Brangus Cross",
	"Braunvieh",
	"Braunvieh F1",
	"British White",
	"Charbray",
	"Charloais F1",
	"Charolais",
	"Charolais Cross",
	"Chianina",
	"Corriente",
	"Criollo",
	"Crossbred",
	"Devon",
	"Dexter",
	"Fleckvieh",
	"Galloway",
	"Gelbvieh",
	"Gelbvieh Cross",
	"Gelbvieh F1",
	"Hereford",
	"Hereford Cross",
	"Hereford F1",
	"Holstein",
	"Irish Blacks",
	"Jersey",
	"LimFlex",
	"Limousin",
	"Limousin Cross",
	"Limousin F1",
	"Longhorn",
	"Lowline",
	"Maine-Anjou",
	"Murray Grey",
	"Piedmontese",
	"Pinzgauer",
	"Polled Hereford",
	"Randall",
	"Red Angus",
	"Red Angus Cross",
	"Red Brangus",
	"Red Poll",
	"Romagnola",
	"Salers",
	"Santa Cruz",
	"Santa Gertrudis",
	"Santa Gertrudis Cross",
	"Scottish Highlander",
	"Senepol",
	"Shorthorn",
	"Shorthorn Cross",
	"Shorthorn F1",
	"SimAngus",
	"Simbrah",
	"Simmental",
	"Simmental Cross",
	"Simmental F1",
	"South Devon",
	"South Poll",
	"Star 5",
	"Tarentaise",
	"Texas Cross",
	"Tigerstripe",
	"Wagyu",
	"White Park",
	"Not Reported",
];

let commonProgramNames = [
	"Conventional",
	"Natural",
	"NHTC",
	"ALL"
];

let commonMiles = [
    50,
    100,
    150,
    200,
    250,
    300,
    400,
    500
];

let commonWeights = [];
for (let i = 400; i <= 950; i+=50) { commonWeights.push(i); }

let commonPreconditioningProgramNames = [
	"Health Track",
	"Value Added Calf-45",
	"OQBN Vac-45 Program",
	"JRS Wean-Vac 45",
	"Superior Livestock Vac-45",
	"TAMU Vac-45",
	"Integrity Beef Alliance Vac-45",
	"MFA Health Track Vac-45",
	"NMSU Vac-45",
	"MCA Vac-45",
	"PrimeVac Vac-45",
	"SelectVac WeanVac"
];

let commonFrames = [
	"N/A",
	"Small",
	"Medium",
	"Large"
];

let commonMusclings = [
	"N/A",
	"Light",
	"Heavy"
];

let commonHorns = [
	"N/A",
	"Horns",
	"No Horns"
]

let commonVaccinations = [
	"Not Applicable",
	"Blackleg",
	"H. Somnus",
	"Pasturella",
	"4-way virus (MLV)",
	"4-way virus (Killed)",
	"5-way virus (MLV)",
	"5-way virus (Killed)",
	"Internal Parasites",
	"External Parasites"
];

let commonDeliveryLocationTypes = [
	"Direct/Off Ranch",
	"Auction",
	"Video Auction",
	"Internet"
];

let commonCastrated = [
	"Not Applicable",
	"Not Castrated",
	"Banded",
	"Blade",
	"Chemicals",
	"Other"
];

let commonFeedingPrograms = [
	"Not Applicable",
	"Native Range",
	"Improved Pasture"
];

let commonImplants = [
	"Not Applicable",
	"Ralgro"
];

let commonCategoryNames = [
	"Mixed Steers and Heifers",
	"Feeder Steers",
	"Feeder Heifers",
	"Beef Dairy Cross Steers",
	"Beef Dairy Cross Heifers",
	"Weaned Heifer Calves",
	"Weaned Steer Calves",
	"Steer Calves",
	"Heifer Calves",
	"Replacement Heifers",
	"Bred Cows"
];

export let SalesGroupFields = {
    commonBreedNames: commonBreedNames,
    commonProgramNames: commonProgramNames,
	commonMiles: commonMiles,
	commonWeights: commonWeights,
	commonPreconditioningProgramNames: commonPreconditioningProgramNames,
	commonFrames: commonFrames,
	commonVaccinations: commonVaccinations,
	commonDeliveryLocationTypes: commonDeliveryLocationTypes,
	commonCastrated: commonCastrated,
	commonFeedingPrograms: commonFeedingPrograms,
	commonImplants: commonImplants,
	commonCategoryNames: commonCategoryNames,
	commonMusclings: commonMusclings,
	commonHorns: commonHorns
};
