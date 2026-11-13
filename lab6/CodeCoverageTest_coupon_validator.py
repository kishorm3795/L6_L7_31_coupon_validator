import pytest
from coupon_validator import coupon_discount, best_discount, is_expired


class TestCouponValidatorCodeCoverage:
    """
    Test suite specifically targeting 100% statement (line) coverage
    for coupon_validator.py as required by Lab 6 Step 5.
    """

    def test_cart_total_zero_or_negative_raises_value_error(self):
        # Covers Line 2-3: Cart total validation
        with pytest.raises(ValueError, match="empty cart"):
            coupon_discount("WELCOME10", 0, True, "mon")
        with pytest.raises(ValueError, match="empty cart"):
            coupon_discount("WELCOME10", -10, True, "mon")

    def test_welcome10_new_user(self):
        # Covers Lines 4-6: WELCOME10 coupon for new user
        assert coupon_discount("WELCOME10", 200, True, "mon") == 20.0

    def test_welcome10_existing_user(self):
        # Covers Line 7: WELCOME10 coupon for returning user
        assert coupon_discount("WELCOME10", 200, False, "mon") == 0

    def test_weekend20_weekend_high_cart(self):
        # Covers Lines 8-11: WEEKEND20 on weekend with cart >= 500
        assert coupon_discount("WEEKEND20", 600, False, "sat") == 120.0

    def test_weekend20_weekend_low_cart(self):
        # Covers Line 12: WEEKEND20 on weekend with cart < 500
        assert coupon_discount("WEEKEND20", 400, False, "sun") == 50

    def test_weekend20_weekday(self):
        # Covers Line 13: WEEKEND20 on a weekday
        assert coupon_discount("WEEKEND20", 600, False, "wed") == 0

    def test_flat100_valid(self):
        # Covers Lines 14-16: FLAT100 with cart > 300
        assert coupon_discount("FLAT100", 500, False, "mon") == 100

    def test_flat100_below_threshold(self):
        # Covers Line 17: FLAT100 with cart <= 300
        assert coupon_discount("FLAT100", 250, False, "mon") == 0

    def test_unknown_coupon(self):
        # Covers Line 18: Fallthrough default return for unrecognized coupon
        assert coupon_discount("DISCOUNT99", 500, True, "sat") == 0

    def test_best_discount_cap_exceeded(self):
        # Covers Lines 21-29: best > cap branch
        # Cart total 100 on saturday gives 50 discount; cap is 100 * 0.4 = 40.
        codes = ["WEEKEND20"]
        assert best_discount(codes, 100, False, "sat") == 40.0

    def test_best_discount_within_cap(self):
        # Covers Line 30: best <= cap branch
        codes = ["WELCOME10"]
        assert best_discount(codes, 200, True, "mon") == 20.0

    def test_is_expired_zero_or_negative_validity(self):
        # Covers Lines 34-35: days_valid <= 0
        assert is_expired(10, 5, 0) is True
        assert is_expired(10, 5, -1) is True

    def test_is_expired_positive_validity_expired(self):
        # Covers Line 36: returns True when today - start > days_valid
        assert is_expired(20, 5, 10) is True

    def test_is_expired_positive_validity_active(self):
        # Covers Line 36: returns False when today - start <= days_valid
        assert is_expired(12, 5, 10) is False
