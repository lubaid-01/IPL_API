from flask import Flask, jsonify, render_template
from aux_cd import team_info, find_matches,match_details,player_stats, pvp,ven_info,season_info,info

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.route('/')
def main():
    return render_template('template.html')
@app.route('/info')
def info_func():
    return jsonify(info())
#team api
@app.route('/team/<string:name>')
def t_func(name):
   
   return jsonify( team_info(name.lower()) )

#match api
@app.route('/vs/<string:t1>/<string:t2>')
def m_func(t1,t2):

    return jsonify( find_matches(t1.lower(),t2.lower()) )

#player stats api

@app.route('/player/<string:name>')
def p_func(name):
    
    return jsonify(player_stats( name.lower() ))

#player vs player api
@app.route('/pvp/<string:batsman>/<string:bowler>')
def pvp_func(batsman, bowler):
    
    return jsonify( pvp(batsman.lower(), bowler.lower()))

#player venue api
@app.route('/playervenue/<string:player>/<string:venue>')
def p_venue_func(player, venue):

    return jsonify( player_stats(player_name=player.lower(), venue= venue.lower()))

#venue api
@app.route('/venue/<string:name>')
def venue_fun(name):

    return jsonify( ven_info( name.lower() ) )

# season api
@app.route('/season/<string:name>')
def season_fun(name):

    return jsonify( season_info( name ) )
if __name__ == '__main__' :
    app.run(debug=True)


#print(team_info('Royal Challengers Bangalore'))
''' 
Royal Challengers Bangalore
Kolkata Knight Riders
Kings XI Punjab
Chennai Super Kings
Rajasthan Royals
Delhi Daredevils

'''
