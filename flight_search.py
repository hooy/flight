import os
import json


class Infinity:
    def __lt__(self, other):
        return False

    def __gt__(self, other):
        return True


def parse_routes(json_data):
    return [(edge["from"], edge["to"]) for edge in json_data]


class fare(object):
    """struct representing fare"""

    def __init__(self, **xargs):
        self.fid = xargs["fid"]
        self.price = xargs["price"]
        self.routes = parse_routes(xargs["routes"])

    def __repr__(self):
        return "Fare({})".format(self.fid, self.price, self.routes)


def parse_fares(json_fares):
    return [fare(**f) for f in json_fares]


def find_optimal_combination(current_itinerary, fares_left, price):
    fl = fares_left[:]
    print(price, current_itinerary, fares_left)

    if current_itinerary:
        if fares_left:
            fare_to_take = fl.pop()

            if set(fare_to_take.routes).issubset(current_itinerary):
                return min(
                    # take this fare
                    find_optimal_combination(
                        current_itinerary - set(fare_to_take.routes),
                        fl,
                        price + fare_to_take.price,
                    ),
                    # dont take this fare
                    find_optimal_combination(current_itinerary, fl, price),
                    key=lambda x: x[0],
                )
            else:  # fare is too "big", skip it
                return find_optimal_combination(current_itinerary, fl, price)

        else:  # there is still route, but no fare left
            return (Infinity(), fares_left)
    else:
        return (price, fares_left)


def main():
    with open(os.environ["DATA_FILE"], "r") as f:
        data = json.loads(f.read())

    itinerary = set(parse_routes(data["itinerary"]))
    fares = parse_fares(data["fares"])

    # filter fares with extra flights
    fares = list(filter(lambda x: not (set(x.routes) - itinerary), fares))
    optimal_price, fares_left = find_optimal_combination(itinerary, fares, 0)

    optimal_fares = [fare.fid for fare in set(fares) - set(fares_left)]
    with open(os.environ["RESULT_FILE"], 'w') as f:
        f.write(json.dumps(optimal_fares))


if __name__ == "__main__":
    main()
