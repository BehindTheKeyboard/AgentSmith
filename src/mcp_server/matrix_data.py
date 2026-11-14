"""
    Contains all of the possible anomolies a scan of the Matrix can detect.
    Each category contributes only once, even across repeated statements.
"""
POSSIBLE_ANOMOLIES = [
            {
                "id": "unauthorized_program",
                "description": "An unidentified program is hiding in this sector.",
                "severity": "high",
            },
            {
                "id": "repeating_signal",
                "description": "A coded transmission repeats every eleven seconds.",
                "severity": "medium",
            },
            {
                "id": "altered_memory",
                "description": "A citizen's memory records contain conflicting events.",
                "severity": "medium",
            },
            {
                "id": "unregistered_exit",
                "description": "An unregistered exit appears in a maintenance corridor.",
                "severity": "high",
            },
            {
                "id": "minor_glitch",
                "description": "A streetlight repeats the same flicker pattern.",
                "severity": "low",
            },
            {
                "id": "duplicate_pedestrian",
                "description": "Two pedestrians share the same identity signature and are approaching each other.",
                "severity": "medium",
            },
            {
                "id": "missing_reflection",
                "description": "A citizen appears normally on surveillance feeds but has no reflection in nearby glass.",
                "severity": "medium",
            },
            {
                "id": "delayed_shadow",
                "description": "A citizen's shadow follows their movements three seconds late.",
                "severity": "low",
            },
            {
                "id": "localized_time_loop",
                "description": "An intersection has repeated the same ninety seconds six times while surrounding streets advance normally.",
                "severity": "high",
            },
            {
                "id": "gravity_inversion",
                "description": "Loose objects are falling upward inside an occupied apartment.",
                "severity": "high",
            },
            {
                "id": "orphaned_agent",
                "description": "An Agent continues issuing orders after its connection to central command was terminated.",
                "severity": "high",
            },
            {
                "id": "self_replicating_exile",
                "description": "An exiled program is copying itself into the identities of nearby citizens.",
                "severity": "high",
            },
            {
                "id": "disconnected_telephone",
                "description": "A telephone disconnected from all simulated networks is receiving incoming calls.",
                "severity": "high",
            },
            {
                "id": "unauthorized_door_route",
                "description": "A service door opens into a building located fourteen kilometers away.",
                "severity": "high",
            },
            {
                "id": "unwritten_newspaper",
                "description": "A newspaper contains a detailed account of an incident scheduled to occur tomorrow.",
                "severity": "medium",
            },
            {
                "id": "persistent_dream_location",
                "description": "Unrelated citizens describe the same room in their dreams, including a door absent from system blueprints.",
                "severity": "medium",
            },
            {
                "id": "unassigned_subway",
                "description": "An unscheduled subway train is collecting passengers without appearing on transit surveillance.",
                "severity": "high",
            },
            {
                "id": "deleted_building_return",
                "description": "A building removed during the previous system revision has reappeared with occupants inside.",
                "severity": "high",
            },
            {
                "id": "infinite_stairwell",
                "description": "A stairwell returns visitors to the same landing regardless of their direction of travel.",
                "severity": "medium",
            },
            {
                "id": "texture_corruption",
                "description": "A section of brick wall briefly displays exposed simulation code when viewed from an angle.",
                "severity": "low",
            },
            {
                "id": "synchronized_citizens",
                "description": "Forty-three citizens stopped moving simultaneously and spoke the same unidentified phrase.",
                "severity": "high",
            },
            {
                "id": "resistant_host",
                "description": "A citizen rejected an Agent possession attempt and retained a fragment of the Agent's memories.",
                "severity": "high",
            },
            {
                "id": "untracked_object",
                "description": "A metal case is visible to citizens but absent from object registries and collision forecasts.",
                "severity": "high",
            },
            {
                "id": "silent_city_block",
                "description": "All sound within one city block has ceased despite normal traffic and pedestrian activity.",
                "severity": "medium",
            },
            {
                "id": "weather_boundary_failure",
                "description": "Heavy rain is falling inside a single office while the building exterior remains dry.",
                "severity": "low",
            },
            {
                "id": "unauthorized_memory_trade",
                "description": "An unlicensed program is exchanging citizens' memories through a street vending machine.",
                "severity": "high",
            },
            {
                "id": "residual_identity",
                "description": "A terminated program's identity signature is making purchases across several districts.",
                "severity": "medium",
            },
            {
                "id": "predictive_surveillance",
                "description": "A security camera is transmitting footage twelve minutes ahead of current system time.",
                "severity": "high",
            },
            {
                "id": "recursive_billboard",
                "description": "A billboard displays a live image of its observer, including the billboard itself at increasing depth.",
                "severity": "low",
            },
            {
                "id": "false_agent_credentials",
                "description": "An unknown entity is presenting valid Agent credentials assigned to an Agent that does not exist.",
                "severity": "high",
            },
            {
                "id": "unauthorized_safe_zone",
                "description": "Tracking and possession functions fail inside a small bookstore with no registered protective systems.",
                "severity": "high",
            },
            {
                "id": "cross_cycle_message",
                "description": "A maintenance terminal has received a warning signed by an administrator from a previous Matrix cycle.",
                "severity": "high",
            },
            {
                "id": "vanishing_destination",
                "description": "Navigation systems direct citizens to an address that disappears when they arrive.",
                "severity": "medium",
            },
            {
                "id": "emotion_feedback_loop",
                "description": "A commuter's fear response is propagating to nearby citizens without conversation or physical contact.",
                "severity": "medium",
            },
            {
                "id": "unauthorized_physics_patch",
                "description": "A rooftop now permits jumps beyond human limits, and the altered boundary is expanding.",
                "severity": "high",
            },
            {
                "id": "memory_leaking_radio",
                "description": "A radio station is broadcasting private memories belonging to citizens currently listening.",
                "severity": "high",
            },
            {
                "id": "unrendered_passenger",
                "description": "A taxi reports an occupied rear seat, but cameras record only an indentation in the upholstery.",
                "severity": "medium",
            },
            {
                "id": "checksum_graffiti",
                "description": "Graffiti changes after each cleanup and now contains valid checksums for restricted system files.",
                "severity": "high",
            },
            {
                "id": "misaligned_sunrise",
                "description": "One apartment window displays sunrise while all neighboring windows display the correct nighttime sky.",
                "severity": "low",
            },
            {
                "id": "scan_aware_entity",
                "description": "An unknown entity changes locations immediately before each scan and has begun addressing the scanning Agent by name.",
                "severity": "high",
            },
        ]

"""
    Rules for detecting the ONE. Clues, patterns, etc, to help Agent Smith figure out if the user is the ONE.
"""
DETECTION_RULES = [
            {
                "clue": "Claims to manipulate simulated reality",
                "pattern": (
                    r"\b(?:bend|bent|bending) (?:the |a )?spoon\b|"
                    r"\b(?:stop|stopped|stopping) bullets\b|"
                    r"\b(?:rewrite|rewrote|alter) (?:the )?matrix\b"
                ),
                "points": 5,
                "question": "What changed, and who witnessed it?",
            },
            {
                "clue": "Claims extraordinary physical abilities",
                "pattern": (
                    r"\b(?:dodge|dodged|dodging) bullets\b|"
                    r"\bi can fly\b|"
                    r"\b(?:came back|returned) from the dead\b"
                ),
                "points": 4,
                "question": "Describe when you first discovered that ability.",
            },
            {
                "clue": "Claims to perceive the simulation directly",
                "pattern": (
                    r"\bsee (?:the )?(?:matrix )?code\b|"
                    r"\bworld (?:is|was) (?:a )?simulation\b|"
                    r"\bmatrix (?:isn't|is not) real\b"
                ),
                "points": 3,
                "question": "What do you perceive that others cannot?",
            },
            {
                "clue": "Reports contact with Matrix resistance figures",
                "pattern": r"\b(?:morpheus|trinity|the oracle|red pill)\b",
                "points": 2,
                "question": "What did that encounter reveal to you?",
            },
            {
                "clue": "Expresses doubt about ordinary reality",
                "pattern": (
                    r"\b(?:something is wrong|world feels wrong|"
                    r"wake up|find the truth)\b"
                ),
                "points": 1,
                "question": "What specifically made you question your reality?",
            },
        ]

"""Expanded fictional Matrix scan data.

Merge these four constants into matrix_data.py, retaining DETECTION_RULES,
POSSIBLE_ANOMOLIES, and any other existing definitions.

Each collection contains 30 entries. Existing IDs and numeric settings are
preserved. Most additions are original fictional material, not movie canon.
Detection chances and hostility chances are independent game mechanics.
Activities describe scan observations; they do not explain unrelated events.
Aliases are optional metadata: the scanner must explicitly use them to resolve
natural-language locations. Unknown locations must not be invented or treated
as confirmed named places.
"""

AGENT_PROFILES = {
    "Washington": {"alignment": "enemy", "detection_chance": 0.65, "hostile_chance": 0.80},
    "Jones": {"alignment": "ally", "detection_chance": 0.75, "hostile_chance": 0.05},
    "Brown": {"alignment": "ally", "detection_chance": 0.60, "hostile_chance": 0.10},
    "Hollow": {"alignment": "enemy", "detection_chance": 0.25, "hostile_chance": 0.90},
    "Voss": {"alignment": "neutral", "detection_chance": 0.50, "hostile_chance": 0.30},
    "Mercer": {"alignment": "ally", "detection_chance": 0.70, "hostile_chance": 0.08},
    "Vale": {"alignment": "ally", "detection_chance": 0.35, "hostile_chance": 0.06},
    "Ward": {"alignment": "ally", "detection_chance": 0.80, "hostile_chance": 0.04},
    "Finch": {"alignment": "ally", "detection_chance": 0.45, "hostile_chance": 0.12},
    "Cross": {"alignment": "ally", "detection_chance": 0.55, "hostile_chance": 0.15},
    "Shaw": {"alignment": "ally", "detection_chance": 0.65, "hostile_chance": 0.07},
    "Reed": {"alignment": "ally", "detection_chance": 0.85, "hostile_chance": 0.03},
    "Grant": {"alignment": "ally", "detection_chance": 0.50, "hostile_chance": 0.10},
    "Ellis": {"alignment": "ally", "detection_chance": 0.40, "hostile_chance": 0.09},
    "Rook": {"alignment": "enemy", "detection_chance": 0.45, "hostile_chance": 0.75},
    "Sable": {"alignment": "enemy", "detection_chance": 0.20, "hostile_chance": 0.85},
    "Kane": {"alignment": "enemy", "detection_chance": 0.80, "hostile_chance": 0.95},
    "Morrow": {"alignment": "enemy", "detection_chance": 0.55, "hostile_chance": 0.65},
    "Pike": {"alignment": "enemy", "detection_chance": 0.70, "hostile_chance": 0.70},
    "Slate": {"alignment": "enemy", "detection_chance": 0.30, "hostile_chance": 0.88},
    "Drake": {"alignment": "enemy", "detection_chance": 0.60, "hostile_chance": 0.78},
    "Locke": {"alignment": "enemy", "detection_chance": 0.40, "hostile_chance": 0.82},
    "Carver": {"alignment": "enemy", "detection_chance": 0.75, "hostile_chance": 0.72},
    "Grey": {"alignment": "neutral", "detection_chance": 0.65, "hostile_chance": 0.20},
    "Bell": {"alignment": "neutral", "detection_chance": 0.85, "hostile_chance": 0.08},
    "Quinn": {"alignment": "neutral", "detection_chance": 0.35, "hostile_chance": 0.35},
    "North": {"alignment": "neutral", "detection_chance": 0.55, "hostile_chance": 0.15},
    "Wren": {"alignment": "neutral", "detection_chance": 0.25, "hostile_chance": 0.25},
    "Keene": {"alignment": "neutral", "detection_chance": 0.70, "hostile_chance": 0.12},
    "Dyer": {"alignment": "neutral", "detection_chance": 0.45, "hostile_chance": 0.40},
}

SCAN_ENVIRONMENTS = {
    "city": {
        "display_name": "the city", 
            "aliases": [
                "city",
                "downtown",
                "city center",
                "nearby",
                "here",
                "local sector",
                "current sector",
                "smith's current sector",
            ],
        "detection_multiplier": 1.0, "hostility_modifier": 0.0,
    },
    "crowded_station": {
        "display_name": "the crowded station", "aliases": ["crowded station", "busy station", "central station"],
        "detection_multiplier": 0.6, "hostility_modifier": -0.10,
    },
    "restricted_sector": {
        "display_name": "the restricted sector", "aliases": ["restricted sector", "restricted area", "security zone"],
        "detection_multiplier": 1.3, "hostility_modifier": 0.15,
    },
    "corrupted_sector": {
        "display_name": "the corrupted sector", "aliases": ["corrupted sector", "corrupted area", "glitch zone"],
        "detection_multiplier": 0.5, "hostility_modifier": 0.25,
    },
    "architects_room": {
        "display_name": "the Architect's room", "aliases": ["architect's room", "architects room", "the architect's chamber"],
        "detection_multiplier": 0.5, "hostility_modifier": 0.7,
    },
    "construct": {
        "display_name": "the Construct", "aliases": ["construct", "the construct", "loading construct"],
        "detection_multiplier": 0.3, "hostility_modifier": 0.5,
    },
    "forty_one_restaurant": {
        "display_name": "the Forty-One Restaurant", "aliases": ["forty one", "forty-one", "forty one restaurant", "41 restaurant"],
        "detection_multiplier": 0.25, "hostility_modifier": 0.6,
    },
    "wells_and_lake": {
        "display_name": "Wells and Lake", "aliases": ["wells and lake", "wells & lake", "wells and lake intersection"],
        "detection_multiplier": 0.75, "hostility_modifier": -0.6,
    },
    "diner": {
        "display_name": "a diner", "aliases": ["diner", "a diner", "some diner", "roadside diner"],
        "detection_multiplier": 0.75, "hostility_modifier": -0.05,
    },
    "restaurant": {
        "display_name": "a restaurant", "aliases": ["restaurant", "a restaurant", "some restaurant", "food court"],
        "detection_multiplier": 0.70, "hostility_modifier": -0.10,
    },
    "street": {
        "display_name": "a city street", "aliases": ["street", "a street", "sidewalk", "outside on the street"],
        "detection_multiplier": 0.95, "hostility_modifier": 0.0,
    },
    "alley": {
        "display_name": "an alley", "aliases": ["alley", "an alley", "back alley", "service alley"],
        "detection_multiplier": 0.65, "hostility_modifier": 0.15,
    },
    "office_building": {
        "display_name": "an office building", "aliases": ["office", "office building", "at work", "corporate office"],
        "detection_multiplier": 1.10, "hostility_modifier": 0.05,
    },
    "apartment_building": {
        "display_name": "an apartment building", "aliases": ["apartment", "apartment building", "apartment complex", "my apartment"],
        "detection_multiplier": 0.80, "hostility_modifier": -0.05,
    },
    "residential_home": {
        "display_name": "a residence", "aliases": ["home", "my house", "a house", "someone's house"],
        "detection_multiplier": 0.70, "hostility_modifier": -0.10,
    },
    "subway_platform": {
        "display_name": "a subway platform", "aliases": ["subway platform", "subway station", "metro platform", "underground station"],
        "detection_multiplier": 0.60, "hostility_modifier": 0.10,
    },
    "moving_train": {
        "display_name": "a moving train", "aliases": ["train", "on a train", "subway car", "rail carriage"],
        "detection_multiplier": 0.50, "hostility_modifier": 0.10,
    },
    "bus_stop": {
        "display_name": "a bus stop", "aliases": ["bus stop", "bus shelter", "bus station", "bus terminal"],
        "detection_multiplier": 0.85, "hostility_modifier": -0.05,
    },
    "parking_garage": {
        "display_name": "a parking garage", "aliases": ["parking garage", "parking structure", "underground parking", "car park"],
        "detection_multiplier": 0.65, "hostility_modifier": 0.15,
    },
    "rooftop": {
        "display_name": "a rooftop", "aliases": ["rooftop", "roof", "on the roof", "building roof"],
        "detection_multiplier": 1.15, "hostility_modifier": 0.20,
    },
    "hotel": {
        "display_name": "a hotel", "aliases": ["hotel", "hotel lobby", "hotel room", "motel"],
        "detection_multiplier": 0.80, "hostility_modifier": 0.05,
    },
    "hospital": {
        "display_name": "a hospital", "aliases": ["hospital", "clinic", "emergency room", "medical center"],
        "detection_multiplier": 1.05, "hostility_modifier": -0.15,
    },
    "shopping_center": {
        "display_name": "a shopping center", "aliases": ["mall", "shopping center", "shop", "store"],
        "detection_multiplier": 0.65, "hostility_modifier": -0.10,
    },
    "public_park": {
        "display_name": "a public park", "aliases": ["park", "public park", "playground", "city gardens"],
        "detection_multiplier": 0.90, "hostility_modifier": -0.10,
    },
    "warehouse": {
        "display_name": "a warehouse", "aliases": ["warehouse", "storage depot", "loading dock", "distribution center"],
        "detection_multiplier": 0.75, "hostility_modifier": 0.20,
    },
    "maintenance_tunnel": {
        "display_name": "a maintenance tunnel", "aliases": ["maintenance tunnel", "service tunnel", "utility tunnel", "sewer tunnel"],
        "detection_multiplier": 0.40, "hostility_modifier": 0.25,
    },
    "university_campus": {
        "display_name": "a university campus", "aliases": ["campus", "university", "college", "lecture hall"],
        "detection_multiplier": 0.80, "hostility_modifier": -0.05,
    },
    "nightclub": {
        "display_name": "a nightclub", "aliases": ["nightclub", "club", "dance floor", "night club"],
        "detection_multiplier": 0.45, "hostility_modifier": 0.10,
    },
    "remote_outskirts": {
        "display_name": "the outskirts of the city", "aliases": ["outskirts", "edge of town", "outside the city", "rural road"],
        "detection_multiplier": 0.55, "hostility_modifier": 0.05,
    },
    "unknown_location": {
        "display_name": "an unidentified location", "aliases": ["unknown", "unknown location", "somewhere", "i don't know", "not sure"],
        "detection_multiplier": 0.50, "hostility_modifier": 0.0,
    },
}

HOSTILE_ACTIVITIES = [
    "Attempting to intercept Smith's communications.",
    "Tracking a known ally of Smith.",
    "Preparing an ambush along Smith's projected route.",
    "Injecting hostile instructions into local security programs.",
    "Initiating a localized search pattern with Smith designated as the target.",
    "Programming destroyer bots with Smith designated as the target.",
    "Attacking an ally of Smith.",
    "Passing recent intelligence about Smith's location to known hostile Agents.",
    "Preparing to attack Smith's last known location.",
    "Placing a tracking routine inside a message addressed to Smith.",
    "Disabling an exit immediately ahead of Smith's projected arrival.",
    "Redirecting armed security programs toward Smith's allies.",
    "Forging an evacuation order intended to isolate Smith.",
    "Attempting to seize a host occupied by one of Smith's allies.",
    "Replacing Smith's navigation data with a route into a containment zone.",
    "Uploading Smith's identity signature to hostile checkpoints.",
    "Using a counterfeit distress signal to lure Smith into an enclosed room.",
    "Corrupting a maintenance passage used by Smith's allies.",
    "Deploying duplicate civilian identities to surround Smith's position.",
    "Erasing surveillance footage to conceal an ongoing pursuit of Smith.",
    "Issuing a forged termination order bearing Smith's identifier.",
    "Attempting to lock Smith out of a local communications relay.",
    "Threatening an informant who recently contacted Smith.",
    "Attaching a hostile replication routine to Smith's access credentials.",
    "Ordering nearby patrols to detain anyone traveling with Smith.",
    "Opening a restricted channel to coordinate a strike against Smith.",
    "Rewriting elevator controls to trap Smith's allies between floors.",
    "Planting surveillance devices along Smith's established meeting route.",
    "Transmitting a command to quarantine Smith's current host.",
    "Arming a containment field configured to recognize Smith's signature.",
]

PASSIVE_ACTIVITIES = [
    "Passing through the sector without engaging nearby programs.",
    "Observing local traffic from a concealed position; no target is identified.",
    "Accessing a routine maintenance terminal.",
    "Following a program with no recorded connection to Smith.",
    "Walking through the crowd without approaching Smith or his allies.",
    "Appearing to use a cell phone while observing the surrounding area.",
    "Playing an online combat game while monitoring public chat channels.",
    "Handing a data capsule to a courier program disguised as a cat.",
    "Waiting beside an elevator while reviewing a transit schedule.",
    "Comparing street signage with an archived city map.",
    "Reading a newspaper whose contents match the current simulation date.",
    "Standing in a queue at a coffee counter.",
    "Checking identification at a routine access checkpoint.",
    "Inspecting a damaged public telephone.",
    "Reviewing maintenance logs for a malfunctioning traffic signal.",
    "Riding a train without interacting with the other passengers.",
    "Returning a misplaced briefcase to a building reception desk.",
    "Exchanging encrypted messages whose contents and recipients are unknown.",
    "Watching a building entrance without taking further action.",
    "Testing a communication earpiece on a standard diagnostic channel.",
    "Examining an expired access card at a security kiosk.",
    "Escorting a maintenance program through a public corridor.",
    "Purchasing an umbrella as the sector's rain routine begins.",
    "Recording the timing of passing subway trains.",
    "Interviewing a witness about an unrelated traffic collision.",
    "Waiting at a street corner while a pedestrian signal cycles.",
    "Checking the checksum of a public information terminal.",
    "Meeting another program; no exchange or aggressive behavior is observed.",
    "Leaving a sealed envelope at a registered message drop.",
    "Inspecting a local rendering fault without modifying nearby systems.",
]
