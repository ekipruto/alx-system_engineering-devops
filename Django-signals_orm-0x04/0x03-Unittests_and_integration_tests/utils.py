#!/usr/bin/env python3
"""Utility functions for GithubOrgClient"""

import requests


def get_json(url):
    """Fetch JSON data from a given URL"""
    response = requests.get(url)
    return response.json()
