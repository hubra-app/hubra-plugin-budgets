"""Budgets: a plan per year and category, compared with booked transactions."""

from hubra.core.contracts import WidgetField, query_contract, widget_contract
from hubra.core.modules import Blueprint, Module

module = Module(
    code="finance.budgets",
    # Access the standard roles get when a club first switches it on
    # (docs/roles.md in hubra-app/hubra).
    role_defaults={"board": "view", "treasurer": "all"},
    name="Budgets",
    description="Yearly budgets per category, with actuals from transactions",
    default_enabled=False,
    depends_on=("finance",),
    blueprints=(
        Blueprint(
            "hubra_budgets.routes",
            "budgets_bp",
            "/api/v1/budgets",
        ),
    ),
    tables=("budgets", "budget_lines"),
    # Hubra's fee basis (Finanzen › Beitragsgrundlage) asks the approved
    # budget as its "budget" source; the billing year comes from Finance.
    provides=(
        query_contract(
            "finance.budgets.fee_basis.budget",
            "hubra_budgets.fee_basis:budget_source",
            input="hubra_budgets.fee_basis:SourceIn",
            output="hubra_budgets.fee_basis:SourceOut",
            # Hubra's fee basis asks as the system; anyone else asking for a
            # member needs the right to see budgets.
            perm="budgets.budgets.read",
            description="The approved budget's expenses of a billing year",
        ),
        # Dashboard widget (hubra_budgets/widgets.py).
        widget_contract(
            "finance.budgets.usage",
            "hubra_budgets.widgets:usage",
            label="budgets.widget.usage",
            description="budgets.widget.usageHint",
            size="m",
            view="list",
            perm="budgets.budgets.read",
            fields=(
                WidgetField("income", "budgets.widget.income", "switch", False),
                WidgetField("count", "budgets.widget.count", "number", 5),
            ),
        ),
    ),
    consumes={"finance.billing_period": ">=1,<2"},
)
