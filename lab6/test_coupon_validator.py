import pytest
from coupon_validator import coupon_discount, best_discount, is_expired

# =============================================================================
# Lab 6: Comprehensive Test Suite for Coupon Validator
# Achieves 100% Statement Coverage and 100% Branch Coverage
# =============================================================================

# Starter test cases
def test_welcome_coupon_new_user():
    assert coupon_discount("WELCOME10", 200, True, "mon") == 20

def test_zero_validity_expired():
    assert is_expired(10, 5, 0) is True


# =============================================================================
# Additional Test Cases for Full Statement & Branch Coverage
# =============================================================================

class TestCouponDiscount:
    def test_cart_total_zero_raises_value_error(self):
        with pytest.raises(ValueError, match="empty cart"):
            coupon_discount("WELCOME10", 0, True, "mon")

    def test_cart_total_negative_raises_value_error(self):
        with pytest.raises(ValueError, match="empty cart"):
            coupon_discount("WELCOME10", -10, True, "mon")

    def test_welcome_coupon_existing_user(self):
        assert coupon_discount("WELCOME10", 200, False, "mon") == 0

    def test_weekend_coupon_saturday_high_cart(self):
        assert coupon_discount("WEEKEND20", 600, False, "sat") == 120.0

    def test_weekend_coupon_saturday_exact_500(self):
        assert coupon_discount("WEEKEND20", 500, False, "sat") == 100.0

    def test_weekend_coupon_sunday_low_cart(self):
        assert coupon_discount("WEEKEND20", 400, False, "sun") == 50

    def test_weekend_coupon_weekday(self):
        assert coupon_discount("WEEKEND20", 600, False, "fri") == 0

    def test_flat100_coupon_valid(self):
        assert coupon_discount("FLAT100", 500, False, "mon") == 100

    def test_flat100_coupon_exact_boundary_300(self):
        assert coupon_discount("FLAT100", 300, False, "mon") == 0

    def test_flat100_coupon_below_threshold(self):
        assert coupon_discount("FLAT100", 250, False, "mon") == 0

    def test_unknown_coupon(self):
        assert coupon_discount("INVALID99", 500, True, "sat") == 0


class TestBestDiscount:
    def test_best_discount_empty_codes(self):
        assert best_discount([], 500, True, "sat") == 0

    def test_best_discount_capped(self):
        # Cart 100 on weekend gives 50 discount; cap is 100 * 0.4 = 40.
        codes = ["WEEKEND20"]
        assert best_discount(codes, 100, False, "sat") == 40.0

    def test_best_discount_exact_cap(self):
        # Cart 125, discount 50; cap is 125 * 0.4 = 50.0.
        codes = ["WEEKEND20"]
        assert best_discount(codes, 125, False, "sat") == 50.0

    def test_best_discount_uncapped(self):
        codes = ["WELCOME10"]
        assert best_discount(codes, 200, True, "mon") == 20.0

    def test_best_discount_multiple_codes_first_better(self):
        codes = ["FLAT100", "UNKNOWN"]
        assert best_discount(codes, 500, False, "mon") == 100

    def test_best_discount_multiple_codes_second_better(self):
        codes = ["WELCOME10", "FLAT100"]
        assert best_discount(codes, 500, True, "mon") == 100


class TestIsExpired:
    def test_expired_negative_validity(self):
        assert is_expired(10, 5, -3) is True

    def test_expired_strictly_after_validity(self):
        assert is_expired(25, 10, 10) is True

    def test_not_expired_exact_validity_boundary(self):
        assert is_expired(20, 10, 10) is False

    def test_not_expired_well_within_validity(self):
        assert is_expired(12, 10, 10) is False
