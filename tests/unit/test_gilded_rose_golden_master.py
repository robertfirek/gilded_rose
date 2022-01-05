# -*- coding: utf-8 -*-
import pickle

import pytest

from gilded_rose import GildedRose, Item


def __hash__(self):
    return hash((self.name, self.sell_in, self.quality))


def __eq__(self, other):
    try:
        return (self.name, self.sell_in, self.quality) == (other.name, other.sell_in, other.quality)
    except AttributeError:
        return NotImplemented


Item.__hash__ = __hash__
Item.__eq__ = __eq__


@pytest.mark.parametrize("sample_number", [sample_number for sample_number in range(2000)])
def test_gilded_rose_should_update_items(sample_number):
    items_file = open(
        f"tests/unit/golden_master_samples/input_items_{sample_number:04d}.pkl", "rb")
    items_after_update_file = open(
        f"tests/unit/golden_master_samples/expected_items_{sample_number:04d}.pkl", "rb")
    items = pickle.load(items_file)
    expected_items_after_update = pickle.load(items_after_update_file)
    print("\nInput:")
    print(items)

    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    print("\nOutput:")
    print(items)
    print("\nExpected output:")
    print(items)

    assert items == expected_items_after_update
