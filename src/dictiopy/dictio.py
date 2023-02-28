#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
import click


API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"

def parse(data):
    first_line = f"{data[0]['word']}  "
    phonetic = data[0].get('phonetic') or data[0].get('phonetics', [{}])[0].get('text', '')
    first_line += phonetic

    all_meanings = []
    all_examples = ['Examples--------------------']
    all_synonyms = []

    for obj in data:
        if len(data) != 1:
            all_meanings.append(f"Etymology: {data.index(obj) + 1}")
        meanings = obj["meanings"]
        for n, meaning in enumerate(meanings):
            word_type = meaning["partOfSpeech"].capitalize()
            all_meanings.append(word_type)
            for m, definition in enumerate(meaning["definitions"], start=1):
                meaning_text = definition["definition"]
                all_meanings.append(f"{m}. {meaning_text}")
                if 'example' in definition:
                    example_text = definition["example"]
                    all_examples.append(example_text)
                if 'synonyms' in definition:
                    synonyms = definition["synonyms"]
                    all_synonyms.extend(synonyms)

    return first_line, all_meanings, all_examples, all_synonyms


@click.command()
@click.argument('word')
@click.option('-a',is_flag=True,help='show all information')
@click.option('-e',is_flag=True,help='show examples only')
@click.option('-s',is_flag=True,help='show synonyms only')
def main(word,a,e,s):
    """
    Look up English words in online dictionary api.
    """
    try:
        # use UTF-8 encoding by default, no need to encode/decode
        headers = {"Accept": "charset=utf-8"}
        url = API_URL + word
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()

        first_line, all_meanings, all_examples, all_synonyms = parse(data)

        if a:
            click.echo(first_line)
            click.echo('\n'.join(all_meanings))
            click.echo('\n'.join(all_examples))
            click.echo('Synonyms--------------------')
            click.echo(', '.join(all_synonyms))

        elif e:
            click.echo(first_line)
            click.echo('\n'.join(all_examples))

        elif s:
            click.echo(first_line)
            click.echo('Synonyms--------------------')
            click.echo(', '.join(all_synonyms))                   

        else:
            click.echo(first_line)
            click.echo('\n'.join(all_meanings))

    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 404:
            click.echo(f"Sorry, We cannot find the word '{word}'")
        else:
            click.echo(f"An error occurred: {err}")
    
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        click.echo("Connection error. Please check your internet connection.")
    
    except json.JSONDecodeError:
        click.echo("Failed to decode the response. Please try again later.")


if __name__ == "__main__":
    main()
