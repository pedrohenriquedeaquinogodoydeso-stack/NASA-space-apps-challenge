##################################
# astronauts.py
#
# Roster of real astronauts and cosmonauts (NASA and its partner agencies).
# Each game draws its crew from this list, without repeating a name.
#
# Notes:
# - Only names, agencies and countries are stored. The game never attributes
#   quotes, actions or fates to these people.
# - People who died in flight accidents are intentionally NOT listed, since
#   crews can be lost in the game.
# - Extend the list freely: add a (name, agency, country) tuple to ROSTER.
##################################

AGENCIES = {
    "NASA": "NASA (United States)",
    "ESA": "European Space Agency",
    "JAXA": "Japan Aerospace Exploration Agency",
    "CSA": "Canadian Space Agency",
    "Roscosmos": "Roscosmos (Russia)",
    "MBRSC": "Mohammed Bin Rashid Space Centre (UAE)",
}

ROSTER = [
    # --- NASA
    ("Peggy Whitson", "NASA", "United States"),
    ("Scott Kelly", "NASA", "United States"),
    ("Christina Koch", "NASA", "United States"),
    ("Jessica Meir", "NASA", "United States"),
    ("Kate Rubins", "NASA", "United States"),
    ("Sunita Williams", "NASA", "United States"),
    ("Butch Wilmore", "NASA", "United States"),
    ("Mike Massimino", "NASA", "United States"),
    ("Ellen Ochoa", "NASA", "United States"),
    ("Eileen Collins", "NASA", "United States"),
    ("Buzz Aldrin", "NASA", "United States"),
    ("Mae Jemison", "NASA", "United States"),
    ("Story Musgrave", "NASA", "United States"),
    ("Franklin Chang-Díaz", "NASA", "United States"),
    ("Cady Coleman", "NASA", "United States"),
    ("Karen Nyberg", "NASA", "United States"),
    ("Tracy Caldwell Dyson", "NASA", "United States"),
    ("Anne McClain", "NASA", "United States"),
    ("Nicole Mann", "NASA", "United States"),
    ("Jasmin Moghbeli", "NASA", "United States"),
    ("Frank Rubio", "NASA", "United States"),
    ("Victor Glover", "NASA", "United States"),
    ("Reid Wiseman", "NASA", "United States"),
    ("Randy Bresnik", "NASA", "United States"),
    ("Shannon Walker", "NASA", "United States"),
    ("Stephanie Wilson", "NASA", "United States"),
    ("Joan Higginbotham", "NASA", "United States"),
    ("Leland Melvin", "NASA", "United States"),
    ("Ron Garan", "NASA", "United States"),
    ("Don Pettit", "NASA", "United States"),
    ("Mike Fincke", "NASA", "United States"),
    ("Mark Vande Hei", "NASA", "United States"),
    ("Raja Chari", "NASA", "United States"),
    ("Kayla Barron", "NASA", "United States"),
    ("Zena Cardman", "NASA", "United States"),
    ("Jonny Kim", "NASA", "United States"),
    ("Jeanette Epps", "NASA", "United States"),
    ("Serena Auñón-Chancellor", "NASA", "United States"),
    ("Nick Hague", "NASA", "United States"),
    ("Andrew Morgan", "NASA", "United States"),
    ("Drew Feustel", "NASA", "United States"),
    ("Kjell Lindgren", "NASA", "United States"),
    ("Megan McArthur", "NASA", "United States"),
    ("Jessica Watkins", "NASA", "United States"),
    ("Bob Behnken", "NASA", "United States"),
    ("Doug Hurley", "NASA", "United States"),
    ("Shane Kimbrough", "NASA", "United States"),
    ("Mike Hopkins", "NASA", "United States"),
    ("Rick Mastracchio", "NASA", "United States"),
    ("Terry Virts", "NASA", "United States"),
    # --- ESA
    ("Samantha Cristoforetti", "ESA", "Italy"),
    ("Thomas Pesquet", "ESA", "France"),
    ("Alexander Gerst", "ESA", "Germany"),
    ("Luca Parmitano", "ESA", "Italy"),
    ("Andreas Mogensen", "ESA", "Denmark"),
    ("Matthias Maurer", "ESA", "Germany"),
    ("Paolo Nespoli", "ESA", "Italy"),
    ("Tim Peake", "ESA", "United Kingdom"),
    ("Pedro Duque", "ESA", "Spain"),
    ("Claudie Haigneré", "ESA", "France"),
    ("Frank De Winne", "ESA", "Belgium"),
    ("André Kuipers", "ESA", "Netherlands"),
    ("Christer Fuglesang", "ESA", "Sweden"),
    ("Marcus Wandt", "ESA", "Sweden"),
    ("Sophie Adenot", "ESA", "France"),
    ("Raphaël Liégeois", "ESA", "Belgium"),
    # --- JAXA
    ("Koichi Wakata", "JAXA", "Japan"),
    ("Soichi Noguchi", "JAXA", "Japan"),
    ("Akihiko Hoshide", "JAXA", "Japan"),
    ("Satoshi Furukawa", "JAXA", "Japan"),
    ("Takuya Onishi", "JAXA", "Japan"),
    ("Kimiya Yui", "JAXA", "Japan"),
    ("Naoko Yamazaki", "JAXA", "Japan"),
    ("Chiaki Mukai", "JAXA", "Japan"),
    ("Norishige Kanai", "JAXA", "Japan"),
    ("Takao Doi", "JAXA", "Japan"),
    # --- CSA
    ("Chris Hadfield", "CSA", "Canada"),
    ("Jeremy Hansen", "CSA", "Canada"),
    ("Joshua Kutryk", "CSA", "Canada"),
    ("Roberta Bondar", "CSA", "Canada"),
    ("Dave Williams", "CSA", "Canada"),
    ("Robert Thirsk", "CSA", "Canada"),
    ("David Saint-Jacques", "CSA", "Canada"),
    ("Jenni Sidey-Gibbons", "CSA", "Canada"),

    # --- MBRSC (UAE)
    ("Sultan AlNeyadi", "MBRSC", "United Arab Emirates"),
    ("Hazzaa AlMansoori", "MBRSC", "United Arab Emirates"),
]


def pick_crew(rng, size):
    """Draw `size` distinct astronauts at random. `rng` is a random.Random instance.

    If the crew is larger than the roster (not expected), names are reused
    after the roster is exhausted so the game never crashes.
    """
    size = max(0, int(size))
    chosen = rng.sample(ROSTER, min(size, len(ROSTER)))
    while len(chosen) < size:
        chosen.append(rng.choice(ROSTER))
    return [
        {"name": name, "agency": agency, "agency_name": AGENCIES[agency], "country": country}
        for name, agency, country in chosen
    ]