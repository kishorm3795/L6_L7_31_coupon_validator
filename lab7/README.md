# Lab 7: Fuzz Testing for Input Validation Bugs

**Course:** Software Engineering Testing & Analysis (SETA)  
**Assigned Repository:** `L6_L7_31_coupon_validator`  
**Target Module:** `coupon_validator.py`  
**Fuzzing Library:** `hypothesis` (Property-Based Testing)  
**Test Framework:** `pytest`  

---

## 1. Executive Summary

This lab uses **Property-Based Fuzz Testing** to discover real-world input validation vulnerabilities and harden an e-commerce coupon processing script. By generating arbitrary, malformed, and adversarial inputs with `Hypothesis` (including unicode strings, empty strings, null bytes, and `None`), we exposed multiple fatal unhandled exceptions (`AttributeError`, `ValueError`) across all three target functions, then re-engineered the script with robust defensive programming to achieve **100% crash-free pass rates**.

---

## 2. Target Functions & Vulnerabilities Discovered

| Function | Signature | Vulnerability Discovered by Hypothesis | Minimizing Counterexample |
|----------|-----------|----------------------------------------|---------------------------|
| `split_code(code)` | Splits `PREFIX-VALUE` | • `AttributeError` when `code is None`<br/>• `ValueError` when `-` is missing<br/>• `ValueError` when value is non-integer | `s=None`<br/>`s=''`<br/>`s='-'` |
| `most_expensive(prices_csv)` | Finds max float price | • `AttributeError` when `prices_csv is None`<br/>• `ValueError` on empty string or element<br/>• `ValueError` calling `max()` on empty list | `s=None`<br/>`s=''` |
| `expiry_days(date_text)` | Calculates days from 2024 | • `AttributeError` when `date_text is None`<br/>• `ValueError` on malformed date parts<br/>• Invalid month/day bounds | `s=None`<br/>`s=''` |

---

## 3. Step-by-Step Lab Workflow

### Step 2: Run Buggy Application with Standard Inputs
```bash
python coupon_validator.py
```
- Inputs: `save-20`, `199,49.5,320`, `2025-10-15`
- **Output:** Successfully processed standard happy-path inputs.
- Screenshot: `screenshots/step2_buggy_app_run.png`

### Step 3: Implement Hypothesis Fuzz Tests
In `test_coupon_validator.py`, we defined crash-freedom property tests:
```python
from hypothesis import given, strategies as st
from coupon_validator import split_code, most_expensive, expiry_days

@given(st.text() | st.none())
def test_split_code_no_crash(s):
    try:
        split_code(s)
    except Exception as e:
        assert False, f"split_code crashed with: {e}"

@given(st.text() | st.none())
def test_most_expensive_no_crash(s):
    try:
        most_expensive(s)
    except Exception as e:
        assert False, f"most_expensive crashed with: {e}"

@given(st.text() | st.none())
def test_expiry_days_no_crash(s):
    try:
        expiry_days(s)
    except Exception as e:
        assert False, f"expiry_days crashed with: {e}"
```

### Step 4: Execute Fuzz Tests Against Buggy Application
```bash
pytest test_coupon_validator.py
```
- **Result:** **3 failed in 5.63s**. Hypothesis discovered multiple crashes across all three functions.
- Screenshot: `screenshots/step4_fuzz_test_failures.png`

### Step 5: Harden Application Script with Defensive Programming
We hardened `coupon_validator.py` by:
1. Validating types with `isinstance(..., str)`.
2. Validating token counts, checking for empty strings, and handling missing delimiters.
3. Catching `ValueError` during integer/float conversions and returning safe fallbacks (`(None, None)` or `None`).
4. Verifying calendar boundaries (months 1-12, days 1-31).

Run the fixed application:
```bash
python coupon_validator.py
```
- Screenshot: `screenshots/step5_fixed_app_run.png`

### Step 6: Re-run Fuzz Tests on Fixed Application
```bash
pytest -v test_coupon_validator.py
```
- **Result:** **3 passed in 0.27s**. Hundreds of random inputs tested per function with **zero unhandled exceptions**.
- Screenshot: `screenshots/step6_fuzz_test_passes.png`

---

## 4. Deliverables Checklist

- [x] **PDF Document with Screenshots:** `Lab_7_Fuzz_Testing_Report.pdf`
- [x] **Fixed Application Script:** `lab7/coupon_validator.py`
- [x] **Updated Hypothesis Test Code:** `lab7/test_coupon_validator.py`
