#<=====>#
# Description
#<=====>#

# FSTrent

# Library for using birdeye.so api calls

# Birdeye URLS

# ***** Premium (Paid) *****
# Request History                                 https://public-api.birdeye.so/defi/history
# Price                                      10   https://public-api.birdeye.so/defi/price                              [check_liquidity, include_liqudity, address]
# Price Multiple                             20   https://public-api.birdeye.so/defi/multi_price                        [check_liquidity, include_liqudity, list_address]
# Price Multiple                             20   https://public-api.birdeye.so/defi/multi_price                        [check_liquidity, include_liqudity]                         [list_address]
# Price Historical                            5   https://public-api.birdeye.so/defi/history_price                      [address, address_type, type, time_from, time_to]
# Trades - Token                             10   https://public-api.birdeye.so/defi/txs/token                          [address, offset, limit, tx_type]
# Trades - Pair                               4   https://public-api.birdeye.so/defi/txs/pair                           [address, offset, limit, tx_type, sort_type]
# OHLCV                                      15   https://public-api.birdeye.so/defi/ohlcv                              [address, type, time_from, time_to]
# OHLCV - Pair                               15   https://public-api.birdeye.so/defi/ohlcv/pair                         [address, type, time_from, time_to]
# OHLCV - Base/Quote                         15   https://public-api.birdeye.so/defi/ohlcv/base_quote                   [base_address, quote_address, type, time_from, time_to]
# Token - List                               25   https://public-api.birdeye.so/defi/tokenlist                          [sort_by, sort_type, offset, limit]
# Token - Security                           50   https://public-api.birdeye.so/defi/token_security                     [address]
# Token - Overview                            5   https://public-api.birdeye.so/defi/token_overview                     [address]
# Token - Creation Token Info                10   https://public-api.birdeye.so/defi/token_creation_info                [address]

# ***** Public *****
# Token - List                               0    https://public-api.birdeye.so/public/tokenlist                        [sort_by, sort_type, offset, limit]   
# Price                                      0    https://public-api.birdeye.so/public/price                            [address]                             
# Price - Multiple                           0    https://public-api.birdeye.so/public/multi_price                      [list_address]
# Price - Historical                         0    https://public-api.birdeye.so/public/history_price                    [address, address_type, time_from, time_to]
# Token - Existed                            0    https://public-api.birdeye.so/public/exists_token                     [address]                             
# AMMs - Supported                           0    https://public-api.birdeye.so/public/amm_supported                                                          

# ***** Wallet APIs (Beta) (Paid) *****
# Supported Networks                              
# Wallet Portfolio                                
# Wallet Portfolio - Multichain                   
# Wallet - Token Balance                          
# Wallet - Transaction History                    
# Wallet - Transaction History - Multichain       
# Transaction Simulation


#<=====>#
# Imports - Common Modules
#<=====>#
#import asyncio
import datetime 
import json
import os
import pandas as pd
import pandas_ta as ta 
import pprint
#import re as reggie
import requests
import sys
import time
import traceback
import websockets
import re

#from datetime import datetime
from datetime import datetime as dt
from datetime import timedelta
#from zoneinfo import ZoneInfo
#from datetime import datetime
from pprint import pprint
from termcolor import cprint
from web3 import exceptions as w3exceptions
from websockets import connect as ws_connect

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode


#<=====>#
# Imports - Download Modules
#<=====>#


#<=====>#
# Imports - Local Library
#<=====>#


#<=====>#
# Variables
#<=====>#
lib_name      = 'cls_birdeye'
log_name      = 'cls_birdeye'
lib_verbosity = 1
lib_debug_lvl = 1

start_time = dt.now()
print('start_time : {}'.format(start_time))


#<=====>#
# Assignments Pre
#<=====>#

http_err_codes = {
    "100": {"name": "Continue", "description": "This interim response indicates that the client should continue the request or ignore the response if the request is already finished."},
    "101": {"name": "Switching Protocols", "description": "This code is sent in response to an Upgrade request header from the client and indicates the protocol the server is switching to."},
    "102": {"name": "Processing (WebDAV)", "description": "This code indicates that the server has received and is processing the request, but no response is available yet."},
    "103": {"name": "Early Hints", "description": "This status code is primarily intended to be used with the Link header, letting the user agent start preloading resources while the server prepares a response or preconnect to an origin from which the page will need resources."},
    "200": {"name": "OK", "description": "The request succeeded. The result meaning of 'success' depends on the HTTP method:"},
    "201": {"name": "Created", "description": "The request succeeded, and a new resource was created as a result. This is typically the response sent after POST requests, or some PUT requests."},
    "202": {"name": "Accepted", "description": "The request has been received but not yet acted upon. It is noncommittal, since there is no way in HTTP to later send an asynchronous response indicating the outcome of the request. It is intended for cases where another process or server handles the request, or for batch processing."},
    "203": {"name": "Non-Authoritative Information", "description": "This response code means the returned metadata is not exactly the same as is available from the origin server, but is collected from a local or a third-party copy. This is mostly used for mirrors or backups of another resource. Except for that specific case, the 200 OK response is preferred to this status."},
    "204": {"name": "No Content", "description": "There is no content to send for this request, but the headers may be useful. The user agent may update its cached headers for this resource with the new ones."},
    "205": {"name": "Reset Content", "description": "Tells the user agent to reset the document which sent this request."},
    "206": {"name": "Partial Content", "description": "This response code is used when the Range header is sent from the client to request only part of a resource."},
    "207": {"name": "Multi-Status (WebDAV)", "description": "Conveys information about multiple resources, for situations where multiple status codes might be appropriate."},
    "208": {"name": "Already Reported (WebDAV)", "description": "Used inside a <dav:propstat> response element to avoid repeatedly enumerating the internal members of multiple bindings to the same collection."},
    "226": {"name": "IM Used (HTTP Delta encoding)", "description": "The server has fulfilled a GET request for the resource, and the response is a representation of the result of one or more instance-manipulations applied to the current instance."},
    "300": {"name": "Multiple Choices", "description": "The request has more than one possible response. The user agent or user should choose one of them. (There is no standardized way of choosing one of the responses, but HTML links to the possibilities are recommended so the user can pick.)"},
    "301": {"name": "Moved Permanently", "description": "The URL of the requested resource has been changed permanently. The new URL is given in the response."},
    "302": {"name": "Found", "description": "This response code means that the URI of requested resource has been changed temporarily. Further changes in the URI might be made in the future. Therefore, this same URI should be used by the client in future requests."},
    "303": {"name": "See Other", "description": "The server sent this response to direct the client to get the requested resource at another URI with a GET request."},
    "304": {"name": "Not Modified", "description": "This is used for caching purposes. It tells the client that the response has not been modified, so the client can continue to use the same cached version of the response."},
    "305": {"name": "Use Proxy Deprecated", "description": "Defined in a previous version of the HTTP specification to indicate that a requested response must be accessed by a proxy. It has been deprecated due to security concerns regarding in-band configuration of a proxy."},
    "306": {"name": "unused", "description": "This response code is no longer used; it is just reserved. It was used in a previous version of the HTTP/1.1 specification."},
    "307": {"name": "Temporary Redirect", "description": "The server sends this response to direct the client to get the requested resource at another URI with the same method that was used in the prior request. This has the same semantics as the 302 Found HTTP response code, with the exception that the user agent must not change the HTTP method used: if a POST was used in the first request, a POST must be used in the second request."},
    "308": {"name": "Permanent Redirect", "description": "This means that the resource is now permanently located at another URI, specified by the Location: HTTP Response header. This has the same semantics as the 301 Moved Permanently HTTP response code, with the exception that the user agent must not change the HTTP method used: if a POST was used in the first request, a POST must be used in the second request."},
    "400": {"name": "Bad Request", "description": "The server cannot or will not process the request due to something that is perceived to be a client error (e.g., malformed request syntax, invalid request message framing, or deceptive request routing)."},
    "401": {"name": "Unauthorized", "description": "Although the HTTP standard specifies 'unauthorized', semantically this response means 'unauthenticated'. That is, the client must authenticate itself to get the requested response."},
    "402": {"name": "Payment Required Experimental", "description": "This response code is reserved for future use. The initial aim for creating this code was using it for digital payment systems, however this status code is used very rarely and no standard convention exists."},
    "403": {"name": "Forbidden", "description": "The client does not have access rights to the content; that is, it is unauthorized, so the server is refusing to give the requested resource. Unlike 401 Unauthorized, the client's identity is known to the server."},
    "404": {"name": "Not Found", "description": "The server cannot find the requested resource. In the browser, this means the URL is not recognized. In an API, this can also mean that the endpoint is valid but the resource itself does not exist. Servers may also send this response instead of 403 Forbidden to hide the existence of a resource from an unauthorized client. This response code is probably the most well known due to its frequent occurrence on the web."},
    "405": {"name": "Method Not Allowed", "description": "The request method is known by the server but is not supported by the target resource. For example, an API may not allow calling DELETE to remove a resource."},
    "406": {"name": "Not Acceptable", "description": "This response is sent when the web server, after performing server-driven content negotiation, doesn't find any content that conforms to the criteria given by the user agent."},
    "407": {"name": "Proxy Authentication Required", "description": "This is similar to 401 Unauthorized but authentication is needed to be done by a proxy."},
    "408": {"name": "Request Timeout", "description": "This response is sent on an idle connection by some servers, even without any previous request by the client. It means that the server would like to shut down this unused connection. This response is used much more since some browsers, like Chrome, Firefox 27+, or IE9, use HTTP pre-connection mechanisms to speed up surfing. Also note that some servers merely shut down the connection without sending this message."},
    "409": {"name": "Conflict", "description": "This response is sent when a request conflicts with the current state of the server."},
    "410": {"name": "Gone", "description": "This response is sent when the requested content has been permanently deleted from server, with no forwarding address. Clients are expected to remove their caches and links to the resource. The HTTP specification intends this status code to be used for 'limited-time, promotional services''. APIs should not feel compelled to indicate resources that have been deleted with this status code."},
    "411": {"name": "Length Required", "description": "Server rejected the request because the Content-Length header field is not defined and the server requires it."},
    "412": {"name": "Precondition Failed", "description": "The client has indicated preconditions in its headers which the server does not meet."},
    "413": {"name": "Payload Too Large", "description": "Request entity is larger than limits defined by server. The server might close the connection or return an Retry-After header field."},
    "414": {"name": "URI Too Long", "description": "The URI requested by the client is longer than the server is willing to interpret."},
    "415": {"name": "Unsupported Media Type", "description": "The media format of the requested data is not supported by the server, so the server is rejecting the request."},
    "416": {"name": "Range Not Satisfiable", "description": "The range specified by the Range header field in the request cannot be fulfilled. It's possible that the range is outside the size of the target URI's data."},
    "417": {"name": "Expectation Failed", "description": "This response code means the expectation indicated by the Expect request header field cannot be met by the server."},
    "418": {"name": "I'm a teapot", "description": "The server refuses the attempt to brew coffee with a teapot."},
    "421": {"name": "Misdirected Request", "description": "The request was directed at a server that is not able to produce a response. This can be sent by a server that is not configured to produce responses for the combination of scheme and authority that are included in the request URI."},
    "422": {"name": "Unprocessable Content (WebDAV)", "description": "The request was well-formed but was unable to be followed due to semantic errors."},
    "423": {"name": "Locked (WebDAV)", "description": "The resource that is being accessed is locked."},
    "424": {"name": "Failed Dependency (WebDAV)", "description": "The request failed due to failure of a previous request."},
    "425": {"name": "Too Early Experimental", "description": "Indicates that the server is unwilling to risk processing a request that might be replayed."},
    "426": {"name": "Upgrade Required", "description": "The server refuses to perform the request using the current protocol but might be willing to do so after the client upgrades to a different protocol. The server sends an Upgrade header in a 426 response to indicate the required protocol(s)."},
    "428": {"name": "Precondition Required", "description": "The origin server requires the request to be conditional. This response is intended to prevent the 'lost update' problem, where a client GETs a resource's state, modifies it and PUTs it back to the server, when meanwhile a third party has modified the state on the server, leading to a conflict."},
    "429": {"name": "Too Many Requests", "description": "The user has sent too many requests in a given amount of time ('rate limiting')."},
    "431": {"name": "Request Header Fields Too Large", "description": "The server is unwilling to process the request because its header fields are too large. The request may be resubmitted after reducing the size of the request header fields."},
    "451": {"name": "Unavailable For Legal Reasons", "description": "The user agent requested a resource that cannot legally be provided, such as a web page censored by a government."},
    "500": {"name": "Internal Server Error", "description": "The server has encountered a situation it does not know how to handle."},
    "501": {"name": "Not Implemented", "description": "The request method is not supported by the server and cannot be handled. The only methods that servers are required to support (and therefore that must not return this code) are GET and HEAD."},
    "502": {"name": "Bad Gateway", "description": "This error response means that the server, while working as a gateway to get a response needed to handle the request, got an invalid response."},
    "503": {"name": "Service Unavailable", "description": "The server is not ready to handle the request. Common causes are a server that is down for maintenance or that is overloaded. Note that together with this response, a user-friendly page explaining the problem should be sent. This response should be used for temporary conditions and the Retry-After HTTP header should, if possible, contain the estimated time before the recovery of the service. The webmaster must also take care about the caching-related headers that are sent along with this response, as these temporary condition responses should usually not be cached."},
    "504": {"name": "Gateway Timeout", "description": "This error response is given when the server is acting as a gateway and cannot get a response in time."},
    "505": {"name": "HTTP Version Not Supported", "description": "The HTTP version used in the request is not supported by the server."},
    "506": {"name": "Variant Also Negotiates", "description": "The server has an internal configuration error: the chosen variant resource is configured to engage in transparent content negotiation itself, and is therefore not a proper end point in the negotiation process."},
    "507": {"name": "Insufficient Storage (WebDAV)", "description": "The method could not be performed on the resource because the server is unable to store the representation needed to successfully complete the request."},
    "508": {"name": "Loop Detected (WebDAV)", "description": "The server detected an infinite loop while processing the request."},
    "510": {"name": "Not Extended", "description": "Further extensions to the request are required for the server to fulfill it."},
    "511": {"name": "Network Authentication Required", "description": "Indicates that the client needs to authenticate to gain network access."}
    }



#<=====>#
# Classes
#<=====>#

class BIRDEYE():
#<=====>#

    def __init__(self, chain='solana', api_free_key=None, api_paid_key=None, wallet_addr=None, throttle=0.25):

        self.chain = chain
        allowed_chains = ['solana', 'ethereum', 'arbitrum', 'avalanche', 'bsc', 'optimism', 'polygon', 'base', 'zksync']
        if self.chain not in allowed_chains:
            print('chain must be in {}...'.format(allowed_chains))
            exit()
        self.wallet_addr = wallet_addr

        self.api_free_key = api_free_key
        self.api_paid_key  = api_paid_key
        if self.api_paid_key and not self.api_free_key:
            self.api_free_key = self.api_paid_key
        if not self.api_free_key and not self.api_paid_key:
            print('api_free_key or api_paid_key or both must be populated...')
            exit()

        self.base_url_public  = 'https://public-api.birdeye.so/public/{}'
        self.base_url_premium = 'https://public-api.birdeye.so/defi/{}'
        self.base_url_v1      = 'https://public-api.birdeye.so/v1/{}'

        self.headers_public   = {"x-chain": self.chain, "X-API-KEY": self.api_free_key}
        self.headers_premium  = {"x-chain": self.chain, "X-API-KEY": self.api_paid_key}
        self.headers_other  = {"x-chain": self.chain, "X-API-KEY": self.api_paid_key}

        self.throttle         = throttle
        self.session_costs    = 0

#<=====>#


    def req_public(self, api_url=None, headers=None, params=None):
        func_name = 'req_public'

        data = None

        try:
            if api_url and headers:
                r = requests.get(api_url, headers=self.headers_public, params=params)
                if r.status_code == 200:
                    data = r.json()
                    if 'data' in data:
                        data = data['data']
                else:
                    err_name = http_err_codes[r.status_code]['name']
                    err_desc = http_err_codes[r.status_code]['description']
                    print("Error {} : {} - {}...".format(r.status_code, err_name, err_desc))
                    print("exiting...")
                    print(r.text)
                    exit()
                # Sleep to avoid hitting rate limits
                time.sleep(self.throttle)

        except requests.exceptions.RequestException as e:
            print("Error {}: exiting...".format(r.status_code))
            print(r.text)
            exit()

        return data


#<=====>#


    def req_premium(self, api_url=None, headers=None, params=None, cost=0):
        func_name = 'req_premium'

        data = None

        try:
            if api_url and headers:
                r = requests.get(api_url, headers=self.headers_premium, params=params)
                if r.status_code == 200:
                    data = r.json()
                    if 'data' in data:
                        data = data['data']
                else:
                    err_name = http_err_codes[r.status_code]['name']
                    err_desc = http_err_codes[r.status_code]['description']
                    print("Error {} : {} - {}...".format(r.status_code, err_name, err_desc))
                    print("exiting...")
                    print(r.text)
                    exit()
                # Sleep to avoid hitting rate limits
                time.sleep(self.throttle)

        except requests.exceptions.RequestException as e:
            print("Error {}: exiting...".format(r.status_code))
            print(r.text)
            exit()

        return data


#<=====>#


    def req_other(self, api_url=None, headers=None, params=None, cost=0):
        func_name = 'req_premium'

        data = self.req_premium(api_url=api_url, headers=headers, params=params, cost=cost)

        return data


#<=====>#


    def hist_data_to_df(self, hist_data):

        df = pd.DataFrame(hist_data)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.set_index("time", inplace=True)

#        first_open = df['open'].iloc[-1]
#        print('first_open : {}'.format(first_open))

        return df


#<=====>#


# AMMs - Supported                                https://public-api.birdeye.so/public/amm_supported                                                          
    '''
        [
            {
                'icon': 'https://cdn.jsdelivr.net/gh/birdeye-so/birdeye-ads/pool_providers/raydium.svg',
                'program_ids': ['675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8'],
                'source': 'raydium',
                'summary': True,
                'symbol': 'RAY',
                'token_address': '4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R',
                'website': 'https://raydium.io'},
                ...
    '''
    def amm_support(self):
        func_name = 'amms_support'

        out_data = None

        api_url = self.base_url_public.format("amm_supported")
        headers = self.headers_public

        data = self.req_public(api_url, headers=headers)

        out_data = data

        return out_data


#<=====>#

# Token - List                               0    https://public-api.birdeye.so/public/tokenlist                        [sort_by, sort_type, offset, limit]   
    '''
    [
        {
            'address': '6Rg6dydAquZKbHXPeEHKM9GQB68fBd6a6ADHQqbEU5rM',
            'decimals': 9,
            'lastTradeUnixTime': 1707302630,
            'liquidity': 0,
            'logoURI': 'https://img.fotofolio.xyz/?url=https%3A%2F%2Fbafkreifuc6el5ypbqvg6etxbmwjweymednu4pwupw26n2wqbl5eqwdiiqi.ipfs.nftstorage.link',
            'mc': None,
            'name': 'NoCap',
            'symbol': 'NCAP',
            'url': 'https://birdeye.so/token/6Rg6dydAquZKbHXPeEHKM9GQB68fBd6a6ADHQqbEU5rM',
            'v24hChangePercent': 91489691688.6077,
            'v24hUSD': 0.0857385747859209
            },
        ...
    '''
    def tkn_list(self, tkns_size=50, sort_by="mc", sort_type="desc"):
        func_name = 'tkn_list'

        out_data = None

        api_url = self.base_url_public.format("tokenlist")
        headers = self.headers_public

        tkns_list       = []
        tkns_tot        = 0
        offset          = 0

        limit           = tkns_size
        if limit > 50: limit = 50

        params = {}

        if sort_by and sort_by in ('mc', 'v24hChangePercent', 'v24hUSD'):
            params['sort_by'] = sort_by
        else:
            params['sort_by'] = 'mc'

        if sort_type and sort_type in ('asc', 'desc'):
            params['sort_type'] = sort_type
        else:
            params['sort_type'] = 'desc'

        while tkns_tot < tkns_size:
            params['offset'] = offset
            params['limit']  = limit

            data = self.req_public(api_url, headers=headers, params=params)

            if data:
                if 'tokens' in data:
                    new_tkns = data['tokens']
                    for tkn in new_tkns:
                        if tkn['name']:
                            tkn['name'] = re.sub("[^a-zA-Z0-9]", "", tkn['name'])
                        if tkn['symbol']:
                            tkn['symbol'] = re.sub("[^a-zA-Z0-9]", "", tkn['symbol'])
                        tkn['url_birdeye']     = "https://birdeye.so/token/{}".format(tkn['address']) 
                        tkn['url_dexscreener'] = "https://dexscreener.com/{}/{}".format(self.chain, tkn['address']) 
                    tkns_list.extend(new_tkns)
                tkns_tot = len(tkns_list)
                offset   += limit
            else:
                print(f"Error {response.status_code}: trying again in 10 seconds...")
                # Sleep longer on error before retrying
                time.sleep(10)
                # Skip to the next pagination
                continue

        out_data = tkns_list

        return out_data


#<=====>#


# Token - Existed                                 https://public-api.birdeye.so/public/exists_token                     [address]                             
    def tkn_exists(self, tkn_addr):
        func_name = 'tkn_exists'

        out_data = None

        api_url = self.base_url_public.format("exists_token")
        headers = self.headers_public

        params = {}
        params['address'] = tkn_addr

        data = self.req_public(api_url, headers=headers, params=params)

        if 'exists' in data:
            out_data = data['exists']

        return out_data


#<=====>#


# Price                                      0    https://public-api.birdeye.so/public/price                            [address]                             
# Price                                      10   https://public-api.birdeye.so/defi/price                              [check_liquidity, include_liqudity, address]
    def tkn_prc(self, tkn_addr):
        func_name = 'tkn_prc'

        out_data = None

        api_url = self.base_url_public.format("price")
        headers = self.headers_public

        params = {}
        params['address'] = tkn_addr

        data = self.req_public(api_url, headers=headers, params=params)

#        {
#            'updateHumanTime': '2024-02-07T19:02:11',
#            'updateUnixTime': 1707332531,
#            'value': 97.5283044868421
#        }

#        print(type(data))
#        pprint(data)

        if 'value' in data:
            out_data = data['value']

        return out_data

#<=====>#


# Price - Multiple                           0    https://public-api.birdeye.so/public/multi_price                      [list_address]
    '''
        {
            'So11111111111111111111111111111111111111112': {
                'priceChange24h': 3.8208007733632243,
                'updateHumanTime': '2024-02-07T21:46:59',
                'updateUnixTime': 1707342419,
                'value': 100.6857724092254
                },
            'mSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So': {
                'priceChange24h': 3.7666138783341605,
                'updateHumanTime': '2024-02-07T21:47:00',
                'updateUnixTime': 1707342420,
                'value': 117.29717826508877
                }
            }
    '''
    def tkn_prc_mult(self, tkn_addr_list=[]):
        func_name = 'tkn_prc_mult'

        out_data = None

        api_url = self.base_url_public.format("multi_price{}")
        headers = self.headers_public

#        params = {}
#        params['list_address'] = addr_list

        param_str = '?list_address=' + "%2C".join(tkn_addr_list)
        api_url = api_url.format(param_str)
        print(api_url)

        data = self.req_public(api_url, headers=headers)

#        {
#            'So11111111111111111111111111111111111111112': {
#                'priceChange24h': 1.5828660715562037,
#                'updateHumanTime': '2024-02-07T19:14:35',
#                'updateUnixTime': 1707333275,
#                'value': 97.60584150727273
#                },
#            'mSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So': {
#                'priceChange24h': 1.608279243760306,
#                'updateHumanTime': '2024-02-07T19:14:44',
#                'updateUnixTime': 1707333284,
#                'value': 113.81216516915146
#                }
#        }

        out_data = data

        return out_data


#<=====>#


# Price - Historical                         0    https://public-api.birdeye.so/public/history_price                    [address, address_type, time_from, time_to]
    '''
        [
            {'unixTime': 1700006400, 'value': 65.53270998171779},
            {'unixTime': 1700092800, 'value': 57.81278296532601},
            {'unixTime': 1700179200, 'value': 58.66642073524119},
            {'unixTime': 1700265600, 'value': 58.592833733845715},
            {'unixTime': 1700352000, 'value': 61.1813586580713},
            ...
    '''
    def tkn_prc_hist(self, tkn_addr, time_from, time_to):
        func_name = 'tkn_prc_hist'

        out_data = None

        api_url = self.base_url_public.format("history_price")
        headers = self.headers_public

        params = {}
        params['address'] = tkn_addr
        params['address_type'] = "token"
        params['time_from'] = time_from
        params['time_to'] = time_to

        data = self.req_public(api_url, headers=headers, params=params)

        if 'items' in data:
            out_data = data['items']
        else:
            out_data = data

        return out_data



#<=====>#


# Price - Historical                         0    https://public-api.birdeye.so/public/history_price                    [address, address_type, time_from, time_to]
    '''
        [
            {'address': '3ne4mWqdYuNiYrYZC9TrA3FcfuFdErghH97vNPbjicr1', 'unixTime': 1700006400, 'value': 1.4881249407047788e-08},
            {'address': '3ne4mWqdYuNiYrYZC9TrA3FcfuFdErghH97vNPbjicr1', 'unixTime': 1700092800, 'value': 1.3943915856378179e-08},
            {'address': '3ne4mWqdYuNiYrYZC9TrA3FcfuFdErghH97vNPbjicr1', 'unixTime': 1700179200, 'value': 1.3840921483278112e-08},
            {'address': '3ne4mWqdYuNiYrYZC9TrA3FcfuFdErghH97vNPbjicr1', 'unixTime': 1700265600, 'value': 1.3822718246279778e-08},
            {'address': '3ne4mWqdYuNiYrYZC9TrA3FcfuFdErghH97vNPbjicr1', 'unixTime': 1700352000, 'value': 1.3309523809523809e-08}
    '''
    def pair_prc_hist(self, pair_addr, time_from, time_to):
        func_name = 'pair_prc_hist'

        out_data = None

        api_url = self.base_url_public.format("history_price")
        headers = self.headers_public

        params = {}
        params['address'] = pair_addr
        params['address_type'] = "pair"
        params['time_from'] = time_from
        params['time_to'] = time_to

        data = self.req_public(api_url, headers=headers, params=params)

        if 'items' in data:
            out_data = data['items']
        else:
            out_data = data

        return out_data



#<=====>#

# Request History                             0   https://public-api.birdeye.so/defi/history
    '''
        {
            'items': [
                'H5PMkStS4uURTxYXJSGzic5AN4BDEb7ya2yrRAbnJYon',
                'DgHQsVm3Qoy49fCrNsyzpvgiymSt1paH5uvWiLP94anM',
                'FSyViTWXCQPP6haLH7TbVKhAy6waRXXtt2uA47xBQo8o',
                'DY7A9o11esjnLGwQrFyczB2UAui8C4DMCQNzCZk7jxMU',
                'FTYPeuYU5Q8Sac5xGFgpYxbqMgh7AhsKiyqxjhLzLwxi',
                '7GLDBGgdPbyVJ3BrZf9YSeuxCMKcbXGG86nv6dantRjf',
                ...
            ],
            'resetInSeconds': 33205
        }
    '''
    # Not sure what this is?
    # A list of tokens looked up?
    # A list of wallets with recent transactions?
    def prem_req_hist(self):
        func_name = 'prem_req_hist'

        if not self.api_paid_key:
            print('this call {} requires a paid key...'.format(func_name))
            exit()

        out_data = None

        api_url = self.base_url_premium.format("history")
        headers = self.headers_premium
        cost = 0

        data = self.req_premium(api_url, headers=headers, cost=cost)
        print(type(data))
        print(data)

        out_data = data
        if 'items' in out_data:
            out_data = out_data['items']

        return out_data


#<=====>#


# Token - List                               25   https://public-api.birdeye.so/defi/tokenlist                          [sort_by, sort_type, offset, limit]
    '''
    [
        {
            'address': '6Rg6dydAquZKbHXPeEHKM9GQB68fBd6a6ADHQqbEU5rM',
            'decimals': 9,
            'lastTradeUnixTime': 1707302630,
            'liquidity': 0,
            'logoURI': 'https://img.fotofolio.xyz/?url=https%3A%2F%2Fbafkreifuc6el5ypbqvg6etxbmwjweymednu4pwupw26n2wqbl5eqwdiiqi.ipfs.nftstorage.link',
            'mc': None,
            'name': 'NoCap',
            'symbol': 'NCAP',
            'url': 'https://birdeye.so/token/6Rg6dydAquZKbHXPeEHKM9GQB68fBd6a6ADHQqbEU5rM',
            'v24hChangePercent': 91489691688.6077,
            'v24hUSD': 0.0857385747859209
            },
        ...
    '''
    # identical to free version, do not use
    def prem_tkn_list(self, tkns_size=50, sort_by="mc", sort_type="desc"):
        func_name = 'prem_tkn_list'

        if not self.api_paid_key:
            print('this call {} requires a paid key...'.format(func_name))
            exit()

        out_data = None

        api_url = self.base_url_premium.format("tokenlist")
        headers = self.headers_premium
        cost = 25

        tkns_list       = []
        tkns_tot        = 0
        offset          = 0

        limit           = tkns_size
        if limit > 50: limit = 50

        params = {}

        if sort_by and sort_by in ('mc', 'v24hChangePercent', 'v24hUSD'):
            params['sort_by'] = sort_by
        else:
            params['sort_by'] = 'mc'

        if sort_type and sort_type in ('asc', 'desc'):
            params['sort_type'] = sort_type
        else:
            params['sort_type'] = 'desc'

        while tkns_tot < tkns_size:
            params['offset'] = offset
            params['limit']  = limit

            data = self.req_premium(api_url, headers=headers, params=params, cost=cost)

            if data:
                if 'tokens' in data:
                    new_tkns = data['tokens']
                    for tkn in new_tkns:
                        if tkn['name']:
                            tkn['name'] = re.sub("[^a-zA-Z0-9]", "", tkn['name'])
                        if tkn['symbol']:
                            tkn['symbol'] = re.sub("[^a-zA-Z0-9]", "", tkn['symbol'])
                        tkn['url'] = "https://birdeye.so/token/{}".format(tkn['address']) 
                    tkns_list.extend(new_tkns)
                tkns_tot = len(tkns_list)
                offset   += limit
            else:
                print(f"Error {response.status_code}: trying again in 10 seconds...")
                # Sleep longer on error before retrying
                time.sleep(10)
                # Skip to the next pagination
                continue

        out_data = tkns_list

        return out_data


#<=====>#


# Token - Security                           50   https://public-api.birdeye.so/defi/token_security                     [address]
    '''
        {
            'creationSlot': None,
            'creationTime': None,
            'creationTx': None,
            'creatorAddress': None,
            'creatorBalance': None,
            'creatorOwnerAddress': None,
            'creatorPercentage': None,
            'freezeAuthority': None,
            'freezeable': None,
            'isToken2022': False,
            'isTrueToken': None,
            'lockInfo': None,
            'metaplexOwnerUpdateAuthority': None,
            'metaplexUpdateAuthority': 'AqH29mZfQFgRpfwaPoTMWSKJ5kqauoc1FwVBRksZyQrt',
            'metaplexUpdateAuthorityBalance': 0,
            'metaplexUpdateAuthorityPercent': None,
            'mintSlot': None,
            'mintTime': None,
            'mintTx': None,
            'mutableMetadata': True,
            'nonTransferable': None,
            'ownerAddress': None,
            'ownerBalance': None,
            'ownerOfOwnerAddress': None,
            'ownerPercentage': None,
            'preMarketHolder': [],
            'top10HolderBalance': 2680924.4445215845,
            'top10HolderPercent': None,
            'top10UserBalance': 0,
            'top10UserPercent': None,
            'totalSupply': None,
            'transferFeeData': None,
            'transferFeeEnable': None
            }
    '''
    def prem_tkn_security(self, tkn_addr):
        func_name = 'prem_tkn_security'

        if not self.api_paid_key:
            print('this call {} requires a paid key...'.format(func_name))
            exit()

        out_data = None

        api_url = self.base_url_premium.format("token_security")
        headers = self.headers_premium
        cost = 50

        params = {}
        params['address'] = tkn_addr

        data = self.req_premium(api_url, headers=headers, params=params, cost=cost)
#        print(type(data))
#        print(data)

        out_data = data

        return out_data


#<=====>#


# Token - Overview                            5   https://public-api.birdeye.so/defi/token_overview                     [address]
    '''
        {
            'address': 'So11111111111111111111111111111111111111112',
            'buy12h': 859678,
            'buy12hChangePercent': 3.213296931015687,
            'buy1h': 81968,
            'buy1hChangePercent': -1.2267129395319691,
            'buy24h': 1692772,
            'buy24hChangePercent': 29.120671243325706,
            'buy2h': 164901,
            'buy2hChangePercent': -2.40003314472407,
            'buy30m': 37361,
            'buy30mChangePercent': -16.307878407741764,
            'buy4h': 333936,
            'buy4hChangePercent': 10.655444363443568,
            'buy6h': 505092,
            'buy6hChangePercent': 42.487749696034484,
            'buy8h': 635707,
            'buy8hChangePercent': 34.14539960413088,
            'buyHistory12h': 832914,
            'buyHistory1h': 82986,
            'buyHistory24h': 1311000,
            'buyHistory2h': 168956,
            'buyHistory30m': 44641,
            'buyHistory4h': 301780,
            'buyHistory6h': 354481,
            'buyHistory8h': 473894,
            'decimals': 9,
            'extensions': {
                'coingeckoId': 'solana',
                'description': 'Wrapped Solana ',
                'discord': 'https://discordapp.com/invite/pquxPsq',
                'medium': 'https://medium.com/solana-labs',
                'serumV3Usdc': '9wFFyRfZBsuAha4YcuxcXLKwMxJR43S7fPfQLusDBzvT',
                'serumV3Usdt': 'HWHvQhFmJB3NUcu1aihKmrKegfVxBEHzwVX6yZCKEsi1',
                'telegram': None,
                'twitter': 'https://twitter.com/solana',
                'website': 'https://solana.com/'
                },
            'history12hPrice': 95.39668441716348,
            'history1hPrice': 97.49748733884371,
            'history24hPrice': 97.23561321176399,
            'history2hPrice': 97.13639400515777,
            'history30mPrice': 97.30871864063741,
            'history4hPrice': 96.16046722189922,
            'history6hPrice': 95.5255460205141,
            'history8hPrice': 95.05262838079787,
            'lastTradeHumanTime': '2024-02-07T19:56:04.000Z',
            'lastTradeUnixTime': 1707335764,
            'liquidity': 339068133.70551795,
            'logoURI': 'https://img.fotofolio.xyz/?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsolana-labs%2Ftoken-list%2Fmain%2Fassets%2Fmainnet%2FSo11111111111111111111111111111111111111112%2Flogo.png',
            'name': 'Wrapped SOL',
            'numberMarkets': 249475,
            'price': 97.39684010868395,
            'priceChange12hPercent': 1.7118625497753146,
            'priceChange1hPercent': -0.47974857627854967,
            'priceChange24hPercent': -0.21172148098391735,
            'priceChange2hPercent': -0.10979352777276848,
            'priceChange30mPercent': -0.28668973665084885,
            'priceChange4hPercent': 0.9039861542301856,
            'priceChange6hPercent': 1.574655758147799,
            'priceChange8hPercent': 2.0800225983333127,
            'sell12h': 930692,
            'sell12hChangePercent': 7.696420078664076,
            'sell1h': 91358,
            'sell1hChangePercent': 2.3641986375044817,
            'sell24h': 1795018,
            'sell24hChangePercent': 26.602385743374246,
            'sell2h': 180544,
            'sell2hChangePercent': 5.341035066223234,
            'sell30m': 42376,
            'sell30mChangePercent': -13.565994248067392,
            'sell4h': 351962,
            'sell4hChangePercent': 4.989634137247005,
            'sell6h': 535739,
            'sell6hChangePercent': 35.689898841514996,
            'sell8h': 687230,
            'sell8hChangePercent': 37.232192244483095,
            'sellHistory12h': 864181,
            'sellHistory1h': 89248,
            'sellHistory24h': 1417839,
            'sellHistory2h': 171390,
            'sellHistory30m': 49027,
            'sellHistory4h': 335235,
            'sellHistory6h': 394826,
            'sellHistory8h': 500779,
            'symbol': 'SOL',
            'trade12h': 1790370,
            'trade12hChangePercent': 5.496156667717482,
            'trade1h': 173326,
            'trade1hChangePercent': 0.6340211572627936,
            'trade24h': 3487790,
            'trade24hChangePercent': 27.81223076920258,
            'trade2h': 345445,
            'trade2hChangePercent': 1.4981812625974744,
            'trade30m': 79737,
            'trade30mChangePercent': -14.872742025024554,
            'trade4h': 685898,
            'trade4hChangePercent': 7.673759644592357,
            'trade6h': 1040831,
            'trade6hChangePercent': 38.90581564031832,
            'trade8h': 1322937,
            'trade8hChangePercent': 35.73136836662142,
            'tradeHistory12h': 1697095,
            'tradeHistory1h': 172234,
            'tradeHistory24h': 2728839,
            'tradeHistory2h': 340346,
            'tradeHistory30m': 93668,
            'tradeHistory4h': 637015,
            'tradeHistory6h': 749307,
            'tradeHistory8h': 974673,
            'uniqueView12h': 2068,
            'uniqueView12hChangePercent': 14.25414364640884,
            'uniqueView1h': 235,
            'uniqueView1hChangePercent': -20.875420875420875,
            'uniqueView24h': 3650,
            'uniqueView24hChangePercent': -22.472387425658454,
            'uniqueView2h': 497,
            'uniqueView2hChangePercent': 6.881720430107527,
            'uniqueView30m': 111,
            'uniqueView30mChangePercent': -18.97810218978102,
            'uniqueView4h': 884,
            'uniqueView4hChangePercent': 10.224438902743142,
            'uniqueView6h': 1276,
            'uniqueView6hChangePercent': 37.945945945945944,
            'uniqueView8h': 1590,
            'uniqueView8hChangePercent': 49.43609022556391,
            'uniqueViewHistory12h': 1810,
            'uniqueViewHistory1h': 297,
            'uniqueViewHistory24h': 4708,
            'uniqueViewHistory2h': 465,
            'uniqueViewHistory30m': 137,
            'uniqueViewHistory4h': 802,
            'uniqueViewHistory6h': 925,
            'uniqueViewHistory8h': 1064,
            'uniqueWallet12h': 124409,
            'uniqueWallet12hChangePercent': 12.355501770103317,
            'uniqueWallet1h': 22675,
            'uniqueWallet1hChangePercent': -6.208636664460622,
            'uniqueWallet24h': 190332,
            'uniqueWallet24hChangePercent': 14.59432121956506,
            'uniqueWallet2h': 37187,
            'uniqueWallet2hChangePercent': -7.531828128108216,
            'uniqueWallet30m': 13867,
            'uniqueWallet30mChangePercent': -3.7949216039961144,
            'uniqueWallet4h': 62855,
            'uniqueWallet4hChangePercent': 9.034294932954014,
            'uniqueWallet6h': 83896,
            'uniqueWallet6hChangePercent': 27.905842175875108,
            'uniqueWallet8h': 99055,
            'uniqueWallet8hChangePercent': 29.055163248820907,
            'uniqueWalletHistory12h': 110728,
            'uniqueWalletHistory1h': 24176,
            'uniqueWalletHistory24h': 166092,
            'uniqueWalletHistory2h': 40216,
            'uniqueWalletHistory30m': 14414,
            'uniqueWalletHistory4h': 57647,
            'uniqueWalletHistory6h': 65592,
            'uniqueWalletHistory8h': 76754,
            'v12h': 3309329.094534236,
            'v12hChangePercent': 19.983314302611205,
            'v12hUSD': 318157729.042338,
            'v1h': 237580.343653941,
            'v1hChangePercent': -21.347817397336687,
            'v1hUSD': 23122559.73664684,
            'v24h': 6067712.236535165,
            'v24hChangePercent': 17.69738306840765,
            'v24hUSD': 584652275.0072763,
            'v2h': 539392.714897277,
            'v2hChangePercent': -30.52750753881534,
            'v2hUSD': 52483817.34725182,
            'v30m': 122251.20928065499,
            'v30mChangePercent': 5.9162077404424585,
            'v30mUSD': 11878851.6751892,
            'v4h': 1316174.000066835,
            'v4hChangePercent': 1.4234283837270743,
            'v4hUSD': 127779440.77256389,
            'v6h': 2215483.498633646,
            'v6hChangePercent': 102.55559775663198,
            'v6hUSD': 213894875.14820188,
            'v8h': 2613800.2555274963,
            'v8hChangePercent': 80.72832889200433,
            'v8hUSD': 251879525.8090718,
            'vBuy12h': 1624659.219247721,
            'vBuy12hChangePercent': 21.229789603413117,
            'vBuy12hUSD': 156242011.09420824,
            'vBuy1h': 111918.955785527,
            'vBuy1hChangePercent': -23.782253077641787,
            'vBuy1hUSD': 10895155.492275236,
            'vBuy24h': 2964917.803649554,
            'vBuy24hChangePercent': 14.421186741675008,
            'vBuy24hUSD': 285741133.956415,
            'vBuy2h': 258676.697415036,
            'vBuy2hChangePercent': -35.02956834619796,
            'vBuy2hUSD': 25174072.954542175,
            'vBuy30m': 54606.428958838,
            'vBuy30mChangePercent': -4.78531095855756,
            'vBuy30mUSD': 5306960.011954344,
            'vBuy4h': 657092.724944175,
            'vBuy4hChangePercent': 3.397643775468881,
            'vBuy4hUSD': 63801671.73809685,
            'vBuy6h': 1097018.779311639,
            'vBuy6hChangePercent': 107.93751458014708,
            'vBuy6hUSD': 105941339.39907072,
            'vBuy8h': 1292459.045230016,
            'vBuy8hChangePercent': 82.59390143043943,
            'vBuy8hUSD': 124580230.43275067,
            'vBuyHistory12h': 1340148.510166168,
            'vBuyHistory12hUSD': 129488614.58041807,
            'vBuyHistory1h': 146841.070885416,
            'vBuyHistory1hUSD': 14287034.925663892,
            'vBuyHistory24h': 2591231.473890716,
            'vBuyHistory24hUSD': 247592109.09694082,
            'vBuyHistory2h': 398145.265208344,
            'vBuyHistory2hUSD': 38601215.09682634,
            'vBuyHistory30m': 57350.84524098,
            'vBuyHistory30mUSD': 5591929.744150913,
            'vBuyHistory4h': 635500.675790129,
            'vBuyHistory4hUSD': 60791155.17522876,
            'vBuyHistory6h': 527571.36273686,
            'vBuyHistory6hUSD': 50293575.83210739,
            'vBuyHistory8h': 707832.537179446,
            'vBuyHistory8hUSD': 67558904.64798245,
            'vHistory12h': 2758157.760326358,
            'vHistory12hUSD': 266473055.07663321,
            'vHistory1h': 302064.527381464,
            'vHistory1hUSD': 29385817.06630481,
            'vHistory24h': 5155350.168668161,
            'vHistory24hUSD': 492550645.0543225,
            'vHistory2h': 776411.923321513,
            'vHistory2hUSD': 75259562.62861234,
            'vHistory30m': 115422.570245569,
            'vHistory30mUSD': 11252813.90224464,
            'vHistory4h': 1297702.1394772818,
            'vHistory4hUSD': 124106698.28447074,
            'vHistory6h': 1093765.6244363692,
            'vHistory6hUSD': 104254048.72506307,
            'vHistory8h': 1446259.2951265508,
            'vHistory8hUSD': 138014664.037339,
            'vSell12h': 1684669.875286515,
            'vSell12hChangePercent': 18.805281072475434,
            'vSell12hUSD': 161915717.94812974,
            'vSell1h': 125661.387868414,
            'vSell1hChangePercent': -19.04484624615136,
            'vSell1hUSD': 12227404.244371602,
            'vSell24h': 3102794.432885611,
            'vSell24hChangePercent': 21.008221624269265,
            'vSell24hUSD': 298911141.05086124,
            'vSell2h': 280716.017482241,
            'vSell2hChangePercent': -25.788855173628082,
            'vSell2hUSD': 27309744.392709643,
            'vSell30m': 67644.780321817,
            'vSell30mChangePercent': 16.484881956703553,
            'vSell30mUSD': 6571891.663234857,
            'vSell4h': 659081.27512266,
            'vSell4hChangePercent': -0.47118418420878894,
            'vSell4hUSD': 63977769.03446704,
            'vSell6h': 1118464.719322007,
            'vSell6hChangePercent': 97.54080798430968,
            'vSell6hUSD': 107953535.74913114,
            'vSell8h': 1321341.21029748,
            'vSell8hChangePercent': 78.94005005600438,
            'vSell8hUSD': 127299295.37632114,
            'vSellHistory12h': 1418009.25016019,
            'vSellHistory12hUSD': 136984440.49621516,
            'vSellHistory1h': 155223.456496048,
            'vSellHistory1hUSD': 15098782.140640918,
            'vSellHistory24h': 2564118.694777445,
            'vSellHistory24hUSD': 244958535.95738167,
            'vSellHistory2h': 378266.658113169,
            'vSellHistory2hUSD': 36658347.53178601,
            'vSellHistory30m': 58071.725004589,
            'vSellHistory30mUSD': 5660884.158093727,
            'vSellHistory4h': 662201.463687153,
            'vSellHistory4hUSD': 63315543.10924197,
            'vSellHistory6h': 566194.261699509,
            'vSellHistory6hUSD': 53960472.89295568,
            'vSellHistory8h': 738426.757947105,
            'vSellHistory8hUSD': 70455759.38935655,
            'view12h': 3804,
            'view12hChangePercent': 19.88654270406555,
            'view1h': 337,
            'view1hChangePercent': -26.89804772234273,
            'view24h': 6975,
            'view24hChangePercent': -24.975798644724104,
            'view2h': 798,
            'view2hChangePercent': 2.8350515463917527,
            'view30m': 152,
            'view30mChangePercent': -17.83783783783784,
            'view4h': 1576,
            'view4hChangePercent': 21.32409545804465,
            'view6h': 2298,
            'view6hChangePercent': 52.589641434262944,
            'view8h': 2875,
            'view8hChangePercent': 61.24509254066181,
            'viewHistory12h': 3173,
            'viewHistory1h': 461,
            'viewHistory24h': 9297,
            'viewHistory2h': 776,
            'viewHistory30m': 185,
            'viewHistory4h': 1299,
            'viewHistory6h': 1506,
            'viewHistory8h': 1783,
            'watch': 816
             }
    '''
    def prem_tkn_overview(self, tkn_addr):
        func_name = 'prem_tkn_overview'

        if not self.api_paid_key:
            print('this call {} requires a paid key...'.format(func_name))
            exit()

        out_data = None

        api_url = self.base_url_premium.format("token_overview")
        headers = self.headers_premium
        cost = 5

        params = {}
        params['address'] = tkn_addr

        data = self.req_premium(api_url, headers=headers, params=params, cost=cost)
#        print(type(data))
#        print(data)

        out_data = data

        return out_data


#<=====>#


# Token - Creation Token Info                10   https://public-api.birdeye.so/defi/token_creation_info                [address]
    '''
        {
            'decimals': 9,
            'owner': 'BULLkeLmVVe9kPsziqfXHRRMxusFXh4W2TDtPfhubEs3',
            'slot': 197410925,
            'tokenAddress': 'BULLa6g9e5UCuTXC5Z3Cf7s7CgvJhnJfY71DwipSmF8w',
            'txHash': '3z81rymQVUi6oKHBpGkukwjvETV5RUVNQ2sNZgr3Enwx8331BWLNGUuDtNx84ZsQpBeu2LQQvSnUPhF1AquNoGnx'}
    '''
    def prem_tkn_creation(self, tkn_addr):
        func_name = 'prem_tkn_creation'

        if not self.api_paid_key:
            print('this call {} requires a paid key...'.format(func_name))
            exit()

        out_data = None

        api_url = self.base_url_premium.format("token_creation_info")
        headers = self.headers_premium
        cost = 10

        params = {}
        params['address'] = tkn_addr

        data = self.req_premium(api_url, headers=headers, params=params, cost=cost)
#        print(type(data))
#        print(data)

        out_data = data

        return out_data


#<=====>#


# OHLCV                                      15   https://public-api.birdeye.so/defi/ohlcv                              [address, type, time_from, time_to]
    '''
        out_df_tf=False
        [
            {'close': 1.64354312775606e-06, 'high': 1.64354312775606e-06, 'low': 1.64354312775606e-06, 'open': 1.64354312775606e-06, 'time': 1707337320, 'volume': 0},
            {'close': 1.64354312775606e-06, 'high': 1.64354312775606e-06, 'low': 1.64354312775606e-06, 'open': 1.64354312775606e-06, 'time': 1707337380, 'volume': 0},
            {'close': 1.64354312775606e-06, 'high': 1.64354312775606e-06, 'low': 1.64354312775606e-06, 'open': 1.64354312775606e-06, 'time': 1707337440, 'volume': 0},
            {'close': 1.64354312775606e-06, 'high': 1.64354312775606e-06, 'low': 1.64354312775606e-06, 'open': 1.64354312775606e-06, 'time': 1707337500, 'volume': 0},
            ...
        ]
        out_df_tf=True
                                 open      high       low     close  volume
        time
        2024-02-07 20:22:00  0.000002  0.000002  0.000002  0.000002       0
        2024-02-07 20:23:00  0.000002  0.000002  0.000002  0.000002       0
        2024-02-07 20:24:00  0.000002  0.000002  0.000002  0.000002       0
        2024-02-07 20:25:00  0.000002  0.000002  0.000002  0.000002       0
        2024-02-07 20:26:00  0.000002  0.000002  0.000002  0.000002       0
        2024-02-07 20:27:00  0.000002  0.000002  0.000002  0.000002       0
        2024-02-07 20:28:00  0.000002  0.000002  0.000002  0.000002       0
        2024-02-07 20:29:00  0.000002  0.000002  0.000002  0.000002       0
        2024-02-07 20:30:00  0.000002  0.000002  0.000002  0.000002       0
        2024-02-07 20:31:00  0.000002  0.000002  0.000002  0.000002       0
    '''
    def prem_ohlcv_tkn(self, tkn_addr, freq, time_from, time_to, out_df_tf=False):
        func_name = 'prem_ohlcv_tkn'

        if not self.api_paid_key:
            print('this call {} requires a paid key...'.format(func_name))
            exit()

        allowed_freqs = ['1m','3m','5m','15m','30m','1H','2H','4H','6H','8H','12H','1D','3D','1W','1M']
        if freq not in allowed_freqs:
            print('freq must be in the following : {}'.format(allowed_freqs))
            exit()

        out_data = None

        api_url = self.base_url_premium.format("ohlcv")
        headers = self.headers_premium
        cost = 15

        params = {}
        params['address']   = tkn_addr
        params['type']      = freq
        params['time_from'] = time_from
        params['time_to']   = time_to

        data = self.req_premium(api_url, headers=headers, params=params, cost=cost)
#        print(type(data))
#        print(data)

        data = data['items']
        hist_data = []
        for row in data:
            hist_row = {}
            hist_row['time']   = row['unixTime']
            hist_row['open']   = row['o']
            hist_row['high']   = row['h']
            hist_row['low']    = row['l']
            hist_row['close']  = row['c']
            hist_row['volume'] = row['v']
#            hist_row['addr']   = row['address']
#            hist_row['freq']   = row['type']
            hist_data.append(hist_row)

        if out_df_tf:
            out_data = self.hist_data_to_df(hist_data)
        else:
            out_data = hist_data

        return out_data


#<=====>#


# OHLCV - Pair                               15   https://public-api.birdeye.so/defi/ohlcv/pair                         [address, type, time_from, time_to]
    '''
        out_df_tf=False
        [
            {'close': 1.64354312775606e-06, 'high': 1.64354312775606e-06, 'low': 1.64354312775606e-06, 'open': 1.64354312775606e-06, 'time': 1707337320, 'volume': 0},
            {'close': 1.64354312775606e-06, 'high': 1.64354312775606e-06, 'low': 1.64354312775606e-06, 'open': 1.64354312775606e-06, 'time': 1707337380, 'volume': 0},
            {'close': 1.64354312775606e-06, 'high': 1.64354312775606e-06, 'low': 1.64354312775606e-06, 'open': 1.64354312775606e-06, 'time': 1707337440, 'volume': 0},
            {'close': 1.64354312775606e-06, 'high': 1.64354312775606e-06, 'low': 1.64354312775606e-06, 'open': 1.64354312775606e-06, 'time': 1707337500, 'volume': 0},
            ...
        ]
        out_df_tf=True
                                 open      high       low     close  volume
        time
        2024-02-07 20:22:00  0.000002  0.000002  0.000002  0.000002       0
        2024-02-07 20:23:00  0.000002  0.000002  0.000002  0.000002       0
        2024-02-07 20:24:00  0.000002  0.000002  0.000002  0.000002       0
        2024-02-07 20:25:00  0.000002  0.000002  0.000002  0.000002       0
        2024-02-07 20:26:00  0.000002  0.000002  0.000002  0.000002       0
        2024-02-07 20:27:00  0.000002  0.000002  0.000002  0.000002       0
        2024-02-07 20:28:00  0.000002  0.000002  0.000002  0.000002       0
        2024-02-07 20:29:00  0.000002  0.000002  0.000002  0.000002       0
        2024-02-07 20:30:00  0.000002  0.000002  0.000002  0.000002       0
        2024-02-07 20:31:00  0.000002  0.000002  0.000002  0.000002       0
    '''
    def prem_ohlcv_pair(self, pair_addr, freq, time_from, time_to, out_df_tf=False):
        func_name = 'prem_ohlcv_pair'

        if not self.api_paid_key:
            print('this call {} requires a paid key...'.format(func_name))
            exit()

        allowed_freqs = ['1m','3m','5m','15m','30m','1H','2H','4H','6H','8H','12H','1D','3D','1W','1M']
        if freq not in allowed_freqs:
            print('freq must be in the following : {}'.format(allowed_freqs))
            exit()

        out_data = None

        api_url = self.base_url_premium.format("ohlcv/pair")
        headers = self.headers_premium
        cost = 15

        params = {}
        params['address']   = pair_addr
        params['type']      = freq
        params['time_from'] = time_from
        params['time_to']   = time_to

        data = self.req_premium(api_url, headers=headers, params=params, cost=cost)
        print(type(data))
        print(data)

        data = data['items']
        hist_data = []
        for row in data:
            hist_row = {}
            hist_row['time']   = row['unixTime']
            hist_row['open']   = row['o']
            hist_row['high']   = row['h']
            hist_row['low']    = row['l']
            hist_row['close']  = row['c']
            hist_row['volume'] = row['v']
#            hist_row['addr']   = row['address']
#            hist_row['freq']   = row['type']
            hist_data.append(hist_row)

        if out_df_tf:
            out_data = self.hist_data_to_df(hist_data)
        else:
            out_data = hist_data

        return out_data


#<=====>#


# OHLCV - Base/Quote                         15   https://public-api.birdeye.so/defi/ohlcv/base_quote                   [base_address, quote_address, type, time_from, time_to]
    def prem_ohlcv_quote(self, base_addr, quote_addr, freq, time_from, time_to, out_df_tf=False):
        func_name = 'prem_ohlcv_quote'

        if not self.api_paid_key:
            print('this call {} requires a paid key...'.format(func_name))
            exit()

        allowed_freqs = ['1m','3m','5m','15m','30m','1H','2H','4H','6H','8H','12H','1D','3D','1W','1M']
        if freq not in allowed_freqs:
            print('freq must be in the following : {}'.format(allowed_freqs))
            exit()

        out_data = None

        api_url = self.base_url_premium.format("ohlcv/base_quote")
        headers = self.headers_premium
        cost = 15

        params = {}
        params['base_address']     = base_addr
        params['quote_address']    = quote_addr
        params['type']             = freq
        params['time_from']        = time_from
        params['time_to']          = time_to
#        data = self.req_premium(api_url, headers=headers, params=params, cost=cost)

        api_url += '?base_address={}'.format(base_addr)
        api_url += '&quote_address={}'.format(quote_addr)
        api_url += '&type={}'.format(freq)
        api_url += '&time_from={}'.format(time_from)
        api_url += '&time_to={}'.format(time_to)
        data = self.req_premium(api_url, headers=headers, cost=cost)

        print(type(data))
        print(data)

        data = data['items']
        hist_data = []
        for row in data:
            hist_row = {}
            hist_row['time']   = row['unixTime']
            hist_row['open']   = row['o']
            hist_row['high']   = row['h']
            hist_row['low']    = row['l']
            hist_row['close']  = row['c']
            hist_row['volume'] = row['vBase']
#            hist_row['volume'] = row['vQuote']
#            hist_row['addr']   = row['address']
#            hist_row['freq']   = row['type']
            hist_data.append(hist_row)

        if out_df_tf:
            out_data = self.hist_data_to_df(hist_data)
        else:
            out_data = hist_data

        return out_data


#<=====>#


# Price                                      10   https://public-api.birdeye.so/defi/price                              [check_liquidity, include_liqudity, address]
    '''
    {
        'liquidity': 95152521.31262425,
        'updateHumanTime': '2024-02-07T23:53:18',
        'updateUnixTime': 1707349998,
        'value': 100.76856153021134
        }
    '''
    def prem_tkn_prc(self, tkn_addr, include_liquidity=False):
        func_name = 'prem_tkn_prc'

        if not self.api_paid_key:
            print('this call {} requires a paid key...'.format(func_name))
            exit()

        out_data = None

        api_url = self.base_url_premium.format("price")
        headers = self.headers_premium
        cost = 10

        params = {}
        params['address'] = tkn_addr
        if include_liquidity:
            params['include_liquidity'] = 'true'

        data = self.req_premium(api_url, headers=headers, params=params, cost=cost)
#        print(type(data))
#        print(data)

        out_data = data
        if not include_liquidity:
            if 'value' in out_data:
                out_data = out_data['value']

        return out_data


#<=====>#


# Price Multiple                             20   https://public-api.birdeye.so/defi/multi_price                        [check_liquidity, include_liqudity, list_address]
# Price Multiple                                  https://public-api.birdeye.so/defi/multi_price                        [check_liquidity, include_liqudity]                         [list_address]
    '''
        {
            'So11111111111111111111111111111111111111112': {
                'priceChange24h': 3.8208007733632243,
                'updateHumanTime': '2024-02-07T21:46:59',
                'updateUnixTime': 1707342419,
                'value': 100.6857724092254
                },
            'mSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So': {
                'priceChange24h': 3.7666138783341605,
                'updateHumanTime': '2024-02-07T21:47:00',
                'updateUnixTime': 1707342420,
                'value': 117.29717826508877
                }
            }
    '''
    # identical to free version, do not use
    def prem_tkn_prc_mult(self, tkn_addr_list=[]):
        func_name = 'prem_tkn_prc_mult'

        if not self.api_paid_key:
            print('this call {} requires a paid key...'.format(func_name))
            exit()

        out_data = None

        api_url = self.base_url_public.format("multi_price{}")
        headers = self.headers_public
        cost = 20

#        params = {}
#        params['list_address'] = addr_list

        param_str = '?list_address=' + "%2C".join(tkn_addr_list)
        api_url = api_url.format(param_str)
        print(api_url)

        data = self.req_premium(api_url, headers=headers, cost=cost)

#        {
#            'So11111111111111111111111111111111111111112': {
#                'priceChange24h': 1.5828660715562037,
#                'updateHumanTime': '2024-02-07T19:14:35',
#                'updateUnixTime': 1707333275,
#                'value': 97.60584150727273
#                },
#            'mSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So': {
#                'priceChange24h': 1.608279243760306,
#                'updateHumanTime': '2024-02-07T19:14:44',
#                'updateUnixTime': 1707333284,
#                'value': 113.81216516915146
#                }
#        }

        out_data = data

        return out_data


#<=====>#


# Price Historical                            5   https://public-api.birdeye.so/defi/history_price                      [address, address_type, type, time_from, time_to]
    '''
        [
            {'unixTime': 1700006400, 'value': 65.53270998171779},
            {'unixTime': 1700092800, 'value': 57.81278296532601},
            {'unixTime': 1700179200, 'value': 58.66642073524119},
            {'unixTime': 1700265600, 'value': 58.592833733845715},
            {'unixTime': 1700352000, 'value': 61.1813586580713},
            ...
    '''
    def prem_tkn_prc_hist(self, tkn_addr, freq, time_from, time_to):
        func_name = 'prem_tkn_prc_hist'

        if not self.api_paid_key:
            print('this call {} requires a paid key...'.format(func_name))
            exit()

        allowed_freqs = ['1m','3m','5m','15m','30m','1H','2H','4H','6H','8H','12H','1D','3D','1W','1M']
        if freq not in allowed_freqs:
            print('freq must be in the following : {}'.format(allowed_freqs))
            exit()

        out_data = None

        api_url = self.base_url_premium.format("history_price")
        headers = self.headers_premium
        cost = 5

        params = {}
        params['address'] = tkn_addr
        params['address_type'] = "token"
        params['type'] = freq
        params['time_from'] = time_from
        params['time_to'] = time_to

        data = self.req_premium(api_url, headers=headers, params=params, cost=cost)

        if 'items' in data:
            out_data = data['items']
        else:
            out_data = data

        return out_data



#<=====>#


# Trades - Token                             10   https://public-api.birdeye.so/defi/txs/token                          [address, offset, limit, tx_type]
    def prem_tkn_trds(self, tkn_addr, txn_type, trds_size=50):
        func_name = 'prem_tkn_trds'

        if not self.api_paid_key:
            print('this call {} requires a paid key...'.format(func_name))
            exit()

        out_data = None

        api_url = self.base_url_premium.format("txs/token")
        headers = self.headers_premium
        cost = 10

        trds_list       = []
        trds_tot        = 0
        offset          = 0

        limit           = trds_size
        if limit > 50: limit = 50

        params = {}
        params['address'] = tkn_addr
        if txn_type and txn_type in ('swap', 'add', 'remove', 'all'):
            params['tx_type'] = txn_type
        else:
            params['tx_type'] = 'all'

#        if sort_type and sort_type in ('asc', 'desc'):
#            params['sort_type'] = sort_type
#        else:
#            params['sort_type'] = 'desc'

        has_next = True

        while trds_tot < trds_size and has_next:
            params['offset'] = offset
            params['limit']  = limit

            data = self.req_premium(api_url, headers=headers, params=params, cost=cost)

            print(type(data))
            pprint(data)

            has_next = data['hasNext']

            if data:
                if 'items' in data:
                    new_trds = data['items']
                    for trd in new_trds:
                        if 'base' in trd:
                            if 'symbol' in trd['base']:
                                trd['base']['symbol'] = re.sub("[^a-zA-Z0-9]", "", trd['base']['symbol'])
                        if 'from' in trd:
                            if 'symbol' in trd['from']:
                                trd['from']['symbol'] = re.sub("[^a-zA-Z0-9]", "", trd['from']['symbol'])
                        if 'quote' in trd:
                            if 'symbol' in trd['quote']:
                                trd['quote']['symbol'] = re.sub("[^a-zA-Z0-9]", "", trd['quote']['symbol'])
                        if 'to' in trd:
                            if 'symbol' in trd['to']:
                                trd['to']['symbol'] = re.sub("[^a-zA-Z0-9]", "", trd['to']['symbol'])
                        trds_list.append(trd)
                        trds_tot = len(trds_list)
                        if trds_tot >= trds_size:
                            break
                offset   += limit
            else:
                print(f"Error {response.status_code}: trying again in 10 seconds...")
                # Sleep longer on error before retrying
                time.sleep(10)
                # Skip to the next pagination
                continue

        out_data = trds_list



#<=====>#


# Trades - Pair                               4   https://public-api.birdeye.so/defi/txs/pair                           [address, offset, limit, tx_type, sort_type]
    def prem_pair_trds(self, pair_addr, txn_type, sort_type, trds_size=50):
        func_name = 'prem_pair_trds'

        if not self.api_paid_key:
            print('this call {} requires a paid key...'.format(func_name))
            exit()

        out_data = None

        api_url = self.base_url_premium.format("txs/pair")
        headers = self.headers_premium
        cost = 10

        trds_list       = []
        trds_tot        = 0
        offset          = 0

        limit           = trds_size
        if limit > 50: limit = 50

        params = {}
        params['address'] = pair_addr
        if txn_type and txn_type in ('swap', 'add', 'remove', 'all'):
            params['tx_type'] = txn_type
        else:
            params['tx_type'] = 'all'

        if sort_type and sort_type in ('asc', 'desc'):
            params['sort_type'] = sort_type
        else:
            params['sort_type'] = 'desc'

        has_next = True

        while trds_tot < trds_size and has_next:
            params['offset'] = offset
            params['limit']  = limit

            data = self.req_premium(api_url, headers=headers, params=params, cost=cost)

            print(type(data))
            pprint(data)

            has_next = data['hasNext']

            if data:
                if 'items' in data:
                    new_trds = data['items']
                    for trd in new_trds:
                        if 'base' in trd:
                            if 'symbol' in trd['base']:
                                trd['base']['symbol'] = re.sub("[^a-zA-Z0-9]", "", trd['base']['symbol'])
                        if 'from' in trd:
                            if 'symbol' in trd['from']:
                                trd['from']['symbol'] = re.sub("[^a-zA-Z0-9]", "", trd['from']['symbol'])
                        if 'quote' in trd:
                            if 'symbol' in trd['quote']:
                                trd['quote']['symbol'] = re.sub("[^a-zA-Z0-9]", "", trd['quote']['symbol'])
                        if 'to' in trd:
                            if 'symbol' in trd['to']:
                                trd['to']['symbol'] = re.sub("[^a-zA-Z0-9]", "", trd['to']['symbol'])
                        trds_list.append(trd)
                        trds_tot = len(trds_list)
                        if trds_tot >= trds_size:
                            break
                offset   += limit
            else:
                print(f"Error {response.status_code}: trying again in 10 seconds...")
                # Sleep longer on error before retrying
                time.sleep(10)
                # Skip to the next pagination
                continue

        out_data = trds_list


#<=====>#


# Price Historical                            5   https://public-api.birdeye.so/defi/history_price                      [address, address_type, type, time_from, time_to]
    '''
        [
            {'address': '3ne4mWqdYuNiYrYZC9TrA3FcfuFdErghH97vNPbjicr1', 'unixTime': 1700006400, 'value': 1.4881249407047788e-08},
            {'address': '3ne4mWqdYuNiYrYZC9TrA3FcfuFdErghH97vNPbjicr1', 'unixTime': 1700092800, 'value': 1.3943915856378179e-08},
            {'address': '3ne4mWqdYuNiYrYZC9TrA3FcfuFdErghH97vNPbjicr1', 'unixTime': 1700179200, 'value': 1.3840921483278112e-08},
            {'address': '3ne4mWqdYuNiYrYZC9TrA3FcfuFdErghH97vNPbjicr1', 'unixTime': 1700265600, 'value': 1.3822718246279778e-08},
            {'address': '3ne4mWqdYuNiYrYZC9TrA3FcfuFdErghH97vNPbjicr1', 'unixTime': 1700352000, 'value': 1.3309523809523809e-08}
    '''
    def prem_pair_prc_hist(self, pair_addr, freq, time_from, time_to):
        func_name = 'prem_pair_prc_hist'

        out_data = None

        api_url = self.base_url_premium.format("history_price")
        headers = self.headers_premium
        cost = 5

        params = {}
        params['address'] = pair_addr
        params['address_type'] = "pair"
        params['type'] = freq
        params['time_from'] = time_from
        params['time_to'] = time_to

        data = self.req_premium(api_url, headers=headers, params=params, cost=cost)

        if 'items' in data:
            out_data = data['items']
        else:
            out_data = data

        return out_data



#<=====>#



# Supported Networks                          1   https://public-api.birdeye.so/v1/wallet/list_supported_chain                  
    def ntwk_support(self):
        func_name = 'ntwk_support'

        if not self.api_paid_key:
            print('this call {} requires a paid key...'.format(func_name))
            exit()

        out_data = None

        api_url = self.base_url_v1.format("wallet/list_supported_chain")
        headers = self.headers_other
        cost = 10

        data = self.req_other(api_url, headers=headers, cost=cost)
#        print(type(data))
#        print(data)

        out_data = data

        return out_data


#<=====>#


# Wallet Portfolio                            45  https://public-api.birdeye.so/v1/wallet/token_list                   
    '''
        {
            'items': [
                    {
                        'address': 'So11111111111111111111111111111111111111111',
                        'balance': 1095235762,
                        'chainId': 'solana',
                        'decimals': 9,
                        'logoURI': 'https://assets.coingecko.com/coins/images/4128/standard/solana.png?1696504756',
                        'name': 'SOL',
                        'priceUsd': 102.5300705651182,
                        'symbol': 'SOL',
                        'uiAmount': 1.095235762,
                        'valueUsd': 112.294599963301
                        },
                    {
                        'address': 'EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm',
                        'balance': 50000000,
                        'chainId': 'solana',
                        'decimals': 6,
                        'icon': 'https://img.fotofolio.xyz/?url=https%3A%2F%2Fbafkreibk3covs5ltyqxa272uodhculbr6kea6betidfwy3ajsav2vjzyum.ipfs.nftstorage.link',
                        'logoURI': 'https://img.fotofolio.xyz/?url=https%3A%2F%2Fbafkreibk3covs5ltyqxa272uodhculbr6kea6betidfwy3ajsav2vjzyum.ipfs.nftstorage.link',
                        'name': 'dogwifhat',
                        'priceUsd': 0.23001895913708792,
                        'symbol': '$WIF',
                        'uiAmount': 50,
                        'valueUsd': 11.500947956854397
                        },
                    {
                        'address': '27G8MtK7VtTcCHkpASjSDdkWWYfoqT6ggEuKidVJidD4',
                        'balance': 5336254,
                        'chainId': 'solana',
                        'decimals': 6,
                        'icon': 'https://img.fotofolio.xyz/?url=https%3A%2F%2Fstatic.jup.ag%2Fjlp%2Ficon.png',
                        'logoURI': 'https://img.fotofolio.xyz/?url=https%3A%2F%2Fstatic.jup.ag%2Fjlp%2Ficon.png',
                        'name': 'Jupiter Perps LP',
                        'priceUsd': 2.0599000417004305,
                        'symbol': 'JLP',
                        'uiAmount': 5.336254,
                        'valueUsd': 10.99214983712409
                        },
                    ...
                ],
            'totalUsd': 181.514980319818,                            
            'wallet': ''
        }
    '''
    def wallet_port(self, wallet_addr):
        func_name = 'wallet_port'

        if not self.api_paid_key:
            print('this call {} requires a paid key...'.format(func_name))
            exit()

        out_data = None

        api_url = self.base_url_v1.format("wallet/token_list")
        headers = self.headers_other
        cost = 45

        params = {}
        params['wallet'] = wallet_addr

        data = self.req_other(api_url, headers=headers, params=params, cost=cost)
#        print(type(data))
#        print(data)

        out_data = data

        return out_data


#<=====>#


# Wallet Portfolio - Multichain               125 https://public-api.birdeye.so/v1/wallet/multichain_token_list                   
    '''
        {
            'items': [
                    {
                        'address': 'So11111111111111111111111111111111111111111',
                        'balance': 1095235762,
                        'chainId': 'solana',
                        'decimals': 9,
                        'logoURI': 'https://assets.coingecko.com/coins/images/4128/standard/solana.png?1696504756',
                        'name': 'SOL',
                        'priceUsd': 102.5300705651182,
                        'symbol': 'SOL',
                        'uiAmount': 1.095235762,
                        'valueUsd': 112.294599963301
                        },
                    {
                        'address': 'EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm',
                        'balance': 50000000,
                        'chainId': 'solana',
                        'decimals': 6,
                        'icon': 'https://img.fotofolio.xyz/?url=https%3A%2F%2Fbafkreibk3covs5ltyqxa272uodhculbr6kea6betidfwy3ajsav2vjzyum.ipfs.nftstorage.link',
                        'logoURI': 'https://img.fotofolio.xyz/?url=https%3A%2F%2Fbafkreibk3covs5ltyqxa272uodhculbr6kea6betidfwy3ajsav2vjzyum.ipfs.nftstorage.link',
                        'name': 'dogwifhat',
                        'priceUsd': 0.23001895913708792,
                        'symbol': '$WIF',
                        'uiAmount': 50,
                        'valueUsd': 11.500947956854397
                        },
                    {
                        'address': '27G8MtK7VtTcCHkpASjSDdkWWYfoqT6ggEuKidVJidD4',
                        'balance': 5336254,
                        'chainId': 'solana',
                        'decimals': 6,
                        'icon': 'https://img.fotofolio.xyz/?url=https%3A%2F%2Fstatic.jup.ag%2Fjlp%2Ficon.png',
                        'logoURI': 'https://img.fotofolio.xyz/?url=https%3A%2F%2Fstatic.jup.ag%2Fjlp%2Ficon.png',
                        'name': 'Jupiter Perps LP',
                        'priceUsd': 2.0599000417004305,
                        'symbol': 'JLP',
                        'uiAmount': 5.336254,
                        'valueUsd': 10.99214983712409
                        },
                    ...
                ],
            'totalUsd': 181.514980319818,                            
            'wallet': ''
        }
    '''
    # I did the test on solana, if I put through an evm address I think that all chains would have come back
    def wallet_port_chains(self, wallet_addr):
        func_name = 'wallet_port_chains'

        if not self.api_paid_key:
            print('this call {} requires a paid key...'.format(func_name))
            exit()

        out_data = None

        api_url = self.base_url_v1.format("wallet/multichain_token_list")
        headers = self.headers_other
        cost = 125

        params = {}
        params['wallet'] = wallet_addr

        data = self.req_other(api_url, headers=headers, params=params, cost=cost)
#        print(type(data))
#        print(data)

        out_data = data

        return out_data


#<=====>#


# Wallet - Token Balance                      1   https://public-api.birdeye.so/v1/wallet/token_balance                   
    '''
        True or False
    '''
    def wallet_tkn_bal(self, wallet_addr, tkn_addr):
        func_name = 'wallet_tkn_bal(wallet_addr={}, tkn_addr={}'.format(wallet_addr, tkn_addr)

        if not self.api_paid_key:
            print('this call {} requires a paid key...'.format(func_name))
            exit()

        out_data = None

        api_url = self.base_url_v1.format("wallet/token_balance")
        headers = self.headers_other
        cost = 1

        params = {}
        params['wallet']           = wallet_addr
        params['token_address']    = tkn_addr

        data = self.req_other(api_url, headers=headers, params=params, cost=cost)
#        print(type(data))
#        print(data)

        if not data:
            out_data = False
        elif 'success' in data:
            out_data = data['success']
        else:
            out_data = False

        return out_data


#<=====>#


# Wallet - Transaction History                55  https://public-api.birdeye.so/v1/wallet/tx_list                   
    '''
        {
            'solana': [
                {
                    'txHash': 'P8GiogdRHvNZ8Yy8Fpb9ES6D2u7VhDxMrs7Vz9sHypBn3Cj6R9Pa93fiHridSGXhv2xhSgjfcxba2xPQ9adEzWD', 
                    'blockNumber': 246755803, 
                    'blockTime': '2024-02-08T00:13:24+00:00', 
                    'status': True, 
                    'from': '5oTtAXDwvygz7LgGQ6HxbNmDNCMAu7NJsC6wFyxUMtSc', 
                    'to': 'BGUMAp9Gq7iTEuizy4pqaxsTyUCBK68MDfK752saRPUY', 
                    'fee': 5000, 
                    'mainAction': 'unknown', 
                    'balanceChange': [
                        {
                            'amount': 0, 
                            'symbol': 'SOL', 
                            'name': 'Wrapped SOL', 
                            'decimals': 9, 
                            'address': 'So11111111111111111111111111111111111111112', 
                            'logoURI': 'https://img.fotofolio.xyz/?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsolana-labs%2Ftoken-list%2Fmain%2Fassets%2Fmainnet%2FSo11111111111111111111111111111111111111112%2Flogo.png'
                            }
                        ], 
                    'contractLabel': {
                        'address': 'BGUMAp9Gq7iTEuizy4pqaxsTyUCBK68MDfK752saRPUY', 
                        'name': 'Bubblegum', 
                        'metadata': {
                            'icon': ''
                                }
                        }
                    }, 
                {
                    'txHash': '5nx7GwpPaiEGZCbAqCgsFParJmUCBB55zXAJYMjFHvL7atyomaFVtyGtbCecGTde15CGg9XxPUBudxEr81fh3TB9', 
                    'blockNumber': 246681146, 
                    'blockTime': '2024-02-07T15:41:31+00:00', 
                    'status': True, 
                    'from': 'DRiPPP2LytGjNZ5fVpdZS7Xi1oANSY3Df1gSxvUKpzny', 
                    'to': 'BGUMAp9Gq7iTEuizy4pqaxsTyUCBK68MDfK752saRPUY', 
                    'fee': 5020, 
                    'mainAction': 'unknown', 
                    'balanceChange': [
                        {
                            'amount': 0, 
                            'symbol': 'SOL', 
                            'name': 'Wrapped SOL', 
                            'decimals': 9, 
                            'address': 'So11111111111111111111111111111111111111112', 
                            'logoURI': 'https://img.fotofolio.xyz/?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsolana-labs%2Ftoken-list%2Fmain%2Fassets%2Fmainnet%2FSo11111111111111111111111111111111111111112%2Flogo.png'
                            }
                        ], 
                    'contractLabel': {
                        'address': 'BGUMAp9Gq7iTEuizy4pqaxsTyUCBK68MDfK752saRPUY', 
                        'name': 'Bubblegum', 
                        'metadata': {
                            'icon': ''
                            }
                        }
                    },
                    ...
                ]
            }
    '''
    def wallet_txn_hist(self, wallet_addr, limit=None, before=None):
        func_name = 'wallet_txn_hist'

        if not self.api_paid_key:
            print('this call {} requires a paid key...'.format(func_name))
            exit()

        out_data = None

        api_url = self.base_url_v1.format("wallet/tx_list")
        headers = self.headers_other
        cost = 55

        params = {}
        params['wallet'] = wallet_addr
        if limit:
            params['limit'] = limit
        # Not sure what this value could be.  Only states str.  Might be txn_hash?
        if before:
            params['before'] = before

        data = self.req_other(api_url, headers=headers, params=params, cost=cost)
#        print(type(data))
#        print(data)

        out_data = data

        return out_data


#<=====>#


# Wallet - Transaction History - Multichain   165 https://public-api.birdeye.so/v1/wallet/multichain_tx_list                   
    '''
        {
            'ethereum': [],
            'polygon': [],
            'bsc': [],
            'avalanche': [],
            'optimism': [],
            'arbitrum': [],
            'base': [],
            'zksync': [],
            'solana': [
                {
                    'txHash': 'P8GiogdRHvNZ8Yy8Fpb9ES6D2u7VhDxMrs7Vz9sHypBn3Cj6R9Pa93fiHridSGXhv2xhSgjfcxba2xPQ9adEzWD', 
                    'blockNumber': 246755803, 
                    'blockTime': '2024-02-08T00:13:24+00:00', 
                    'status': True, 
                    'from': '5oTtAXDwvygz7LgGQ6HxbNmDNCMAu7NJsC6wFyxUMtSc', 
                    'to': 'BGUMAp9Gq7iTEuizy4pqaxsTyUCBK68MDfK752saRPUY', 
                    'fee': 5000, 
                    'mainAction': 'unknown', 
                    'balanceChange': [
                        {
                            'amount': 0, 
                            'symbol': 'SOL', 
                            'name': 'Wrapped SOL', 
                            'decimals': 9, 
                            'address': 'So11111111111111111111111111111111111111112', 
                            'logoURI': 'https://img.fotofolio.xyz/?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsolana-labs%2Ftoken-list%2Fmain%2Fassets%2Fmainnet%2FSo11111111111111111111111111111111111111112%2Flogo.png'
                            }
                        ], 
                    'contractLabel': {
                        'address': 'BGUMAp9Gq7iTEuizy4pqaxsTyUCBK68MDfK752saRPUY', 
                        'name': 'Bubblegum', 
                        'metadata': {
                            'icon': ''
                                }
                        }
                    }, 
                {
                    'txHash': '5nx7GwpPaiEGZCbAqCgsFParJmUCBB55zXAJYMjFHvL7atyomaFVtyGtbCecGTde15CGg9XxPUBudxEr81fh3TB9', 
                    'blockNumber': 246681146, 
                    'blockTime': '2024-02-07T15:41:31+00:00', 
                    'status': True, 
                    'from': 'DRiPPP2LytGjNZ5fVpdZS7Xi1oANSY3Df1gSxvUKpzny', 
                    'to': 'BGUMAp9Gq7iTEuizy4pqaxsTyUCBK68MDfK752saRPUY', 
                    'fee': 5020, 
                    'mainAction': 'unknown', 
                    'balanceChange': [
                        {
                            'amount': 0, 
                            'symbol': 'SOL', 
                            'name': 'Wrapped SOL', 
                            'decimals': 9, 
                            'address': 'So11111111111111111111111111111111111111112', 
                            'logoURI': 'https://img.fotofolio.xyz/?url=https%3A%2F%2Fraw.githubusercontent.com%2Fsolana-labs%2Ftoken-list%2Fmain%2Fassets%2Fmainnet%2FSo11111111111111111111111111111111111111112%2Flogo.png'
                            }
                        ], 
                    'contractLabel': {
                        'address': 'BGUMAp9Gq7iTEuizy4pqaxsTyUCBK68MDfK752saRPUY', 
                        'name': 'Bubblegum', 
                        'metadata': {
                            'icon': ''
                            }
                        }
                    },
                    ...
                ]
            }
    '''
    def wallet_txn_hist_chains(self, wallet_addr):
        func_name = 'wallet_txn_hist_chains'

        if not self.api_paid_key:
            print('this call {} requires a paid key...'.format(func_name))
            exit()

        out_data = None

        api_url = self.base_url_v1.format("wallet/multichain_tx_list")
        headers = self.headers_other
        cost = 165

        params = {}
        params['wallet'] = wallet_addr

        data = self.req_other(api_url, headers=headers, params=params, cost=cost)
#        print(type(data))
#        print(data)

        out_data = data

        return out_data


#<=====>#


# Transaction Simulation                      125 https://public-api.birdeye.so/v1/wallet/simulate                   
    '''
        [
            'solana',
            'ethereum',
            'arbitrum',
            'avalanche',
            'bsc',
            'optimism',
            'polygon',
            'base',
            'zksync'
            ]
    '''
    def txn_sim(self, from_addr, to_addr, val, data):
        func_name = 'txn_sim'

        if not self.api_paid_key:
            print('this call {} requires a paid key...'.format(func_name))
            exit()

        out_data = None

        api_url = self.base_url_v1.format("wallet/simulate ")
        headers = self.headers_other
        cost = 125

        params = {}
        params['from']   = from_addr
        params['to']     = to_addr
        params['value']  = val
        params['data']   = data

        data = self.req_other(api_url, headers=headers, params=params, cost=cost)
#        print(type(data))
#        print(data)

        out_data = data

        return out_data


#<=====>#
# Functions
#<=====>#


def test_main(be):
    print('test_main()')

    test_free_working_yn = 'Y'
    test_free_broken_yn  = 'Y'

    test_prem_working_yn = 'Y'
    test_prem_broken_yn  = 'Y'

    test_other_working_yn = 'Y'
    test_other_broken_yn  = 'Y'


    if test_free_working_yn == 'Y': test_free_working(be)
    if test_free_broken_yn  == 'Y': test_free_broken(be)

    if test_prem_working_yn == 'Y': test_prem_working(be)
    if test_prem_broken_yn  == 'Y': test_prem_broken(be)

    if test_other_working_yn == 'Y': test_other_working(be)
    if test_other_broken_yn  == 'Y': test_other_broken(be)

    print('useage costs : {}'.format(be.session_costs))


#<=====>#

def test_free_working(be):
    print('test_free_working()')

    # works
    print('')
    print('public amm_support')
    data = be.amm_support()
    pprint(data)

    # works
    print('')
    print('public tkn_list')
    data = be.tkn_list(tkns_size=10, sort_by="v24hChangePercent", sort_type="desc")
    pprint(data)

    # works
    print('')
    print('public tkn_exists')
    data = be.tkn_exists(tkn_addr="So11111111111111111111111111111111111111112")
    pprint(data)

    # works
    print('')
    print('public tkn_prc')
    data = be.tkn_prc(tkn_addr="So11111111111111111111111111111111111111112")
    pprint(data)

    # works
    print('')
    print('public tkn_prc_hist')
    data = be.tkn_prc_hist(tkn_addr="So11111111111111111111111111111111111111112", time_from=1700000000, time_to=1707247534)
    pprint(data)

    # works
    print('')
    print('public pair_prc_hist')
    data = be.pair_prc_hist(pair_addr="3ne4mWqdYuNiYrYZC9TrA3FcfuFdErghH97vNPbjicr1", time_from=1700000000, time_to=1707247534)
    pprint(data)

    # works
    print('')
    print('public tkn_prc_mult')
    addr_list = []
    addr_list.append("So11111111111111111111111111111111111111112")
    addr_list.append("mSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So")
    data = be.tkn_prc_mult(tkn_addr_list=addr_list)
    pprint(data)

    pass


#<=====>#


def test_prem_working(be):
    print('test_prem_working()')

    # works
    print('')
    print('premium prem_req_hist')
    data = be.prem_req_hist()
    pprint(data)

    # works
    print('')
    print('premium tkn_list')
    data = be.prem_tkn_list(tkns_size=10, sort_by="v24hChangePercent", sort_type="desc")
    pprint(data)

    # works
    print('')
    print('premium prem_tkn_security')
    data = be.prem_tkn_security(tkn_addr="So11111111111111111111111111111111111111112")
    pprint(data)

    # works
    print('')
    print('premium prem_tkn_overview')
    data = be.prem_tkn_overview(tkn_addr="So11111111111111111111111111111111111111112")
    pprint(data)

    # works
    print('')
    print('premium prem_tkn_creation')
    data = be.prem_tkn_creation(tkn_addr="BULLa6g9e5UCuTXC5Z3Cf7s7CgvJhnJfY71DwipSmF8w")
    pprint(data)

    # works
    print('')
    print('premium prem_ohlcv')
    data = be.prem_ohlcv_tkn(tkn_addr="BULLa6g9e5UCuTXC5Z3Cf7s7CgvJhnJfY71DwipSmF8w", freq='1m', time_from=1707337311, time_to=1707337911)
    pprint(data)
    print('')
    print('premium prem_ohlcv')
    df = be.prem_ohlcv_tkn(tkn_addr="BULLa6g9e5UCuTXC5Z3Cf7s7CgvJhnJfY71DwipSmF8w", freq='1m', time_from=1707337311, time_to=1707337911, out_df_tf=True)
    print(df)

    # works
    print('')
    print('premium pair_ohlcv')
    data = be.prem_ohlcv_pair(pair_addr="3ne4mWqdYuNiYrYZC9TrA3FcfuFdErghH97vNPbjicr1", freq='1m', time_from=1707337311, time_to=1707337911)
    pprint(data)
    print('')
    print('premium pair_ohlcv')
    df = be.prem_ohlcv_pair(pair_addr="3ne4mWqdYuNiYrYZC9TrA3FcfuFdErghH97vNPbjicr1", freq='1m', time_from=1707337311, time_to=1707337911, out_df_tf=True)
    print(df)


    # works
    print('')
    print('premium pair_quote_ohlcv')
    data = be.prem_ohlcv_quote(base_addr="So11111111111111111111111111111111111111112", quote_addr="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v", freq='1m', time_from=1707337311, time_to=1707337911)
    pprint(data)
    print('')
    print('premium pair_quote_ohlcv')
    data = be.prem_ohlcv_quote(base_addr="So11111111111111111111111111111111111111112", quote_addr="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v", freq='1m', time_from=1707337311, time_to=1707337911, out_df_tf=True)
    pprint(data)


    # works
    print('')
    print('premium tkn_prc')
    data = be.prem_tkn_prc(tkn_addr="So11111111111111111111111111111111111111112")
    pprint(data)

    # works
    print('')
    print('premium tkn_prc_mult')
    addr_list = []
    addr_list.append("So11111111111111111111111111111111111111112")
    addr_list.append("mSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So")
    data = be.prem_tkn_prc_mult(tkn_addr_list=addr_list)
    pprint(data)

    # works
    print('')
    print('premium tkn_prc_hist')
    data = be.prem_tkn_prc_hist(tkn_addr="So11111111111111111111111111111111111111112", freq='1m', time_from=1707337311, time_to=1707337911)
    pprint(data)

    # works
    print('')
    print('premium pair_prc_hist')
    data = be.prem_pair_prc_hist(pair_addr="3ne4mWqdYuNiYrYZC9TrA3FcfuFdErghH97vNPbjicr1", freq='1m', time_from=1707337311, time_to=1707337911)
    pprint(data)

    # works
    print('')
    print('premium tkn_trds')
    data = be.prem_tkn_trds(tkn_addr="So11111111111111111111111111111111111111112", txn_type='all', trds_size=5)
    pprint(data)

    # works
    print('')
    print('premium pair_trds')
    data = be.prem_pair_trds(pair_addr="3ne4mWqdYuNiYrYZC9TrA3FcfuFdErghH97vNPbjicr1", txn_type='all', sort_type='desc', trds_size=5)
    pprint(data)

    pass


#<=====>#


def test_other_working(be):
    print('test_other_working()')

    # works
    print('')
    print('premium ntwk_support')
    data = be.ntwk_support()
    pprint(data)

    # works
    print('')
    print('premium wallet_port')
    data = be.wallet_port(wallet_addr=be.wallet_addr)
    pprint(data)

    # works
    print('')
    print('premium wallet_port_chains')
    data = be.wallet_port_chains(wallet_addr=be.wallet_addr)
    pprint(data)

    # works
    print('')
    print('premium wallet_tkn_bal')
    data = be.wallet_tkn_bal(wallet_addr=be.wallet_addr, tkn_addr="EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm")
    pprint(data)

    # works
    print('')
    print('premium wallet_tkn_bal')
    data = be.wallet_tkn_bal(wallet_addr=be.wallet_addr, tkn_addr="AZsHEMXd36Bj1EMNXhowJajpUXzrKcK57wW4ZGXVa7yR")
    pprint(data)

    # works
    print('')
    print('premium wallet_txn_hist')
    data = be.wallet_txn_hist(wallet_addr=be.wallet_addr)
    print(data)

    # works
    print('')
    print('premium wallet_txn_hist_chains')
    data = be.wallet_txn_hist_chains(wallet_addr=be.wallet_addr)
    print(data)

    pass


#<=====>#

def test_free_broken(be):
    print('test_free_broken()')

    pass


#<=====>#


def test_prem_broken(be):
    print('test_prem_broken()')

    pass

#<=====>#


def test_other_broken(be):
    print('test_other_broken()')


    # no idea how to populate val and data
    print('')
    print('premium txn_sim')
    data = be.txn_sim(from_addr="", to_addr="", val="", data="")
    pprint(data)

    pass


#<=====>#
# Assignments Post
#<=====>#


# Or Use the DOTENV
free_key  = 'PutYourFreeChainHere'
paid_key  = 'PutYourPaidChainHere'
wallet_addr  = 'PutYourWalletAddrHere'

be = BIRDEYE(chain='solana', api_free_key=free_key, api_paid_key=paid_key, wallet_addr=wallet_addr, throttle=0.25)

#<=====>#
# Default Run
#<=====>#

if __name__ == "__main__":
    be = test_main(be)


#<=====>#

