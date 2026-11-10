"""Dashboard widget of Budgets (docs/dashboards.md in hubra-app/hubra).

finance.budgets.usage  list  this year's budget lines: booked against planned,
                             the most used first

It reads as the viewing member, who needs ``budgets.budgets.read``.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import select

from hubra.core.extensions import db

from .models import Budget
from .services import actuals

_ZERO = Decimal("0")


def _chf(amount) -> str:
    return f"CHF {Decimal(amount or 0):,.0f}".replace(",", "'")


def usage(ctx, config: dict) -> dict:
    """Lines of this year's budget (the approved one first), most used first."""
    try:
        count = max(1, min(int(config.get("count") or 5), 20))
    except (TypeError, ValueError):
        count = 5
    kind = "income" if config.get("income") else "expense"
    year = date.today().year
    budget = db.session.scalar(
        select(Budget)
        .where(Budget.year == year)
        .order_by(Budget.approved.desc(), Budget.updated_at.desc(), Budget.id.desc())
        .limit(1)
    )
    if budget is None:
        return {"items": [], "total": 0}
    booked = actuals(year)
    rows = []
    for line in budget.lines:
        if line.kind != kind:
            continue
        actual = booked.get((line.category_id, line.kind), _ZERO)
        share = int(actual * 100 / line.planned) if line.planned else 0
        rows.append((share, line, actual))
    rows.sort(key=lambda r: (-r[0], r[1].id))
    items = [
        {
            "label": line.category.name if line.category else "–",
            "sub": f"{_chf(actual)} / {_chf(line.planned)} · {share}%",
            "path": "/app/finance/budgets",
        }
        for share, line, actual in rows[:count]
    ]
    return {"items": items, "total": len(rows)}
