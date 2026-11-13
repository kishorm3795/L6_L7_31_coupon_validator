"""
L6_L7_31 — Coupon Validator (Hardened Implementation for Lab 7)
Defensively programmed against arbitrary, unexpected, and malformed inputs.
Discovered and verified via Hypothesis property-based fuzz testing.
"""

def split_code(code):
    """
    Splits a coupon code (e.g. 'SAVE-20') into prefix and integer value.
    Returns (prefix, value) or (None, None) if the input is malformed or not a string.
    """
    if not isinstance(code, str):
        return None, None
    parts = code.strip().upper().split('-')
    if len(parts) != 2:
        return None, None
    prefix, value_str = parts
    if not prefix:
        return None, None
    try:
        return prefix, int(value_str)
    except ValueError:
        return None, None


def most_expensive(prices_csv):
    """
    Extracts the highest price from a comma-separated values string.
    Returns the maximum float price, or None if the input contains no valid numeric prices.
    """
    if not isinstance(prices_csv, str):
        return None
    parts = prices_csv.split(',')
    prices = []
    for p in parts:
        item = p.strip()
        if not item:
            continue
        try:
            prices.append(float(item))
        except ValueError:
            continue
    if not prices:
        return None
    return max(prices)


def expiry_days(date_text):
    """
    Calculates the approximate days from 2024-01-01 to the given date (YYYY-MM-DD).
    Returns total days as an integer, or None if the input is invalid or out of range.
    """
    if not isinstance(date_text, str):
        return None
    parts = date_text.strip().split('-')
    if len(parts) != 3:
        return None
    try:
        year, month, day = [int(p.strip()) for p in parts]
        if month < 1 or month > 12 or day < 1 or day > 31:
            return None
        return (year - 2024) * 365 + (month - 1) * 30 + day
    except ValueError:
        return None


def main():
    print("==== Running split_code ====")
    user_input = input("Enter a coupon code (e.g. save-20): ")
    result = split_code(user_input)
    print("Prefix and Value:", result)

    print("\n==== Running most_expensive ====")
    user_input = input("Enter item prices as CSV (e.g. 199,49.5,320): ")
    result = most_expensive(user_input)
    print("Most Expensive Item:", result)

    print("\n==== Running expiry_days ====")
    user_input = input("Enter an expiry date as YYYY-MM-DD: ")
    result = expiry_days(user_input)
    print("Days Since 2024:", result)


if __name__ == "__main__":
    main()
