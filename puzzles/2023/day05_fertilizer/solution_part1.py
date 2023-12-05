import re
from typing import Dict


def main():
    with open("sample_input.txt") as f:
        seeds = []
        seed_to_soil = {}
        soil_to_fertilizer = {}
        fertilizer_to_water = {}
        water_to_light = {}
        light_to_temp = {}
        temp_to_humidity = {}
        humidity_to_loc = {}

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
                seeds = [int(s) for s in trimmed.split(":")[1].strip().split(" ")]
            elif trimmed == "":
                section = None
            else:
                if not section:
                    m = re.match("(\\w+-to-\\w+) map:", trimmed)
                    section = m.group(1)
                else:
                    populate_dict_from_line(trimmed, d_of_d[section])

        locations = []
        for seed in seeds:
            soil = seed_to_soil.get(seed, seed)
            fertilizer = soil_to_fertilizer.get(soil, soil)
            water = fertilizer_to_water.get(fertilizer, fertilizer)
            light = water_to_light.get(water, water)
            temp = light_to_temp.get(light, light)
            humidity = temp_to_humidity.get(temp, temp)
            locations.append(humidity_to_loc.get(humidity, humidity))
        print(min(locations))


def populate_dict_from_line(trimmed: str, d: Dict) -> None:
    nums = [int(n) for n in trimmed.split(" ")]
    for i in range(0, nums[2]):
        d[nums[1] + i] = nums[0] + i


if __name__ == '__main__':
    main()
