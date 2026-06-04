def test_inventory_not_empty():

    inventory = [
        {
            "name": "Arroz",
            "quantity": "2 tazas"
        }
    ]

    assert len(inventory) > 0