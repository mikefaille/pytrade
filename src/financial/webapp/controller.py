# import hashlib
# from config import db
from bruces.webapp.controller import BaseViewController
# from wsx.core.exceptions import AuthenticationError
# from wsx.user.model import User
# from wsx.sports.model import League
# from wsx.sports.model import Team
# from wsx.trade.model import Order
# from wsx.trade.model import Portfolio
# from wsx.trade.model import StockValue
# from wsx.social.model import Follow
# from wsx.social.model import FollowRequest
# from wsx.leader.model import PlayerRank

class BaseController(BaseViewController):
    def __init__(self, *args, **kwargs):
        super(BaseController, self).__init__(*args, **kwargs)
        self.wsgi.add_header('Content-Type', 'text/html')
        self.wsgi.session.start()
        
    def __enter__(self):
        super(BaseController, self).__enter__()
        
        # Error handling
        try:
            self.wsgi.error = self.wsgi.session["error"]
        except KeyError:
            self.wsgi.error = None
            
        try:
            self.wsgi.message = self.wsgi.session["message"]
        except KeyError:
            self.wsgi.message = None
            
        return self
    
    def __exit__(self, etype, value, traceback):
        pass
        # if self.view is not None:
        #     if hasattr(self.view, "outer"):
        #         # The leagues
        #         leagues = League.fetch()

        #         self.view.outer.context.leagues = leagues
        #         league = leagues[0]
        #         
        #         # The ticker
        #         self.view.outer.context.ticker = User.get_ticker(None,-1)
        #         
        #         # The user
        #         self.view.outer.context.is_authenticated = False
        #         
        #         # The view 
        #         self.view.outer.context.viewdir = self.view.viewdir
        #         self.view.outer.context.filename = self.view.filename
        #         self.view.outer.context.fullpath = self.wsgi.environ["REQUEST_URI"]

        #         # Get bid, ask and last trade values for each team
        #         teams = Team.get_teams(league)
        #         for team in teams:
        #             team.bid = Order.get_current_bid(team.ticker)
        #             if team.bid is not None:
        #                 team.bid.price = team.bid.unit_price
        #                 team.bid.quantity = Order.get_pending_volume_by_price(team.ticker, team.bid.unit_price)
        #             team.ask = Order.get_current_ask(team.ticker)
        #             if team.ask is not None:
        #                 team.ask.price = team.ask.unit_price
        #                 team.ask.quantity = Order.get_pending_volume_by_price(team.ticker, team.ask.unit_price)
        #             team.last = StockValue.get_last_trade_value(team.ticker)
        #         self.view.outer.context.teams = teams

        #         # Get player rankings (leaders) for ticker. Remove any "None" users.
        #         self.view.outer.context.players = [p for p in PlayerRank.calculate_ranks(league) if p[0].user is not None]
        #         self.view.outer.context.prize_pool = User.get_prize_pool()

        #         try:
        #             user_id = self.wsgi.session["user_id"];
        #             self.user = User()
        #             if user_id is not None:
        #                 self.view.context.user_id = self.wsgi.session["user_id"]
        #                 self.user.load(user_id)
        #                 userhash = hashlib.sha1()
        #                 userhash.update('gt5de3aq1' + str(self.user.pk))

        #                 if self.wsgi.session["user_hash"] != userhash.hexdigest():
        #                     raise AuthenticationError('The hash does not match.')

        #                 self.view.outer.context.is_authenticated = True
        #                 self.view.outer.context.username = self.user.username
        #                 self.view.outer.context.current_user = self.user
        #                 self.view.outer.context.portfolio = self.user.get_portfolios()[0]

        #                 # The social stuff
        #                 self.view.outer.context.followers = Follow.get_followers(self.user)
        #                 self.view.outer.context.following = Follow.get_following(self.user)
        #                 self.view.outer.context.new_following = Follow.get_following(self.user, seen="False")
        #                 self.view.outer.context.requests_to_follow = FollowRequest.get_requests_to_follow(self.user)
        #                 self.view.outer.context.unseen_requests_to_follow = FollowRequest.get_requests_to_follow(self.user, seen=False)

        #                 # Get rank and portfolio info for requests, followers and following
        #                 league = League.get_by_name('NHL')
        #                 for request in self.view.outer.context.requests_to_follow:
        #                     portfolio = Portfolio.get_by_league_and_user(league, request.request_user)

        #                 for follower in self.view.outer.context.followers:
        #                     portfolio = Portfolio.get_by_league_and_user(league, follower.user)
        #                     follower.total = portfolio.total + portfolio.get_stock_value()

        #                 for following in self.view.outer.context.following:
        #                     portfolio = Portfolio.get_by_league_and_user(league, following.follows)
        #                     following.total = portfolio.total + portfolio.get_stock_value()

        #                 for new_following in self.view.outer.context.new_following:
        #                     portfolio = Portfolio.get_by_league_and_user(league, new_following.follows)
        #                     new_following.total = portfolio.total + portfolio.get_stock_value()

        #             else:
        #                 self.view.outer.context.is_authenticated = False
        #                 self.view.outer.context.username = None
        #                 self.view.outer.context.current_user = None
        #                 self.view.outer.context.portfolio = None

        #         except (KeyError, AuthenticationError):
        #             self.view.outer.context.is_authenticated = False
        #             self.view.outer.context.username = None
        #             self.view.outer.context.current_user = None
        #             self.view.outer.context.portfolio = None

        # super(BaseController, self).__exit__(etype, value, traceback)
