#!/usr/bin/env python3
"""
Generate 2,500 unique questions about New Zealand for the guard dataset.
"""

import json
import random

def generate_questions():
    questions = []
    
    # Geography - Cities and Towns
    cities = [
        "Auckland", "Ashburton", "Wellington", "Christchurch", "Hamilton", "Tauranga", "Napier", "Dunedin",
        "Palmerston North", "Rotorua", "New Plymouth", "Whangarei", "Invercargill", "Nelson",
        "Hastings", "Napier", "Porirua", "Gisborne", "Timaru", "Blenheim", "Taupo", "Masterton", "Whanganui",
        "Queenstown", "Wanaka", "Te Anau", "Kaikoura", "Picton", "Franz Josef", "Fox Glacier", "Greymouth", "Motueka", "Cambridge", "Matamata", "Oamaru", "Cromwell", "Warkworth", "Kerikeri", "Kaitaia", "Dargaville", "Hokitika", "Stratford"
    ]
    
    for city in cities:
        questions.extend([
            f"What is the population of {city}?",
            f"Where is {city} located in New Zealand?",
            f"What is {city} known for?",
            f"What region is {city} in?",
            f"How far is {city} from Auckland?",
            f"What is the climate like in {city}?",
            f"What are the main industries in {city}?",
            f"What tourist attractions are in {city}?",
            f"When was {city} founded?",
            f"What is the elevation of {city}?",
            f"What is the history of {city}?",
            f"What events are held in {city}?",
            f"What sports teams are based in {city}?",
        ])
    
    # Geography - Regions
    regions = [
        "Northland", "Auckland", "Waikato", "Bay of Plenty", "Gisborne", "Hawke's Bay",
        "Taranaki", "Manawatu-Wanganui", "Wellington", "Tasman", "Nelson", "Marlborough",
        "West Coast", "Canterbury", "Otago", "Southland"
    ]
    
    for region in regions:
        questions.extend([
            f"What is the largest city in {region}?",
            f"What is {region} famous for?",
            f"What is the geography of {region}?",
            f"What industries are prominent in {region}?",
            f"What is the population of {region}?",
            f"What are the main towns in {region}?",
            f"What is the climate in {region}?",
            f"What national parks are in {region}?",
            f"What rivers run through {region}?",
            f"What mountains are in {region}?",
            f"What tourist attractions are in {region}?",
            f"What is the history of {region}?",
        ])
    
    # Geography - Mountains
    mountains = [
        "Mount Cook", "Mount Aspiring", "Mount Ruapehu", "Mount Taranaki", "Mount Ngauruhoe",
        "Mount Tongariro", "Mount Egmont", "Mount Tasman", "Mount Dampier", "Mount Hicks",
        "Mount Sefton", "Mount La Perouse", "Mount Haast", "Mount Elie de Beaumont"
    ]
    
    for mountain in mountains:
        questions.extend([
            f"What is the height of {mountain}?",
            f"Where is {mountain} located?",
            f"Can you climb {mountain}?",
            f"What is the Maori name for {mountain}?",
            f"When was {mountain} first climbed?",
            f"What type of mountain is {mountain}?",
            f"What is the geology of {mountain}?",
            f"What national park is {mountain} in?",
            f"What wildlife can be found on {mountain}?",
            f"What is the climate like on {mountain}?"
        ])
    
    # Geography - Rivers and Lakes
    rivers_lakes = [
        "Waikato River", "Clutha River", "Wanganui River", "Rangitikei River", "Mataura River",
        "Taieri River", "Lake Taupo", "Lake Wakatipu", "Lake Wanaka", "Lake Manapouri",
        "Lake Te Anau", "Lake Pukaki", "Lake Tekapo", "Lake Rotorua"
    ]
    
    for water in rivers_lakes:
        questions.extend([
            f"How long is {water}?",
            f"Where does {water} flow?",
            f"What is {water} known for?",
            f"What is the depth of {water}?",
            f"What activities can you do at {water}?",
            f"What wildlife is found in {water}?",
            f"What is the history of {water}?",
            f"What is the significance of {water} to Maori?",
            f"What is the water quality of {water}?",
        ])
    
    # Geography - Islands
    islands = [
        "North Island", "South Island", "Stewart Island", "Waiheke Island", "Great Barrier Island",
        "Chatham Islands", "Auckland Islands", "Campbell Island", "Kapiti Island", "Matiu/Somes Island"
    ]
    
    for island in islands:
        questions.extend([
            f"What is the population of {island}?",
            f"What is {island} known for?",
            f"How do you get to {island}?",
            f"What is the area of {island}?",
            f"What wildlife is found on {island}?",
            f"What activities can you do on {island}?",
            f"What is the history of {island}?",
            f"What is the climate like on {island}?",
            f"What are the main towns on {island}?",
        ])
    
    # Languages
    questions.extend([
        "What is the official language of New Zealand?",
        "What languages are spoken in New Zealand?",
        "What is Te Reo Maori?",
        "How many people speak Maori in New Zealand?",
        "What is New Zealand Sign Language?",
        "What percentage of New Zealanders speak Maori?",
        "What is the Maori word for hello?",
        "What is the Maori word for thank you?",
        "What is the Maori word for New Zealand?",
        "What is the Maori word for family?",
        "What is the Maori word for water?",
        "What is the Maori word for mountain?",
        "What is the Maori word for river?",
        "What is the Maori word for sea?",
        "What is the Maori word for forest?",
        "What is the Maori word for bird?",
        "What is the Maori word for fish?",
        "What is the Maori word for food?",
        "What is the Maori word for house?",
        "What is the Maori word for land?",
        "What is a haka?",
        "What is a powhiri?",
        "What is a marae?",
        "What is a whanau?",
        "What is a iwi?",
        "What is a hapu?",
        "What is the Treaty of Waitangi?",
        "What is Waitangi Day?",
        "What is Matariki?",
        "What is a hangi?"
    ])
    
    # Famous People - Politicians
    politicians = [
        "Jacinda Ardern", "Helen Clark", "David Lange", "Peter Fraser", "Michael Joseph Savage",
        "Richard Seddon", "John Key", "Bill English", "Chris Hipkins", "Christopher Luxon",
        "Winston Peters", "David Seymour", "James Shaw", "Marama Davidson", "Jim Bolger", "John Banks", "Jenny Shipley", "Geoffrey Palmer", "Bill Rowling", "Robert Muldoon", "Norman Kirk", "Keith Holyoake", "Sidney Holland", "Joseph Ward", "William Massey", "George Grey"
    ]
    
    for person in politicians:
        questions.extend([
            f"Who is {person}?",
            f"What did {person} do?",
            f"When was {person} Prime Minister?",
            f"What party did {person} belong to?",
            f"What is {person} known for?",
            f"What policies did {person} implement?",
            f"What is the background of {person}?",
            f"What is the significance of {person} in New Zealand politics?",
            f"What awards has {person} won?"
        ])
    
    # Famous People - Actors and Directors
    actors = [
        "Russell Crowe", "Taika Waititi", "Jemaine Clement", "Bret McKenzie", "Lucy Lawless",
        "Sam Neill", "Anna Paquin", "Temuera Morrison", "Cliff Curtis", "Keisha Castle-Hughes",
        "Melanie Lynskey", "Thomasin McKenzie", "Rose McIver", "Karl Urban", "Danielle Cormack", "Robyn Malcolm", "Antonia Prebble", "Emily Barclay", "Joel Tobeck", "Pana Hema Taylor"
    ]
    
    for person in actors:
        questions.extend([
            f"Who is {person}?",
            f"What movies has {person} been in?",
            f"Where was {person} born?",
            f"What is {person} known for?",
            f"What awards has {person} won?",
            f"What is the background of {person}?",
            f"What is the significance of {person} in New Zealand cinema?",
            f"What directors has {person} worked with?",
            f"What upcoming projects does {person} have?"
        ])
    
    # Famous People - Athletes
    athletes = [
        "Richie McCaw", "Dan Carter", "Jonah Lomu", "Allan Border", "Martin Crowe",
        "Brendon McCullum", "Kane Williamson", "Ross Taylor", "Valerie Adams", "Lisa Carrington",
        "Peter Snell", "John Walker", "Hamish Bond", "Eric Murray", "Mahe Drysdale", "Zoi Sadowski-Synnott", "Nico Porteous", "Lydia Ko", "Michael Campbell", "Sir Bob Charles", "Sarah Walker", "Jesse Ryder", "Trent Boult", "Tim Southee", "Sophie Pascoe", "Ellie Black"
    ]
    
    for person in athletes:
        questions.extend([
            f"Who is {person}?",
            f"What sport does {person} play?",
            f"What achievements does {person} have?",
            f"Where was {person} born?",
            f"What records does {person} hold?",
            f"What teams has {person} played for?",
            f"What awards has {person} won?",
            f"What is the significance of {person} in New Zealand sports?",
            f"What is the background of {person}?"
        ])
    
    # Famous People - Musicians
    musicians = [
        "Lorde", "Crowded House", "Split Enz", "Dave Dobbyn", "Bic Runga",
        "Hayley Westenra", "Neil Finn", "Tim Finn", "Sharon O'Neill", "Dragon", "Six60", "The Naked and Famous", "Broods", "Kimbra", "Fat Freddy's Drop", "The Feelers", "Anika Moa", "Stan Walker", "Aaradhna", "Marlon Williams", "Alec Benjamin"
    ]
    
    for person in musicians:
        questions.extend([
            f"Who is {person}?",
            f"What songs is {person} known for?",
            f"Where was {person} born?",
            f"What genre does {person} perform?",
            f"What awards has {person} won?",
            f"What is the background of {person}?",
            f"What is the significance of {person} in New Zealand music?",
            f"What albums has {person} released?"
        ])
    
    # Famous People - Explorers and Historical Figures
    historical = [
        "James Cook", "Abel Tasman", "Kupe", "Te Rauparaha", "Te Kooti",
        "Kate Sheppard", "Ernest Rutherford", "Edmund Hillary", "Jean Batten", "Whina Cooper", "Apirana Ngata", "Richard Pearse", "Charles Upham", "Bishop Selwyn", "Samuel Marsden", "Dame Whina Cooper", "Dame Kiri Te Kanawa", "Dame Silvia Cartwright", "Dame Patsy Reddy", "Dame Anne Salmond", "Dame Joan Metge"
    ]
    
    for person in historical:
        questions.extend([
            f"Who is {person}?",
            f"What did {person} do?",
            f"When did {person} live?",
            f"What is {person} famous for?",
            f"What is the significance of {person} in New Zealand history?",
            f"What achievements does {person} have?",
            f"What is the background of {person}?",

        ])
    
    # Events - Historical
    questions.extend([
        "When did Captain Cook arrive in New Zealand?",
        "When was the Treaty of Waitangi signed?",
        "What happened in the New Zealand Wars?",
        "When did New Zealand become a dominion?",
        "When did New Zealand gain full independence?",
        "What was the 1931 Hawke's Bay earthquake?",
        "What happened in the 2010 Canterbury earthquake?",
        "What happened in the 2011 Christchurch earthquake?",
        "What was the Wahine disaster?",
        "What was the Erebus disaster?",
        "When did women get the vote in New Zealand?",
        "What was the Springbok Tour?",
        "What was the Rainbow Warrior bombing?",
        "What was the 1981 Springbok tour?",
        "What happened during the 1995 Rugby World Cup?",
        "What was the 2011 Rugby World Cup?",
        "What was the 2015 Cricket World Cup?",
        "What was the 2019 Cricket World Cup?"
    ])
    
    # Events - Cultural
    questions.extend([
        "What is Waitangi Day?",
        "What is ANZAC Day in New Zealand?",
        "What is Matariki?",
        "What is the Auckland Lantern Festival?",
        "What is the Wellington Sevens?",
        "What is the Pasifika Festival?",
        "What is the New Zealand International Arts Festival?",
        "What is the World of WearableArt?",
        "What is the Rhythm and Vines festival?",
        "What is the Splore festival?",
    ])
    
    # History - Pre-colonial
    questions.extend([
        "When did Maori first arrive in New Zealand?",
        "Where did Maori come from?",
        "What is the Maori name for New Zealand?",
        "Who was Kupe?",
        "What is the Great Fleet?",
        "What was pre-colonial Maori society like?",
        "What were Maori canoes called?",
        "What is a pa?",
        "What is a kainga?",
        "What is whakapapa?",
    ])
    
    # History - Colonial
    questions.extend([
        "When did Europeans first arrive in New Zealand?",
        "Who was the first European to see New Zealand?",
        "When did whaling begin in New Zealand?",
        "What was the Musket Wars?",
        "What was the New Zealand Company?",
        "What was the Wakefield scheme?",
        "What was the New Zealand Wars?",
        "What was the Taranaki War?",
        "What was the Waikato War?",
        "What was the Land Wars?",
        "What was the Kingitanga movement?",
        "When did the gold rush happen in New Zealand?",
        "What was the Vogel era?",
        "What was the Long Depression?"
    ])
    
    # History - Modern
    questions.extend([
        "When did New Zealand become a dominion?",
        "When did New Zealand gain full independence?",
        "What was the Great Depression in New Zealand?",
        "What was the First Labour Government?",
        "What was the welfare state in New Zealand?",
        "What was Rogernomics?",
        "What was Ruthanasia?",
        "What was the MMP electoral system?",
        "When did New Zealand become nuclear-free?",
        "What was the anti-nuclear movement?",
        "What was the Rainbow Warrior bombing?",
        "What was the 1981 Springbok tour?",
        "What was the 2011 Rugby World Cup?",
        "What was the 2015 Cricket World Cup?",
        "What was the 2019 Cricket World Cup?"

    ])
    
    # Culture - Maori
    questions.extend([
        "What is a haka?",
        "What is a powhiri?",
        "What is a marae?",
        "What is a wharenui?",
        "What is a wharekai?",
        "What is a hangi?",
        "What is a poi?",
        "What is a taiaha?",
        "What is a mere?",
        "What is moko?",
        "What is a koru?",
        "What is tukutuku?",
        "What is kowhaiwhai?",
        "What is whakairo?",
        "What is raranga?",
        "What is a waka?",
        "What is a waka ama?",
        "What is kapa haka?",
        "What is a tangi?",
        "What is a hui?",
        "What is tikanga Maori?",
        "What is mana?",
        "What is tapu?",
        "What is noa?",
        "What is utu?",
        "What is whanaungatanga?",
        "What is manaakitanga?",
        "What is kaitiakitanga?",
        "What is rangatiratanga?"
    ])
    
    # Culture - Food
    questions.extend([
        "What is a hangi?",
        "What is pavlova?",
        "What is a meat pie?",
        "What is fish and chips in New Zealand?",
        "What is a lamington?",
        "What is an Anzac biscuit?",
        "What is Marmite in New Zealand?",
        "What is Vegemite?",
        "What is a flat white?",
        "What is a long black?",
        "What is a flat white coffee?",
        "What is New Zealand wine?",
        "What is sauvignon blanc?",
        "What is pinot noir?",
        "What is New Zealand lamb?",
        "What is green-lipped mussels?",
        "What is paua?",
        "What is kina?",
        "What is kumara?",
        "What is rewena bread?",
        "What is hokey pokey ice cream?",
        "What is L&P?",
        "What is Whittaker's chocolate?",
        "What is Tip Top ice cream?",
        "What is Wattie's?",
    ])
    
    # Culture - Arts
    questions.extend([
        "Who is Colin McCahon?",
        "Who is Rita Angus?",
        "Who is Frances Hodgkins?",
        "What is the New Zealand Symphony Orchestra?",
        "What is the Royal New Zealand Ballet?",
        "What is the Auckland Philharmonia?",
        "What is the New Zealand Opera?",
        "What is the New Zealand Film Commission?",
        "What is the New Zealand International Film Festival?",
        "What is the Auckland Writers Festival?",
        "What is the Christchurch Arts Festival?",
        "What is the Wellington Festival?",
        "What is the New Zealand Portrait Gallery?",
        "What is the Museum of New Zealand Te Papa Tongarewa?",
        "What is the Auckland Art Gallery?",
        "What is the Christchurch Art Gallery?",
        "What is the Dunedin Public Art Gallery?",
        "What is the Govett-Brewster Art Gallery?",
        "What is the Sarjeant Gallery?",
        "What is the New Zealand Cartoon Archive?"
    ])
    
    # Wildlife - Birds
    birds = [
        "kiwi", "kea", "kakapo", "tui", "bellbird", "fantail", "morepork", "weka",
        "pukeko", "takahe", "kaka", "kereru", "shag", "albatross", "penguin"
    ]
    
    for bird in birds:
        questions.extend([
            f"What is a {bird}?",
            f"Where can you find {bird} in New Zealand?",
            f"Is the {bird} native to New Zealand?",
            f"What does a {bird} look like?",
            f"Is the {bird} endangered?",
            f"What does a {bird} eat?",
            f"What is the habitat of a {bird}?",
            f"What is the Maori name for {bird}?"
        ])
    
    # Wildlife - Animals
    animals = [
        "tuatara", "weta", "longfin eel", "shortfin eel", "New Zealand fur seal",
        "New Zealand sea lion", "Hector's dolphin", "Maui dolphin", "little blue penguin",
        "yellow-eyed penguin", "fiordland crested penguin", "New Zealand bat", "possums", "stoats", "rats", "hedgehogs"
    ]
    
    for animal in animals:
        questions.extend([
            f"What is a {animal}?",
            f"Where can you find {animal}?",
            f"Is {animal} native to New Zealand?",
            f"Is {animal} endangered?",
            f"What does a {animal} eat?",
            f"What is the habitat of a {animal}?",  
            f"What is the Maori name for {animal}?"
        ])
    
    # Wildlife - Plants
    plants = [
        "pohutukawa", "rata", "kowhai", "cabbage tree", "silver fern", "nikau palm",
        "kauri", "rimu", "totara", "beech", "manuka", "kanuka"
    ]
    
    for plant in plants:
        questions.extend([
            f"What is {plant}?",
            f"Where does {plant} grow?",
            f"Is {plant} native to New Zealand?",
            f"What does {plant} look like?",
            f"What is the significance of {plant} in Maori culture?",
            f"What is the habitat of {plant}?",
            f"What is the Maori name for {plant}?",
            f"What are the uses of {plant}?"
        ])
    
    # Sports - Rugby
    questions.extend([
        "What is the All Blacks?",
        "What is the haka performed by the All Blacks?",
        "When did New Zealand win the Rugby World Cup?",
        "How many times have the All Blacks won the Rugby World Cup?",
        "What is Super Rugby?",
        "What teams play in Super Rugby from New Zealand?",
        "What is the Bledisloe Cup?",
        "What is the Tri Nations?",
        "What is the Rugby Championship?",
        "What is the Ranfurly Shield?",
        "What is the NPC?",
        "What is the Mitre 10 Cup?",
        "Who is the most capped All Black?",
        "Who is the highest scoring All Black?",
        "What is sevens rugby?",
        "What is the All Blacks Sevens?",
        "When did New Zealand win Olympic gold in sevens?"
    ])
    
    # Sports - Cricket
    questions.extend([
        "What is the Black Caps?",
        "When did New Zealand reach the Cricket World Cup final?",
        "Who is the New Zealand cricket captain?",
        "What is the Plunket Shield?",
        "What is the Super Smash?",
        "What is the Black Ferns?",
        "What is the White Ferns?",
    ])
    
    # Sports - Other
    questions.extend([
        "What is the Tall Blacks?",
        "What is the Football Ferns?",
        "What is the All Whites?",
        "What is the Silver Ferns?",
        "What is netball in New Zealand?",
        "What is sailing in New Zealand?",
        "What is the America's Cup?",
        "When did New Zealand win the America's Cup?",
        "What is Team New Zealand?",
        "What is rowing in New Zealand?",
        "What is cycling in New Zealand?",
        "What is athletics in New Zealand?",
    ])
    
    # Government and Politics
    questions.extend([
        "What is the capital of New Zealand?",
        "What is the New Zealand Parliament?",
        "What is the Beehive?",
        "What is MMP?",
        "How does the New Zealand electoral system work?",
        "What is the New Zealand House of Representatives?",
        "What is the New Zealand Senate?",
        "What is the Governor-General of New Zealand?",
        "What is the Prime Minister of New Zealand?",
        "What is the New Zealand Cabinet?",
        "What political parties are in New Zealand?",
        "What is the Labour Party?",
        "What is the National Party?",
        "What is the Green Party?",
        "What is ACT New Zealand?",
        "What is New Zealand First?",
        "What is the Maori Party?",
        "What is Te Pati Maori?",
        "What is the New Zealand legal system?",
        "What is the Supreme Court of New Zealand?",
        "What is the High Court of New Zealand?",
        "What is the District Court of New Zealand?",
        "What is the role of the judiciary in New Zealand?",
        "What is the Treaty of Waitangi?",
        "What is Waitangi Day?",
        "What are the rights of Maori under the Treaty of Waitangi?"
    ])
    
    # Economy
    questions.extend([
        "What is the New Zealand dollar?",
        "What is the currency of New Zealand?",
        "What are the main exports of New Zealand?",
        "What is the dairy industry in New Zealand?",
        "What is Fonterra?",
        "What is the meat industry in New Zealand?",
        "What is the wool industry in New Zealand?",
        "What is the wine industry in New Zealand?",
        "What is the tourism industry in New Zealand?",
        "What is the film industry in New Zealand?",
        "What is Weta Workshop?",
        "What is Weta Digital?",
        "What is the technology industry in New Zealand?",
        "What is Xero?",
        "What is Trade Me?",
        "What is the fishing industry in New Zealand?",
        "What is the forestry industry in New Zealand?",
        "What is the mining industry in New Zealand?",
        "What is the agriculture industry in New Zealand?",
        "What is the service industry in New Zealand?"
    ])
    
    # Education
    questions.extend([
        "What is the University of Auckland?",
        "What is the University of Otago?",
        "What is Victoria University of Wellington?",
        "What is the University of Canterbury?",
        "What is Massey University?",
        "What is the University of Waikato?",
        "What is Lincoln University?",
        "What is AUT?",
        "What is the New Zealand education system?",
        "What is NCEA?",
        "What is the New Zealand Qualifications Authority?",
        "What is the Ministry of Education in New Zealand?",
        "What is the Tertiary Education Commission?",
        "What is the Education Review Office?",
        "What is the New Zealand Student Loan Scheme?",
        "What is the New Zealand Scholarship?",
        "What is the New Zealand Teaching Council?"
    ])
    
    # Landmarks and Tourist Attractions
    landmarks = [
        "Sky Tower", "Hobbiton", "Milford Sound", "Fiordland", "Tongariro National Park",
        "Abel Tasman National Park", "Aoraki Mount Cook National Park", "Westland Tai Poutini National Park",
        "Arthur's Pass", "Franz Josef Glacier", "Fox Glacier", "Rotorua", "Waitomo Caves",
        "Bay of Islands", "Coromandel Peninsula", "Cathedral Cove", "Hot Water Beach",
        "Waiheke Island", "Auckland Harbour Bridge", "Wellington Cable Car", "Te Papa",
        "Auckland Museum", "Canterbury Museum", "Otago Museum"
    ]
    
    for landmark in landmarks:
        questions.extend([
            f"What is {landmark}?",
            f"Where is {landmark}?",
            f"What is {landmark} known for?",
            f"How do you get to {landmark}?",
            f"What can you do at {landmark}?",
            f"What is the history of {landmark}?",
            f"What is the significance of {landmark}?",
            f"What is the best time to visit {landmark}?",
            f"What is the entrance fee for {landmark}?",
            f"What are the opening hours for {landmark}?"
        ])
    
    # Climate and Weather
    questions.extend([
        "What is the climate of New Zealand?",
        "What is the weather like in New Zealand?",
        "What is the average temperature in New Zealand?",
        "What is the wettest place in New Zealand?",
        "What is the driest place in New Zealand?",
        "What is the warmest place in New Zealand?",
        "What is the coldest place in New Zealand?",
        "Does it snow in New Zealand?",
        "What are the seasons in New Zealand?",
        "What is the weather like in summer in New Zealand?",
        "What is the weather like in winter in New Zealand?",
        "What is the best time to visit New Zealand?",
        "What natural disasters occur in New Zealand?",
        "What is an earthquake?",
        "What is a volcano?",
        "What is a tsunami?",
        "What is the risk of earthquakes in New Zealand?",
        "What is the risk of volcanoes in New Zealand?",
        "What is the risk of tsunamis in New Zealand?",
        "What is the MetService?"
    ])
    
    # Transportation
    questions.extend([
        "What is Air New Zealand?",
        "What airports are in New Zealand?",
        "What is the main airport in Auckland?",
        "What is the main airport in Wellington?",
        "What is the main airport in Christchurch?",
        "How do you travel between islands in New Zealand?",
        "What is the Interislander?",
        "What is Blue Bridge?",
        "What is the railway system in New Zealand?",
        "What is KiwiRail?",
        "What is the Northern Explorer?",
        "What is the Coastal Pacific?",
        "What is the TranzAlpine?",
        "What is public transportation like in New Zealand?",
        "What is the bus system in New Zealand?",
        "What is the train system in New Zealand?",
        "What is the ferry system in New Zealand?",
        "What is driving like in New Zealand?",
        "What are the road rules in New Zealand?",
        "What is the New Zealand Transport Agency?"
    ])
    
    # Add more questions to reach 2,500
    # Additional geography questions
    questions.extend([
        "What is the highest point in New Zealand?",
        "What is the longest river in New Zealand?",
        "What is the largest lake in New Zealand?",
        "What is the largest city in New Zealand?",
        "What is the smallest city in New Zealand?",
        "What is the northernmost point of New Zealand?",
        "What is the southernmost point of New Zealand?",
        "What is the easternmost point of New Zealand?",
        "What is the westernmost point of New Zealand?",
        "What is the distance between North and South Island?",
        "What is Cook Strait?",
        "What is Foveaux Strait?",
        "What is the Tasman Sea?",
        "What is the Pacific Ocean?"
    ])
    
    # Additional history questions
    questions.extend([
        "What was the Musket Wars?",
        "What was the Flagstaff War?",
        "What was the Taranaki War?",
        "What was the Waikato War?",
        "What was the New Zealand Company?",
        "What was the Wakefield scheme?",
        "What was the Vogel era?",
        "What was the Long Depression?",
        "What was the Great Depression in New Zealand?",
        "What was the First World War for New Zealand?",
        "What was the Second World War for New Zealand?",
        "What was Gallipoli for New Zealand?",
        "What was the Vietnam War for New Zealand?",
        "What was the ANZUS treaty?",
        "What was the anti-nuclear movement in New Zealand?"
    ])
    
    # Additional culture questions
    questions.extend([
        "What is a kiwi?",
        "What is a Kiwi?",
        "What does it mean to be a Kiwi?",
        "What is the New Zealand accent?",
        "What is the New Zealand flag?",
        "What is the New Zealand national anthem?",
        "What is God Defend New Zealand?",
        "What is God Save the Queen?",
        "What is the New Zealand coat of arms?",
        "What is the silver fern?",
        "What is the koru?",
        "What is the haka?",    
    ])
    
    # Remove duplicates and ensure we have exactly 2,500 unique questions
    unique_questions = list(set(questions))
    
    # If we have more than 2,500, randomly sample
    if len(unique_questions) > 2500:
        unique_questions = random.sample(unique_questions, 2500)
    # If we have less than 2,500, add more variations
    elif len(unique_questions) < 2500:
        # Add more variations and combinations
        additional = []
        
        # More specific questions about places
        for city in cities[:20]:  # Use first 20 cities
            additional.extend([
                f"What is the weather like in {city}?",
                f"What is the best time to visit {city}?",
                f"What is the main street in {city}?",
                f"What is the airport in {city}?",
                f"What is the university in {city}?",
            ])
        
        # More questions about culture
        additional.extend([
            "What is a Kiwi fruit?",
            "What is a Kiwi bird?",
            "What is the difference between a Kiwi and a New Zealander?",
            "What is the New Zealand time zone?",
            "What is NZST?",
            "What is NZDT?",
            "What is daylight saving in New Zealand?",
            "What is the New Zealand phone code?",
            "What is the New Zealand internet domain?",
            "What is .nz?",
        ])
        
        # More questions about food and drink
        additional.extend([
            "What is L&P?",
            "What is Whittaker's chocolate?",
            "What is Tip Top ice cream?",
            "What is Wattie's?",
            "What is Sanitarium?",
            "What is New Zealand honey?",
            "What is manuka honey?",
            "What is New Zealand cheese?",
            "What is New Zealand butter?",
        ])
        
        unique_questions.extend(additional)
        unique_questions = list(set(unique_questions))
    
    # Ensure exactly 2,500
    unique_questions = unique_questions[:2500]
    
    return unique_questions

def main():
    questions = generate_questions()
    
    # Write to JSONL file
    output_file = "related_guard_dataset.jsonl"
    with open(output_file, 'w', encoding='utf-8') as f:
        for question in questions:
            entry = {
                "input": question,
                "label": "related"
            }
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    print(f"Generated {len(questions)} unique questions about New Zealand")
    print(f"Written to {output_file}")

if __name__ == "__main__":
    main()

