"""
OurFood Financial Model - Sensitivity Analysis

Shows which input parameters have the biggest impact on the platform fee percentage.
No external dependencies required - pure Python.
"""


def calculate_platform_fee(
    merchants_in_network=100,
    orders_per_merchant_per_day=60,
    average_order_value=30,
    payment_processing_fee_percentage=0.029,
    courier_to_merchant_ratio=1.2,
    courier_monthly_salary=2_300,
    management_dev_team_size=4,
    management_dev_monthly_salary=2_800,
    courier_to_bike_ratio=1.5,
    bike_maintenance_per_bike_per_month=200,
    operational_expenses=2_000,
    reserve_fund_percentage=0.05,
):
    """Calculate platform fee percentage given input parameters."""

    total_monthly_revenue = (
        merchants_in_network * orders_per_merchant_per_day * average_order_value * 30
    )

    payment_processing_fee = total_monthly_revenue * payment_processing_fee_percentage

    courier_count = merchants_in_network * courier_to_merchant_ratio
    courier_salaries = courier_count * courier_monthly_salary

    management_dev_salaries = management_dev_team_size * management_dev_monthly_salary

    bike_count = courier_count / courier_to_bike_ratio
    bike_maintenance = bike_count * bike_maintenance_per_bike_per_month

    expenses = (
        courier_salaries + management_dev_salaries + bike_maintenance + operational_expenses
    )

    total_before_reserve = total_monthly_revenue - payment_processing_fee - expenses

    reserve_fund_allocation = total_before_reserve * reserve_fund_percentage

    amount_returned_to_merchants = total_before_reserve - reserve_fund_allocation

    platform_fee = (
        (total_monthly_revenue - amount_returned_to_merchants) / total_monthly_revenue
    )

    return platform_fee * 100  # Return as percentage


def sensitivity_analysis(variation_percent=20):
    """
    Perform sensitivity analysis by varying each parameter and measuring impact.

    Args:
        variation_percent: How much to vary each parameter (default 20%)

    Returns:
        Dictionary mapping parameter names to their impact on platform fee
    """

    # Baseline values
    baseline_params = {
        'merchants_in_network': 100,
        'orders_per_merchant_per_day': 60,
        'average_order_value': 30,
        'payment_processing_fee_percentage': 0.029,
        'courier_to_merchant_ratio': 1.2,
        'courier_monthly_salary': 2_300,
        'management_dev_team_size': 4,
        'management_dev_monthly_salary': 2_800,
        'courier_to_bike_ratio': 1.5,
        'bike_maintenance_per_bike_per_month': 200,
        'operational_expenses': 2_000,
        'reserve_fund_percentage': 0.05,
    }

    baseline_fee = calculate_platform_fee(**baseline_params)

    # Calculate impact of varying each parameter
    impacts = {}

    for param_name, baseline_value in baseline_params.items():
        # Create parameter dict with one parameter varied
        params_high = baseline_params.copy()
        params_low = baseline_params.copy()

        variation = baseline_value * (variation_percent / 100)
        params_high[param_name] = baseline_value + variation
        params_low[param_name] = baseline_value - variation

        fee_high = calculate_platform_fee(**params_high)
        fee_low = calculate_platform_fee(**params_low)

        # Impact = total change in platform fee across the variation range
        impact = abs(fee_high - fee_low)
        impacts[param_name] = {
            'impact': impact,
            'baseline': baseline_fee,
            'high': fee_high,
            'low': fee_low,
            'direction': 'increases' if fee_high > fee_low else 'decreases'
        }

    return impacts, baseline_fee


def print_sensitivity_report(impacts, baseline_fee, variation_percent=20):
    """Print a formatted sensitivity analysis report."""

    print("=" * 80)
    print(f"OurFood Financial Model - Sensitivity Analysis")
    print("=" * 80)
    print(f"\nBaseline Platform Fee: {baseline_fee:.2f}%")
    print(f"Variation: ±{variation_percent}% for each parameter\n")
    print("-" * 80)

    # Sort by impact (highest to lowest)
    sorted_impacts = sorted(
        impacts.items(),
        key=lambda x: x[1]['impact'],
        reverse=True
    )

    print(f"{'Parameter':<45} {'Impact':<12} {'Direction':<12}")
    print("-" * 80)

    for param_name, data in sorted_impacts:
        # Format parameter name for readability
        display_name = param_name.replace('_', ' ').title()
        impact_str = f"±{data['impact']:.2f}pp"
        direction = f"Fee {data['direction']}"

        print(f"{display_name:<45} {impact_str:<12} {direction:<12}")

    print("-" * 80)
    print("\nKey Insights:")
    print(f"  • Top 3 most impactful parameters:")

    for i, (param_name, data) in enumerate(sorted_impacts[:3], 1):
        display_name = param_name.replace('_', ' ').title()
        print(f"    {i}. {display_name}: ±{data['impact']:.2f} percentage points")

    print(f"\n  • Baseline scenario breakdown:")
    print(f"    - {variation_percent}% increase in {sorted_impacts[0][0].replace('_', ' ')} → "
          f"{impacts[sorted_impacts[0][0]]['high']:.2f}% platform fee")
    print(f"    - {variation_percent}% decrease in {sorted_impacts[0][0].replace('_', ' ')} → "
          f"{impacts[sorted_impacts[0][0]]['low']:.2f}% platform fee")

    print("\n" + "=" * 80)


def create_ascii_tornado(impacts, baseline_fee, variation_percent=20):
    """Create an ASCII tornado diagram showing sensitivity analysis results."""

    # Sort by impact
    sorted_impacts = sorted(
        impacts.items(),
        key=lambda x: x[1]['impact'],
        reverse=True
    )

    print("\n" + "=" * 80)
    print("ASCII Tornado Diagram")
    print("=" * 80)
    print(f"Baseline: {baseline_fee:.2f}%")
    print("-" * 80)

    max_impact = max(data['impact'] for _, data in sorted_impacts)
    bar_width = 40  # characters for full bar

    for param_name, data in sorted_impacts:
        display_name = param_name.replace('_', ' ').title()[:30]

        # Calculate bar lengths proportional to impact
        impact_ratio = data['impact'] / max_impact
        bar_length = int(bar_width * impact_ratio)

        # Create the bar
        bar = '█' * bar_length

        print(f"{display_name:<30} |{bar:<40}| ±{data['impact']:.2f}pp")

    print("-" * 80)
    print(f"Bar length represents impact magnitude (longest = ±{max_impact:.2f}pp)")
    print("=" * 80)


if __name__ == '__main__':
    # Run sensitivity analysis with ±20% variation
    impacts, baseline_fee = sensitivity_analysis(variation_percent=20)

    # Print report
    print_sensitivity_report(impacts, baseline_fee, variation_percent=20)

    # Create ASCII visualization
    create_ascii_tornado(impacts, baseline_fee, variation_percent=20)

    # Optional: Try different variation percentages
    print("\n\n" + "=" * 80)
    print("Alternative Analysis: ±10% variation")
    print("=" * 80)
    impacts_10, baseline_fee_10 = sensitivity_analysis(variation_percent=10)
    print_sensitivity_report(impacts_10, baseline_fee_10, variation_percent=10)