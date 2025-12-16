#!/usr/bin/env python3
"""GithubOrgClient module"""

from utils import get_json  # ✅ Import from utils, not define locally
import requests


class GithubOrgClient:
    """Client for GitHub organization information"""

    ORG_URL = "https://api.github.com/orgs/{}"

    def __init__(self, org_name):
        self.org_name = org_name

    @property
    def org(self):
        """Fetch organization information"""
        return get_json(self.ORG_URL.format(self.org_name))

    @property
    def _public_repos_url(self):
        """Fetch the public repos URL"""
        return self.org.get("repos_url")

    def public_repos(self, license=None):
        """List public repositories"""
        repos = get_json(self._public_repos_url)
        repo_names = [repo["name"] for repo in repos]

        if license:
            repo_names = [
                repo["name"] for repo in repos
                if repo.get("license", {}).get("key") == license
            ]
        return repo_names
    def has_license(self, repo, license_key):
        """Check if repo has the specified license"""
        if "license" not in repo:
            return False
        return repo.get("license", {}).get("key") == license_key