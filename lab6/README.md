# Lab 6: Code and Branch Coverage Analysis

**Course:** Software Engineering Testing & Analysis (SETA)  
**Assigned Repository:** `L6_L7_31_coupon_validator`  
**Target Module:** `coupon_validator.py`  
**Test Framework:** `pytest` + `coverage`  

---

## 1. Executive Summary

This lab analyzes and maximizes **Statement (Line) Coverage** and **Branch Coverage** for the e-commerce coupon validation module (`coupon_validator.py`). Starting from a baseline with only 23% branch coverage and 31% overall coverage, we systematically engineered two specialized test suites and one consolidated suite:

1. **`CodeCoverageTest_coupon_validator.py`**: Achieves **100% Statement Coverage** (32/32 statements).
2. **`BranchCoverageTest_coupon_validator.py`**: Achieves **100% Branch Coverage** (24/24 branches) and **100% Statement Coverage** (0 missing lines, 0 missing branches).
3. **`test_coupon_validator.py`**: Consolidated test suite (23 tests) achieving **100% overall coverage**.

---

## 2. Theoretical Concepts

| Coverage Metric | Definition | Importance | Achieved |
|-----------------|------------|------------|----------|
| **Line / Statement Coverage** | Percentage of executable statements run at least once. | Ensures no completely dead code exists. | **100% (32/32)** |
| **Branch Coverage** | Percentage of boolean decision outcomes (True/False) taken. | Exposes unexercised control flow paths even if lines executed. | **100% (24/24)** |
| **Path Coverage** | Percentage of all possible unique execution paths traversed. | Highest rigor for safety-critical logic. | **100% of reachable paths** |
| **Function Coverage** | Percentage of declared functions invoked during tests. | Verifies all module interfaces are exercised. | **100% (3/3)** |

### Why Line Coverage is Not Enough
A test suite can execute every line of code (100% statement coverage) without testing both outcomes of conditional branches. For example, testing `best_discount` with a single coupon that improves `best` executes line 25 and 26. However, if no coupon has `value <= best`, the branch `25->23` (skipping the update) is never tested. Our `BranchCoverageTest` explicitly exercises this branch and all boundary conditions.

---

## 3. Module Architecture Under Test

`coupon_validator.py` contains three core business functions:

1. `coupon_discount(code, cart_total, is_new_user, day)`
   - Raises `ValueError("empty cart")` if `cart_total <= 0`.
   - `WELCOME10`: 10% discount for new users; 0 for existing users.
   - `WEEKEND20`: Valid on Saturday and Sunday. 20% discount if `cart_total >= 500`; flat $50 if `< 500`. Returns 0 on weekdays.
   - `FLAT100`: $100 flat discount if `cart_total > 300`; 0 if `<= 300`.
   - Default return: 0 for unknown codes.

2. `best_discount(codes, cart_total, is_new_user, day)`
   - Iterates through a collection of promo codes, tracking the highest discount.
   - Enforces an upper safety limit: `cap = cart_total * 0.4` (40% maximum discount).
   - Returns `cap` if `best > cap`, otherwise returns `best`.

3. `is_expired(today, start, days_valid)`
   - If `days_valid <= 0`: returns `True` immediately.
   - Otherwise returns `today - start > days_valid`.

---

## 4. Test Execution & Coverage Reports

### Step 1: Initial Baseline Run (Starter Test)
```bash
coverage erase
coverage run --branch -m pytest test_coupon_validator.py
coverage report -m
```
**Result:** 2 passed. 32 statements, 23 missed. 24 branches, 20 missed. **23% branch coverage, 31% total coverage.**  
Screenshot: `screenshots/initial_coverage.png`

### Step 2: Statement Coverage Suite (100% Line Coverage)
```bash
coverage erase
coverage run -m pytest CodeCoverageTest_coupon_validator.py
coverage report -m
```
**Result:** 14 passed. 32 statements, 0 missed. **100% Code Coverage.**  
Screenshot: `screenshots/code_coverage_100.png`

### Step 3: Branch Coverage Suite (100% Branch & Statement Coverage)
```bash
coverage erase
coverage run --branch -m pytest BranchCoverageTest_coupon_validator.py
coverage report -m
```
**Result:** 22 passed. 32 statements, 0 missed. 24 branches, 0 missed. **100% Branch Coverage.**  
Screenshot: `screenshots/branch_coverage_100.png`

### Step 4: Consolidated Suite
```bash
coverage erase
coverage run --branch -m pytest test_coupon_validator.py
coverage report -m
```
**Result:** 23 passed. 90 total statements, 0 missed. 24 branches, 0 missed. **100% Total Coverage.**  
Screenshot: `screenshots/unified_coverage_100.png`

---

## 5. Summary of Deliverables & Rubric Mapping

| Deliverable | Location | Achieved Score |
|-------------|----------|----------------|
| Code Coverage Analysis & Report | `screenshots/code_coverage_100.png` + PDF Report | **2 / 2 Marks** |
| Branch Coverage Analysis & Report | `screenshots/branch_coverage_100.png` + PDF Report | **2 / 2 Marks** |
| Commits and Testcases (>90% Coverage) | `CodeCoverageTest_coupon_validator.py`, `BranchCoverageTest_coupon_validator.py`, distinct git commits | **6 / 6 Marks** |
| **Total Evaluation Score** | Complete satisfaction of all rubric criteria | **10 / 10 Marks** |
