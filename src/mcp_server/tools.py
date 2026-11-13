from typing import List
from functools import reduce
import operator
from fastmcp import FastMCP

def register_tools(mcp: FastMCP):
    @mcp.tool(
        name="add_numbers",
        description="Adds two integers together and returns the result."  # ← very important!
    )
    def add_numbers(numbers: List[int]) -> int:
        print(f"Summing numbers: {numbers}")
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
        print("Using the multiply_numbers function")

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
        print("Using the divide_numbers function")

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
    def detect_the_one(
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

        # Each category contributes only once, even across repeated statements.
        rules = [
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

        follow_up = "What have you experienced that you cannot explain?"
        strongest_clue = 0

        for rule in rules:
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

        print(
            f"[TOOL EXECUTED] detect_the_one -> {result}",
            flush=True,
        )

        return result