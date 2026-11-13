# Software Engineering Testing & Analysis (SETA) — Labs 6 & 7

**Repository:** `L6_L7_31_coupon_validator`  
**Student Workspace:** `/Users/pavankishorm/Documents/My Projects/L6_L7_31_coupon_validator`  

This repository contains the complete implementation, test suites, terminal output evidence, and formal laboratory reports for both **Lab 6** and **Lab 7**.

---

## Quick Navigation

| Lab | Title | Topic | Deliverables & Artifacts | Status |
|:---:|:------|:------|:-------------------------|:------:|
| **Lab 6** | Code & Branch Coverage Analysis | Line, Branch, Path Coverage using `coverage` & `pytest` | • [`Lab_6_Code_and_Branch_Coverage_Report.pdf`](./Lab_6_Code_and_Branch_Coverage_Report.pdf)<br/>• [`CodeCoverageTest_coupon_validator.py`](./lab6/CodeCoverageTest_coupon_validator.py)<br/>• [`BranchCoverageTest_coupon_validator.py`](./lab6/BranchCoverageTest_coupon_validator.py)<br/>• [`test_coupon_validator.py`](./lab6/test_coupon_validator.py)<br/>• [`lab6/screenshots/`](./lab6/screenshots/) | **100% Statements<br/>100% Branches<br/>(10/10 Marks)** |
| **Lab 7** | Fuzz Testing for Input Validation | Property-Based Fuzzing with `Hypothesis` | • [`Lab_7_Fuzz_Testing_Report.pdf`](./Lab_7_Fuzz_Testing_Report.pdf)<br/>• [`lab7/coupon_validator.py`](./lab7/coupon_validator.py) (Hardened)<br/>• [`lab7/test_coupon_validator.py`](./lab7/test_coupon_validator.py)<br/>• [`lab7/screenshots/`](./lab7/screenshots/) | **100% Pass Rate<br/>All Edge Cases Hardened** |

---

## Lab 6: Code & Branch Coverage Summary

- **Initial Baseline:** 23% branch coverage, 31% overall coverage (23 missed statements, 20 missed branches).
- **Code Coverage Suite:** `CodeCoverageTest_coupon_validator.py` achieves **100% line coverage** (32/32 statements).
- **Branch Coverage Suite:** `BranchCoverageTest_coupon_validator.py` achieves **100% branch coverage** (24/24 branches) and **100% statement coverage**.
- **Consolidated Suite:** `test_coupon_validator.py` contains 23 comprehensive unit tests validating every predicate, equivalence partition, and boundary value.

### How to Run Lab 6
```bash
cd lab6
# Run statement coverage:
coverage run -m pytest CodeCoverageTest_coupon_validator.py
coverage report -m

# Run branch coverage:
coverage run --branch -m pytest BranchCoverageTest_coupon_validator.py
coverage report -m

# Run consolidated suite:
coverage run --branch -m pytest test_coupon_validator.py
coverage report -m
```

---

## Lab 7: Fuzz Testing with Hypothesis Summary

- **Vulnerabilities Discovered:** The original `lab7/coupon_validator.py` crashed with `AttributeError` when given `None`, and `ValueError` when given empty strings, invalid delimiters, non-numeric values, and empty CSV lists.
- **Hypothesis Test Suite:** Implemented crash-freedom property tests `@given(st.text() | st.none())` uncovering 7 distinct failure modes.
- **Defensive Hardening:** Refactored `lab7/coupon_validator.py` with type checks, safe token parsing, boundary validation, and robust exception handling.
- **Verification:** Re-running `pytest test_coupon_validator.py` against the hardened code passes 100% across hundreds of random fuzz inputs.

### How to Run Lab 7
```bash
cd lab7
# Run the hardened application:
python coupon_validator.py

# Run Hypothesis property-based fuzz tests:
pytest -v test_coupon_validator.py
```

---

## Git Commit Structure

Per the rubric instructions (minimum 2 commits for Lab 6 plus dedicated Lab 7 commits):
1. `Lab 6: Add CodeCoverageTest suite achieving 100% statement coverage`
2. `Lab 6: Add BranchCoverageTest suite achieving 100% branch and statement coverage`
3. `Lab 7: Add Hypothesis property-based fuzz test suite exposing crash vulnerabilities`
4. `Lab 7: Harden coupon validator with defensive programming and verify crash-freedom`
5. `Docs: Add publication-quality PDF reports and high-resolution terminal screenshots`
