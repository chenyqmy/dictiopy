#!/usr/bin/python3
# -*- coding: utf-8 -*-
# author: Chen Yu-Qiao

import json
import requests
import click

URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"


def parse(data):
    first_line=''
    all_meanings=[]
    all_examples=['Examples--------------------']
    all_synonyms=[]
    first_line += data[0]['word'] + '  '
    if "phonetic" in data[0]:
        first_line += data[0]["phonetic"]

    elif "phonetics" in data[0]:
        for j in data[0]["phonetics"]:
            if "text" in j:
                first_line += j["text"]
                break   
            else:
                first_line += ''


    #parse meanings and examples into a list
    for obj in data:
        if len(data) != 1:
            all_meanings.append(f"Etymology: {data.index(obj) + 1}")
        meanings = obj["meanings"]
        i = 0
        for n in range(len(meanings)):
            word_type = meanings[n]["partOfSpeech"]
            all_meanings.append(word_type.capitalize())
            for m in range(len(meanings[n]["definitions"])):
                i += 1
                meaning = meanings[n]["definitions"][m]["definition"]
                all_meanings.append(f"{i}. {meaning}")
                
                if 'example' in meanings[n]["definitions"][m]:
                    all_examples.append(meanings[n]["definitions"][m]["example"])

    
    #parse synonyms into one string
    for obj in data:
        meanings = obj["meanings"]
        for n in range(len(meanings)):
            all_synonyms.extend(meanings[n]["synonyms"])


    return first_line, all_meanings, all_examples, all_synonyms


@click.command()
@click.argument('word')
@click.option('-a',is_flag=True,help='show all information')
@click.option('-e',is_flag=True,help='show examples only')
@click.option('-s',is_flag=True,help='show synonyms only')
def main(word,a,e,s):
    """
    Look up english words in online dictionary api.\n
    date: 2022-11-10
    author: Chen Yu-Qiao
    """
    try:
        word = word.encode("utf-8")

        header = {"Accept": "charset=utf-8"}

        url = URL + word.decode("utf-8")

        response = requests.request("GET", url, headers=header)

        data = json.loads(response.text.encode("utf-8"))

        first_line, all_meanings, all_examples, all_synonyms = parse(data)

        if a:
            click.echo(first_line)
            click.echo('\n'.join(all_meanings))
            click.echo('\n'.join(all_examples))
            click.echo('Synonyms--------------------')
            click.echo(' '.join(all_synonyms))

        elif e and (a is False):
            click.echo(first_line)
            click.echo('\n'.join(all_examples))
        elif s and (a is False):
            click.echo(first_line)
            click.echo('Synonyms--------------------')
            click.echo(' '.join(all_synonyms))                   
        else:
            click.echo(first_line)
            click.echo('\n'.join(all_meanings))

    except KeyError:
        print(
            "Sorry, We cannot find this word!"
        )
        return


if __name__ == "__main__":
    main()