"""The approved budget as the source of the yearly expenses that percentage
and formula tiers share (Finanzen › Beitragsgrundlage in Hubra)."""

from __future__ import annotations

from decimal import Decimal

from sqlalchemy import select

from hubra.core.extensions import db

from .models import Budget


def budget_lines(year: int) -> list[dict] | None:
    """The expense lines of the year's approved budgets, one per category;
    None when no budget of that year is approved."""
    budgets = db.session.scalars(
        select(Budget).where(Budget.year == year).where(Budget.approved.is_(True))
    ).all()
    if not budgets:
        return None
    lines: dict[int, dict] = {}
    for budget in budgets:
        for line in budget.lines:
            if line.kind != "expense":
                continue
            entry = lines.setdefault(
                line.category_id,
                {
                    "category_id": line.category_id,
                    "name": line.category.name if line.category else None,
                    "color": line.category.color if line.category else None,
                    "amount": Decimal(0),
                    "items": [],
                },
            )
            entry["amount"] += Decimal(line.planned)
            entry["items"].append(
                {"description": line.note or budget.name, "amount": float(line.planned)}
            )
    return sorted(lines.values(), key=lambda line: -line["amount"])


def register() -> None:
    """Offer the budget as a source, on a Hubra that has the fee basis."""
    try:
        from hubra.api.finance.fee_basis import register_source
    except ImportError:  # Hubra before the Beitragsgrundlage page
        return
    register_source("budget", "finance.budgets", budget_lines)
