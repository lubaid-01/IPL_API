import pandas as pd
import numpy as np
import kagglehub



def mch_transform():
    mch['player_of_match'] = mch['player_of_match'].str.lower()
    mch['venue'] = mch['venue'].str.lower()
    mch['team1'] = mch['team1'].str.lower()
    mch['team1'] = mch['team1'].str.replace('bengaluru','bangalore')
    mch['team1'] = mch['team1'].str.replace('supergiants','supergiant')
    mch['team2'] = mch['team2'].str.lower()
    mch['team2'] = mch['team2'].str.replace('bengaluru','bangalore')
    mch['team2'] = mch['team2'].str.replace('supergiants','supergiant')
    mch['toss_winner'] = mch['toss_winner'].str.lower()
    mch['toss_winner'] = mch['toss_winner'].str.replace('bengaluru','bangalore')
    mch['toss_winner'] = mch['toss_winner'].str.replace('supergiants','supergiant')
    mch['winner'] = mch['winner'].str.lower()
    mch['winner'] = mch['winner'].str.replace('bengaluru','bangalore')
    mch['winner'] = mch['winner'].str.replace('supergiants','supergiant')
    mch['season'] = mch['season'].str.replace('2007/08','2008')
    mch['season'] = mch['season'].str.replace('2020/21','2020')
    mch['season'] = mch['season'].str.replace('2009/10','2010')



def delv_transform():

    delv['batter'] = delv['batter'].str.lower()
    delv['bowler'] = delv['bowler'].str.lower()
    delv['non_striker'] = delv['non_striker'].str.lower()
    delv['bowling_team'] = delv['bowling_team'].str.lower()
    delv['bowling_team'] = delv['bowling_team'].str.replace('bengaluru','bangalore')
    delv['bowling_team'] = delv['bowling_team'].str.replace('supergiant','supergiants')
    delv['batting_team'] = delv['batting_team'].str.lower()
    delv['batting_team'] = delv['batting_team'].str.replace('bengaluru','bangalore')
    delv['batting_team'] = delv['batting_team'].str.replace('supergiant','supergiants')
    delv['player_dismissed'] = delv['player_dismissed'].str.lower()
    delv['fielder'] = delv['fielder'].str.lower()
    return
  
# correcting the veenue
def veneu_transform():
    def veneu_resolve(ven):
        if ',' in ven:
            ven = ven.split(",", 1)[0].strip()
        return ven 

    mch['venue'] = mch['venue'].apply(veneu_resolve)
    mch.loc[mch['venue'] == 'm.chinnaswamy stadium', 'venue'] = 'm chinnaswamy stadium'
    mch.loc[mch['venue'] == 'punjab cricket association is bindra stadium', 'venue'] = 'punjab cricket association stadium'
    

# loading the dataset
path = kagglehub.dataset_download("patrickb1912/ipl-complete-dataset-20082020")
mch = pd.read_csv(f'{path}/matches.csv')
delv = pd.read_csv(f'{path}/deliveries.csv')

#get only inning 1, 2
delv = delv[(delv['inning'].isin([1,2]))]

#transfrorm datasets

mch_transform()
delv_transform()
veneu_transform()


#info about data
def info() -> dict[str,list[str]]:
    all_teams = np.union1d(mch['team1'], mch['team2'])
    players = np.unique(
        np.concatenate((delv['batter'].dropna(),
                        delv['non_striker'].dropna(),
                        delv['bowler'].dropna(),
                        delv['fielder'].dropna())))
    season = mch['season'].unique()
    venue = mch['venue'].unique()
    dic: dict[str, any] = {
        'teams': list(np.sort(all_teams)),
        'players': list(players),
        'Seasons': list(np.sort(season)),
        'venues': list(np.sort(venue))
    }
    return dic
# info about single team
def team_info(name) -> dict[str, object]:

    # name = 'Royal Challengers Bangalore'
    team_df = mch[ (mch['team1'] == name) | (mch['team2'] == name) ]
    t_matches = team_df.shape[0]
    alltime_bat = delv[delv['batting_team'] == name].groupby('batter')['batsman_runs'].sum()
    highest_run_scorer = alltime_bat.idxmax() if alltime_bat.shape[0] > 0 else ''
    highest_run_scored = alltime_bat.max() if alltime_bat.shape[0] > 0 else 0
    alltime_ball = delv[(delv['bowling_team'] == name)& (delv['dismissal_kind'].isin(['bowled', 'caught', 'lbw', 'stumped', 'caught and bowled', 'hit wicket']))].groupby('bowler')['is_wicket'].sum()
    best_bowler = alltime_ball.idxmax() if alltime_bat.shape[0] > 0 else ''
    best_bowler_wickets = alltime_ball.max() if alltime_bat.shape[0] > 0 else 0
    m_won = team_df['winner'][team_df['winner'] == name].shape[0]
    m_win_per = (m_won / t_matches)*100 if t_matches > 0 else 0
    t_won = team_df['toss_winner'][team_df['toss_winner'] == name].shape[0]
    t_win_per = (t_won/t_matches)*100 if t_matches > 0 else 0
    tm_won = mch[ (mch['toss_winner'] == name) & ( mch['winner'] == name) ].shape[0]
    tm_per = (tm_won / t_matches) *100 if t_matches > 0 else 0
    n_title = mch[(mch['match_type'] == 'Final') & (mch['winner'] == name) ].shape[0]
    t_year  = mch[(mch['match_type'] == 'Final') & (mch['winner'] == name) ]['season'].values

    dic: dict[str, object] = {
        'total matches' : int(t_matches),
        'highest run scorer' : (highest_run_scorer,int(highest_run_scored)),
        'highest wicket taker' : (best_bowler, int(best_bowler_wickets)),
        'matches won'   : int(m_won),
        'win percentage': round(m_win_per,2),
        'toss won'      : int(t_won),
        'toss win prct' : round(t_win_per,2),
        'toss match won prct' : round(tm_per,2),
        'num title won' : int(n_title),
        'won in'        : list(t_year)
    }
    return dic

#Match Details: Match ID, Date, Venue, Teams Playing, Match Result, Toss Winner, Man of the Match. Scorecard:
#Team 1: Runs, Wickets, Overs Played.
#Team 2: Runs, Wickets, Overs Played.
#venue, toss winner , elecetd to, match winner, margin, player performane, POM, highest scorrer.(extra runs per over)
def match_details(match_id : int)  -> dict[str, object]:
    # Filter data for the given match ID
    match_df = mch[mch['id'] == match_id]
    dlv_df = delv[delv['match_id'] == match_id]

    # Basic match info
    date = match_df['date'].values[0]
    venue = match_df['venue'].values[0]
    team1 = dlv_df['batting_team'].values[0]  # Team 1
    team2 = dlv_df['bowling_team'].values[0]  # Team 2
    toss_winner = match_df['toss_winner'].values[0] # Toss Winner
    elected_to = match_df['toss_decision'].values[0]  # Toss decision (bat/ball)
    match_winner = match_df['winner'].values[0]  # Match Winner
    margin = match_df['result_margin'].values[0]  # Win Margin
    win_by = match_df['result'].values[0]
    pom = match_df['player_of_match'].values[0]  # Player of the Match (POM)

    # Team 1 performance
    team1_runs = int(dlv_df[dlv_df['batting_team'] == team1]['total_runs'].sum())
    team1_wickets = int(dlv_df[dlv_df['batting_team'] == team1]['is_wicket'].sum())
    team1_overs = int(dlv_df[dlv_df['batting_team'] == team1]['over'].nunique())

    # Team 2 performance
    team2_runs = int(dlv_df [dlv_df ['batting_team'] == team2]['total_runs'].sum())
    team2_wickets = int(dlv_df [dlv_df ['batting_team'] == team2]['is_wicket'].sum())
    team2_overs = int(dlv_df [dlv_df ['batting_team'] == team2]['over'].nunique())

    # Highest scorer ???????
    highest_scorer = dlv_df.groupby('batter')['batsman_runs'].sum().idxmax()
    highest_score = int(dlv_df.groupby('batter')['batsman_runs'].sum().max())

    # Final dictionary to store match details
    match_info : dict[str, object] = {
        'venue': venue,
        'teams_playing': (team1, team2),
        'toss_winner': toss_winner,
        'elected_to': elected_to,
        'match_winner': match_winner,
        'win_margin': (margin , win_by),

        'player_of_match': pom,
        'team1_performance': {
            'runs': team1_runs,
            'wickets': team1_wickets,
            'overs': team1_overs
        },
        'team2_performance': {
            'runs': team2_runs,
            'wickets': team2_wickets,
            'overs': team2_overs
        },
        'highest_scorer': {
            'player': highest_scorer,
            'score': highest_score
        }
    }
    return match_info


def find_matches(team1 : str, team2: str)   -> dict[str, dict[str, dict[str, object]]]:
    #finding all matches one by one
    seasons = mch['season'].unique() # get all seasons
    dic : dict[str, dict[str, dict[str, object]]] = {}
    for i in seasons :

        season_df = mch[mch['season'] == i]
        match_ids = season_df[((season_df['team1'] == team1) & (season_df['team2'] == team2)) | ((season_df['team1'] == team2) & (season_df['team2'] == team1))]['id'].values
        dates = {}
        for j in match_ids :
            dates[ season_df[season_df['id'] == j ]['date'].values[0] ] = match_details(j)

        dic[i] = dates

    return dic

#player stats function 

def player_stats( player_name : str, venue = " " )  -> dict[str, object] :
    local_delv = delv.copy()
    if(venue != " "):
       local_delv = local_delv[ local_delv['match_id'].isin(mch[mch['venue'] == venue]['id'].values) ]
    batting_stats_df = local_delv[local_delv['batter'] == player_name]
    bowling_stats_df = local_delv[local_delv['bowler'] == player_name]


    # Batting Stats
    num_of_times_batted = local_delv[(local_delv['batter'] == player_name) | (local_delv['non_striker'] == player_name)]['match_id'].nunique()
    runs_scored = batting_stats_df['batsman_runs'].sum()
    outs = (local_delv['player_dismissed'] == player_name).sum()
    player_bat_data = batting_stats_df.groupby('match_id')['batsman_runs'].sum()

    centuries = (player_bat_data  >= 100).sum()
    fifties = (player_bat_data  >= 50).sum() - centuries
    average = runs_scored / outs if outs > 0 else 0
    #strike rate
    balls_faced = batting_stats_df.shape[0] - (batting_stats_df['extras_type'] == 'wides').sum()
    strike_rate = runs_scored / balls_faced *100 if balls_faced > 0 else 0

    convert_rate_30s_to_50s = (player_bat_data >= 50).sum()/ (player_bat_data >= 30).sum() *100 if (player_bat_data >= 30).sum()  > 0 else 0
    convert_rate_70s_to_100s = (player_bat_data >= 100).sum() / (player_bat_data >= 70).sum() *100 if (player_bat_data >= 70).sum()  > 0 else 0

    # Performance in (Powerplay, Middle, Death)
    out_in_pp = local_delv[ (local_delv['over'] <=6) & ( local_delv['player_dismissed'] == player_name) ].shape[0]
    powerplay_avg = batting_stats_df[batting_stats_df['over'] <= 6]['batsman_runs'].sum() / out_in_pp if out_in_pp > 0 else 0
    out_in_mo = local_delv[ (batting_stats_df['over'] > 6) & (batting_stats_df['over'] <= 15) & ( local_delv['player_dismissed'] == player_name) ].shape[0]
    middle_overs_avg = batting_stats_df[(batting_stats_df['over'] > 6) & (batting_stats_df['over'] <= 15)]['batsman_runs'].sum()  / out_in_mo if out_in_mo > 0 else 0
    out_in_do = outs - out_in_pp - out_in_mo
    death_overs_avg = batting_stats_df[batting_stats_df['over'] > 15]['batsman_runs'].sum()  / out_in_do  if out_in_do > 0 else 0

    # Bowling Stats
    num_of_times_bowled = bowling_stats_df['match_id'].nunique()
    real_wk_df =  bowling_stats_df[bowling_stats_df['dismissal_kind'].isin( ['bowled', 'caught', 'lbw', 'stumped', 'caught and bowled', 'hit wicket'])]
    wickets_taken = real_wk_df.shape[0]
    balls_bowled = (~bowling_stats_df['extras_type'].isin([ 'noballs', 'wides'])).sum()  #  uff
    run_conceved = bowling_stats_df[~bowling_stats_df['extras_type'].isin([ 'byes', 'legbyes','penalty'])]['total_runs'].sum()
    economy_rate =  run_conceved / (balls_bowled / 6) if balls_bowled> 0 else 0  #   ???
    bowling_average = run_conceved / wickets_taken if wickets_taken > 0 else 0
    wkts_in_mtch_df = real_wk_df.groupby('match_id')['is_wicket'].sum()
    hi_wickets = wkts_in_mtch_df.max() if wkts_in_mtch_df.shape[0] > 0 else 0
    f_wckt_haual = wkts_in_mtch_df[ wkts_in_mtch_df >= 5 ].shape[0]
    powerplay_wickets = (real_wk_df[real_wk_df['over'] <= 6]).shape[0]


    # Fielding Stats
    catches = (local_delv[local_delv['fielder'] == player_name]['dismissal_kind'] == 'caught').sum()
    run_outs = (local_delv[local_delv['fielder'] == player_name]['dismissal_kind'] == 'run out').sum()
    stumpings = (local_delv[local_delv['fielder'] == player_name]['dismissal_kind'] == 'stumped').sum()


    batting_stats = {
        'num_of_times_batted': int(num_of_times_batted),
        'runs_scored': int(runs_scored),
        'balls_faced' :int(balls_faced),
        'batting_average': round(average,2),
        'strike_rate': round(strike_rate,2),
        'centuries': int(centuries),
        'fifties': int(fifties),
        'convert_rate_30s_to_50s': round(convert_rate_30s_to_50s,2),
        'convert_rate_70s_to_100s': round(convert_rate_70s_to_100s,2),
        'powerplay_avg': round(powerplay_avg,2),
        'middle_overs_avg': round(middle_overs_avg,2),
        'death_overs_avg': round(death_overs_avg,2),

    }
    bowling_stats = {
        'num_of_times_bowled': int(num_of_times_bowled),
        'balls_bowled' : int(balls_bowled),
        'run_conceved' : int(run_conceved),
        'wickets_taken': int(wickets_taken),
        'economy_rate': round(economy_rate,2),
        'bowling_average': round(bowling_average,2),
        'powerplay_wickets': int(powerplay_wickets),
        'highest_wickets' : int(hi_wickets),
        'five_wickets_haul' : int(f_wckt_haual)

    }

    fielding_stats = {
        'catches': int(catches),
        'run_outs': int(run_outs),
        'stumpings': int(stumpings)
    }
    return {
        'player_name': player_name,
        'batting_stats': batting_stats,
        'bowling_stats': bowling_stats,
        'fielding_stats': fielding_stats
    }


#player vs player

def pvp(batsman : str, bowler : str)  -> dict[str, dict[str, int]]:
    local_df = delv[ (delv['bowler'] == bowler) & (delv['batter'] == batsman)]

    #no of times out
    out = local_df[ local_df['dismissal_kind'].isin( ['bowled', 'caught', 'lbw', 'stumped', 'caught and bowled', 'hit wicket'])].shape[0]
    #no of runs conceaved
    runs = local_df['batsman_runs'].sum()
    #no of fours
    fours = local_df[local_df['batsman_runs'] == 4].shape[0]
    #no of sixes
    six = local_df[local_df['batsman_runs'] == 6].shape[0]
    #avg of bats man
    avg = runs / out if out > 0 else 0

    #ttl balls bowled
    bowler_bowled = local_df[ (local_df['extras_type'] != 'wides') & (local_df['extras_type'] != 'noballs')].shape[0]
    #balls faced by batsman
    bats_faced = bowler_bowled - (local_df['extras_type'] == 'wides').sum()

    strike_rate = (runs / bats_faced) *100 if bats_faced > 0 else 0

    #dots
    dots = (local_df['total_runs'] == 0).sum()

    runs_conceaved  = local_df[~local_df['extras_type'].isin([ 'byes', 'legbyes','penalty'])]['total_runs'].sum()
    #econmy
    economy = (runs_conceaved / (bowler_bowled/6) ) if bowler_bowled > 0 else 0

    dic: dict[str, dict[str, int]] = {
        'batsman_stats': {
            'no_outs': int(out),
            'batsman_runs': int(runs),
            'no_of_fours': int(fours),
            'no_of_sixes': int(six),
            'batsman_avg': int(avg),
            'strike_rate': int(strike_rate),
            'balls_faced': int(bats_faced)
        },
        'bowler_stats': {
            'balls_bowled': int(bowler_bowled),
            'dots': int(dots),
            'economy': int(economy)
        }
    }
    return dic

#venue info

def ven_info( name : str )  -> dict[str, object] :
    ven_df = mch[ mch['venue'] == name ]

    #run stats
    stats_df = ven_df['target_runs'].describe()

    n_mtch = ven_df.shape[0]
    max_runs = stats_df['max']
    min_runs = stats_df['min']
    min_run_row = ven_df[ ven_df['target_runs'] == min_runs ]
    condition = min_run_row['result'] == 'runs'
    ing = 'first'
    if  condition.values[0]:
        min_runs = min_runs - min_run_row['result_margin'].values[0]
        ing = 'second'
    hi_chased  = ven_df[ven_df['result'] == 'wickets']['target_runs'].max()
    chase_win_prct = ( ven_df[ven_df['result'] == 'wickets'].shape[0] / n_mtch ) * 100
    toss_win_prct = ( (ven_df[ven_df[ 'toss_winner' ] == ven_df['winner']].shape[0]) / n_mtch ) * 100
    loc = ven_df['city'].values[0] if ven_df.shape[0] >0 else ''
    
    dic : dict[str , object] = {
        'locaton' : loc,
        'total_matches' : int(n_mtch),
        'max_target' : int(max_runs),
        'min_runs' : (int(min_runs), ing),
        'highest_chased' : int(hi_chased),
        'chase_win_perct' : float(chase_win_prct),
        'toss_win_perct'  : float(toss_win_prct)

    }
    return dic

#season_info 

def season_info(season_year : str)  -> dict[str, object] :
    # Filter matches for the given season
    season_df = mch[mch['season'] == season_year]

    # Total matches played in that season
    t_matches = season_df.shape[0]

    # Total teams participated
    teams = pd.concat([season_df['team1'], season_df['team2']]).unique()

    # Find the team that won the most matches
    top_team = season_df['winner'].value_counts().idxmax()
    top_team_wins = season_df['winner'].value_counts().max()

    # Calculate win percentage of the top team
    top_team_matches = season_df[(season_df['team1'] == top_team) | (season_df['team2'] == top_team)].shape[0]
    top_team_win_per = (top_team_wins / top_team_matches)

    # Winning team of the final match
    final_winner = season_df[season_df['match_type'] == 'Final']['winner'].values[0]

    dic : dict[str , object]= {
        'season': season_year,
        'total matches': int(t_matches),
        'teams participated': list(teams),
        'top team': top_team,
        'top team wins': int(top_team_wins),
        'top team win percentage': round(top_team_win_per,2),
        'final winner': final_winner
    }

    return dic

   
