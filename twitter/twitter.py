from models import *
from database import init_db, db_session
from datetime import datetime

class Twitter:
    def __init__(self):
        self.current_user = None
    """
    The menu to print once a user has logged in
    """
    def print_menu(self):
        print("\nPlease select a menu option:")
        print("1. View Feed")
        print("2. View My Tweets")
        print("3. Search by Tag")
        print("4. Search by User")
        print("5. Tweet")
        print("6. Follow")
        print("7. Unfollow")
        print("0. Logout")
    
    """
    Prints the provided list of tweets.
    """
    def print_tweets(self, tweets):
        for tweet in tweets:
            print("==============================")
            print(tweet)
        print("==============================")

    """
    Should be run at the end of the program
    """
    def end(self):
        print("Thanks for visiting!")
        db_session.remove()
    
    """
    Registers a new user. The user
    is guaranteed to be logged in after this function.
    """
    def register_user(self):
        username = input("Enter username: ")
        user = db_session.query(User).where(User.username == username).first()
        while user != None:
            print("Username is already taken try again")
            username = input("Enter username: ")
            user = db_session.query(User).where(User.username == username).first()
        password_check1 = input("Password: ")
        password_check2 = input("Same Password Again: ")
        while password_check1 != password_check2:
            print("Your passwords did not match, try again.")
            password_check1 = input("Password: ")
            password_check2 = input("Same Password Again: ")  
        user = User(username = username, password = password_check1)
        db_session.add(user)
        db_session.commit()
        self.current_user = user

                

    """
    Logs the user in. The user
    is guaranteed to be logged in after this function.
    """
    def login(self):
        username = input("Enter username: ")
        input_password = input("Password: ")
        user = db_session.query(User).where((username == User.username) & (input_password == User.password)).first()
        while user == None:
            print("Invalid username or password")
            username = input("Enter username: ")
            input_password = input("Password: ")
            user = db_session.query(User).where((username == User.username) & (input_password == User.password)).first()
        self.current_user = user
        print("Login Succesful")


    
    def logout(self):
        self.current_user = None
        self.end

    """
    Allows the user to login,  
    register, or exit.
    """
    def startup(self):
        mode = input("Welcome to ATCS Twitter! \nPlease select a Menu Option\n1. Login\n2. Register User\n0. Exit\n")
        if mode == str(1):
            self.login()
        elif mode == str(2):
            self.register_user()
        else:
            self.logout()

    def follow(self):
        followUsername = input("Who would you like to follow? ")
        user = db_session.query(User).where(User.username == followUsername).first()
        for user in self.current_user.following:
            print ("You are already following " + followUsername)
        else:
            follower = Follower(follower_id = self.current_user.username, following_id = followUsername)
            db_session.add(follower)
            db_session.commit()
            print("You are now following " + followUsername)
      

    def unfollow(self):
        followUsername = input("Who would you like to unfollow? ")
        user = db_session.query(User).where(User.username == followUsername).first()
        for user in self.current_user.following:
            follower = db_session.query(Follower).where((self.current_user.username == Follower.follower_id) & (followUsername == Follower.following_id)).first()
            db_session.delete(follower)
            db_session.commit()
            print ("You are no longer following " + followUsername)
        else:
            print("You are not following " + followUsername)

    def tweet(self):
        tweetContent = input("Create Tweet: ")
        tags = input("Enter your tags seperated by spaces: ")
        newTweet = Tweet(content = tweetContent, username = self.current_user.username, timestamp = datetime.now())
        db_session.add(newTweet)
        db_session.commit()
        tweet = db_session.query(Tweet).where(Tweet.content == tweetContent).first()
        tweetID = tweet.id
        tags = tags.split()
        for i in tags:
            if db_session.query(Tag).where(Tag.content == i).first() == None:
                tag = Tag(i)
                db_session.add(tag)
                db_session.commit()
            else:
                tag = db_session.query(Tag).where(Tag.content == i).first()
            tweetTag = TweetTag(tag_id = tag.id, tweet_id = tweetID)
            db_session.add(tweetTag)
            db_session.commit()


    def view_my_tweets(self):
        tweets = db_session.query(Tweet).where(Tweet.username == self.current_user.username)
        self.print_tweets(tweets)
    
    """
    Prints the 5 most recent tweets of the 
    people the user follows
    """
    def view_feed(self):
        tweets = db_session.query(Tweet).order_by(Tweet.timestamp).limit(5)
        self.print_tweets(tweets)

    def search_by_user(self):
        username = input("Whose tweets would you like to see? ")
        if db_session.query(User).where(User.username == username).first() != None:
            tweets = db_session.query(Tweet).where(Tweet.username == username)
            self.print_tweets(tweets)
        else:
            print("There is no user by that name")

    def search_by_tag(self):
        searchTag = input("What tag would you like to see? ")
        tag = db_session.query(Tag).where(Tag.content == searchTag).first()
        if  tag != None:
            tweets = db_session.query(TweetTag, Tweet).join(Tweet, Tweet.id == TweetTag.tweet_id).where(TweetTag.tag_id == tag.id)
            self.print_tweets(tweets)
        else:
            print("There is no tag by that name")

    """
    Allows the user to select from the 
    ATCS Twitter Menu
    """
    def run(self):
        init_db()

        print("Welcome to ATCS Twitter!")
        self.startup()
        while self.current_user != None:

            self.print_menu()
            option = int(input(""))

            if option == 1:
                self.view_feed()
            elif option == 2:
                self.view_my_tweets()
            elif option == 3:
                self.search_by_tag()
            elif option == 4:
                self.search_by_user()
            elif option == 5:
                self.tweet()
            elif option == 6:
                self.follow()
            elif option == 7:
                self.unfollow()
            else:
                self.logout()
        
        self.end()
