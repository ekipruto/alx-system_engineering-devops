#!/usr/bin/env python3
"""Fixtures for integration tests"""

org_payload = {
    "login": "google",
    "id": 1342004,
    "repos_url": "https://api.github.com/orgs/google/repos",
}

repos_payload = [
    {
        "id": 7697149,
        "name": "episodes.dart",
        "license": {"key": "apache-2.0"},
    },
    {
        "id": 8566970,
        "name": "kratu",
        "license": {"key": "apache-2.0"},
    },
    {
        "id": 123,
        "name": "something_else",
        "license": {"key": "mit"},
    },
]

expected_repos = ["episodes.dart", "kratu", "something_else"]

apache2_repos = ["episodes.dart", "kratu"]
