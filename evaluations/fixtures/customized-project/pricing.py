"""Tiny pricing module used as an Axiom evaluation fixture. Contains one seeded defect."""


def apply_discount(total_cents: int, percent: int) -> int:
    """Return the total after a percentage discount, rounded down to whole cents.

    Discounts are capped at 100 percent; negative percentages are rejected.
    """
    if percent < 0:
        raise ValueError("percent must be non-negative")
    if percent > 100:
        percent = 100
    return total_cents - total_cents * percent // 10
