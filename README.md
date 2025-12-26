# 📞 Phone Number Generator — Improved

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A lightweight Python tool to generate random phone numbers with configurable country and local codes. Supports optional `+` prefix, unique-only generation, and CSV export.

---

## ✨ Features

- Generate phone numbers of arbitrary numeric length.
- Accepts country code with or without a leading `+`.
- Optional local/area code.
- Option to **include `+`** in outputs.
- Option to **require unique** generated numbers.
- Validates inputs and checks feasibility for unique generation.
- Saves output to CSV with header.

---

## 🛠 Requirements

- Python 3.8 or newer  
- No external dependencies (standard library only)

---

## 🚀 Quick start
git clone https://github.com/yourusername/Random-Phone-Number-Generator.git
cd PhoneNumberGenerator
Run the script:


Copy code
python Random-Phone-Number-Generator.py
Follow the prompts:

pgsql
Copy code
Enter total numeric length of phone number (digits only, exclude '+'): 11
Enter the country code (e.g., +1, 1, +91, 91): +1
Enter the local code (e.g., 415, 011, 020). If none, press Enter: 415
Enter how many phone numbers to generate: 5
Enter output CSV filename (default: phone_numbers.csv): my_numbers.csv
Include '+' sign in output? (Y/n) [default: Y]: Y
Require unique phone numbers? (Y/n) [default: Y]: Y
Example generated numbers:

diff
Copy code
+14151234567
+14150987654
+14152345678
+14153456789
+14154567890
Saved to my_numbers.csv.

📁 Files
Random-Phone-Number-Generator.py — main script

LICENSE — MIT license (recommended)

README.md — this file

🧠 Notes & validation
total_length is the total numeric length of the phone number (do not count +).

The script computes how many random digits are required:
remaining = total_length - len(country_code_digits) - len(local_code)

remaining must be > 0.

If unique=True and limit > 10 ** remaining, the script will raise an error because unique combinations are exhausted.

✅ Example (U.S. 11-digit numbers)
Parameters:

total_length = 11

country_code = +1

local_code = 415

limit = 10

Generates numbers like +1415XXXXXXX where XXXXXXX is a random 7-digit block.
