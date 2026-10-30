# Grants

## Migrating
Migrating from ColdFront v1.1.7 -> v1.1.8 changes grants to use [`django-money`](https://github.com/django-money/django-money)'s `MoneyField`s instead of custom ones, requiring a migration.
Migration 0004 pulls the default currency from project settings - specify `DEFAULT_CURRENCY` in your local settings.
Any existing grants will be set to use that currency.

The original `coldfront.core.grant.MoneyField` and `coldfront.core.grant.PercentField` has been removed, other than for historical/migration reasons.
`coldfront.core.grant.MoneyField` has been replaced with `djmoney.models.fields.MoneyField`, and `coldfront.core.grant.PercentField` has been replaced with `django.db.models.FloatField`.

The new `MoneyField`s are configured for 19 max digits and 4 decimal places of resolution as [suggested by `django-money`](https://github.com/django-money/django-money#model-usage) (supporting numbers up to about 999 trillion: 100 000 000 000 000.0000).

## Settings
You can find a list of currencies with the following:
[(original docs)](https://py-moneyed.readthedocs.io/en/latest/usage.html#list-all-currencies)
```py
>>> from moneyed import list_all_currencies
>>> list_all_currencies()
[ADP, AED, AFA, ...]
```

- `DEFAULT_CURRENCY` 
    - Default value: `"USD"`
    - Sets the default currency when migrating (see above)
    - Sets the default currency in grant forms
    - The only currency considered for the chart in the center summary page
    - Appears first in the "grant totals" table
- `CURRENCIES` 
    - Default value: `None`
    - Example value: `["USD", "EUR"]`
    - Sets list of allowed currencies throughout the project.
    - By default, all available currencies are listed.
