from typing import List, Dict, Set
import json

from postcode_lookup import get_postcodes_data, get_nearest_postcodes

# Path to the JSON file with stores
STORES_PAH = 'data/stores.json'


def get_stores() -> List[Dict]:
    """
    Reads the JSON file with stores and returns the list of dictionaries with th store data.
    :return: list of dictionaries with th store data
    """
    with open(STORES_PAH, 'r') as file:
        data = json.load(file)
        return data


def add_coords_to_stores(stores: List[Dict]) -> List[Dict]:
    """
    Adds location data (coordinates in the form of longitude and latitude float fields) to the each store dictionary.
    :param stores: lost of stores to find and add coordinates for
    :return: extended list of stores with the location data (longitude and latitude float fields).
    If the location can't be found the fieldsa are added as None
    """
    postcodes: List[str] = list(set([store['postcode'] for store in stores]))
    postcodes_data: List[Dict] = get_postcodes_data(postcodes)
    ext_stores = extend_dict_list(stores, postcodes_data, 'postcode', ['longitude', 'latitude'])
    return ext_stores


def get_nearby_stores(postcode: str, radius: int, limit: int, widesearch: bool = False) -> List[Dict]:
    """
    Returns the list of stores with the postcodes located in the given radius of the given postcode.
    :param postcode: postcode to get the nearest stores for
    :param radius: radius (in meters!) to get the nearby stores for.
    Should be <= 2000 if widesearch == False or <= 20000 if widesearch = True
    :param limit: the maximal number of nearest postcodes to return the stores in to return
    Should be <= 100 if widesearch == False or <= 100 if widesearch = True
    :param widesearch: True to use the widesearch (> 2km but <= 20km)
    :return: list of the stores with postcodes nearest to the given one (in the given radius)
    """
    all_stores: List[Dict] = get_stores()
    postcodes: Set[str] = set(get_nearest_postcodes(postcode=postcode,
                                                    radius=radius,
                                                    limit=limit,
                                                    widesearch=widesearch))
    result: List[Dict] = [store for store in all_stores if store['postcode'] in postcodes]
    return result


def extend_dict_list(source: List[Dict],
                     ext_list: List[Dict],
                     join_key: str,
                     ext_attrs: List[str]) -> List[Dict]:
    """
    "Left joins" the source list with the ext_list one using the join_key to match the records
    and adds the given attributes from the ext_attrs to the copy of the source list.
    :param source: list to add the extra attributes to the copy of
    :param ext_list: list with extra attributes to join with the source
    :param join_key: name of the dictionary key to join teh two list by the values of
    :param ext_attrs: array of attributes from the ext_list to add to the source one
    :return: copy of the source list with extra attributes from the second one if the matched element found
    (if not None values added)
    """
    ext_map: Dict[str, Dict] = {ext_item[join_key]: ext_item for ext_item in ext_list}
    result: List[Dict] = [item.copy() for item in source]
    for item in result:
        key: str = item[join_key]
        ext_item: Dict = ext_map[key] if key in ext_map else {}
        for ext_attr in ext_attrs:
            item[ext_attr] = ext_item.get(ext_attr)

    return result
