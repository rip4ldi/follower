from follower import Follower
from follower import UserData
import stdiomask, threading

def remove_users(followers: list, client: Follower) -> None:
    removed_count = 0
    for follower in followers:
        # remove excha
        if client.remove_follower(follower):
            removed_count += 1
            print(f"[+] Removed {removed_count}/{len(followers)} | Status: {followers.index(follower)}/{len(followers)}", end="\r")

    print("Finished the list!")


def get_followers_from_account_data(user: UserData) -> list:
    if user.followed_by_count != 0:
        followers = client.get_followers(user)
        return followers        
    else:
        print("You don't have any followers")
        return []


client = Follower()
client.username = input("[+] Username: ")
password = stdiomask.getpass(mask='*', prompt='[+] Password: ')

# If username and password are correct then execute the following code [i didnt need to add '== True' but its alot more readable]
if client.login(client.username, password) == True:
    print("[>] Logged into the username.")
    time.sleep(2)
    user = client.get_user_data()

    # Check if we received data in the struct
    if user.got_success:
        followers = get_followers_from_account_data(user)

        # i feel the need to comment this as this is could confuse some developers

        # if we got followers from the user, make function equal to a thread.start function to unfollow all the users, otherwise make function equal to the exit function
        function = threading.Thread(target=remove_users, args=[followers, client], daemon=True).start if len(followers) != 0 else exit

        # call whatever function we stored from above
        function()
        input()
    else:
        print("Could not grab user data")
else:
    print("Could not login to the user")
