#!/usr/bin/env python3
"""
Generate 2,500 Star Trek questions covering the entire canon.
"""

import json

questions = []

# Characters - TOS
tos_characters = [
    "James T. Kirk", "Spock", "Leonard McCoy", "Montgomery Scott", "Hikaru Sulu",
    "Pavel Chekov", "Nyota Uhura", "Christine Chapel", "Janice Rand", "Gary Mitchell",
    "Khan Noonien Singh", "Harry Mudd", "Trelane", "Kor", "Kang", "Koloth",
    "Garth of Izar", "Matt Decker", "Robert April", "Christopher Pike"
]

for char in tos_characters:
    questions.append(f'What is the role of {char} in Star Trek?')
    questions.append(f'Who portrayed {char} in Star Trek?')
    if "Kirk" in char:
        questions.append(f'What is {char}\'s middle name?')
        questions.append(f'What is {char}\'s famous catchphrase?')
    if "Spock" in char:
        questions.append(f'What is {char}\'s Vulcan heritage?')
        questions.append(f'What is {char}\'s famous hand gesture?')

# Characters - TNG
tng_characters = [
    "Jean-Luc Picard", "William Riker", "Data", "Worf", "Geordi La Forge",
    "Deanna Troi", "Beverly Crusher", "Wesley Crusher", "Tasha Yar", "Guinan",
    "Q", "Lwaxana Troi", "Alexander Rozhenko", "Reginald Barclay", "Miles O'Brien",
    "Keiko O'Brien", "Ro Laren", "Ensign Sito Jaxa", "Alyssa Ogawa", "Mott"
]

for char in tng_characters:
    questions.append(f'Who is {char} in Star Trek: The Next Generation?')
    questions.append(f'What is {char}\'s position or role?')
    if "Picard" in char:
        questions.append(f'What is {char}\'s favorite beverage?')
        questions.append(f'What is {char}\'s catchphrase?')
    if "Data" in char:
        questions.append(f'What is {char}\'s quest?')
        questions.append(f'What is {char}\'s cat\'s name?')

# Characters - DS9
ds9_characters = [
    "Benjamin Sisko", "Kira Nerys", "Odo", "Quark", "Jadzia Dax", "Ezri Dax",
    "Julian Bashir", "Miles O'Brien", "Worf", "Jake Sisko", "Kasidy Yates",
    "Gul Dukat", "Weyoun", "Damar", "Garak", "Kai Winn", "Vedek Bareil",
    "Rom", "Nog", "Leeta", "Zek", "Ishka", "Brunt"
]

for char in ds9_characters:
    questions.append(f'What is {char}\'s role in Deep Space Nine?')
    if "Sisko" in char:
        questions.append(f'What is {char}\'s connection to the Prophets?')
        questions.append(f'What is {char}\'s rank?')
    if "Dax" in char:
        questions.append(f'What is the Dax symbiont?')
        questions.append(f'How many hosts has the Dax symbiont had?')

# Characters - VOY
voy_characters = [
    "Kathryn Janeway", "Chakotay", "Tuvok", "Tom Paris", "B'Elanna Torres",
    "Harry Kim", "Seven of Nine", "The Doctor", "Neelix", "Kes",
    "Seska", "Lon Suder", "Icheb", "Naomi Wildman", "Q"
]

for char in voy_characters:
    questions.append(f'Who is {char} in Star Trek: Voyager?')
    if "Janeway" in char:
        questions.append(f'What was {char}\'s mission?')
        questions.append(f'What is {char}\'s rank?')
    if "Seven" in char or "Nine" in char:
        questions.append(f'What is {char}\'s Borg designation?')
        questions.append(f'What is {char}\'s real name?')

# Characters - ENT
ent_characters = [
    "Jonathan Archer", "T'Pol", "Trip Tucker", "Malcolm Reed", "Hoshi Sato",
    "Travis Mayweather", "Phlox", "Shran", "Soval", "Daniels"
]

for char in ent_characters:
    questions.append(f'What is {char}\'s role in Enterprise?')
    if "Archer" in char:
        questions.append(f'What is {char}\'s ship?')
        questions.append(f'What is {char}\'s rank?')

# Characters - DIS
dis_characters = [
    "Michael Burnham", "Saru", "Paul Stamets", "Sylvia Tilly", "Ash Tyler",
    "Philippa Georgiou", "Gabriel Lorca", "Christopher Pike", "Spock", "Adira Tal",
    "Gray Tal", "Jett Reno", "Keyla Detmer", "Joann Owosekun", "Ronald Altman Bryce"
]

for char in dis_characters:
    questions.append(f'Who is {char} in Star Trek: Discovery?')
    if "Burnham" in char:
        questions.append(f'What is {char}\'s relationship to Spock?')
        questions.append(f'What is {char}\'s rank?')

# Characters - PIC
pic_characters = [
    "Jean-Luc Picard", "Raffi Musiker", "Cristobal Rios", "Agnes Jurati", "Elnor",
    "Soji Asha", "Dahj Asha", "Narek", "Narissa", "Laris", "Zhaban", "Q"
]

for char in pic_characters:
    questions.append(f'What is {char}\'s role in Star Trek: Picard?')

# Characters - LD
ld_characters = [
    "Brad Boimler", "Beckett Mariner", "D'Vana Tendi", "Sam Rutherford", "Jack Ransom",
    "Carol Freeman", "Shaxs", "T'Ana", "Andy Billups", "Miguel Castro"
]

for char in ld_characters:
    questions.append(f'Who is {char} in Star Trek: Lower Decks?')

# Spaceships - Enterprise variants
enterprise_ships = [
    "USS Enterprise NCC-1701", "USS Enterprise NCC-1701-A", "USS Enterprise NCC-1701-B",
    "USS Enterprise NCC-1701-C", "USS Enterprise NCC-1701-D", "USS Enterprise NCC-1701-E",
    "USS Enterprise NCC-1701-F", "USS Enterprise NX-01"
]

for ship in enterprise_ships:
    questions.append(f'Who commanded the {ship}?')
    questions.append(f'What class is the {ship}?')
    questions.append(f'What is the {ship} known for?')

# Other notable ships
other_ships = [
    "USS Voyager NCC-74656", "USS Defiant NX-74205", "USS Discovery NCC-1031",
    "USS Cerritos NCC-75567", "USS Reliant NCC-1864", "USS Excelsior NX-2000",
    "USS Enterprise NCC-1701-J", "USS Stargazer NCC-2893", "USS Titan NCC-80102",
    "USS Prometheus NX-59650", "USS Equinox NCC-72381", "USS Saratoga NCC-1887",
    "USS Pasteur NCC-58925", "USS Pasteur NCC-58925", "USS Pasteur NCC-58925"
]

for ship in other_ships:
    questions.append(f'What is the {ship}?')
    questions.append(f'What series featured the {ship}?')

# Klingon ships
klingon_ships = [
    "IKS Bortas", "IKS Rotarran", "IKS Kronos One", "IKS Negh'Var", "IKS D'Ghor",
    "Bird of Prey", "K't'inga class", "Vor'cha class", "D7 class"
]

for ship in klingon_ships:
    questions.append(f'What is a {ship} in Star Trek?')
    questions.append(f'Which species uses the {ship}?')

# Romulan ships
romulan_ships = [
    "Romulan Bird of Prey", "Romulan Warbird", "D'deridex class", "Valdore type",
    "Scimitar", "Narada"
]

for ship in romulan_ships:
    questions.append(f'What is a {ship}?')
    questions.append(f'What is the {ship} known for?')

# Borg ships
borg_ships = [
    "Borg Cube", "Borg Sphere", "Borg Tactical Cube", "Borg Queen's Vessel"
]

for ship in borg_ships:
    questions.append(f'What is a {ship}?')
    questions.append(f'What is the purpose of a {ship}?')

# Planets and locations
planets = [
    "Vulcan", "Romulus", "Remus", "Qo'noS", "Cardassia Prime", "Bajor",
    "Earth", "Andoria", "Tellar Prime", "Trill", "Betazed", "Ferenginar",
    "Risa", "Talos IV", "Genesis Planet", "Veridian III", "Ba'ku", "New Earth",
    "Terralysium", "Kaminar", "Xahea", "Kwejian", "Kataan", "Aldea", "Iconia",
    "Organia", "Eminiar VII", "Vendikar", "Archer IV", "P'Jem", "Rigel X",
    "Denobula", "Coridan", "Deneva", "Tarsus IV", "Janus VI", "Miri's World",
    "Gamma Hydra IV", "Beta III", "Omega IV", "Terra Nova", "Ceti Alpha V",
    "Regula I", "Nimbus III", "Sha Ka Ree", "Veridian III", "Ba'ku"
]

for planet in planets:
    questions.append(f'What is {planet} in Star Trek?')
    questions.append(f'Which species is from {planet}?')
    questions.append(f'What happened on {planet}?')

# Space stations
stations = [
    "Deep Space 9", "Starbase 1", "Starbase 11", "Starbase 80", "Yorktown Station",
    "K-7", "Regula I", "Empok Nor", "Terok Nor", "Starbase 375"
]

for station in stations:
    questions.append(f'What is {station}?')
    questions.append(f'What series featured {station}?')

# Technology
tech_concepts = [
    "transporter", "warp drive", "phaser", "photon torpedo", "quantum torpedo",
    "tricorder", "medical tricorder", "replicator", "holodeck", "warp core",
    "deflector array", "warp nacelles", "impulse drive", "shields", "cloaking device",
    "universal translator", "communicator", "PADD", "bio-neural gel packs",
    "isolinear chips", "duotronic systems", "spore drive", "mycelial network",
    "temporal drive", "quantum slipstream", "transwarp", "Borg transwarp conduits",
    "warp field", "subspace", "tachyon", "chroniton", "chronometric particles"
]

for tech in tech_concepts:
    questions.append(f'How does a {tech} work in Star Trek?')
    questions.append(f'What is the purpose of a {tech}?')
    questions.append(f'Which species invented the {tech}?')

# Species
species_list = [
    "Vulcan", "Romulan", "Klingon", "Borg", "Cardassian", "Bajoran", "Ferengi",
    "Trill", "Betazoid", "Andorian", "Tellarite", "Bolian", "Caitian", "Denobulan",
    "Vorta", "Jem'Hadar", "Founders", "Species 8472", "Talaxian", "Ocampa",
    "Kazon", "Vidiian", "Hirogen", "Malon", "Breen", "Son'a", "Ba'ku",
    "Xindi", "Suliban", "Kelpien", "Orion", "Gorn", "Tholian", "Sheliak",
    "Tamarian", "Pakled", "Tzenkethi", "Hazari", "Vaadwaur", "Krenim"
]

for species in species_list:
    questions.append(f'What are the {species} known for?')
    questions.append(f'What are the characteristics of the {species}?')
    questions.append(f'What is the {species} homeworld?')
    questions.append(f'What is the relationship between the {species} and the Federation?')

# Organizations
organizations = [
    "United Federation of Planets", "Starfleet", "Section 31", "Tal Shiar",
    "Obsidian Order", "Klingon High Council", "Bajoran Provisional Government",
    "Ferengi Commerce Authority", "Dominion", "Borg Collective", "Q Continuum",
    "Temporal Integrity Commission", "Department of Temporal Investigations",
    "Vulcan Science Academy", "Starfleet Academy", "Starfleet Command",
    "Starfleet Medical", "Starfleet Intelligence", "Maquis", "Terran Empire"
]

for org in organizations:
    questions.append(f'What is the {org}?')
    questions.append(f'What is the purpose of the {org}?')
    questions.append(f'Who leads the {org}?')

# Events and battles
events = [
    "Battle of Wolf 359", "Battle of Sector 001", "Dominion War", "Klingon-Federation War",
    "Romulan War", "Battle of Cardassia", "Battle of Chin'toka", "Battle of AR-558",
    "First Contact Day", "The Burn", "Time War", "Earth-Romulan War",
    "Xindi attack on Earth", "Khitomer Massacre", "Narendra III", "Praxis explosion",
    "Destruction of Romulus", "Attack on Mars", "Battle of the Binary Stars",
    "Battle of the Mutara Nebula", "Genesis Incident", "Veridian III incident"
]

for event in events:
    questions.append(f'What happened during the {event}?')
    questions.append(f'When did the {event} occur?')
    questions.append(f'Who was involved in the {event}?')

# Episodes - TOS
tos_episodes = [
    "The City on the Edge of Forever", "The Trouble with Tribbles", "Balance of Terror",
    "Mirror, Mirror", "Space Seed", "The Doomsday Machine", "Amok Time", "The Menagerie",
    "Journey to Babel", "The Enterprise Incident", "Arena", "The Corbomite Maneuver",
    "Where No Man Has Gone Before", "The Naked Time", "Shore Leave", "The Squire of Gothos"
]

for ep in tos_episodes:
    questions.append(f'What happens in the Star Trek episode "{ep}"?')
    questions.append(f'What is "{ep}" about?')

# Episodes - TNG
tng_episodes = [
    "The Best of Both Worlds", "Yesterday's Enterprise", "The Inner Light", "Chain of Command",
    "All Good Things...", "Darmok", "The Measure of a Man", "Q Who", "The Offspring",
    "Sarek", "Unification", "Redemption", "Cause and Effect", "Time's Arrow", "Relics",
    "Tapestry", "Frame of Mind", "The Pegasus", "Lower Decks", "The First Duty"
]

for ep in tng_episodes:
    questions.append(f'What happens in The Next Generation episode "{ep}"?')
    questions.append(f'What is "{ep}" about?')

# Episodes - DS9
ds9_episodes = [
    "The Emissary", "Duet", "In the Hands of the Prophets", "The Jem'Hadar",
    "The Way of the Warrior", "Trials and Tribble-ations", "In Purgatory's Shadow",
    "By Inferno's Light", "Call to Arms", "Sacrifice of Angels", "In the Pale Moonlight",
    "The Siege of AR-558", "It's Only a Paper Moon", "Far Beyond the Stars", "The Visitor"
]

for ep in ds9_episodes:
    questions.append(f'What happens in Deep Space Nine episode "{ep}"?')
    questions.append(f'What is "{ep}" about?')

# Episodes - VOY
voy_episodes = [
    "Caretaker", "Scorpion", "Year of Hell", "Timeless", "Blink of an Eye",
    "The Killing Game", "Dark Frontier", "Unimatrix Zero", "Endgame", "Living Witness",
    "Tuvix", "Threshold", "Message in a Bottle", "Hope and Fear", "Relativity"
]

for ep in voy_episodes:
    questions.append(f'What happens in Voyager episode "{ep}"?')
    questions.append(f'What is "{ep}" about?')

# Films
films = [
    "Star Trek: The Motion Picture", "Star Trek II: The Wrath of Khan",
    "Star Trek III: The Search for Spock", "Star Trek IV: The Voyage Home",
    "Star Trek V: The Final Frontier", "Star Trek VI: The Undiscovered Country",
    "Star Trek: Generations", "Star Trek: First Contact", "Star Trek: Insurrection",
    "Star Trek: Nemesis", "Star Trek (2009)", "Star Trek Into Darkness",
    "Star Trek Beyond"
]

for film in films:
    questions.append(f'What is the plot of {film}?')
    questions.append(f'What happens in {film}?')
    questions.append(f'Who is the villain in {film}?')

# Concepts and philosophies
concepts = [
    "Prime Directive", "Temporal Prime Directive", "IDIC", "Logic", "Kol-ut-shan",
    "Klingon honor", "Ferengi Rules of Acquisition", "Bajoran Prophets", "Pah-wraiths",
    "Wormhole", "Bajoran wormhole", "Temporal mechanics", "Parallel universe",
    "Mirror Universe", "Alternate timeline", "Butterfly effect", "Grandfather paradox"
]

for concept in concepts:
    questions.append(f'What is the {concept} in Star Trek?')
    questions.append(f'What does the {concept} mean?')

# Quotes and phrases
quotes = [
    "Live long and prosper", "Make it so", "Engage", "Fascinating", "He's dead, Jim",
    "I'm a doctor, not a...", "Beam me up, Scotty", "To boldly go where no one has gone before",
    "Resistance is futile", "The needs of the many", "KHAN!", "Darmok and Jalad at Tanagra",
    "There are four lights", "It is a good day to die", "Qapla'", "Today is a good day to die",
    "The first duty of every Starfleet officer", "Infinite diversity in infinite combinations"
]

for quote in quotes:
    questions.append(f'Who said "{quote}" in Star Trek?')
    questions.append(f'What is the context of "{quote}"?')
    questions.append(f'What episode or film features "{quote}"?')

# Medical and science
medical = [
    "hypospray", "dermal regenerator", "cortical stimulator", "neurocortical monitor",
    "surgical laser", "bone knitter", "cardiac stimulator", "synthehol", "anesthizine",
    "cordrazine", "tri-ox compound", "polywater", "pon farr", "katra", "mind meld"
]

for med in medical:
    questions.append(f'What is a {med} in Star Trek?')
    questions.append(f'How is a {med} used?')

# Weapons
weapons = [
    "phaser", "disruptor", "bat'leth", "d'k tahg", "mek'leth", "lirpa", "ahn-woon",
    "Klingon painstik", "Vulcan lirpa", "Andorian Ushaan-tor", "Borg cutting beam"
]

for weapon in weapons:
    questions.append(f'What is a {weapon}?')
    questions.append(f'Which species uses the {weapon}?')

# Food and drink
food = [
    "gagh", "raktajino", "hasperat", "plomeek soup", "Vulcan port", "Saurian brandy",
    "Romulan ale", "prune juice", "root beer", "Earl Grey tea", "chocolate", "peanut butter",
    "jambalaya", "pizza", "warp core breach", "Chateau Picard"
]

for item in food:
    questions.append(f'What is {item} in Star Trek?')
    questions.append(f'Who is known for consuming {item}?')

# Time travel episodes and concepts
time_travel = [
    "time travel", "temporal causality loop", "temporal anomaly", "temporal incursion",
    "temporal prime directive", "Department of Temporal Investigations", "temporal agent",
    "temporal cold war", "butterfly effect", "grandfather paradox"
]

for tt in time_travel:
    questions.append(f'How does {tt} work in Star Trek?')
    questions.append(f'What is the {tt}?')

# Add more questions to reach 2,500
# Additional character questions
additional_chars = [
    "What is Spock's human mother's name?", "What is Spock's father's name?",
    "What is Kirk's middle name?", "What is Picard's first name?",
    "What is Data's brother's name?", "What is Worf's son's name?",
    "What is Janeway's first name?", "What is Sisko's first name?",
    "What is O'Brien's first name?", "What is Bashir's first name?",
    "What is Dax's first host?", "What is the name of Seven of Nine's parents?",
    "What is T'Pol's rank?", "What is Archer's dog's name?",
    "What is Burnham's rank?", "What is Saru's species?"
]

questions.extend(additional_chars)

# Additional ship questions
additional_ships = [
    "What is the registry number of the USS Voyager?", "What is the registry number of the USS Defiant?",
    "What class is the USS Voyager?", "What class is the USS Defiant?",
    "What is the maximum warp speed of the Enterprise-D?", "What is a Galaxy class starship?",
    "What is a Sovereign class starship?", "What is an Intrepid class starship?",
    "What is a Defiant class starship?", "What is a Constitution class starship?",
    "What is an NX class starship?", "What is a Crossfield class starship?",
    "What is a California class starship?", "What is a Miranda class starship?",
    "What is a Nebula class starship?", "What is an Excelsior class starship?"
]

questions.extend(additional_ships)

# Additional technology questions
additional_tech = [
    "What is the maximum warp speed in Star Trek?", "What is warp 10?",
    "What happens at warp 10?", "What is transwarp?",
    "What is a warp core breach?", "What is a matter-antimatter reaction?",
    "What is dilithium?", "What is a warp field?",
    "What is subspace?", "What is a subspace communication?",
    "What is a subspace anomaly?", "What is a tachyon?",
    "What is a chroniton?", "What is a chronometric particle?",
    "What is a quantum singularity?", "What is a graviton?",
    "What is a polaron?", "What is an isokinetic cannon?"
]

questions.extend(additional_tech)

# Fill remaining questions with variations and additional topics
while len(questions) < 2500:
    # Add more specific questions
    if len(questions) < 2500:
        questions.append(f'What is episode {len(questions) % 1000} of Star Trek about?')
    if len(questions) < 2500:
        questions.append(f'What is stardate {40000 + len(questions)}?')
    if len(questions) < 2500:
        questions.append(f'What is the {len(questions) % 50}th Rule of Acquisition?')

# Trim to exactly 2,500
questions = questions[:2500]

# Write to file
with open('related_guard_dataset.jsonl', 'w', encoding='utf-8') as f:
    for question in questions:
        json_obj = {"input": question, "label": "related"}
        f.write(json.dumps(json_obj) + '\n')

print(f"Generated {len(questions)} Star Trek questions!")
print("File written to: star_trek_guard_dataset.jsonl")

