import requests
import json

#fetches json data from URL and converts it to python data
def get_data_from_json_site(siteURL, endpoints='', params='', headers=''):

    siteURL += get_endpoints_for_url(*endpoints) + get_params_for_url(params)
    if headers != '':
        try:
            site = requests.get(siteURL, headers=headers)
        except AttributeError:
            raise Exception('headers must be a dictionary')
    else:
        site = requests.get(siteURL)

    if not(site_available(site)):
        raise Exception('Cannot connect to site')

    
    try:
        data = site.json()

    except json.JSONDecodeError:
        raise Exception('Incorrect file format')

    else:
        return data

#posts data as json to the given URL
def post_json_data_to_site(data, siteURL, endpoints='', headers=''):

    siteURL += get_endpoints_for_url(*endpoints)
    if headers != '':
        try:
            response =requests.post(siteURL, headers=headers, json=data)
        except AttributeError:
            raise Exception('headers must be a dictionary')
    else:
        response = requests.post(siteURL, json=data)
    
    return response

#sends a delete request to the given URL
def delete_json_data_from_site(siteURL, endpoints='', params='', headers=''):

    siteURL += get_endpoints_for_url(*endpoints) + get_params_for_url(params)
    if headers != '':
        try:
            response = requests.delete(siteURL, headers=headers)
        except AttributeError:
            raise Exception('headers must be a dictionary')
    else:
        response = requests.post(siteURL)
    
    return response

#returns a string of endpoints to add to an URL
def get_endpoints_for_url(*endpoints):

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

#returns a string of parameters to add to an URL
def get_params_for_url(params):
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

#returns an URL with added parameters
def get_url_with_params(siteURL, params):
    return siteURL + get_params_for_url(params)

#returns an URL with added endpoints
def get_url_with_endpoints(siteURL, *endpoints):
    return siteURL + get_endpoints_for_url(*endpoints)

#returns an URL with added both endpoints and parameters
def get_url_with_endpoints_and_params(siteURl, params, *endpoints):
    return siteURl + get_endpoints_for_url(*endpoints) + get_params_for_url(params)

#checks whether the given site is available(you can either give it an URL or a full site)
def site_available(site=None, siteURL='', endpoints='', params=''):
    
    if siteURL != '':
        site = requests.get(siteURL + get_endpoints_for_url(*endpoints) + get_params_for_url(params))
    else:
        if site == None:
            raise Exception('No site or siteURL given')

    if site.status_code == 200:
        return True
    else:
        return False