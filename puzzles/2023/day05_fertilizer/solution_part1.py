import dataclasses
import re
from collections import namedtuple
from typing import List, Optional

MapRange = namedtuple("MapRange", ["dest", "source", "range"])


@dataclasses.dataclass
class MapRange:
    dest: int
    source: int
    range: int

    def dest_for_source(self, val: int) -> Optional[int]:
        if self.source <= val <= self.source + self.range:
            inc = val - self.source
            return self.dest + inc
        else:
            return None


class Ranges:

    def __init__(self):
        super().__init__()
        self.ranges: List[MapRange] = []

    def add(self, m: MapRange) -> None:
        self.ranges.append(m)

    def dest_for_source(self, val: int) -> int:
        for r in self.ranges:
            if r.dest_for_source(val):
                return r.dest_for_source(val)
        return val


def main():
    with open("input.txt") as f:
        seeds = []
        seed_to_soil = Ranges()
        soil_to_fertilizer = Ranges()
        fertilizer_to_water = Ranges()
        water_to_light = Ranges()
        light_to_temp = Ranges()
        temp_to_humidity = Ranges()
        humidity_to_loc = Ranges()

        d_of_d = {
            "seed-to-soil": seed_to_soil,
            "soil-to-fertilizer": soil_to_fertilizer,
            "fertilizer-to-water": fertilizer_to_water,
            "water-to-light": water_to_light,
            "light-to-temperature": light_to_temp,
            "temperature-to-humidity": temp_to_humidity,
            "humidity-to-location": humidity_to_loc
        }
        section = None
        for line in f.readlines():
            trimmed = line.strip()
            if trimmed.startswith("seeds:"):
                # First line, get all the seeds
                seeds = [int(s) for s in trimmed.split(":")[1].strip().split(" ")]
            elif trimmed == "":
                # Newline between sections, reset section
                section = None
            else:
                # We are either processing the map declaration (i.e. "seed-to-soil map:")
                # or it is one of the range lines.
                # For the declaration, parse the type and store that as the section value.
                # For range lines, parse and add to the current dictionary.
                if not section:
                    m = re.match("(\\w+-to-\\w+) map:", trimmed)
                    section = m.group(1)
                else:
                    populate_dict_from_line(trimmed, d_of_d[section])

        locations = []
        for seed in seeds:
            soil = seed_to_soil.dest_for_source(seed)
            fertilizer = soil_to_fertilizer.dest_for_source(soil)
            water = fertilizer_to_water.dest_for_source(fertilizer)
            light = water_to_light.dest_for_source(water)
            temp = light_to_temp.dest_for_source(light)
            humidity = temp_to_humidity.dest_for_source(temp)
            locations.append(humidity_to_loc.dest_for_source(humidity))
            # soil = seed_to_soil.get(seed, seed)
            # fertilizer = soil_to_fertilizer.get(soil, soil)
            # water = fertilizer_to_water.get(fertilizer, fertilizer)
            # light = water_to_light.get(water, water)
            # temp = light_to_temp.get(light, light)
            # humidity = temp_to_humidity.get(temp, temp)
            # locations.append(humidity_to_loc.get(humidity, humidity))
        print(min(locations))


def populate_dict_from_line(trimmed: str, d: Ranges) -> None:
    nums = [int(n) for n in trimmed.split(" ")]
    m = MapRange(nums[0], nums[1], nums[2])
    d.add(m)


if __name__ == '__main__':
    main()
