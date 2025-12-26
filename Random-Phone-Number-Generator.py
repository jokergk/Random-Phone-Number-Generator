#!/usr/bin/env python3
"""
Random-Phone-Number-Generator.py

Generate random phone numbers with configurable country code, local code, and total numeric length.
Features:
- Accepts country code with or without leading '+'
- Optional '+' in output
- Optional uniqueness enforcement (checked for feasibility)
- Interactive prompts (default) + optional CLI arguments (argparse)
- Saves results to CSV

Usage (interactive):
    python Random-Phone-Number-Generator.py

Usage (CLI example):
    python Random-Phone-Number-Generator.py --total 11 --country +1 --local 415 --count 10 --out my_numbers.csv
"""

from __future__ import annotations
import csv
import random
import sys
import argparse
from typing import List

rng = random.SystemRandom()


def generate_phone_numbers(total_length: int,
                           country_code: str,
                           local_code: str,
                           limit: int,
                           include_plus: bool = True,
                           unique: bool = True) -> List[str]:
    """
    Generate `limit` phone numbers as strings.

    total_length: total numeric digits in the final phone string (exclude '+' if present).
    country_code: country prefix (e.g. '+1' or '1')
    local_code: local area code digits (e.g. '415') (may be empty)
    include_plus: if True, returned numbers start with '+' (if applicable)
    unique: if True, ensures all generated numbers are unique (raises if impossible)
    """
    if total_length <= 0:
        raise ValueError("total_length must be a positive integer.")

    country_digits = country_code.strip().lstrip('+')
    local_digits = local_code.strip()

    if not country_digits.isdigit():
        raise ValueError("Country code must contain digits only (you may include a leading '+').")
    if local_digits and not local_digits.isdigit():
        raise ValueError("Local code must contain digits only.")

    remaining_length = total_length - len(country_digits) - len(local_digits)
    if remaining_length <= 0:
        raise ValueError(
            "Total length is too short for the specified country and local codes. "
            f"Need remaining random digits > 0, got {remaining_length}."
        )

    max_possible = 10 ** remaining_length
    if unique and limit > max_possible:
        raise ValueError(
            f"Cannot generate {limit} unique numbers with {remaining_length} random digits. "
            f"Maximum unique combinations = {max_possible}."
        )

    results: List[str] = []
    seen = set()

    while len(results) < limit:
        number_body = ''.join(rng.choice('0123456789') for _ in range(remaining_length))
        full_number = f"{country_digits}{local_digits}{number_body}"
        if unique:
            if full_number in seen:
                continue
            seen.add(full_number)

        if include_plus:
            results.append(f"+{full_number}")
        else:
            results.append(full_number)

    return results


def save_to_csv(phone_numbers: List[str], filename: str = "phone_numbers.csv") -> None:
    """
    Save a list of phone number strings to CSV with a single header column.
    """
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Phone Number"])
        writer.writerows([[p] for p in phone_numbers])


def prompt_int(prompt_text: str, default: int | None = None) -> int:
    """
    Prompt user for integer input, optionally allowing Enter to accept a default.
    """
    while True:
        try:
            raw = input(prompt_text).strip()
            if raw == "" and default is not None:
                return default
            val = int(raw)
            return val
        except ValueError:
            print("Please enter a valid integer.")


def interactive_mode() -> argparse.Namespace:
    """
    Gather inputs from the user interactively and return a namespace-like object.
    """
    print("Random Phone Number Generator — Interactive Mode")
    total_length = prompt_int("Enter total numeric length of phone number (digits only, exclude '+'): ")
    country_code = input("Enter the country code (e.g., +1, 1, +91, 91): ").strip()
    if not country_code:
        print("Country code is required.")
        sys.exit(1)
    local_code = input("Enter the local code (e.g., 415, 011, 020). If none, press Enter: ").strip() or ""
    count = prompt_int("Enter how many phone numbers to generate: ")
    filename = input("Enter output CSV filename (default: phone_numbers.csv): ").strip() or "phone_numbers.csv"
    include_plus_str = input("Include '+' sign in output? (Y/n) [default: Y]: ").strip().lower()
    include_plus = not (include_plus_str == "n")
    unique_str = input("Require unique phone numbers? (Y/n) [default: Y]: ").strip().lower()
    unique = not (unique_str == "n")

    ns = argparse.Namespace(
        total=total_length,
        country=country_code,
        local=local_code,
        count=count,
        out=filename,
        no_plus=(not include_plus),
        no_unique=(not unique)
    )
    return ns


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="Random-Phone-Number-Generator",
                                     description="Generate random phone numbers and export to CSV.")
    parser.add_argument("--total", "-t", type=int, help="Total numeric length of phone number (exclude '+').")
    parser.add_argument("--country", "-c", type=str, help="Country code (e.g., +1 or 1).")
    parser.add_argument("--local", "-l", type=str, default="", help="Local area code (optional).")
    parser.add_argument("--count", "-n", type=int, default=10, help="How many phone numbers to generate (default: 10).")
    parser.add_argument("--out", "-o", type=str, default="phone_numbers.csv", help="Output CSV filename.")
    parser.add_argument("--no-plus", action="store_true", help="Do NOT include '+' in output.")
    parser.add_argument("--no-unique", action="store_true", help="Allow duplicates (do not require uniqueness).")
    parser.add_argument("--interactive", "-i", action="store_true", help="Force interactive prompts.")
    args = parser.parse_args()

    # If interactive flag set or no required args supplied, go interactive
    if args.interactive or (args.total is None or args.country is None):
        return interactive_mode()
    return args


def main() -> None:
    args = parse_args()

    # argv options map:
    total_length = args.total
    country_code = args.country
    local_code = getattr(args, "local", "") or ""
    count = args.count
    filename = args.out
    include_plus = not getattr(args, "no_plus", False)
    unique = not getattr(args, "no_unique", False)

    try:
        phone_numbers = generate_phone_numbers(
            total_length=total_length,
            country_code=country_code,
            local_code=local_code,
            limit=count,
            include_plus=include_plus,
            unique=unique
        )
        save_to_csv(phone_numbers, filename)
        print(f"Success — generated {len(phone_numbers)} phone numbers and saved to '{filename}'.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
