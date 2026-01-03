def assign_team(category: str, confidence: float | None) -> str:
    if confidence is not None and confidence < 0.6:
        return "MANUAL_REVIEW"

    if category == "Payments":
        return "PAYMENTS_TEAM"

    if category == "Login":
        return "IDENTITY_TEAM"

    if category == "Technical":
        return "TECH_SUPPORT"

    return "GENERAL_SUPPORT"
