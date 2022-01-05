import pickle
import random
import uuid

from gilded_rose import Item, GildedRose


def produce_samples():
    for sample_number in range(1000):
        name = uuid.uuid4().hex
        sell_in = random.randint(-50, 50)
        quality = random.randint(0, 50)
        available_items = [
            Item(name, sell_in=sell_in, quality=quality),
            Item("Aged Brie", sell_in=sell_in, quality=quality),
            Item("Backstage passes to a TAFKAL80ETC concert", sell_in=sell_in, quality=quality),
            Item("Sulfuras, Hand of Ragnaros", sell_in=random.randint(-50, 0), quality=80),
        ]

        items = random.choices(available_items, weights=[10, 1, 1, 1], k=random.randint(1, 15))

        input_file = open(f"golden_master_samples/input_{sample_number:04d}.pkl", "wb")
        pickle.dump(items, input_file)

        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        result_file = open(f"golden_master_samples/output_{sample_number:04d}.pkl", "wb")
        pickle.dump(items, result_file)


if __name__ == '__main__':
    produce_samples()
