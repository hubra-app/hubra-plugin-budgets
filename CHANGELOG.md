# Changelog

## 1.4.0

- Gives the standard roles access when a club first switches it on (`role_defaults`, docs/roles.md in hubra-app/hubra): Vorstand Ansehen, Kassier/in Alles. Roles without access don't see it; their own data from it stays on their profile. Needs Hubra 0.2.5 or later.

## 1.3.0

- A budget can have an owner (Verantwortlich), such as a team's leader.
  Whoever may edit budgets picks the owner above the budget. The owner
  plans that budget's lines and notes without the right to edit every
  budget; approving, renaming, deleting and handing it on stay with
  `budgets.write`. The owner still needs `budgets.read` to see the Budgets
  tab. Copying a budget to the next year keeps its owner.
  Migration `3d7b1e9a5c42` adds `budgets.owner_id`.

## 1.2.0

- An approved budget can be the source of the yearly expenses that
  percentage and formula tiers share (Finanzen › Beitragsgrundlage, Hubra
  with that page). Its expense lines count, per category; with several
  approved budgets in a year, all of them.

## 1.1.0

Built for Hubra 0.2 (Mantine 9, plugin host API 2). Needs Hubra 0.2 or newer.

## 1.0.1

- A planned amount of "NaN" or one too large to store is refused with a
  message instead of a server error.
- A budget name that isn't text is refused with a message too.

## 1.0.0

First release as a plugin. Before, Budgets was built into Hubra.
