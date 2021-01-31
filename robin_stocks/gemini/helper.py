from robin_stocks.gemini.globals import (LOGGED_IN,
                                         RETURN_PARSED_JSON_RESPONSE, SESSION,
                                         USE_SANDBOX_URLS)


def set_default_json_flag(parse_json):
    """ Sets whether you want all functions to return the json parsed response or not.

    :param parse_json: Set to change value of global variable.
    :type parse_json: bool
    """
    global RETURN_PARSED_JSON_RESPONSE
    RETURN_PARSED_JSON_RESPONSE = parse_json


def get_default_json_flag():
    """ Gets the boolean flag on the default JSON setting.
    """
    return RETURN_PARSED_JSON_RESPONSE


def get_sandbox_flag():
    """ Gets whether all functions are to use the sandbox base url.
    """
    return USE_SANDBOX_URLS


def use_sand_box_urls(use_sandbox):
    """ Sets whether you want all functions to use the sandbox base url.

    :param use_sandbox: Set to change value of global variable.
    :type use_sandbox: bool
    """
    global USE_SANDBOX_URLS
    USE_SANDBOX_URLS = use_sandbox


def set_login_state(logged_in):
    """ Sets the login state

    :param logged_in: Set to change value of global variable.
    :type logged_in: bool
    """
    global LOGGED_IN
    LOGGED_IN = logged_in


def login_required(func):
    """ A decorator for indicating which methods require the user to be logged in.
    """
    @wraps(func)
    def login_wrapper(*args, **kwargs):
        global LOGGED_IN
        if not LOGGED_IN:
            raise Exception('{} can only be called when logged in'.format(
                func.__name__))
        return(func(*args, **kwargs))
    return(login_wrapper)


def request_get(url, payload, parse_json):
    """ Generic function for sending a get request.

    :param url: The url to send a get request to.
    :type url: str
    :param payload: Dictionary of parameters to pass to the url. Will append the requests url as url/?key1=value1&key2=value2.
    :type payload: dict
    :param parse_json: Requests serializes data in the JSON format. Set this parameter true to parse the data to a dictionary \
        using the JSON format.
    :type parse_json: bool
    :returns: Returns a tuple where the first entry is the response and the second entry will be an error message from the \
        get request. If there was no error then the second entry in the tuple will be None. The first entry will either be \
        the raw request response or the parsed JSON response based on whether parse_json is True or not.
    """
    response_error = None
    try:
        response = SESSION.get(url, params=payload)
        response.raise_for_status()
    except Exception as e:
        response_error = e
    # Return either the raw request object so you can call response.text, response.status_code, response.headers, or response.json()
    # or return the JSON parsed information if you don't care to check the status codes.
    if parse_json:
        return response.json(), response_error
    else:
        return response, response_error