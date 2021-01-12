import csv
import InsertModel
import MatchModel
import MatchGeneratorMFA
import re
import json
import traceback

import DatabaseInterface

print('Launching Tester')
print('Loading an insert...')

example_insert = InsertModel.InsertModel()
example_insert.id = 102421
example_insert.account = 582
example_insert.namespace = 'MFA'
example_insert.type = 'Animal'
example_insert.fields = '["AnimalID", "OrganizationalUnitID", "TennantID", "UserID", "VisualID", "AnimalTypeID", "EID", "AlternateID1", "AlternateID2", "TatooID", "TatooLocation", "BrandID", "BrandLocation", "Sire", "SireAnimalID", "Dam", "DamAnimalID", "DonorCow", "DonorCowAnimalID", "Birthdate", "BirthWeight", "CalfSexID", "CastrationMethodID", "CastrationDate", "HideColorID", "BreedID", "RegistrationNumber", "WeanDate", "Owner", "DeathDate", "AnimalGroupID", "LocationID", "IsActive", "ArtificialInseminationBullInventoryID", "CreatedTimestamp", "ModifiedTimestamp", "ArchiveTimestamp", "EraseTimestamp"]'
example_insert.fields = json.loads(example_insert.fields)
example_insert.row = '["aa647b80-0b5b-444f-bc24-9ca796d365c0", 43, 41, 10036, "BH4678", 1, "982000422129460", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", true, "", "2018-06-27T15:57:35.32", "2020-12-21T16:57:59.537", "", ""]'
example_insert.row = json.loads(example_insert.row)
example_insert.created = '2020-12-30 14:46:45'

example_fields = example_insert.fields
example_row = example_insert.row

for i in range(0, len(example_fields)):
    print(str(example_fields[i]) + ' : [' + str(example_row[i]) + ']' + ' -> data type : ' + str(type(example_row[i])))


matchGenerator = None
if (example_insert.namespace == "MFA"):
    matchGenerator = MatchGeneratorMFA.MatchGeneratorMFA()
else:
    matchGenerator = None

matches = matchGenerator.generate_matches(example_insert)

print('---------------------------------')
print('----------End Results------------')
print('---------------------------------')

for m in matches:
    print(str(m.to_list()) + ' verified: ' + str(m.verify_values()))


print('---------------------------------')
print()
print('Launching DB Interface Tests')
print('----------------------------------')

print('Attempting DB Connection')
db_interface = DatabaseInterface.DatabaseInterface()
print('Resulting Inserts')
print('-----------------------------------')
temp_insert = db_interface.get_next_insert()
num_insert = 0
matches = []
while (temp_insert != None):
    #print('Insert: ' + str(num_insert))
    num_insert += 1
    #print(temp_insert.to_list())
    #print()

    try:
        matchGenerator = None
        if (temp_insert.namespace == "MFA"):
            matchGenerator = MatchGeneratorMFA.MatchGeneratorMFA()
        else:
            print('No match generator found for insert #' + str(num_insert))
            matchGenerator = None

        matches.extend(matchGenerator.generate_matches(temp_insert))
        if (matchGenerator.generate_matches(temp_insert) == None):
            print('No matches found for insert #' + str(num_insert))
        else:
            print(str(len(matchGenerator.generate_matches(temp_insert))) + ' MATCHES MADE FOR INSERT #' + str(num_insert))
    except Exception as e:
        print('Match generation failed, skipping insert #' + str(num_insert))
        print(e)

    temp_insert = db_interface.get_next_insert()

print ('Completed iterating over inserts!')
print ('-----------------------------------')
print('Generated Matches')
print('------------------------------------')
for i in range(0, len(matches)):
    print('Match [' + str(i) + ']: ' + str(matches[i].to_list()))
db_interface.close_connection()


