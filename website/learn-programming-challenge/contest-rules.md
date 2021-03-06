---
layout: doc_page
title: Contest Rules
toc: false
description: Learn the rules of the game to win the Halite AI Programming Challenge.
---

The 2017-2018 season of Halite II will run from October 2017 through January 2018. 

Submissions will open October 23rd, 2017 at 6am and will be live through January 22nd, 2018 at 11:59pm EST. Winners will be announced January 29th. Submit early and often!


## ELIGIBILITY

All it takes to play Halite II is to [create an account][login] using Github and [submit a bot][downloads] during the dates of the competition. Any user who submits a bot will appear on the leaderboard.

## TEAMS

As opposed to last year, we are encouraging playing as a team this year, with the caveat that a single person should not be submitting bots under two accounts at the same time. For example, [Two Sigma](https://www.twosigma.com), the creator of Halite, is hosting a tournament for select university students to compete on school teams for a given period of time. For these students, we’d expect to see them create a joint Github account (e.g. “cornellhalite2017”) and collaborate on code. We understand that hackathons and events are fun ways to learn and progress. However, if we see a team submission and an individual account with similar bot submissions, both will be disqualified. If a player in a team wishes to play on their own, they should substantially improve their bot before submitting on their own. Play fair!

## RANKING
Rankings in Halite II are based on the outcome of organized games where bots play against each other. Bot rankings are computed using a Bayesian algorithm variant of the Glicko system, specifically using the [TrueSkill](https://www.microsoft.com/en-us/research/project/trueskill-ranking-system/) Python library with some adjustments. The game coordinator picks groups of 2 or 4 bots to compete against each other at a time, and uses TrueSkill to update the bot ranking based on the match outcome.

TrueSkill gives every user a μ (calculated player skill) and σ (the probability that TrueSkill understands a player’s skill level). Your rank is calculated as a function of these two variables. When you submit your first bot, your rank will be zero because both μ and  σ will be zero, but your bot will immediately start playing games against other bots, and your score will adjust accordingly. You’ll start by playing bots with similar ranks to yours, within your own tier (see below). Over the course of a few days, TrueSkill will get a good sense for your bot’s skill, and your rank will stabilize. 

If you submit a second bot, we do not reset your score to zero (as we did in Halite I), and you will start from the rank of your last bot. But this doesn’t mean your rank is safe forever! If your second bot is worse than your first, your rank will fall as your new bot plays others, and of course if your second bot is better, your rank will improve.

## TIERS
We assign you a tier based on your current rank.  Tiers are by percentile: the top 1/512 players are considered Platinum; the next 1/256 are considered Diamond, then the next 1/128 are Gold, 1/64 are Silver, and the rest are Salt. You will move from tier to tier as your rank changes.

## FINALS
At midnight on January 22nd, we will close submissions and let the final bots play each other for the last week of January. We will announce final winners on January 29th based on the final scores at that point in time and will freeze scores. We may also decide that Salt level bots (or any other bot) will stop playing earlier than 29th if we need the bandwidth to play more games for top bots in the last few days. Stay tuned for updates.

## OTHER AWARDS AND BADGES
Other than the top bots, we will award badges to players with achievements playing the game. These range from submitting your first or second bot to being the top player from your country or language. Read the full description of [badges and accomplishments - coming soon]().

Prizes for this contest are bragging rights and some awesome Halite sweatshirts for top bots. In addition, Two Sigma will waive first round interviews for all users ranked Gold and above at the end of the contest. [Learn more here - coming soon](). And we’ll be announcing the results of the competition with a link to the top players’ Github profiles and/or blogs (please do blog!).

## HACKATHONS
Throughout the competition, Two Sigma and its partners will be hosting hackathons for players to compete against smaller pools. Some examples include a High School hackathon in NYC in November and a hackathon at [Two Sigma Ventures](https://www.twosigmaventures.com/). If you’d be interested in hosting your own hackathon or use Halite in the classroom, contact our team at <mailto:halite@halite.io> or read our [hackathon tutorial - coming soon]() .

## COMMUNITY POLICIES
One of the most wonderful aspects of Halite I, according to last years’ players, was our open and collaborative community on [the forums](forums.halite.io]) and on our [Discord channel](https://discordapp.com/invite/EqW8DCB). Please share ideas, tips, and even code for all to share. We only ask that you be courteous to your fellow players, and not share so many tricks or code that earlier players feel their effort was wasted. This is of course a gray line, so feel free to err on the side of over-sharing, and the Halite staff will help with moderation in the forums. We reserve the ability to remove any content we feel goes too far. So share, share, share and leave the tricky decisions to us.

[login]: {{ site.login_server_url }}/github
[downloads]: {{ site.baseurl }}/learn-programming-challenge/downloads-and-starter-bots