import pytest

from gilded_rose import Item, GildedRose

conjured_quality_degradation_factor = 2


@pytest.mark.parametrize(
    "_scenario, initial_sell_in, initial_quality, expected_quality_after_update_quality",
    [
        ("sellable conjured item", 10, 10, 10 - conjured_quality_degradation_factor),
        ("non-sellable conjured item", -10, 25, 25 - conjured_quality_degradation_factor),
        ("conjured item about to degrade completely", -10, 1, 0),
        ("degraded conjured", -10, 0, 0),
    ])
def test_conjured_items_should_degrade_twice_fast_as_regular_item(_scenario, initial_sell_in,
                                                                  initial_quality,
                                                                  expected_quality_after_update_quality):
    items = [Item("Conjured item", sell_in=initial_sell_in, quality=initial_quality)]
    expected_sell_in_after_update_quality = initial_sell_in - 1

    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    assert items[0].name == "Conjured item"
    assert items[0].sell_in == expected_sell_in_after_update_quality
    assert items[0].quality == expected_quality_after_update_quality
