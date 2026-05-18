# Financial Model

## Playground

This spreadsheet allows experimentation with the financial model of the project.
Feel free to make a copy and play with the values.

<https://docs.google.com/spreadsheets/d/1oXnOxSqnoVSOA7BvlAhDODCzNZ_g-T1eSLabW8rk3CM/edit?usp=sharing>

## Analysis

This pseudocode explains how the platform fee is generated based on a month's
activity:

```python
merchants_in_network = 100
orders_per_merchant_per_day = 60
average_order_value = 30
total_monthly_revenue = (
    merchants_in_network * orders_per_merchant_per_day * average_order_value * 30
) # = €5,400,000.00
payment_processing_fee_percentage = 0.029  # Eg Stripe
payment_processing_fee = (
    total_monthly_revenue * payment_processing_fee_percentage
) # = €156,600.00
courier_to_merchant_ratio = 1.2  # Depends on economy of scale, routing algorithm
courier_count = merchants_in_network * courier_to_merchant_ratio  # = 120
courier_monthly_salary = 2_300  # Including insurance, benefits, etc.
courier_salaries = courier_count * courier_monthly_salary  # = €276,000.00
management_dev_team_size = 4
management_dev_monthly_salary = 2_800  # Including insurance, benefits, etc.
management_dev_salaries = (
  management_dev_team_size * management_dev_monthly_salary
)  # = €11,200.00
salaries = courier_salaries + management_dev_salaries  # = €287,200.00
courier_to_bike_ratio = 1.5  # Couriers share bikes, when one is off-shift another uses their bike
bike_count = courier_count / courier_to_bike_ratio  # = 80
bike_maintenance_per_bike_per_month = 200  # Including gas
bike_maintenance = bike_count * bike_maintenance_per_bike_per_month  # = €16,000.00
operational_expenses = 2_000  # Hosting, digital services, legal, accounting, etc.
expenses = (  # Required to keep the lights on if zero orders
    courier_salaries + management_dev_salaries + bike_maintenance + operational_expenses
)  # = €305,200.00
total_before_reserve = (
    total_monthly_revenue - payment_processing_fee - expenses
)  # = €4,938,800.00
reserve_fund_percentage = 0.05
reserve_fund_allocation = total_before_reserve * reserve_fund_percentage  # = €246,940.00
amount_returned_to_merchants = (
  total_before_reserve - reserve_fund_allocation
)  # = €4,691,860.00
platform_fee = (
  (total_monthly_revenue - amount_returned_to_merchants) / total_monthly_revenue
)  # = 13.12%
```

We can use this to calculate which input parameters have the biggest impact on
the platform fee. According to
[the analysis script](docs/sensitivity_analysis.py).

> Top 3 Most Impactful Parameters:
>
> 1. Orders per merchant per day (±2.24pp impact)
>    - More orders = lower platform fee (spreads fixed costs)
>    - This is your leverage point for sustainability
> 2. Average order value (±2.24pp impact)
>    - Higher order values = lower platform fee
>    - Payment processing is percentage-based, but most costs are fixed
> 3. Courier to merchant ratio (±2.05pp impact)
>    - More efficient routing/batching = fewer couriers needed = lower fee
>    - This is your operational efficiency metric
>
> Key Takeaways:
>
> Growth is your friend: The platform fee drops from 14.5% → 12.2% just by
> increasing orders 20%. This means:
>
> - Early phase will have higher fees (lower volume)
> - As you scale, fees naturally decrease
> - Critical to communicate this trajectory to early merchant-members
>
> Salaries matter less than you'd think: A 20% courier salary increase only adds
> ~2pp to the fee. This means you can afford to pay couriers well without
> breaking the model.
>
> Bike costs are negligible: Maintenance and bike/courier ratios barely move the
> needle. Don't stress over bike optimization—focus on order volume and routing
> efficiency.
>
> Strategy Implications:
>
> - Phase 1 launch: Accept that you'll start at ~15-18% fee (lower volume)
> - Growth target: Hit the 60 orders/merchant/day baseline to get to 13%
> - Competitive advantage: Even at 15%, you're still 20pp cheaper than
>   incumbents
> - Courier wages: You have room to pay competitively without hurting the model

So, it is imperative that merchants promote OurFood to their customers as much
as possible and a big research effort is needed for the routing algorithm.
