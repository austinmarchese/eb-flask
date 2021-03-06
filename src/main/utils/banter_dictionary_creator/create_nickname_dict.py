import json
import re

import requests
from bs4 import BeautifulSoup

from src.main.utils.nlp_conversion_util import NLPConversionUtil
import os
from os.path import dirname, realpath

BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(dirname(realpath(__file__)))))
SAVE_LOCATION = '%s/resources/reference_dict' % BASEDIR

def create_nba_nicknames_dict():
    """
    Source: https://en.wikipedia.org/wiki/List_of_nicknames_used_in_basketball
    :return: Nickname dict format:
    {
    nickname: Player Name
    The King: Lebron James
    }
    """
    url = "https://en.wikipedia.org/wiki/List_of_nicknames_used_in_basketball"
    # desktop user-agent
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    # mobile user-agent
    MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
    headers = {"user-agent": USER_AGENT}
    resp = requests.get(url, headers=headers)
    nickname_dict = {}
    if resp.status_code == 200:
        print(resp.content)
        soup = BeautifulSoup(resp.content, "html.parser")

    for index, value in enumerate(soup.findAll('li')):
        try:
            name_nickname_split: list = value.text.split(' – ')
            first_name = name_nickname_split[0]
            # Sample Format ' "Splash Brothers" (Curry and Klay Thompson), "Baby-Faced Assassin", "Chef Curry", "Steph", "The Golden Boy"'
            # Splitting between quotes, and taking odd values
            nick_names = name_nickname_split[1].split('"')[1::2]
            for i in nick_names:
                nickname_dict[NLPConversionUtil().normalize_text(i)] = NLPConversionUtil.normalize_text(first_name)

        except Exception as e:
            print(e)

    return nickname_dict


def create_nfl_nicknames_dict():
    """
    Source: https://en.wikipedia.org/wiki/List_of_baseball_nicknames

    :return: Nickname dict format:
    {
    nickname: Player Name
    The King: Lebron James
    }
    """
    url = "https://en.wikipedia.org/wiki/List_of_NFL_nicknames"
    # desktop user-agent
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    # mobile user-agent
    MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
    headers = {"user-agent": USER_AGENT}
    resp = requests.get(url, headers=headers)
    nickname_dict = {}
    if resp.status_code == 200:
        print(resp.content)
        soup = BeautifulSoup(resp.content, "html.parser")

    for index, value in enumerate(soup.findAll('tr')):
        try:
            name_nickname_split: list = value.text.split('\n')[1::2]  # Getting Between Values
            first_name = name_nickname_split[1]

            # Sample Format ' "Splash Brothers" (Curry and Klay Thompson), "Baby-Faced Assassin", "Chef Curry", "Steph", "The Golden Boy"'
            # Splitting between quotes, and taking odd values
            if '[' in name_nickname_split[0]:
                nick_names = re.sub(r'\[.*?\]', '', name_nickname_split[0])
                if ' or ' in nick_names:
                    nick_names = nick_names.split(' or ')
                    for i in nick_names:
                        nickname_dict[NLPConversionUtil().normalize_text(i)] = NLPConversionUtil.normalize_text(
                            first_name)

                if '/' in nick_names:
                    nick_names = nick_names.split('/')
                    for i in nick_names:
                        nickname_dict[NLPConversionUtil().normalize_text(i)] = NLPConversionUtil.normalize_text(
                            first_name)

        except Exception as e:
            print(e)

    return nickname_dict


def create_mlb_nicknames_dict():
    """
    Source: https://en.wikipedia.org/wiki/List_of_baseball_nicknames

    :return: Nickname dict format:
    {
    nickname: Player Name
    The King: Lebron James
    }
    """
    url = "https://en.wikipedia.org/wiki/List_of_baseball_nicknames"
    # desktop user-agent
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    # mobile user-agent
    MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
    headers = {"user-agent": USER_AGENT}
    resp = requests.get(url, headers=headers)
    nickname_dict = {}
    if resp.status_code == 200:
        print(resp.content)
        soup = BeautifulSoup(resp.content, "html.parser")

    for index, value in enumerate(soup.findAll('li')):
        try:
            name_nickname_split: list = value.text.split(': ')
            first_name = name_nickname_split[0]
            if "(" in first_name:
                first_name = first_name.split(" (")[0]
            # Sample: "Hammerin' Hank": 'Hank Aaron, Henry Louis Aaron'
            if "," in first_name:
                first_name = first_name.split(", ")[0]
            # Sample Format ' "Splash Brothers" (Curry and Klay Thompson), "Baby-Faced Assassin", "Chef Curry", "Steph", "The Golden Boy"'
            # Splitting between quotes, and taking odd values
            if '"' in name_nickname_split[1]:
                nick_names = name_nickname_split[1].split('"')[1::2]
                for i in nick_names:
                    nickname_dict[NLPConversionUtil().normalize_text(i)] = NLPConversionUtil.normalize_text(first_name)

        except Exception as e:
            print(e)

    return nickname_dict

def save_dict(dictionary, file_name):
    tmp_json = json.dumps(dictionary)
    f = open(f"{SAVE_LOCATION}/{file_name}.json", "w")
    f.write(tmp_json)
    f.close()

def create_nickname_dict():
    nickname_dict = create_nba_nicknames_dict()
    save_dict(nickname_dict, "NBA_nickname_dict")

    mlb_nickname_dict = create_mlb_nicknames_dict()
    save_dict(mlb_nickname_dict, "MLB_nickname_dict")

    nfl_nickname_dict = create_nfl_nicknames_dict()
    save_dict(nfl_nickname_dict, "NFL_nickname_dict")
