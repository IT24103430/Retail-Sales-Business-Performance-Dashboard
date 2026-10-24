"""Generate fictional Sri Lankan retail CSVs using only the Python standard library.

Run from the project root: python3 scripts/generate_data.py
The fixed seed reproduces the same files; rerunning replaces the five raw CSVs.
"""

import csv
import random
from datetime import date, timedelta
from pathlib import Path


SEED = 20250930
TARGET_LINES = 5_000
CUSTOMER_COUNT = 700
START_DATE = date(2025, 1, 1)
END_DATE = date(2026, 9, 30)
RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"

FACT_COLUMNS = [
    "SalesLineID", "OrderID", "OrderDate", "ProductID", "CustomerID",
    "RegionID", "ChannelID", "Quantity", "UnitPrice", "UnitCost", "DiscountAmount",
]

# Fictional catalogue: product label, category, typical selling price in LKR.
PRODUCT_CATALOGUE = [
    ("Samba Rice 5 kg", "Groceries", 1_450),
    ("Red Raw Rice 1 kg", "Groceries", 290),
    ("Red Lentils 1 kg", "Groceries", 410),
    ("Coconut Oil 750 ml", "Groceries", 1_050),
    ("Coconut Milk Powder 300 g", "Groceries", 780),
    ("Curry Powder 100 g", "Groceries", 250),
    ("White Sugar 1 kg", "Groceries", 310),
    ("Wheat Flour 1 kg", "Groceries", 240),
    ("Cream Crackers 400 g", "Groceries", 520),
    ("String Hopper Flour 1 kg", "Groceries", 360),
    ("Black Tea 200 g", "Beverages", 640),
    ("Instant Coffee 100 g", "Beverages", 1_150),
    ("Ginger Drink 1 L", "Beverages", 440),
    ("Mango Nectar 1 L", "Beverages", 690),
    ("Drinking Water 1.5 L", "Beverages", 180),
    ("Laundry Powder 1 kg", "Household", 920),
    ("Dishwashing Liquid 500 ml", "Household", 480),
    ("Floor Cleaner 1 L", "Household", 790),
    ("Kitchen Towels 2 Pack", "Household", 650),
    ("Food Storage Box 1 L", "Household", 580),
    ("Herbal Soap 100 g", "Personal Care", 190),
    ("Shampoo 200 ml", "Personal Care", 890),
    ("Toothpaste 120 g", "Personal Care", 470),
    ("Hand Wash 250 ml", "Personal Care", 540),
    ("Exercise Book 160 Pages", "Stationery", 260),
    ("Blue Ballpoint Pens 5 Pack", "Stationery", 350),
    ("Colour Pencils 12 Pack", "Stationery", 690),
    ("Electric Kettle 1.7 L", "Small Appliances", 6_900),
    ("Rice Cooker 1.8 L", "Small Appliances", 12_500),
    ("Table Fan 16 Inch", "Small Appliances", 15_900),
]

# Each region uses a representative city; weights are fictional sales assumptions.
REGION_CATALOGUE = [
    ("R01", "Western", "Colombo", 30),
    ("R02", "Central", "Kandy", 14),
    ("R03", "Southern", "Galle", 12),
    ("R04", "Northern", "Jaffna", 7),
    ("R05", "Eastern", "Batticaloa", 7),
    ("R06", "North Western", "Kurunegala", 11),
    ("R07", "North Central", "Anuradhapura", 7),
    ("R08", "Uva", "Badulla", 6),
    ("R09", "Sabaragamuwa", "Ratnapura", 6),
]

CHANNELS = [
    {"ChannelID": "CH01", "ChannelName": "Physical Store"},
    {"ChannelID": "CH02", "ChannelName": "Online Store"},
    {"ChannelID": "CH03", "ChannelName": "Mobile App"},
    {"ChannelID": "CH04", "ChannelName": "Telephone Order"},
]


def money(cents):
    """Format integer cents without floating-point rounding of money."""
    return f"{cents // 100}.{cents % 100:02d}"


def write_csv(filename, columns, rows):
    with (RAW_DIR / filename).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_dimensions(rng):
    products = [
        {"ProductID": f"P{index:03d}", "ProductName": name, "Category": category}
        for index, (name, category, _) in enumerate(PRODUCT_CATALOGUE, start=1)
    ]
    regions = [
        {"RegionID": key, "RegionName": name, "City": city}
        for key, name, city, _ in REGION_CATALOGUE
    ]
    customers = []
    for index in range(1, CUSTOMER_COUNT + 1):
        region = rng.choices(regions, weights=[r[3] for r in REGION_CATALOGUE])[0]
        customers.append({
            "CustomerID": f"C{index:04d}",
            "CustomerLabel": f"Synthetic customer {index:04d}",
            "CustomerSegment": rng.choices(
                ["Household", "Student", "Small Business"], weights=[70, 18, 12]
            )[0],
            "RegionID": region["RegionID"],
        })
    return products, customers, regions


def build_sales(rng, products, customers):
    # One to four distinct products per basket; stop at exactly 5,000 lines.
    basket_sizes = []
    remaining = TARGET_LINES
    while remaining:
        size = min(rng.choices([1, 2, 3, 4], weights=[38, 32, 20, 10])[0], remaining)
        basket_sizes.append(size)
        remaining -= size

    days = [
        START_DATE + timedelta(days=offset)
        for offset in range((END_DATE - START_DATE).days + 1)
    ]
    # Illustrative April/December shopping peaks and slightly higher weekend demand.
    day_weights = [
        (1.6 if day.month in (4, 12) else 1.0)
        * (1.2 if day.weekday() >= 5 else 1.0)
        for day in days
    ]
    # Include both endpoints, with all other order dates sampled within the range.
    order_dates = sorted(
        [START_DATE, END_DATE]
        + rng.choices(days, weights=day_weights, k=len(basket_sizes) - 2)
    )
    sales = []
    for order_number, (order_date, basket_size) in enumerate(
        zip(order_dates, basket_sizes), start=1
    ):
        customer = rng.choice(customers)
        channel = rng.choices(CHANNELS, weights=[60, 22, 13, 5])[0]
        for product in rng.sample(products, k=basket_size):
            base_price = PRODUCT_CATALOGUE[int(product["ProductID"][1:]) - 1][2]
            # Price varies around the catalogue price; a small 2026 uplift is assumed.
            price_percent = rng.randint(95, 105) + (3 if order_date.year == 2026 else 0)
            unit_price = base_price * price_percent  # LKR * percent gives integer cents.
            unit_cost = unit_price * rng.randint(60, 78) // 100
            if product["Category"] == "Small Appliances":
                quantity = rng.choices([1, 2], weights=[95, 5])[0]
            elif customer["CustomerSegment"] == "Small Business":
                quantity = rng.randint(3, 10)
            else:
                quantity = rng.choices([1, 2, 3, 4, 5], weights=[42, 30, 16, 8, 4])[0]
            gross_cents = quantity * unit_price
            # Discounts are line totals, between 0% and 20% of gross line sales.
            discount_percent = rng.choices([0, 5, 10, 15, 20], weights=[55, 20, 15, 7, 3])[0]
            discount_cents = (gross_cents * discount_percent + 50) // 100
            sales.append({
                "SalesLineID": f"SL{len(sales) + 1:06d}",
                "OrderID": f"ORD{order_number:05d}",
                "OrderDate": order_date.isoformat(),
                "ProductID": product["ProductID"],
                "CustomerID": customer["CustomerID"],
                "RegionID": customer["RegionID"],
                "ChannelID": channel["ChannelID"],
                "Quantity": quantity,
                "UnitPrice": money(unit_price),
                "UnitCost": money(unit_cost),
                "DiscountAmount": money(discount_cents),
            })
    return sales


def main():
    rng = random.Random(SEED)
    products, customers, regions = build_dimensions(rng)
    sales = build_sales(rng, products, customers)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    write_csv("dim_products.csv", ["ProductID", "ProductName", "Category"], products)
    write_csv(
        "dim_customers.csv",
        ["CustomerID", "CustomerLabel", "CustomerSegment", "RegionID"],
        customers,
    )
    write_csv("dim_regions.csv", ["RegionID", "RegionName", "City"], regions)
    write_csv("dim_channels.csv", ["ChannelID", "ChannelName"], CHANNELS)
    write_csv("fact_sales.csv", FACT_COLUMNS, sales)
    print(f"Created five CSV files in {RAW_DIR} ({len(sales):,} sales lines).")


if __name__ == "__main__":
    main()
