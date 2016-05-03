# __author__ = 'dimitrios'
import requests
import itertools


class APICalls(object):
    """
    Class that simulates the low level API calls.
    For now, only implements get (for reading only purposes)
    Code based on https://github.com/hawesie/python-canvas-api
    Canvas API returns a responses which contain several data points in them. This combines all the responses to a list
    """
    def __init__(self, oauth_token, api_url, verbose=True):
        self.oauth_token = oauth_token
        self.api_url = api_url
        self.verbose = verbose

    def _get_response(self, url, parameters=None):
        """
        lowest call, directly to the API. Combines the parameters with the access token. Returns 100 results if not
        otherwise specified
        :param url: string
        :param parameters: dictionary
        :return: one response
        """
        if parameters is None:
            parameters = {}
        parameters['access_token'] = self.oauth_token

        if parameters.get('per_page', None) is None:
            parameters['per_page'] = 100

        r = requests.get(url, params=parameters)
        r.raise_for_status()
        return r


    def _get_responses(self, url, parameters=None):
        """
        Simple wrapper that keeps asking for responses until there are no more left, returns a list of responses
        :param url: string
        :param parameters: dictionary
        :return: list of responses
        """
        url = self.api_url + url
        if self.verbose:
            print url
        responses = []
        while True:
            r = self._get_response(url, parameters)
            responses.append(r)

            if 'next' in r.links:
                url = r.links['next']['url']
            else:
                break

        return responses


    def get(self, request_url, to_json=True, parameters=None, single=False):
        """
        :param request_url: string API given url for this entity
        :param to_json: boolean Decides whether make responses as a list of dictionaries (based on their json object)
        :param parameters: string extra parameters in the API given url to specify different behavior if needed
        :param single: boolean if there is only one response returned rather than a list (of there is only one, then
        a list is returned. This depends on the API call)
        :return: list of json objects, based on the url
        """
        responses = self._get_responses(request_url, parameters=parameters)

        if to_json:
            responses = [r.json() for r in responses]
        if single:
            return responses[0]
        else:
            # combine the list of dictionaries (or responses) into one list
            return list(reduce(lambda x, y: itertools.chain(x, y), responses))