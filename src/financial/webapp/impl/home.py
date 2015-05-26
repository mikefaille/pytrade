# import feedparser
# from config import db
from financial.webapp.controller import BaseController
from financial.webapp.layout import DefaultLayoutView
# from wsx.leader.model import PlayerRank
# from wsx.sports.model import League
# from wsx.sports.model import Team
# from wsx.trade.model import StockValue
# from wsx.trade.model import Order
# from wsx.social.model import Follow
# from wsx.social.model import FollowRequest


class HomeController(BaseController):
    def default(self):
        pass
        # from wsx.user.model import User
        # import traceback
        # self.view = HomeView()
        # self.view.current_page = 'home'

        # try:

        #     league = League.get_leagues()[0]
        #     self.view.league = league
        #     # for league in leagues:
        #     # players = PlayerRank.calculate_ranks(league)
        #     # self.view.players = filter(lambda p: p[0].user.username != 'Claude', players)[:4]
        #     self.view.players = PlayerRank.calculate_ranks(league)[:4]

        #     url = 'http://www.nhl.com/rss/features.xml'
        #     feed = feedparser.parse(url)
        #     self.view.feed = feed['items'][:4]

        #     if len(self.view.feed) == 0:
        #         self.view.feed = None

        #     # Set up biggest winner / biggest loser
        #     import operator

        #     # changes = Order.get_price_changes_as_dict()
        #     # changes = sorted(changes.iteritems(), key=operator.itemgetter(1))

        #     ticker = User.get_ticker(None,-1)

        #     changes = {t['ticker']:t['change'] for t in ticker}
        #     changes = sorted(changes.iteritems(), key=operator.itemgetter(1))

        #     # print
        #     self.view.biggest_winner = League.fetch_team_or_player(changes[-1][0])
        #     self.view.biggest_loser = League.fetch_team_or_player(changes[0][0])
        #     self.view.winner_graph_data = StockValue.get_graph_values(self.view.biggest_winner.ticker)
        #     self.view.loser_graph_data = StockValue.get_graph_values(self.view.biggest_loser.ticker)

        #     # Get bid, ask and last trade values for each team
        #     teams = Team.get_teams(self.view.league)
        #     daily_volumes = Order.get_daily_volumes_for_all_stocks(3600)  # cached values up to 1hr old are ok

        #     for team in teams:
        #         team.bid = Order.get_current_bid(team.ticker)
        #         if team.bid is not None:
        #             team.bid.price = team.bid.unit_price
        #             team.bid.quantity = Order.get_pending_volume_by_price(team.ticker, team.bid.unit_price)
        #         team.ask = Order.get_current_ask(team.ticker)
        #         if team.ask is not None:
        #             team.ask.price = team.ask.unit_price
        #             team.ask.quantity = Order.get_pending_volume_by_price(team.ticker, team.ask.unit_price)
        #         team.daily_volume = daily_volumes.get(team.ticker, 0)
        #         # team.average_volume = Order.get_average_volume(team.ticker)
        #         team.last = StockValue.get_last_trade_value(team.ticker)
        #     self.view.teams = teams

        # except Exception as e:
        #     self.view.teams = {}
        #     print traceback.format_exc()
        #     print 'error in home view controller teams:', e

        # try:
        #     # Get user info
        #     from wsx.user.model import User
        #     watched = []
        #     user = User()
        #     user.load(self.wsgi.session["user_id"])
        #     self.view.current_user = user
        #     watched_stock = user.get_watched_stocks()
        #     for item in watched_stock:
        #         stockdict = {}
        #         stockdict['stock'] = League.fetch_team_or_player(item.ticker)
        #         stockdict['current_bid'] = Order.get_current_bid(item.ticker)
        #         stockdict['current_ask'] = Order.get_current_ask(item.ticker)
        #         stockdict['last'] = StockValue.get_last_trade_value(item.ticker)
        #         watched.append(stockdict)

        #     self.view.watched = watched

        #     # Fetch a list of all the people the current user is following
        #     following = Follow.get_following(user)
        #     self.view.following = []
        #     for follow in following:
        #         self.view.following.append(follow.follows.pk)

        #     # Add code to fetch a list of all the pending follow requests from the current user
        #     requested = FollowRequest.get_follow_requests(user)
        #     self.view.requested = []
        #     for request in requested:
        #         self.view.requested.append(request.response_user.pk)

        # except Exception as e:
        #     self.view.current_user = None
        #     print traceback.format_exc()
        #     print 'error in home view controller user:', e


class HomeView(DefaultLayoutView):
    viewdir = "home/"
    filename = "default.html"


