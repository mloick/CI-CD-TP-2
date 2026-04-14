from src.validators import is_valid_email, is_valid_password, is_valid_age

class TestValidators:
    # isValidEmail tests
    def test_is_valid_email_examples(self):
        assert is_valid_email("user@example.com") is True
        assert is_valid_email("user.name+tag@domain.co") is True
        assert is_valid_email("invalid") is False
        assert is_valid_email("@domain.com") is False
        assert is_valid_email("user@") is False
        assert is_valid_email("") is False
        assert is_valid_email(None) is False

    # isValidPassword tests
    def test_is_valid_password_examples(self):
        res = is_valid_password("Passw0rd!")
        assert res["valid"] is True
        assert len(res["errors"]) == 0

        res = is_valid_password("short")
        assert res["valid"] is False
        assert "too_short" in res["errors"]
        assert "missing_uppercase" in res["errors"]
        assert "missing_digit" in res["errors"]
        assert "missing_special" in res["errors"]

        res = is_valid_password("alllowercase1!")
        assert res["valid"] is False
        assert "missing_uppercase" in res["errors"]

        res = is_valid_password("ALLUPPERCASE1!")
        assert res["valid"] is False
        assert "missing_lowercase" in res["errors"]

        res = is_valid_password("NoDigits!here")
        assert res["valid"] is False
        assert "missing_digit" in res["errors"]

        res = is_valid_password("NoSpecial1here")
        assert res["valid"] is False
        assert "missing_special" in res["errors"]

        res = is_valid_password("")
        assert res["valid"] is False
        assert len(res["errors"]) > 0

        res = is_valid_password(None)
        assert res["valid"] is False
        assert "invalid_type" in res["errors"]

    # isValidAge tests
    def test_is_valid_age_examples(self):
        assert is_valid_age(25) is True
        assert is_valid_age(0) is True
        assert is_valid_age(150) is True
        assert is_valid_age(-1) is False
        assert is_valid_age(151) is False
        assert is_valid_age(25.5) is False
        assert is_valid_age("25") is False
        assert is_valid_age(None) is False
