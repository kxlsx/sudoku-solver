import requests
import json


def get_data_from_json_site(siteURL, endpoints='', params='', headers=''):
    """
    Fetches json data from URL and converts it to python data structures.
    
    Arguments:
        siteURL {str}
    
    Keyword Arguments:
        endpoints {str} (default: {''})
        params {dict} (default: {''})
        headers {dict} (default: {''})
    
    Raises:
        ConnectionError: Cannot connect to site.
        ConnectionError: Incorrect file format.
        AttributeError: Headers must be a dictionary.
    
    Returns:
        {any} -- data from the site
    """

    siteURL += get_endpoints_for_url(*endpoints) + get_params_for_url(params)
    if headers != '':
        try:
            site = requests.get(siteURL, headers=headers)
        except AttributeError:
            raise AttributeError('Headers must be a dictionary.')
    else:
        site = requests.get(siteURL)

    if not(site_available(site)):
        raise ConnectionError('Cannot connect to site.')

    
    try:
        data = site.json()

    except json.JSONDecodeError:
        raise ConnectionError('Incorrect file format.')

    else:
        return data

def post_json_data_to_site(data, siteURL, endpoints='', headers=''):
    """
    Posts data as json to the given URL.
    
    Arguments:
        data {any} -- data to post
        siteURL {str} -- [description]
    
    Keyword Arguments:
        endpoints {str} -- [description] (default: {''})
        headers {str} -- [description] (default: {''})
    
    Raises:
        AttributeError: Headers must be a dictionary
    
    Returns:
        {any} -- site's response
    """

    siteURL += get_endpoints_for_url(*endpoints)
    if headers != '':
        try:
            response =requests.post(siteURL, headers=headers, json=data)
        except AttributeError:
            raise AttributeError('Headers must be a dictionary')
    else:
        response = requests.post(siteURL, json=data)
    
    return response

def delete_json_data_from_site(siteURL, endpoints='', params='', headers=''):
    """
    Sends a delete request to the given URL.
    
    Arguments:
        siteURL {str} -- 
    
    Keyword Arguments:
        endpoints {str} (default: {''})
        params {str} (default: {''})
        headers {dict} (default: {''})
    
    Raises:
         AttributeError: Headers must be a dictionary
    
    Returns:
        {any} -- site's response
    """

    siteURL += get_endpoints_for_url(*endpoints) + get_params_for_url(params)
    if headers != '':
        try:
            response = requests.delete(siteURL, headers=headers)
        except AttributeError:
            raise AttributeError('headers must be a dictionary')
    else:
        response = requests.post(siteURL)
    
    return response


def get_endpoints_for_url(*endpoints):
    """
    Returns a string of endpoints to add to an URL.

    Arguments:
        endpoints {str or tuple}
    
    Returns:
        {str} -- endpoints ready to add to an URL
    """

    if len(endpoints) == 1 and endpoints[0] == '':
        return ''

    formedEndpoints = ''
    for endpoint in endpoints:

        if isinstance(endpoint, str):

            if endpoint[0] == '/':
                formedEndpoints += endpoint
            else:
                formedEndpoints += ('/' + endpoint)
        else:

            for nestedEndpoint in endpoint:

                if nestedEndpoint[0] == '/':
                    formedEndpoints += nestedEndpoint
                else:
                    formedEndpoints += ('/' + nestedEndpoint)

    return formedEndpoints

def get_params_for_url(params):
    """
    Returns a string of parameters to add to an URL.
    
    Arguments:
        params {dict}
    
    Returns:
        {str} -- parameters ready to add to an URL
    """

    formedParams = '?'

    try:
        paramsItems = params.items()
        
    except AttributeError:
        formedParams = ''

    else:
        maxi = len(params) - 1
        i = 0
        for param, value in paramsItems:
            formedParams += (str(param) + '=' + str(value))

            if i != maxi:
                formedParams += '&'
        
            i += 1
    finally:
        return formedParams

def get_url_with_params(siteURL, params):
    """
    Returns an URL with added parameters.
    
    Arguments:
        siteURL {str} 
        params {dict}
    
    Returns:
        {str} -- URL with parameters
    """

    return siteURL + get_params_for_url(params)

def get_url_with_endpoints(siteURL, *endpoints):
    """Returns an URL with added endpoints.
    
    Arguments:
        siteURL {str}
        endpoints {str or tuple}
    
    Returns:
        {str} -- URL with endpoints
    """

    return siteURL + get_endpoints_for_url(*endpoints)

def get_url_with_endpoints_and_params(siteURl, params, *endpoints):
    """
    Returns an URL with added both endpoints and parameters.
    
    Arguments:
        siteURL {str} 
        params {dict}
        endpoints {str or tuple}

    
    Returns:
        {str} -- URL with endpoints and parameters
    """

    return siteURl + get_endpoints_for_url(*endpoints) + get_params_for_url(params)


def site_available(site=None, siteURL='', endpoints='', params=''):
    """
    Checks whether the given site is available (you can either give it an URL or a full site).
    
    Keyword Arguments:
        site {site object} -- site you want to connect with (default: {None})
        siteURL {str} -- site URL you want to connect with (default: {''})
        endpoints {str} (default: {''})
        params {str} (default: {''})
    
    Raises:
        ConnectionError: No site or siteURL given.
    
    Returns:
        {bool}
    """

    if siteURL != '':
        site = requests.get(siteURL + get_endpoints_for_url(*endpoints) + get_params_for_url(params))
    else:
        if site == None:
            raise ConnectionError('No site or siteURL given')

    if site.status_code == 200:
        return True
    else:
        return False


class ConnectionError(Exception):
    """
    Raised when program encounters an error with the connection
    """

    def __init__(self, *args):
        
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__ (self):
        print('Exception has occured: ConnectionError')
        if self.message:
            return '{0}'.format(self.message)
        else:
            return 'ConnectionError has been raised'
