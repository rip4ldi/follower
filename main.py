import requests, time, stdiomask, secrets, threading

# Struct
class UserData():
    def __init__ (self):
        self.username = None
        self.following_count = 0
        self.user_id = None
        self.private = False
        self.name = None
        self.followed_by_count = 0
        self.got_success = False


class Follower():
    def __init__(self):
        self.username = None
        # in case i want to use spinners
        # self.spinners = ["\\", "-", "/", "|"]
        self.session = requests.session()
        self.web_login_url = "https://instagram.com/accounts/login/ajax/"
        self.get_data_url = "https://instagram.com/{}/?__a=1"
        self.base_get_followers_url = "https://i.instagram.com/api/v1/friendships/{}/followers/?count=12&search_surface=follow_list_page"
        self.remove_follower_url = "https://www.instagram.com/web/friendships/{}/remove_follower/"
        self.unfollow_url = "https://www.instagram.com/web/friendships/{}/unfollow/"

    def remove_follower(self, follower_id: str) -> bool:
        response = self.session.post(url=self.remove_follower_url.format(follower_id)).text
        return "{\"status\":\"ok\"}" in response

    def unfollow(self) -> bool:
        response = self.session.post(url=self.unfollow_url.format(follower_id)).text
        return "{\"status\":\"ok\"}" in response

    def get_followers(self, userdata: UserData) -> list:
        # print("[+] Grabbing followers...")
        user_ids = []
        max_id = ''

        # variable for readability
        while True:
            # if the max id doesnt exist just start without the max id, else append the max id to the url
            url = self.base_get_followers_url.format(userdata.user_id) if max_id == "" else self.base_get_followers_url.format(userdata.user_id) + f"&max_id={max_id}"
            response = self.session.get(url=url, headers={"user-agent": "Instagram 113.0.0.39.122 Android (24/5.0; 515dpi; 1440x2416; 'huawei/google; Nexus 6P; angler; angler; en_US)"})

            # if there is more, append the more users to the list
            if "next_max_id" in response.text:
                max_id = response.json()["next_max_id"]

                #iterate through each username
                for user in list(response.json()["users"]):
                    user_ids.append(user["pk"])

            # otherwise, we are finished and can break out of the while loop
            else:
                break
            # i got an account banned from spamming too many requests so this is to try and prevent that
            time.sleep(2)
        return user_ids

    def get_user_data(self, user: str = None) -> UserData:
        userData = UserData()

        # if the username is empty, get the logged in username data else get whatever user was passed
        user = user if user != None else self.username
        response = self.session.get(self.get_data_url.format(user)).json()

        
        try:
            userData.followed_by_count = int(response["graphql"]["user"]["edge_followed_by"]["count"])
            userData.following_count = int(response["graphql"]["user"]["edge_follow"]["count"])
            userData.name = str(response["graphql"]["user"]["full_name"])
            userData.private = bool(response["graphql"]["user"]["is_private"])
            userData.user_id = str(response["graphql"]["user"]["id"])
            userData.username = str(response["graphql"]["user"]["username"])
            userData.got_success = True
        except requests.exceptions.JSONDecodeError as json_exception:
            print('JSON Decode Error has been thrown. User most likely does not exist.')
            print('JSON Error Message:', json_exception)
        except Exception as exception:
            print("Unknown exception has been thrown. Please refer to the following exception.")
            print("Exception Message:", exception)
        return userData

    def login(self, username: str, password: str) -> bool:
        payload = {"username": username, "enc_password": f"#PWD_INSTAGRAM_BROWSER:0:0:{password}", "queryParams": "{}", "optIntoOneTap": "true"}
        headers = {"user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36', 'x-csrftoken': 'missing', 'mid': secrets.token_hex(8)*2}
        response = self.session.post(self.web_login_url, headers=headers, data=payload)
        return "userId" in response.text
            