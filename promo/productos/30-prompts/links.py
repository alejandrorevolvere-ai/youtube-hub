# -*- coding: utf-8 -*-
"""Helper de enlaces UTM del pack."""
BASE = "https://senalabierta.pages.dev"
UTM = "?utm_source=kofi&utm_medium=shop&utm_campaign=pack30"


def link(slug):
    return f"{BASE}/v/{slug}/{UTM}"
