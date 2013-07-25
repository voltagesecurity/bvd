#
# BVD LDAP Configuration File
#   Add the appropriate values to this file to match your LDAP configuration
#

import ldap
from django_auth_ldap.config import LDAPSearch, LDAPSearchUnion

AUTH_LDAP_USER_SEARCH = LDAPSearchUnion(
    # LDAPSearch(args),
)

import logging

logger = logging.getLogger('django_auth_ldap')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

AUTH_LDAP_BIND_DN = ""
AUTH_LDAP_BIND_PASSWORD = ""
AUTH_LDAP_SERVER_URI = ""
AUTH_LDAP_USER_ATTR_MAP = {
    "username" : "",
    "first_name": "",
    "last_name": "",
    "email": ""
}