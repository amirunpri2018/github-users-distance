
def check_followers_following(first_user, second_user, access_session):
    url_followers = "/users/{0}/followers".format(second_user)
    url_following = "/users/{0}/following".format(second_user)
    list_of_followers = access_session.get(url_followers)
    list_of_following = access_session.get(url_following)

    is_followers = [x for x in list_of_followers.json() if x['login'] == first_user]
    is_following = [x for x in list_of_following.json() if x['login'] == first_user]

    if is_followers != []:
        return is_followers
    elif is_following != []:
        return is_following
    else:
        return "User wasn't find in followers and following list!"
