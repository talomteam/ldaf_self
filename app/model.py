#!/usr/bin/python3
# import class and constants
from ast import Try
import ssl
import json
#from jsondb import Database
from ldap3 import Tls, NTLM, Connection, Server, SUBTREE, MODIFY_REPLACE
#from slackclient import SlackClient

# ===============

file = open("src/config.json")
variables = json.loads(file.read())

# ===============

#SLACK_BOT_TOKEN = variables['SLACK_BOT_TOKEN']          #
# slack_db = "src/" + variables['slack_db']               # slack db users

#db = Database(slack_db)

#sc = SlackClient(SLACK_BOT_TOKEN)

# ===============


def disconnect():
    """
    Force to disconnect the ldap connection with the server.
    """
    pass


def conx(domain, domain_name, user, passwd):
    """
    Connection to the server
    """
    tls_configuration = Tls(validate=ssl.CERT_NONE,
                            version=ssl.PROTOCOL_TLSv1_2)

    # define the server and the connection
    s = Server(domain, port=636, use_ssl=True, tls=tls_configuration)

    conn = Connection(s, domain_name + "\\" + user,
                      passwd, authentication=NTLM)
    conn.start_tls()
    conn.bind()

    # perform the Bind operation
    try:
        if not conn.bind():
            conn.unbind()
            raise ValueError("Invalid credentials")
    finally:
        pass

    # print("Connected")

    return conn


def search_slack_id(email):
    for users in db['members']:
        # print(users)
        if not (users['is_bot'] and users['deleted']):
            # noinspection PyBroadException
            try:
                if users['profile']['email'] == email:
                    # print(users['id'], users['profile']['email'])
                    return users['id']
            except:
                print("User with this email: " + email + " no found!!")


def search_userx(username, conn, basedn):
    """
        Verifies credentials for username and password.
        Returns True on success or False on failure
    """
    global user_dn
    SEARCHFILTER = '(&(|' \
                   '(userPrincipalName=' + username + ')' \
                                                      '(samaccountname=' + username + ')' \
                                                                                      '(mail=' + username + '))' \
                                                                                                            '(objectClass=person))'
    print(SEARCHFILTER)
    # SEARCHFILTER_DEFAULT = '(objectClass=person)'

    conn.search(search_base=basedn, search_filter=SEARCHFILTER,
                search_scope=SUBTREE, attributes=['cn',
                                                  'mail'], paged_size=5)
    for entry in conn.response:
        # print(entry)
        # user_dn1 = entry.get("dn")
        user_mail = entry.get("attributes")["mail"]
        if entry.get("dn") and entry.get("attributes"):
            if entry.get("attributes").get("cn"):
                user_dn = entry.get("dn")

        return user_dn


def authenticate(domain, domain_name, username, password):
    """
    Verifies credentials for username and password.
    Returns True on success or False on failure
    """

    tls_configuration = Tls(validate=ssl.CERT_NONE,
                            version=ssl.PROTOCOL_TLSv1_2)
    # define the server and the connection
    s = Server(domain, port=636, use_ssl=True, tls=tls_configuration)
    conn = Connection(s, domain_name + "\\" + username,
                      password, authentication=NTLM)
    conn.start_tls()
    conn.bind()
    # print(conn.usage)
    # perform the Bind operation
    try:
        if not conn.bind():
            print("Not Connected")
            conn.unbind()
            return False
        else:
            print("Connected")
            conn.unbind()
            return True
    finally:
        pass


def reset_passwd(domain, user_admin, passwd_admin, basedn, username, current, new_passwd, domain_name, enable):
    """
    Verifies credentials for username and password.
    Returns True on success or False on failure
    """

    conn = conx(domain, domain_name, user_admin, passwd_admin)
    user = search_userx(username, conn, basedn)

    try:
        if not authenticate(domain, domain_name, username, current):
            print("unauth")
            return False
        else:
            # perform the Bind operation

            enc_pwd = '"{}"'.format(new_passwd).encode('utf-16-le')

            changes = {'unicodePwd': [(MODIFY_REPLACE, [enc_pwd])]}

            x = conn.modify(user, changes=changes)

            print(x)
            # Slack Notification for the user
            if enable:
                x = search_slack_id(email)

                result = sc.api_call("chat.postMessage", channel=x,
                                     text="You password was reset! testing :) not panic :tada:", as_user=True)

                print("Result: ", result['ok'])
            else:
                pass

        # a new password is set, hashed with sha256 and a random salt
        return True

    finally:
        conn.unbind()


def new_user(domain, user_admin, passwd_admin, basedn, domain_name, user):
    try:
        conn = conx(domain, domain_name, user_admin, passwd_admin)
        userdn = "CN={},OU={},{}".format(
            user['username'], user['level'], basedn)
        print(userdn)
        entry = {
            "objectClass": ["person", "organizationalPerson", "user", "top"],
            "sAMAccountName": user['username'],
            "displayName": user['username'],
            'userPrincipalName': "{}@{}".format(user['username'], domain_name),
            "givenname": user['firstname'],
            "sn": user['lastname'],
            "mail": user['email'],
            "employeeID": str(user['idcard']),
            "telephoneNumber": str(user['telephone']),
            "mobile": str(user['mobile']),
            "Description": str(user['position']),
            "Department": str(user['department']),
            "Company": str(user['office']),
            "Street": str(user['branch'])
        }
        print(entry)
        conn.add(userdn, attributes=entry)
        conn.extend.microsoft.modify_password(userdn, user['password'])
        conn.modify(userdn, {'userAccountControl': [('MODIFY_REPLACE', 512)]})
        conn.unbind()
        return True
    except:
        conn.unbind()
        return False


def reset_pwd_user(domain, user_admin, passwd_admin, basedn, domain_name, user):
    conn = conx(domain, domain_name, user_admin, passwd_admin)
    user = search_userx(user['username'], conn, basedn)
    if user:
        try:
            enc_pwd = '"{}"'.format(user['password']).encode('utf-16-le')

            changes = {'unicodePwd': [(MODIFY_REPLACE, [enc_pwd])]}

            x = conn.modify(user, changes=changes)
        finally:
            conn.unbind()

    return True


# =================================================
