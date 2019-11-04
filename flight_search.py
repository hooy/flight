import os
import json
import time

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

def find_optimal_combination_kruskal(path, fares):
    tree_set = {}

def find_optimal_combination_iterative(path, fares):
    minimal_route = (None, Infinity())

    for f1 in fares:
        current_path, current_price, current_fares = set(f1.routes), f1.price, {f1}
        other_fares = fares.copy()
        other_fares.remove(f1)
        for f2 in other_fares:
            routes = set(f2.routes)
            if (routes.intersection(current_path)):  # cannot take fare, contains edge we already took
                pass
            else:
                current_path = current_path.union(routes)
                current_price += f2.price
                current_fares.update({f2})
                if not(path - current_path): # finished route
                    break
        if not(path - current_path) and current_price < minimal_route[1]:
            minimal_route = (current_fares, current_price)

    return minimal_route


def find_optimal_combination(path, fares):

    def fare_taker(current_path, available_fares, fares_taken, price):
        global current_optimal
        # print(current_path, available_fares, fares_taken, price)
        # time.sleep(1)
        if (path - current_path):  # itineary is not finished
            fl = set(available_fares - fares_taken)  # fares left
            if fl:
                fare_to_take = fl.pop()
                if (set(fare_to_take.routes).intersection(current_path)): # cannot take fare, contains edge we already took
                    return fare_taker(current_path, fl, fares_taken, price)
                else:  # can take fare
                    return min(
                        fare_taker( # take
                            current_path.union(set(fare_to_take.routes)),
                            fl,
                            fares_taken.union({fare_to_take}),
                            price + fare_to_take.price
                        ),
                        fare_taker(current_path, fl, fares_taken, price),  # do not take
                        key=lambda x: x[1]
                    )

            else:  # there are no fares left but path is unfinished
                return (fares_taken, Infinity())
        else:
            return (fares_taken, price)

    # print(path, fares)
    return fare_taker(current_path=set(), available_fares=fares, fares_taken=set(), price=0)

def main():
    with open(os.environ["DATA_FILE"], "r") as f:
        data = json.loads(f.read())

    itinerary = set(parse_routes(data["itinerary"]))
    fares = set(parse_fares(data["fares"]))

    # filter fares with extra flights
    fares = set(filter(lambda x: not (set(x.routes) - itinerary), fares))
    # fares_taken, price = find_optimal_combination(itinerary, fares)
    fares_taken, price = find_optimal_combination_iterative(itinerary, fares)

    answer = [fare.fid for fare in fares_taken]
    # print(answer)
    with open(os.environ["RESULT_FILE"], 'w') as f:
        f.write(json.dumps(answer))


if __name__ == "__main__":
    main()
