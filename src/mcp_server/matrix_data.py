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

AGENT_PROFILES = {
    "Washington": {
        "alignment": "enemy",
        "detection_chance": 0.65,
        "hostile_chance": 0.80,
    },
    "Jones": {
        "alignment": "ally",
        "detection_chance": 0.75,
        "hostile_chance": 0.05,
    },
    "Brown": {
        "alignment": "ally",
        "detection_chance": 0.60,
        "hostile_chance": 0.10,
    },
    "Hollow": {
        "alignment": "enemy",
        "detection_chance": 0.25,
        "hostile_chance": 0.90,
    },
    "Voss": {
        "alignment": "neutral",
        "detection_chance": 0.50,
        "hostile_chance": 0.30,
    },
}

SCAN_ENVIRONMENTS = {
    "city": {
        "detection_multiplier": 1.0,
        "hostility_modifier": 0.0,
    },
    "crowded_station": {
        "detection_multiplier": 0.6,
        "hostility_modifier": -0.10,
    },
    "restricted_sector": {
        "detection_multiplier": 1.3,
        "hostility_modifier": 0.15,
    },
    "corrupted_sector": {
        "detection_multiplier": 0.5,
        "hostility_modifier": 0.25,
    },
    "architects_room": {
        "detection_multiplier": 0.5,
        "hostility_modifier": 0.7,
    },
    "construct": {
        "detection_multiplier": 0.3,
        "hostility_modifier": 0.5,
    },
    "forty_one_restaurant": {
        "detection_multiplier": 0.25,
        "hostility_modifier": 0.6,
    },
    "wells_and_lake": {
        "detection_multiplier": 0.75,
        "hostility_modifier": -0.6,
    },
}

HOSTILE_ACTIVITIES = [
    "Attempting to intercept Smith's communications.",
    "Tracking a known ally of Smith.",
    "Preparing an ambush along Smith's projected route.",
    "Injecting hostile instructions into local security programs.",
    "Initiating a localized search pattern, target: Smith.",
    "Programming destroyer bots, target: Smith.",
    "Attacking an ally of Smith.",
    "Coordinating with other known hostile Agents, passing recent intel on Smiths location.",
    "Preparing to attack Smiths last known location."
]

PASSIVE_ACTIVITIES = [
    "Passing through the sector without engaging.",
    "Observing local traffic from a concealed position.",
    "Accessing a maintenance terminal.",
    "Following an unrelated program.",
    "Walking through the crowd.",
    "Pretending to use their cell phone while observing conditions generally.",
    "Pretending to play Call of Duty while gathering online intelligence.",
    "Passing information off to an informant cat currier."
]