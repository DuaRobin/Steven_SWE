# ---- Tool 1, look up a policy status ----------------------------------

_POLICIES = {
    "A1B2C3D4": {
        "holder": "Jordan Reyes",
        "type": "Homeowners",
        "status": "active",
        "renewal_due": "2026-09-01",
    },
    "E5F6G7H8": {
        "holder": "Sam Carter",
        "type": "Auto",
        "status": "lapsed",
        "renewal_due": "2026-04-15",
    },
    "J9K0L1M2": {
        "holder": "Priya Shah",
        "type": "Renters",
        "status": "active",
        "renewal_due": "2026-11-20",
    },
    "N3P4Q5R6": {
        "holder": "Dana Lowe",
        "type": "Umbrella",
        "status": "active",
        "renewal_due": "2027-01-10",
    },
    "S7T8U9V0": {
        "holder": "Alex Kim",
        "type": "Auto",
        "status": "pending_cancellation",
        "renewal_due": "2026-07-05",
    },
}


def get_policy_status(policy_id: str) -> dict:
    """Look up the current status of a single insurance policy.

    Args:
        policy_id: The 8 character alphanumeric policy ID, for example "A1B2C3D4".

    Returns:
        A dict with the policy details when found, otherwise a dict with an
        "error" key and a "hint" the agent can act on.
    """
    cleaned = policy_id.strip().upper()
    if len(cleaned) != 8 or not cleaned.isalnum():
        return {
            "error": "invalid policy id",
            "hint": "A policy ID is 8 alphanumeric characters, like A1B2C3D4.",
        }
    policy = _POLICIES.get(cleaned)
    if policy is None:
        return {
            "error": "policy not found",
            "hint": "Check the 8 character ID and try again.",
        }
    return {"policy_id": cleaned, **policy}


# ---- Tool 2, search the policy documents ------------------------------

_DOCS = [
    {
        "id": "HO-FLOOD-01",
        "policy_type": "Homeowners",
        "title": "Flood damage exclusion",
        "text": "Damage from flood, surface water, or overflow of a body of water "
        "is not covered under the standard homeowners policy. Flood coverage "
        "requires a separate National Flood Insurance Program policy.",
    },
    {
        "id": "HO-WATER-02",
        "policy_type": "Homeowners",
        "title": "Water damage from plumbing",
        "text": "Sudden and accidental water damage from a burst pipe or appliance "
        "is covered. Gradual leaks, seepage, and damage from long-term lack "
        "of maintenance are not covered.",
    },
    {
        "id": "GEN-DEDUCT-03",
        "policy_type": "General",
        "title": "How deductibles work",
        "text": "The deductible is the amount the policyholder pays before coverage "
        "applies. The standard homeowners deductible is 1000 dollars. Wind "
        "and hail claims may carry a separate percentage deductible.",
    },
    {
        "id": "AUTO-COLL-04",
        "policy_type": "Auto",
        "title": "Collision and comprehensive coverage",
        "text": "Collision covers damage to your vehicle from an accident regardless "
        "of fault. Comprehensive covers non-collision events such as theft, "
        "hail, fire, and animal strikes.",
    },
    {
        "id": "UMB-LIAB-05",
        "policy_type": "Umbrella",
        "title": "Umbrella liability limits",
        "text": "An umbrella policy extends liability coverage above the limits of "
        "your auto and homeowners policies, in increments of one million.",
    },
    {
        "id": "REN-PROP-06",
        "policy_type": "Renters",
        "title": "Personal property coverage",
        "text": "Renters coverage protects personal belongings against covered perils "
        "such as fire and theft. Replacement cost coverage pays to replace "
        "items new rather than at depreciated value.",
    },
    {
        "id": "HO-WIND-07",
        "policy_type": "Homeowners",
        "title": "Wind and hail",
        "text": "Wind and hail are covered perils under the homeowners policy. In some "
        "coastal states a separate wind or hurricane deductible applies.",
    },
]


def search_policy_docs(query: str, top_k: int = 3) -> list[dict]:
    """Search the Hartford policy documents and return the closest snippets.

    Args:
        query: A natural language question about coverage, for example
            "what is covered for flood damage".
        top_k: The maximum number of snippets to return. Defaults to 3.

    Returns:
        A list of snippet dicts, each with title, policy_type, and text, most
        relevant first. Returns an empty list when nothing matches.
    """
    words = [w for w in query.lower().split() if len(w) > 2]
    scored = []
    for doc in _DOCS:
        haystack = (doc["title"] + " " + doc["text"] + " " + doc["policy_type"]).lower()
        score = sum(1 for w in words if w in haystack)
        if score > 0:
            scored.append((score, doc))
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [
        {"title": d["title"], "policy_type": d["policy_type"], "text": d["text"]}
        for _, d in scored[:top_k]
    ]


# ---- Tool 3, quote a renewal ------------------------------------------


def request_renewal_quote(policy_id: str, term_months: int) -> dict:
    """Produce a renewal quote estimate for a policy.

    Args:
        policy_id: The 8 character policy ID to renew.
        term_months: The renewal length in months, for example 6 or 12.

    Returns:
        A dict with the policy_id, term_months, and a premium estimate.
    """
    monthly = 142.50  # a real system would call a rating engine here
    return {
        "policy_id": policy_id,
        "term_months": term_months,
        "premium_estimate": round(monthly * term_months, 2),
        "currency": "USD",
    }
