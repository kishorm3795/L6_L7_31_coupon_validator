import pytest
from coupon_validator import coupon_discount, best_discount, is_expired


class TestCouponValidatorBranchCoverage:
    """
    Test suite targeting 100% Branch Coverage and 100% Statement Coverage
    for coupon_validator.py as required by Lab 6 Step 7.
    Covers every decision branch (True/False) and boundary condition.
    """

    # -------------------------------------------------------------------------
    # Branch 1: cart_total <= 0
    # -------------------------------------------------------------------------
    def test_branch_cart_total_zero_raises(self):
        # True branch: cart_total == 0
        with pytest.raises(ValueError, match="empty cart"):
            coupon_discount("WELCOME10", 0, True, "mon")

    def test_branch_cart_total_negative_raises(self):
        # True branch: cart_total < 0
        with pytest.raises(ValueError, match="empty cart"):
            coupon_discount("WELCOME10", -15.5, True, "mon")

    # -------------------------------------------------------------------------
    # Branch 2 & 3: code == "WELCOME10" and is_new_user
    # -------------------------------------------------------------------------
    def test_branch_welcome10_new_user(self):
        # code == "WELCOME10" (True), is_new_user (True)
        assert coupon_discount("WELCOME10", 250, True, "tue") == 25.0

    def test_branch_welcome10_existing_user(self):
        # code == "WELCOME10" (True), is_new_user (False)
        assert coupon_discount("WELCOME10", 250, False, "tue") == 0

    # -------------------------------------------------------------------------
    # Branch 4, 5, 6: code == "WEEKEND20", day in ("sat", "sun"), cart_total >= 500
    # -------------------------------------------------------------------------
    def test_branch_weekend20_saturday_cart_above_threshold(self):
        # code == "WEEKEND20" (True), day == "sat" (True), cart_total >= 500 (True)
        assert coupon_discount("WEEKEND20", 600, False, "sat") == 120.0

    def test_branch_weekend20_saturday_cart_exact_boundary_500(self):
        # cart_total == 500 (True branch boundary for cart_total >= 500)
        assert coupon_discount("WEEKEND20", 500, False, "sat") == 100.0

    def test_branch_weekend20_sunday_cart_below_threshold(self):
        # code == "WEEKEND20" (True), day == "sun" (True), cart_total >= 500 (False)
        assert coupon_discount("WEEKEND20", 499, False, "sun") == 50

    def test_branch_weekend20_weekday_ineligible(self):
        # code == "WEEKEND20" (True), day in ("sat", "sun") (False)
        assert coupon_discount("WEEKEND20", 800, False, "fri") == 0

    # -------------------------------------------------------------------------
    # Branch 7 & 8: code == "FLAT100" and cart_total > 300
    # -------------------------------------------------------------------------
    def test_branch_flat100_above_threshold(self):
        # code == "FLAT100" (True), cart_total > 300 (True)
        assert coupon_discount("FLAT100", 301, False, "wed") == 100

    def test_branch_flat100_exact_threshold_300(self):
        # code == "FLAT100" (True), cart_total > 300 (False: cart_total == 300)
        assert coupon_discount("FLAT100", 300, False, "wed") == 0

    def test_branch_flat100_below_threshold(self):
        # code == "FLAT100" (True), cart_total > 300 (False: cart_total < 300)
        assert coupon_discount("FLAT100", 150, False, "wed") == 0

    # -------------------------------------------------------------------------
    # Branch 9: Fallthrough default return for unrecognized code
    # -------------------------------------------------------------------------
    def test_branch_unrecognized_coupon_code(self):
        # All if checks evaluate to False
        assert coupon_discount("SUMMERSALE", 1000, True, "sat") == 0

    # -------------------------------------------------------------------------
    # Branch 10, 11, 12: best_discount loop, value > best, and best > cap
    # -------------------------------------------------------------------------
    def test_branch_best_discount_empty_codes_list(self):
        # Loop for code in codes executes 0 times (skips loop body)
        assert best_discount([], 500, True, "sat") == 0

    def test_branch_best_discount_value_less_than_or_equal_best(self):
        # Branch 25->23: tests value <= best so best does NOT update
        # First coupon gives 100, second coupon gives 0 -> 0 <= 100
        codes = ["FLAT100", "UNKNOWN_CODE"]
        # cart 500: FLAT100 gives 100. UNKNOWN gives 0. Cap is 500 * 0.4 = 200.
        # 100 <= 200, returns best = 100
        assert best_discount(codes, 500, False, "mon") == 100

    def test_branch_best_discount_multiple_codes_increasing(self):
        # Multiple codes where value > best triggers update
        # WELCOME10 gives 50, FLAT100 gives 100. Cap = 200.
        codes = ["WELCOME10", "FLAT100"]
        assert best_discount(codes, 500, True, "mon") == 100

    def test_branch_best_discount_capped(self):
        # best > cap branch evaluates to True
        # Cart total 100 on weekend gives 50 discount; cap is 100 * 0.4 = 40.
        # 50 > 40 -> returns cap 40.0
        codes = ["WEEKEND20"]
        assert best_discount(codes, 100, False, "sat") == 40.0

    def test_branch_best_discount_exact_cap_boundary(self):
        # best == cap boundary (best > cap evaluates to False)
        # Cart total 250, FLAT100 gives 0. WELCOME10 gives 25. Cap = 250 * 0.4 = 100.
        # To get exact cap: cart 250, cap = 100. FLAT100 on cart 500 gives 100, cap is 200.
        # What if cart 250 with WEEKEND20 on sat < 500? gives 50. Cap is 250 * 0.4 = 100.
        # What gives best == cap? Cart = 250, discount = 100? FLAT100 needs > 300.
        # If cart = 125, WEEKEND20 gives 50. Cap = 125 * 0.4 = 50.0!
        # best = 50, cap = 50.0. best > cap is False! Returns best = 50
        codes = ["WEEKEND20"]
        assert best_discount(codes, 125, False, "sat") == 50.0

    # -------------------------------------------------------------------------
    # Branch 13 & 14: is_expired days_valid <= 0 and today - start > days_valid
    # -------------------------------------------------------------------------
    def test_branch_is_expired_days_valid_zero(self):
        # days_valid == 0 (True branch boundary)
        assert is_expired(today=10, start=5, days_valid=0) is True

    def test_branch_is_expired_days_valid_negative(self):
        # days_valid < 0 (True branch)
        assert is_expired(today=10, start=5, days_valid=-5) is True

    def test_branch_is_expired_strictly_expired(self):
        # days_valid > 0, today - start > days_valid evaluates to True
        assert is_expired(today=25, start=10, days_valid=10) is True

    def test_branch_is_expired_exact_validity_boundary(self):
        # days_valid > 0, today - start == days_valid (evaluates to False)
        assert is_expired(today=20, start=10, days_valid=10) is False

    def test_branch_is_expired_well_within_validity(self):
        # days_valid > 0, today - start < days_valid (evaluates to False)
        assert is_expired(today=12, start=10, days_valid=10) is False
