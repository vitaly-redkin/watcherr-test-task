from typing import List, Dict, Set
import tornado.ioloop
import tornado.web

from utils import get_stores, add_coords_to_stores


class Task1Handler(tornado.web.RequestHandler):
    """
    Handler for the first task requests.
    """
    def get(self):
        """
        GET request handler.
        :return: HTML for the stores names, post codes and their coordinates.
        """
        stores: List[Dict] = get_stores()
        stores.sort(key=lambda s: s['name'].upper())
        ext_stores: List[Dict] = add_coords_to_stores(stores)

        self.render("templates/task1.html", stores=ext_stores)


class Task2Handler(tornado.web.RequestHandler):
    """
    Handler for the second task requests.
    """
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')

    def get(self):
        """
        GET request handler.
        Stores first matched by the post code, than by name. Stores sorted alphabetically (by postcode and by name)
        before matching.
        Expects three query parameters:
        q string to search stores by
        starts_with number of the store matching the criteria to start the returned data (zero-based)
        n number of stores to return
        :return: JSON with the stores with matching post codes and names. JSON result has such format:
        {
            portion: [{"name": "name1", "postcode": "postcode1"}],
            total_count: 100
        }

        """
        q: str = get_arg(self, 'q', '').upper()
        start_with: int = int(get_arg(self, 'start_with', '0'))
        n: int = int(get_arg(self, 'n', '3'))

        if q == '' or start_with < 0 or n <= 0:
            result: Dict = {'portion': [], 'total_count': -1}
            self.write(result)
            return

        stores: List[Dict] = get_stores()
        stores_pc: List[Dict] = [store for store in stores]
        stores_n: List[Dict] = [store for store in stores]
        stores_pc.sort(key=lambda s: s['postcode'].upper())
        stores_n.sort(key=lambda s: s['name'].upper())

        by_postcode: List[Dict] = [store for store in stores_pc if q.replace(' ', '') in store['postcode'].upper()]
        by_name: List[Dict] = [store for store in stores_n if q in store['name'].upper()]

        by_post_code_names: Set[str] = set([store['name'] for store in by_postcode])

        found_stores: List[Dict] = by_postcode + [store for store in by_name if store['name'] not in by_post_code_names]
        portion: List[Dict] = found_stores[start_with:start_with + n]
        result: Dict = {'portion': portion, 'total_count': len(found_stores)}

        self.write(result)


def get_arg(req: tornado.web.RequestHandler, name: str, def_value: str = None) -> str:
    """
    Returns web request argument value.
    :param req: web request to get the argument of
    :param name: name of the argument
    :param def_value: default value to use if the argument is absent
    :return: web request argument value (or the default value if absent)
    """
    arg: List[str] = req.get_arguments(name=name, strip=True)
    return arg[0] if len(arg) == 1 else def_value


def make_app():
    return tornado.web.Application([
        (r"/task1", Task1Handler),
        (r"/task2", Task2Handler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
