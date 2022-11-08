#!/usr/bin/python3
# -*- coding: utf-8 -*-
# author: Chen Yu-Qiao

import json
import requests
import sys

URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"


def meaning(data):
    for obj in data:
        if len(data) != 1:
            print("Etymology:", data.index(obj) + 1)
        meanings = obj["meanings"]
        i = 0
        for n in range(len(meanings)):
            word_type = meanings[n]["partOfSpeech"]
            print(word_type.capitalize())
            for m in range(len(meanings[n]["definitions"])):
                i += 1
                meaning = meanings[n]["definitions"][m]["definition"]
                print(f"{i}. {meaning}")


def main(word):
    try:
        word = word.encode("utf-8")

        header = {"Accept": "charset=utf-8"}

        url = URL + word.decode("utf-8")

        response = requests.request("GET", url, headers=header)

        data = json.loads(response.text.encode("utf-8"))

        print(data[0]["word"], end="  ")
        if "phonetic" in data[0]:
            print(data[0]["phonetic"])
        elif "phonetics" in data[0]:
            for j in data[0]["phonetics"]:
                if "text" in j:
                    print(j["text"])
                    break
        else:
            print()

        meaning(data)
    except KeyError:
        print(
            "Sorry, We cannot find this word! Verify if you're typing the correct language."
        )
        return


if __name__ == "__main__":

    main(sys.argv[1])
