from typing import List, Dict, Tuple, Optional
import requests
import json

# postcodes.ui API endpoint URLs
POSTCODES_LOOKUP_URL = 'https://api.postcodes.io/postcodes'
REVERSE_GEOCODING_LOOKUP_URL = 'https://api.postcodes.io/postcodes?lon={lon}&lat={lat}&radius={rad}&limit={lim}&widesearch={wide}'


def get_postcodes_data(postcodes: List[str]) -> List[Dict]:
    """
    Retrieves from the postcodes.io data for the given post codes.
    :param postcodes: array with the postcodes to return the data for. Must include at least TWO postcodes.
    :return: array with the postcode data dictionaries. Each dictionary has numerous fields
    (see "Available Data Fields" in https://postcodes.io/docs for the full list)
    """
    response: requests.Response = requests.post(POSTCODES_LOOKUP_URL, data={'postcodes': postcodes})
    check_response(response)
    resp = json.loads(response.text)
    postcode_data: List[Dict] = [item['result'] for item in resp['result'] if item['result'] is not None]
    return postcode_data


def get_postcode_location(postcode: str) -> Optional[Tuple[float, float]]:
    """
    Gets the location (coordinates as (longitide, latitude tuple)) for the given postcode.
    :param postcode: postcode to get the location for
    :return: coordinates as (longitide, latitude tuple) for the given postcode
    """
    # Hack: https://api.postcodes.io/postcodes requires an array with >=2 postcodes
    postcode_data: List[Dict] = get_postcodes_data([postcode, postcode])
    if len(postcode_data) == 0:
        return None

    return postcode_data[0]['longitude'], postcode_data[0]['latitude']


def get_nearest_postcodes(postcode: str, radius: int, limit: int, widesearch: bool = False) -> List[str]:
    """
    Returns the array of the postcodes located in the given radius near the given one.
    :param postcode: postcode to get the nearest postcodes for
    :param radius: radius (in meters!) to get the nearby postcodes for.
    Should be <= 2000 if widesearch == False or <= 20000 if widesearch = True
    :param limit: the maximal number of nearest postcodes to return.
    Should be <= 100 if widesearch == False or <= 100 if widesearch = True
    :param widesearch: True to use the widesearch (> 2km but <= 20km)
    :return: list of the postcodes nearest to the given one (in the given radius)
    """
    coords: Optional[Tuple[float, float]] = get_postcode_location(postcode)
    if coords is None:
        return []

    url: str = REVERSE_GEOCODING_LOOKUP_URL.format(
        lon=coords[0], lat=coords[1], rad=radius, lim=limit, wide=str(widesearch).lower())
    response: requests.Response = requests.get(url)
    check_response(response)
    resp = json.loads(response.text)
    locations: List[Dict] = resp['result']
    locations.sort(key=lambda loc: -loc['latitude'])
    return [item['postcode'] for item in locations]


def check_response(response: requests.Response):
    """
    Check if response is successful. Raises an exception otherwise.
    :param response: response to check.
    :return: nothing. If response returned an error raises an exception.
    """
    if response.status_code >= 400:
        error: str = 'Error {url} {method}: {message}'.format(
            url=response.request.url,
            method=response.request.method,
            message=response.text)

        raise Exception(error)
