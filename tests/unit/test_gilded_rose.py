# -*- coding: utf-8 -*-

import pytest

from gilded_rose import Item, GildedRose


def test_update_quality_always_lowers_sell_in_and_quality_values_for_every_item():
    initial_sell_in = 1
    initial_quality = 2
    items = [
        Item("Some item", sell_in=initial_sell_in, quality=initial_quality),
    ]
    expected_sell_in_after_update_quality = initial_sell_in - 1
    normal_quality_degradation_factor = 1
    expected_quality_after_update_quality = initial_quality - normal_quality_degradation_factor
    gilded_rose = GildedRose(items)

    gilded_rose.update_quality()

    assert items[0].name == "Some item"
    assert items[0].sell_in == expected_sell_in_after_update_quality
    assert items[0].quality == expected_quality_after_update_quality


@pytest.mark.parametrize("_scenario, initial_sell_in, initial_quality", [
    ("sell by date passed yesterday", 0, 2),
    ("sell by date passed eleven days ago", -10, 8),
])
def test_update_quality_once_sell_by_date_has_passed_quality_degrades_twice_as_fast(
        _scenario,
        initial_sell_in,
        initial_quality):
    items = [
        Item("Item sell by date which passed", sell_in=initial_sell_in, quality=initial_quality),
    ]
    expected_sell_in_after_update_quality = initial_sell_in - 1
    double_quality_degradation_factor = 2
    expected_quality_after_update_quality = initial_quality - double_quality_degradation_factor
    gilded_rose = GildedRose(items)

    gilded_rose.update_quality()

    assert items[0].name == "Item sell by date which passed"
    assert items[0].sell_in == expected_sell_in_after_update_quality
    assert items[0].quality == expected_quality_after_update_quality


def test_update_quality_should_not_change_quality_when_quality_is_zero():
    initial_sell_in = 10
    initial_quality = 0
    minimum_quality = 0
    items = [
        Item("Item with zero quality", sell_in=initial_sell_in, quality=initial_quality),
    ]
    expected_sell_in_after_update_quality = initial_sell_in - 1
    gilded_rose = GildedRose(items)

    gilded_rose.update_quality()

    assert items[0].name == "Item with zero quality"
    assert items[0].sell_in == expected_sell_in_after_update_quality
    assert items[0].quality == minimum_quality


normal_quality_increase_factor = 1


@pytest.mark.parametrize("_scenario, initial_sell_in, initial_quality, expected_quality_after_update_quality", [
    ("initial quality is below 50", 10, 1, 1 + normal_quality_increase_factor),
    ("initial quality is below 50 and sell by date expired", -1, 12, 12 + normal_quality_increase_factor*2),# is it a bug?
    ("initial quality is 50", 12, 50, 50),
])
def test_update_quality_should_increase_quality_when_item_is_aged_brie(
        _scenario, initial_sell_in, initial_quality, expected_quality_after_update_quality
):
    items = [
        Item("Aged Brie", sell_in=initial_sell_in, quality=initial_quality),
    ]
    expected_sell_in_after_update_quality = initial_sell_in - 1
    gilded_rose = GildedRose(items)

    gilded_rose.update_quality()

    assert items[0].name == "Aged Brie"
    assert items[0].sell_in == expected_sell_in_after_update_quality
    assert items[0].quality == expected_quality_after_update_quality


def test_update_quality_never_changes_the_legendary_sulfuras_item():
    initial_sell_in = 0
    initial_quality = 80
    items = [
        Item("Sulfuras, Hand of Ragnaros", sell_in=initial_sell_in, quality=initial_quality),
    ]
    gilded_rose = GildedRose(items)

    gilded_rose.update_quality()

    assert items[0].name == "Sulfuras, Hand of Ragnaros"
    assert items[0].sell_in == initial_sell_in
    assert items[0].quality == initial_quality


normal_quality_increase_factor_for_backstage_passes = 2
increased_quality_increase_factor_for_backstage_passes = 3


@pytest.mark.parametrize(
    "_scenario, initial_sell_in, initial_quality, expected_quality_after_update_quality", [
        ("more than 10 days to the concert", 12, 20, 20 + normal_quality_increase_factor),
        ("10 days to the concert", 10, 33, 33 + normal_quality_increase_factor_for_backstage_passes),
        ("less than 10 days and more than 5 days to the concert", 7, 47,
         47 + normal_quality_increase_factor_for_backstage_passes),
        ("5 days to the concert", 5, 37,
         37 + increased_quality_increase_factor_for_backstage_passes),
        ("less than 5 days and more than 0 days to the concert", 3, 3,
         3 + increased_quality_increase_factor_for_backstage_passes),
        ("quality drops to zero after the concert", 0, 10, 0),
        ("quality cannot be bigger than 50 - 10 day to the concert", 10, 49, 50),
        ("quality cannot be bigger than 50 - less than 10 days to the concert", 7, 49, 50),
        ("quality cannot be bigger than 50 - 5 days to the concert", 5, 49, 50),
        ("quality cannot be bigger than 50 - less than 5 days to the concert", 3, 49, 50),
    ])
def test_update_quality_should_increases_quality_as_sell_in_value_approaches_for_backstage_passes(
        _scenario, initial_sell_in, initial_quality, expected_quality_after_update_quality
):
    items = [
        Item("Backstage passes to a TAFKAL80ETC concert",
             sell_in=initial_sell_in,
             quality=initial_quality),
    ]
    expected_sell_in_after_update_quality = initial_sell_in - 1
    gilded_rose = GildedRose(items)

    gilded_rose.update_quality()

    assert items[0].name == "Backstage passes to a TAFKAL80ETC concert"
    assert items[0].sell_in == expected_sell_in_after_update_quality
    assert items[0].quality == expected_quality_after_update_quality
