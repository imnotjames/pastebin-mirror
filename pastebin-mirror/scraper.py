import requests
import os
import sys
import xml.etree.ElementTree as ET

class PastebinComScraper:
    def __init__(self, api_key=None):
        self.__RAW_URL__ = 'https://pastebin.com/raw/'
        self.__ITEM_URL__ = 'https://pastebin.com/api_scrape_item.php'
        self.__METADATA_URL__ = 'https://pastebin.com/api_scrape_item_meta.php'
        self.__LIST_URL__ = 'https://pastebin.com/api_scraping.php'
        self.__TRENDING_URL__ = 'https://pastebin.com/api/api_post.php'
        self.__ERROR_TEXT__ = 'Error, we cannot find this paste.'
        self.__API_KEY__ = api_key

    def get_paste_content(self, key):
        try:
            result = requests.get(self.__RAW_URL__ + key)
        except Exception as e:
            print('[!] Exception making request to {}'\
                  .format(self.__RAW_URL__ + key), file=sys.stderr)
            return None

        if not result.ok:
            print('[!] Request to {} returned non-200 code'\
                  .format(self.__RAW_URL__ + key), file=sys.stderr)
            return None

        return result.content

    def get_paste_metadata(self, key):
        try:
            paste = requests.get(self.__METADATA_URL__, params={'i': key})
        except Exception as e:
            print('[!] Exception making request to {} for paste {}'\
                  .format(self.__METADATA_URL__, key), file=sys.stderr)
            return None

        if not paste.ok:
            print('[!] Request to {} returned non-200 code for paste {}'\
                  .format(self.__METADATA_URL__, key), file=sys.stderr)
            return None

        if paste.text == self.__ERROR_TEXT__:
            print('[!] Recieved "{}" for paste {}'\
                  .format(self.__ERROR_TEXT__, key), file=sys.stderr)
            return None

        return paste.json()[0]

    def get_recent_pastes(self, limit=250):
        try:
            # for some reason including limit as query object like params={limit:100} doesn't
            # work, so we are including the query params in the url
            paste_list = requests.get('{}?limit={}'.format(self.__LIST_URL__, min(250, limit)))
        except Exception as e:
            print('[!] Exception making request to {}'\
                  .format(self.__LIST_URL__), file=sys.stderr)
            return []

        if not paste_list.ok:
            print('[!] Request to {} returned non-200 code'\
                  .format(self.__LIST_URL__), file=sys.stderr)
            return []

        return paste_list.json()

    def get_trending_pastes(self):

        def trends_xml_to_json(xml_response):
            # <paste>
            #     <paste_key>QMavhK80</paste_key>
            #     <paste_date>1499490337</paste_date>
            #     <paste_title></paste_title>
            #     <paste_size>45191</paste_size>
            #     <paste_expire_date>0</paste_expire_date>
            #     <paste_private>0</paste_private>
            #     <paste_format_short>text</paste_format_short>
            #     <paste_format_long>None</paste_format_long>
            #     <paste_url>https://pastebin.com/QMavhK80</paste_url>
            #     <paste_hits>849</paste_hits>
            # </paste>
            json = []
            root = ET.fromstring('<trending>{}</trending>'.format(xml_response))
            for child in root:
                if child.tag == 'paste':
                    paste = dict()
                    for field in child:
                        if field.tag == 'paste_key': paste['key'] = field.text
                        if field.tag == 'paste_date': paste['date'] = field.text
                        if field.tag == 'paste_size': paste['size'] = field.text
                        if field.tag == 'paste_expire_date': paste['expire'] = field.text
                        if field.tag == 'paste_title': paste['title'] = field.text
                        if field.tag == 'paste_format_short': paste['syntax'] = field.text
                        if field.tag == 'paste_hits': paste['hits'] = field.text
                    json.append(paste)
            return json

        if self.__API_KEY__ is None: return []

        data = {
            'api_option': 'trends',
            'api_dev_key': self.__API_KEY__
        }

        try:
            paste_list = requests.post(self.__TRENDING_URL__, data=data)
        except Exception as e:
            print('[!] Exception making request to {}'\
                  .format(self.__TRENDING_URL__), file=sys.stderr)
            return []

        if not paste_list.ok:
            print('[!] Request to {} returned non-200 code'\
                  .format(self.__TRENDING_URL__), file=sys.stderr)
            return []

        return trends_xml_to_json(paste_list.text)
