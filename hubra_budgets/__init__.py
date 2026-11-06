"""Budgets: a plan per year and category, compared with booked transactions."""

from hubra.core.contracts import query_contract
from hubra.core.modules import Blueprint, Module

module = Module(
    code="finance.budgets",
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
            description="The approved budget's expenses of a billing year",
        ),
    ),
    consumes={"finance.billing_period": ">=1,<2"},
)
