def test_password_min_length():
    password = "123456"
    assert len(password) >= 6


def test_password_not_empty():
    password = "123456"
    assert password != ""


def test_email_format():
    email = "usuario@example.com"
    assert "@" in email
    assert "." in email
