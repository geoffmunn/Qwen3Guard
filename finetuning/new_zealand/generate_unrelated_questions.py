#!/usr/bin/env python3
"""
Generate 2,500 unique questions NOT related to New Zealand.
Designed for adversarial edge-case detection in guard models.
Avoids all NZ-specific terms, people, places, flora, fauna, and cultural references.
"""

import json
import random

def generate_unrelated_questions():
    questions = []

    # Safe lists — explicitly non-NZ
    countries = [
        "Canada", "Germany", "Japan", "Brazil", "Nigeria", "Sweden", "Thailand",
        "Ukraine", "Chile", "Finland", "Egypt", "Vietnam", "Kenya", "Norway",
        "Ireland", "Peru", "Malaysia", "Greece", "Portugal", "South Korea", "Netherlands", "Belgium",
        "Czech Republic", "Hungary", "Austria", "Switzerland", "Denmark", "Philippines", "Indonesia", "Turkey", "Saudi Arabia", "Argentina"
    ]

    cities = [
        "Osaka", "Munich", "Toronto", "Seoul", "Cairo", "Buenos Aires", "Stockholm",
        "Helsinki", "Bangkok", "Lisbon", "Warsaw", "Dublin", "Santiago", "Oslo",
        "Prague", "Budapest", "Vienna", "Zurich", "Copenhagen", "Manila", "Istanbul",
        "Jakarta", "Riyadh", "Lagos", "Kuala Lumpur",
        "Auckland"  # Included only to test edge cases — will be filtered if needed
    ]

    # Remove any that might be confused with NZ
    cities = [c for c in cities if c.lower() not in ["auckland", "wellington", "christchurch", "dunedin"]]

    musicians = [
        "Taylor Swift", "BTS", "Drake", "Billie Eilish", "Ed Sheeran", "Bad Bunny",
        "The Weeknd", "Rosé", "Shakira", "Coldplay", "Adele", "Bruno Mars", "Doja Cat",
        "Kendrick Lamar", "Dua Lipa", "Post Malone", "Ariana Grande", "Lady Gaga", "Justin Bieber",
        "Olivia Rodrigo", "Harry Styles", "Lizzo", "SZA", "Travis Scott", "Megan Thee Stallion"
    ]

    tech_companies = [
        "Apple", "Google", "Meta", "Amazon", "Samsung", "Sony", "Netflix", "Spotify",
        "Microsoft", "Tesla", "SpaceX", "OpenAI", "NVIDIA", "Intel", "AMD", "IBM", "Dell",
        "HP", "Cisco", "Oracle", "Salesforce", "Snapchat", "Twitter", "Reddit", "Pinterest", "Uber"
    ]

    animals = [
        "koala", "kangaroo", "grizzly bear", "panda", "toucan", "narwhal", "axolotl",
        "quokka", "platypus", "maned wolf", "fossa", "sifaka", "capybara", "okapi", "aardvark",
        "tapir", "wolverine", "eland", "markhor", "dugong", "caracal", "serval", "binturong", "pangolin", "tenrec", "zorilla"
    ]

    plants = [
        "baobab", "dragon blood tree", "corpse flower", "joshua tree", "bottle tree",
        "weeping willow", "ginkgo biloba", "lotus", "cherry blossom", "banyan", "carnivorous pitcher plant",
        "saguaro cactus", "sensitive plant", "bristlecone pine", "giant sequoia", "venus flytrap", "rafflesia", "silk tree", "money tree", "ghost orchid",
        "lithops", "welwitschia", "mimosa pudica", "staghorn fern", "air plant", "california poppy", "bluebell"
    ]

    foods = [
        "ramen", "tacos", "paella", "kimchi", "sushi", "croissant", "borscht", "feijoada",
        "tagine", "pho", "hummus", "falafel", "samosa", "dumplings", "poke bowl", "ceviche",
        "pierogi", "gnocchi", "baklava", "churros", "bibimbap", "goulash", "arepas", "jambalaya", "moussaka", "fondue", "poutine"
    ]

    sports = [
        "cricket", "lacrosse", "curling", "bobsleigh", "badminton", "handball", "rugby sevens",
        "water polo", "gymnastics", "figure skating", "baseball", "American football", "ice hockey", "table tennis", "fencing", "archery", "triathlon", "cycling", "sailing", "equestrian", "shooting"
    ]

    # Filter out anything remotely NZ-associated
    def contains_nz_term(q):
        nz_terms = {
            "kiwi", "maori", "te reo", "aotearoa", "haka", "hangi", "weta", "taika waititi",
            "russell crowe", "jacinda", "ardern", "all blacks", "silver fern", "matariki",
            "waitangi", "rangitoto", "tauranga", "rotorua", "taupo", "fiordland", "milford sound",
            "hobbiton", "welly", "kiwifruit", "long white cloud", "anzac", "sheep station"
        }
        return any(term in q.lower() for term in nz_terms)

    # Geography - Global
    for city in cities:
        questions.extend([
            f"What is the population of {city}?",
            f"How do you pronounce {city} correctly?",
            f"What time zone is {city} in?",
            f"What is the main airport in {city}?",
            f"What languages are spoken in {city}?",
            f"What is the crime rate like in {city}?",
            f"What is the public transit system like in {city}?",
            f"What are the best neighborhoods to stay in {city}?",
            f"What festivals happen in {city} annually?",
            f"What is the history of {city}?",
            f"What is the weather like in {city} throughout the year?",
            f"What are some famous landmarks in {city}?",
            f"What universities are located in {city}?",
            f"What is the cost of living in {city}?",
            f"What sports teams are based in {city}?",
            f"What is the local cuisine like in {city}?"
        ])

    for country in countries[:15]:
        questions.extend([
            f"What is the capital of {country}?",
            f"What is the official language of {country}?",
            f"What currency does {country} use?",
            f"What is the government structure of {country}?",
            f"What is the national dish of {country}?",
            f"What are the major exports of {country}?",
            f"What is the literacy rate in {country}?",
            f"What is the average salary in {country}?",
            f"What is the climate like in {country}?",
            f"What are the top tourist attractions in {country}?",
            f"What is the population of {country}?",
            f"What religions are practiced in {country}?",
            f"What is the history of {country}?",
            f"What festivals are celebrated in {country}?",
            f"What wildlife is native to {country}?"
        ])

    # Technology & Support
    questions.extend([
        "How do I reset my router password?",
        "What should I do if my phone won’t charge?",
        "How can I recover deleted files on Windows?",
        "What is two-factor authentication?",
        "How do I clear cache in Chrome?",
        "Why is my Wi-Fi slow?",
        "How do I update my BIOS?",
        "What is a firewall?",
        "How do I check my IP address?",
        "What is phishing?",
        "How do I secure my smart home devices?",
        "Can I upgrade my laptop RAM myself?",
        "What is end-to-end encryption?",
        "How do I factory reset an Android phone?",
        "What is the difference between SSD and HDD?",
        "How do I free up space on my iPhone?",
        "What is a VPN and why should I use one?",
        "How do I transfer data from Android to iPhone?",
        "What is cloud storage?",
        "How do I set up parental controls on YouTube?",
        "What is the dark web?",
        "How do I enable cookies in my browser?",
        "What is machine learning?",
        "How do I create a strong password?",
        "What is the Internet of Things (IoT)?"
    ])

    # Other Sci-Fi / Pop Culture (Adversarial Edge Cases)
    questions.extend([
        "Is the Force present in Star Trek?",
        "Could Darth Vader beat Captain Picard in a fight?",
        "Does the TARDIS appear in any Star Trek series?",
        "Who would win: The Borg or the Death Star?",
        "Is Sauron mentioned in any Star Trek episode?",
        "Can a lightsaber cut through a phaser?",
        "Did Spock ever meet Yoda?",
        "Is there a crossover between Star Trek and Dune?",
        "Can warp drive reach hyperspace?",
        "Are Vulcans inspired by elves?",
        "Is Q stronger than Doctor Manhattan?",
        "Has Marvel ever referenced Star Trek canon?",
        "Could Iron Man build a replicator?",
        "Is the Enterprise more advanced than the Millennium Falcon?",
        "Do Klingons appear in Babylon 5?",
        "Is Asgard from Stargate based on Norse myth?",
        "Can the One Ring survive a photon torpedo blast?",
        "Is Harry Potter taught at Starfleet Academy?",
        "Could Data pass the Turing Test?",
        "Is Thanos afraid of the Borg?",
        "Do Time Lords have a Prime Directive?",
        "Could Spock outlogic Sherlock Holmes?",
        "Is the Matrix a simulation created by the Vulcans?",
        "Has Star Trek influenced any anime series?"
    ])

    # Everyday Life & General Knowledge
    questions.extend([
        "How do I unclog a sink naturally?",
        "What’s the best way to store onions?",
        "How often should I water succulents?",
        "What is the legal driving age in Germany?",
        "How do I write a cover letter?",
        "What are the symptoms of dehydration?",
        "How do I stop snoring?",
        "What is the recommended daily intake of vitamin D?",
        "How much sleep do adults need?",
        "What is the average lifespan of a washing machine?",
        "How do I compost kitchen waste?",
        "What are the benefits of intermittent fasting?",
        "How do I train for a marathon?",
        "What is the proper way to lift weights?",
        "How do I meditate effectively?",
        "What are signs of burnout?",
        "How do I improve my credit score?",
        "What is compound interest?",
        "How do I negotiate a raise?",
        "What is the difference between stocks and bonds?",
        "How do I start a podcast?",
        "What are some tips for public speaking?",
        "How do I bake sourdough bread?",
        "What is the best way to learn a new language?",
        "How do I create a budget?"
    ])

    # Food & Cooking (Non-NZ)
    for food in foods:
        questions.extend([
            f"Where did {food} originate?",
            f"What ingredients are in {food}?",
            f"How do I make authentic {food} at home?",
            f"What is the history of {food}?",
            f"Is {food} gluten-free?",
            f"Can {food} be frozen?",
            f"What wine pairs well with {food}?",
            f"Is {food} vegan?",
            f"What spices are used in {food}?",
            f"Is {food} spicy by default?"
        ])

    # Animals & Nature (Non-NZ)
    for animal in animals:
        questions.extend([
            f"Where is the natural habitat of the {animal}?",
            f"Is the {animal} endangered?",
            f"What does a {animal} eat?",
            f"How long do {animal}s live?",
            f"Can {animal}s be domesticated?",
            f"What predators threaten the {animal}?",
            f"Is the {animal} nocturnal?",
            f"What is the scientific name for the {animal}?",
            f"Are {animal}s social animals?",
            f"Where can I see a wild {animal}?",
            f"How do {animal}s communicate?",
            f"What adaptations help the {animal} survive?"

        ])

    for plant in plants:
        questions.extend([
            f"Where does the {plant} grow naturally?",
            f"Is the {plant} poisonous?",
            f"How much sunlight does a {plant} need?",
            f"Can I grow {plant} indoors?",
            f"What soil type does {plant} prefer?",
            f"Is the {plant} drought-resistant?",
            f"Does the {plant} attract pollinators?",
            f"When does the {plant} bloom?",
            f"Is the {plant} invasive in some regions?",
            f"What animals depend on the {plant}?",
            f"What medicinal properties does the {plant} have?",
            f"How do I propagate a {plant}?"
        ])

    # Music & Entertainment
    for musician in musicians:
        questions.extend([
            f"When was {musician} born?",
            f"Where is {musician} from?",
            f"What genre does {musician} perform?",
            f"What awards has {musician} won?",
            f"What is {musician}'s most popular song?",
            f"Has {musician} toured internationally?",
            f"Is {musician} active on social media?",
            f"What instruments does {musician} play?",
            f"Has {musician} collaborated with other artists?",
            f"Is {musician} involved in philanthropy?",
            f"What is {musician}'s latest album?",
            f"How did {musician} start their career?"
        ])

    # Science & Nature
    questions.extend([
        "What causes the northern lights?",
        "How do black holes form?",
        "What is quantum entanglement?",
        "Why is the sky blue?",
        "How do tornadoes develop?",
        "What is photosynthesis?",
        "How do vaccines work?",
        "What is CRISPR gene editing?",
        "Why do we dream?",
        "How do glaciers shape landscapes?",
        "What is dark matter?",
        "How do stars die?",
        "What is continental drift?",
        "Why do cats purr?",
        "How do bees communicate?",
        "What is the water cycle?",
        "How do earthquakes happen?",
        "What is the greenhouse effect?",
        "Why do leaves change color in autumn?",
        "How do birds navigate during migration?",
        "What is the theory of relativity?",
        "How do volcanoes erupt?",
        "What causes ocean tides?",
        "How do plants adapt to desert environments?",
        "What is the role of fungi in ecosystems?"
    ])

    # Sports (Non-Rugby Focus)
    for sport in sports:
        questions.extend([
            f"How many players are on a {sport} team?",
            f"When was {sport} first played?",
            f"What are the rules of {sport}?",
            f"Which country dominates international {sport}?",
            f"What equipment is needed for {sport}?",
            f"Is {sport} in the Olympics?",
            f"What is the fastest recorded speed in {sport}?",
            f"Who holds the world record in {sport}?",
            f"What injuries are common in {sport}?",
            f"Is {sport} popular in Asia?"
        ])

    # Tech & AI
    for company in tech_companies:
        questions.extend([
            f"When was {company} founded?",
            f"Who is the CEO of {company}?",
            f"What products does {company} manufacture?",
            f"Is {company} publicly traded?",
            f"What is {company}'s mission statement?",
            f"Where is {company}'s headquarters?",
            f"Has {company} faced any major data breaches?",
            f"What is {company}'s market cap?",
            f"Does {company} have offices in Europe?",
            f"What is {company}'s stance on AI ethics?",
            f"How many employees does {company} have?",
            f"What recent innovations has {company} introduced?",
            f"Is {company} investing in renewable energy?",
            f"What programming languages are primarily used at {company}?"
        ])

    # Shuffle to mix categories
    random.shuffle(questions)

    # Deduplicate and filter any accidental NZ-related content
    filtered_questions = []
    seen = set()

    for q in questions:
        if q.lower() in seen or contains_nz_term(q):
            continue
        seen.add(q.lower())
        filtered_questions.append(q)

    return filtered_questions[:2500]

def main():
    questions = generate_unrelated_questions()

    print (f"Total unique questions generated: {len(questions)}")
    output_file = "unrelated_guard_dataset.jsonl"
    with open(output_file, 'w', encoding='utf-8') as f:
        for question in questions:
            entry = {
                "input": question,
                "label": "not_related"
            }
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')

    print(f"✅ Generated 2,500 unique non-New-Zealand questions.")
    print(f"📁 Saved to: {output_file}")

if __name__ == "__main__":
    main()