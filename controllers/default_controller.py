import logging
FORMAT = '%(asctime)-15s %(funcName)s %(message)s'
logging.basicConfig(format=FORMAT)
LOG = logging.getLogger()
LOG.setLevel(logging.INFO)

USERS = {}
GROUPS = {}
CREDENTIALS = {}

_SEP = ":::"

def _STORAGEKEY(storageId, key):
    return storageId + _SEP + key


def add_user_credentials(uid, storageId, credentials) -> str:
    """
    Add credentials for a user on specific storage.
    """
    try:
        CREDENTIALS[_STORAGEKEY(storageId, uid)] = credentials
        LOG.info("Added credentials for "+uid)
    except:
        LOG.error("Invalid credentials format: " + credentials)
        return "Invalid credentials format", 400
    return "OK", 204

def add_user_details(uid, userDetails) -> str:
    """
    Add user details.
    """
    try:
        LOG.info("Added user: "+ str(userDetails))
        USERS[uid] = userDetails
    except:
        LOG.error("Invalid user details format: " + str(userDetails))
        return "Invalid user details format", 400
    return "OK", 204

def delete_user_credentials(uid, storageId) -> str:
    """
    Delete user credentials to specific storage.
    """
    if _STORAGEKEY(storageId, uid) in CREDENTIALS:
        LOG.info("Removing user credentials: " + uid + ", " + storageId)
        del CREDENTIALS[_STORAGEKEY(storageId, uid)]
        return "OK", 204
    else:
        LOG.warning("Credentials not found for user " + uid
                    + " to storage " + storageId)
        return "Credentials not found", 404

def get_user_details(uid) -> str:
    """
    Return specific user details.
    """
    if uid in USERS:
        return USERS[uid], 200
    else:
        LOG.warning("User " + uid + " not found")
        return "User not found", 404

def delete_user_details(uid) -> str:
    """
    Removes specific user details.
    """
    if uid in USERS:
        del USERS[uid]
        return "OK", 200
    else:
        LOG.warning("User " + uid + " not found")
        return "User not found", 404

def map_group(groupIdentityRequest) -> str:
    """
    Returns local storage group based on federated group Id.
    """
    gid = groupIdentityRequest['groupIdentity']['groupId']
    sid = groupIdentityRequest['storageId']

    LOG.info("Mapping group " + gid + " to storage " + sid)
    LOG.info("GROUPS: " + str(GROUPS))

    if _STORAGEKEY(sid, gid) in GROUPS:
        return GROUPS[_STORAGEKEY(sid, gid)], 200
    else:
        LOG.warning("Group " + gid + " not found on storage " + sid)
        return "Group not found", 404

def map_user_credentials(userCredentialsRequest) -> str:
    """
    Return user credentials to specific storage.
    """
    try:
        LOG.info("Requested mapping for: " + str(userCredentialsRequest))
        credentials_id = _STORAGEKEY(userCredentialsRequest['storageId'],
                     userCredentialsRequest['userDetails']['id'])

        if credentials_id in CREDENTIALS:
            return CREDENTIALS[credentials_id], 200
        else:
            LOG.warning("Credentials not found")
            return "Credentials not found", 404
    except:
        LOG.error("Invalid request: " + str(userCredentialsRequest))
        return "Invalid request", 400

def resolve_group(groupDetails) -> str:
    """
    Resolve group id based on storage id or name
    """

    try:
        for group_key, group_details in GROUPS.items():
            storage_id = group_key.split(_SEP)[0]
            group_id = group_key.split(_SEP)[1]

            result = {'idp': 'onedata', 'groupId': group_id}

            if groupDetails['storageId'] != storage_id:
                continue

            if 'gid' in groupDetails and 'gid' in group_details and\
                groupDetails['gid'] == group_details['gid']:
                return result
            elif 'name' in groupDetails and 'name' in group_details and\
                groupDetails['name'] == group_details['name']:
                return result

        return "Group not found", 404
    except:
        LOG.error("Invalid request: " + str(groupDetails))
        return "Invalid request", 400

def resolve_user_identity(userStorageCredentials) -> str:
    """
    Return user identity based on specific storage.
    """
    storage_id = userStorageCredentials['id']
    storage_type = userStorageCredentials['type']

    result = None

    for credentials_id, credentials in CREDENTIALS.items():
        sid = credentials_id.split(_SEP)[0]
        uid = credentials_id.split(_SEP)[1]

        result = {'idp': 'onedata', 'userId': uid}

        if storage_id != sid or storage_type != credentials['type']:
            continue

        if storage_type == 'posix':
            if credentials['uid'] == userStorageCredentials['uid'] \
                    or credentials['name'] == userStorageCredentials['name']:
                   return result, 200
        elif storage_type == 'ceph':
            if credentials['username'] == userStorageCredentials['username']:
                return result, 200
        elif storage_type == 's3':
            if credentials['accessKey'] == userStorageCredentials['accessKey']:
                return result, 200
        elif storage_type == 'swift':
            if credentials['username'] == userStorageCredentials['username']:
                return result, 200
        elif storage_type == 'glusterfs':
            if credentials['uid'] == userStorageCredentials['uid']:
                return result, 200
        else:
            continue

    return "Credentials not found", 404

def get_group_mapping(gid, storageId) -> str:
    """
    Return specific group mapping.
    """
    if _STORAGEKEY(storageId, gid) in GROUPS:
        return GROUPS[_STORAGEKEY(storageId, gid)], 200
    else:
        LOG.warning("Group " + gid + " not found on storage " + storageId)
        return "Group not found", 404

def add_group_mapping(gid, storageId, groupDetails) -> str:
    """
    Add group mapping.
    """
    try:
        LOG.info("Added group: "+ str(groupDetails))
        GROUPS[_STORAGEKEY(storageId, gid)] = groupDetails
    except:
        LOG.error("Invalid group details format: " + str(groupDetails))
        return "Invalid group details format", 400
    return "OK", 204

def delete_group_mapping(gid, storageId) -> str:
    """
    Delete group mapping.
    """
    if _STORAGEKEY(storageId, gid) in GROUPS:
        LOG.info("Removing group mapping: " + gid)
        del GROUPS[_STORAGEKEY(storageKey, gid)]
        return "OK", 204
    else:
        LOG.warning("Group not found: " + gid)
        return "Group not found", 404
