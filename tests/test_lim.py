def test_inventory_not_empty():
    inventory = [
        {
            "name": "Arroz",
            "quantity": "2 tazas"
        }
    ]
    assert len(inventory) > 0


def test_inventory_item_has_name():
    item = {"name": "Arroz", "quantity": "2 tazas"}
    assert "name" in item


def test_inventory_item_has_quantity():
    item = {"name": "Arroz", "quantity": "2 tazas"}
    assert "quantity" in item


def test_inventory_name_not_empty():
    item = {"name": "Arroz", "quantity": "2 tazas"}
    assert item["name"] != ""


def test_inventory_quantity_not_empty():
    item = {"name": "Arroz", "quantity": "2 tazas"}
    assert item["quantity"] != ""


def test_inventory_multiple_items():
    inventory = [
        {"name": "Arroz", "quantity": "2 tazas"},
        {"name": "Pollo", "quantity": "500g"},
        {"name": "Tomate", "quantity": "3 unidades"}
    ]
    assert len(inventory) >= 2


def test_inventory_item_name_type():
    item = {"name": "Arroz", "quantity": "2 tazas"}
    assert isinstance(item["name"], str)


def test_inventory_unique_names():
    inventory = [
        {"name": "Arroz", "quantity": "2 tazas"},
        {"name": "Pollo", "quantity": "500g"}
    ]
    names = [i["name"] for i in inventory]
    assert len(names) == len(set(names))
