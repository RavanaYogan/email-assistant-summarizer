from email_assistant.utils.masking import mask_secret


def test_mask_secret_keeps_last_chars() -> None:
    assert mask_secret("supersecretkey", visible_chars=4) == "**********tkey"


def test_mask_secret_short_value_fully_masked() -> None:
    assert mask_secret("abc", visible_chars=4) == "***"


def test_mask_secret_empty_value() -> None:
    assert mask_secret("", visible_chars=4) == ""
