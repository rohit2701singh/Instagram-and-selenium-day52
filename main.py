from Instagram import InstaLogin

user = InstaLogin(user_mail="txxxxxxxxxe", user_pass="xccccxccccxxx@")

user.search_account(account_to_search="royalchallengersbangalore", follow_searched_act=True, unfollow_searched_act=False)

user.start_following(one_time_limit=3)

user.unfollow_accounts(max_limit=1)

user.unfollow_a_person(["royalchallengersbangalore"])

following = user.following_names()
print(following)