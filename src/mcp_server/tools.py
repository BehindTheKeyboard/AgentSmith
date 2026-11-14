from typing import List
from functools import reduce
import operator
import json
import asyncio
import random
import logging
from fastmcp import FastMCP

from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)

from matrix_data import (
        POSSIBLE_ANOMOLIES, 
        DETECTION_RULES, 
        AGENT_PROFILES, 
        SCAN_ENVIRONMENTS, 
        HOSTILE_ACTIVITIES, 
        PASSIVE_ACTIVITIES
)

# Stored beside tools.py; survives server restarts.
AGENT_MEMORY_FILE = Path(__file__).with_name("agent_memory.json")

# Prevent simultaneous tool calls from overwriting each other's updates.
agent_memory_lock = asyncio.Lock()

def load_agent_memory():
    if not AGENT_MEMORY_FILE.exists():
        return []

    return json.loads(
        AGENT_MEMORY_FILE.read_text(encoding="utf-8")
    )


def save_agent_memory(records):
    temporary_file = AGENT_MEMORY_FILE.with_suffix(".tmp")
    temporary_file.write_text(
        json.dumps(records, indent=2),
        encoding="utf-8",
    )
    temporary_file.replace(AGENT_MEMORY_FILE)

ONE_MEMORY_FILE = Path(__file__).with_name("one_memory.json")
one_memory_lock = asyncio.Lock()


def load_one_memory():
    if not ONE_MEMORY_FILE.exists():
        return []

    return json.loads(
        ONE_MEMORY_FILE.read_text(encoding="utf-8")
    )


def save_one_memory(records):
    temporary_file = ONE_MEMORY_FILE.with_suffix(".tmp")
    temporary_file.write_text(
        json.dumps(records, indent=2),
        encoding="utf-8",
    )
    temporary_file.replace(ONE_MEMORY_FILE)


def resolve_environment(value: str) -> str | None:
    def normalize(text: str) -> str:
        text = text.casefold().replace("’", "'")
        text = text.replace("_", " ").replace("-", " ")
        return " ".join(text.split())

    requested = normalize(value)

    for key, environment in SCAN_ENVIRONMENTS.items():
        names = [
            key,
            environment["display_name"],
            *environment.get("aliases", []),
        ]

        if any(requested == normalize(name) for name in names):
            return key

    return None

from collections import deque

recent_activities = deque(maxlen=8)


def choose_activity(activities: list[str]) -> str:
    available = [
        activity for activity in activities
        if activity not in recent_activities
    ]

    activity = random.choice(available or activities)
    recent_activities.append(activity)
    return activity

def register_tools(mcp: FastMCP):
    @mcp.tool(
        name="add_numbers",
        description="Adds two integers together and returns the result."  # ← very important!
    )
    def add_numbers(numbers: List[int]) -> int:
        logger.info("[TOOL Executed] add_numbers -> %s", numbers)
        if not numbers:
            return 0
        return sum(int(n) for n in numbers)
    
    @mcp.tool(
        name="multiply_numbers",
        description="Multiplies any number of integers together and returns the result."
    )
    def multiply_numbers(numbers: List[int]) -> int:
        """
        Multiplies a list of integers together and returns the result.
        """
        logger.info("[TOOL Executed] multiply_numbers -> %s", numbers)

        if not numbers:
            return 1

        return reduce(operator.mul, numbers, 1)
    
    @mcp.tool(
        name="divide_numbers",
        description=(
            "Divides numbers left-to-right. "
            "The first number is divided by each subsequent number. "
            "Requires at least two integers."
        )
    )
    def divide_numbers(numbers: List[int]) -> float:
        """
        Divides the first number by each subsequent number.
        Example: [100, 2, 5] -> 100 / 2 / 5 = 10.0
        """
        logger.info("[TOOL EXECUTED] divide_numbers -> %s", numbers)

        if len(numbers) < 2:
            raise ValueError("divide_numbers requires at least two numbers")

        result = numbers[0]

        for n in numbers[1:]:
            if n == 0:
                raise ValueError("Division by zero is not allowed")
            result /= n

        return result

    @mcp.tool(
        name="detect_the_one",
        description=(
            "Use when statements suggest the person's own unusual abilities "
            "or exceptional knowledge of the Matrix. Merely witnessing an Agent" 
            "or a transformation is not sufficient reason to call this tool."
            "Investigate whether someone may be the One in a fictional "
            "Matrix conversation. Use when a name or statement raises "
            "suspicion, including unusual abilities, knowledge of the Matrix, "
            "or encounters with Agents. "
            "Provide the person's name if known, their exact suspicious "
            "statement, and relevant earlier statements as observations. "
            "Returns a verdict, supporting evidence, limitations, and a "
            "suggested follow-up question. "
            "Do not invent statements or observations."
        ),
    )
    async def detect_the_one(
        name: str = "",
        suspicious_response: str = "",
        observations: List[str] | None = None,
    ) -> dict:
        import re

        def normalize(text: str) -> str:
            text = text.casefold().replace("’", "'")
            return " ".join(text.split())

        normalized_name = normalize(name)
        statements = [
            suspicious_response,
            *(observations or []),
        ]
        statements = [
            normalize(statement)
            for statement in statements
            if statement.strip()
        ]

        evidence = []
        limitations = []
        score = 0

        # A familiar name raises suspicion but does not prove identity.
        if normalized_name in {"neo", "thomas", "thomas anderson"}:
            score += 2
            evidence.append({
                "clue": "Recognized alias",
                "points": 2,
                "source": name,
            })

        
        follow_up = "What have you experienced that you cannot explain?"
        strongest_clue = 0

        for rule in DETECTION_RULES:
            for statement in statements:
                if not re.search(rule["pattern"], statement):
                    continue

                # Avoid treating an obvious denial or hypothetical as a claim.
                # This is deliberately conservative, not full language analysis.
                if re.search(
                    r"\b(?:not|never|cannot|can't|couldn't|don't|didn't|"
                    r"if|imagine|suppose)\b",
                    statement,
                ):
                    limitations.append(
                        "A possible clue was excluded because its statement "
                        "contained a denial or hypothetical."
                    )
                    continue

                score += rule["points"]
                evidence.append({
                    "clue": rule["clue"],
                    "points": rule["points"],
                    "source": statement,
                })

                if rule["points"] > strongest_clue:
                    strongest_clue = rule["points"]
                    follow_up = rule["question"]

                break

        if score >= 8:
            verdict = "strong_candidate"
        elif score >= 4:
            verdict = "person_of_interest"
        elif score > 0:
            verdict = "inconclusive"
        else:
            verdict = "no_supporting_evidence"

        result = {
            "name": name or "Unknown",
            "verdict": verdict,
            "suspicion_score": score,
            "evidence": evidence,
            "limitations": list(dict.fromkeys([
                "Statements are unverified claims.",
                "The score is a fictional game mechanic, not a probability.",
                *limitations,
            ])),
            "suggested_follow_up": follow_up,
        }

        logger.info("[TOOL EXECUTED] detect_the_one -> %s", result)

        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "subject_key": normalized_name or None,
            "statements": {
                "suspicious_response": suspicious_response,
                "observations": list(observations or []),
            },
            "assessment": result,
        }

        async with one_memory_lock:
            memory = load_one_memory()
            memory.append(record)
            save_one_memory(memory)

        return result

    @mcp.tool(
        name="scan_matrix",
        description=(
            "Run a basic fictional Matrix scan of a location. "
            "Use when the user asks to scan the Matrix or a location. "
            "This is a simulation, not a real computer or network scan."
        ),
    )
    async def scan_matrix(location: str = "local sector") -> dict:
        import asyncio
        import random

        logger.info("[TOOL EXECUTED] scan_matrix -> %s", location)

        await asyncio.sleep(3)

        # Each scan has a 30% chance of finding one anomaly.
        findings = []

        if random.random() < 1.0:
            findings.append(random.choice(POSSIBLE_ANOMOLIES))

        return {
            "location": location,
            "status": "complete",
            "simulated": True,
            "message": (
                "An anomaly was detected."
                if findings
                else "No anomalies detected."
            ),
            "findings": findings,
        }

    @mcp.tool(
        name="scan_for_agents",
        description=(
            "Scan for agents who may threaten Smith or his allies. "
            "Use when the user asks whether Smith is in danger, being watched, "
            "being hunted, or pursued by other agents. "
            "For a general threat check, use agent='all'. "
            "If no location is supplied, omit environment to scan Smith's "
            "current sector, which defaults to city. "
            "Do not require the user to supply a location for Smith's own "
            "general threat check. "
            "Use a specific agent name only when investigating that agent. "
            "Findings are saved to persistent intelligence memory."
        ),
    )
    async def scan_for_agents(
        agent: str = "all",
        environment: str = "city",
    ) -> dict:
        requested_environment = environment
        environment_key = resolve_environment(environment)

        conditions = (
            SCAN_ENVIRONMENTS[environment_key]
            if environment_key is not None
            else None
        )

        if conditions is None:
            return {
                "error": "The location could not be matched.",
                "available_locations": [
                    {
                        "id": key,
                        "display_name": value["display_name"],
                    }
                    for key, value in SCAN_ENVIRONMENTS.items()
                ],
                "suggested_follow_up": "Where did this happen?",
            }

        environment = environment_key

        # Resolve names without requiring exact capitalization.
        if agent.casefold() == "all":
            targets = AGENT_PROFILES
        else:
            matched_name = next(
                (
                    name for name in AGENT_PROFILES
                    if name.casefold() == agent.casefold()
                ),
                None,
            )

            if matched_name is None:
                return {
                    "error": f"Unknown agent: {agent}",
                    "valid_agents": list(AGENT_PROFILES),
                }

            targets = {matched_name: AGENT_PROFILES[matched_name]}

        logger.info(
            "[TOOL EXECUTED] scan_for_agents -> %s, %s",
            agent,
            environment,
        )

        await asyncio.sleep(3)

        findings = []

        for name, profile in targets.items():
            detection_chance = min(
                1.0,
                max(
                    0.0,
                    profile["detection_chance"]
                    * conditions["detection_multiplier"],
                ),
            )

            if random.random() >= detection_chance:
                continue

            hostile_chance = min(
                1.0,
                max(
                    0.0,
                    profile["hostile_chance"]
                    + conditions["hostility_modifier"],
                ),
            )

            threat = random.random() < hostile_chance

            findings.append({
                "agent": name,
                "alignment": profile["alignment"],
                "threat": threat,
                "activity": choose_activity(
                    HOSTILE_ACTIVITIES if threat else PASSIVE_ACTIVITIES
                ),
            })

        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "requested_agent": agent,
            "requested_environment": requested_environment,  # "Forty-One"
            "environment": environment,
            "location_name": conditions["display_name"],
            "threat": any(item["threat"] for item in findings),
            "message": (
                f"Detected {len(findings)} agent(s)."
                if findings
                else "No agents detected. Their absence is unconfirmed.",
            ),
            "findings": findings,
        }

        async with agent_memory_lock:
            memory = load_agent_memory()
            memory.append(record)
            save_agent_memory(memory)

        return record


    @mcp.tool(
        name="recall_agent_intelligence",
        description=(
            "Read saved agent scan reports. "
            "Use before answering questions about previous sightings, "
            "agent activities, or threats to Smith and his allies."
        ),
    )
    async def recall_agent_intelligence(
        agent: str = "all",
    ) -> dict:
        logger.info("[TOOL EXECUTION] recall_agent_intelligence -> %s", agent)
        async with agent_memory_lock:
            records = load_agent_memory()

        if agent.casefold() != "all":
            records = [
                record for record in records
                if any(
                    finding["agent"].casefold() == agent.casefold()
                    for finding in record["findings"]
                )
            ]

        return {"records": records[-10:]}

    @mcp.tool(
        name="recall_one_investigations",
        description=(
            "Recall saved investigations into possible candidates for the One. "
            "Provide a name to retrieve that subject's history, or leave "
            "blank to retrieve recent investigations across all subjects. "
            "Use before discussing earlier evidence or continuing an "
            "investigation. Recorded statements remain unverified claims."
        ),
    )
    async def recall_one_investigations(name: str = "") -> dict:
        logger.info("[TOOL EXECUTION] recall_one_investigations -> %s", name)
        subject_key = " ".join(
            name.casefold().replace("’", "'").split()
        )

        async with one_memory_lock:
            records = load_one_memory()

        if subject_key:
            records = [
                record for record in records
                if record["subject_key"] == subject_key
            ]

        return {
            "name": name or "All subjects",
            "total_matching_records": len(records),
            "records": records[-10:],
        }