def test_ingredient_name():
    ingredient = "Tomate"
    assert ingredient != ""


def test_quantity():
    quantity = "2"
    assert quantity != ""


def test_user_id():
    user_id = 1
    assert user_id > 0


def test_ingredient_name_min_length():
    ingredient = "Sal"
    assert len(ingredient) >= 2


def test_ingredient_name_no_numbers():
    ingredient = "Tomate"
    assert not ingredient.isdigit()


def test_quantity_not_negative():
    quantity = 2
    assert quantity >= 0


def test_ingredient_name_stripped():
    ingredient = "  Tomate  ".strip()
    assert ingredient == "Tomate"


def test_multiple_ingredients():
    ingredients = ["Tomate", "Cebolla", "Ajo"]
    assert len(ingredients) >= 2
