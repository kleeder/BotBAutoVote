import requests
import csv

# check your cookies when logged in to get your botb-account-data
user_id = "12345"
serial = "1a2b3c"
botbr_id = "54321"


# something.csv (should be in the same dir as this script, otherwise use the full path
# the cvs should only contain rows in the following pattern:
# entry_id,cat1,cat2,cat3,cat4,cat5
# for example:
# 12345,5,6,5,6,5 would result in a cat1=5,cat2=6,cat3=5,cat4=6,cat5=5 vote on the entry with the id 12345
# pls make sure that your file is formatted properly, because i was too lazy to implement any error handling
csv_name = "votes.csv"

# creating the cookie-dict to use when making the post-request
cookies = {
    "user_id":  user_id,
    "serial":   serial,
    "botbr_id": botbr_id
}


# the post-request is created and sent to botb
def make_post_request(entry_id, cat1, cat2, cat3, cat4, cat5):
    url = "https://battleofthebits.com/vote_record/Save/{}/".format(entry_id)
    data = {
        'cat1': cat1,
        'cat2': cat2,
        'cat3': cat3,
        'cat4': cat4,
        'cat5': cat5
    }

    post_request = requests.post(url, cookies=cookies, data=data)

    # minimalistic feedback, in case you need updates while the votes are being saved
    print("Successfully voted on Entry {}!".format(entry_id))
    print("Voted: {}-{}-{}-{}-{}".format(cat1, cat2, cat3, cat4, cat5))


def check_user(entry_id):
    url = "https://battleofthebits.com/api/v1/entry/load/{}".format(entry_id)
    json_data = requests.get(url).json()
    return str(json_data['botbr']['id'])


def check_if_voter(entry_id, botbr_id):
    entry_botbr = check_user(entry_id)
    return botbr_id == entry_botbr


with open(csv_name, newline='') as csvfile:
    battle_votes = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in battle_votes:
        if check_if_voter(row[0], botbr_id):
            pass
        else:
            make_post_request(row[0], row[1], row[2], row[3], row[4], row[5])
