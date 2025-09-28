from fastapi import FastAPI, Request, Path , Query
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from aux_cd import (
    team_info, find_matches, match_details, player_stats,
    pvp, ven_info, season_info, info
)

app = FastAPI(title="Cricket API", version="1.0")

templates = Jinja2Templates(directory="templates")

# Serve static files if you have (css/js/img)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/info")
async def info_func():
    return info()

# Team API
@app.get("/team/{name}")
async def team_stats(name: str = Path(... , description= "Enter Team Name" ,example="Royal Challengers Bangalore")):
    return team_info(name.lower())

# Match API
@app.get("/vs")
async def get_matchup(
    team1: str = Query(..., description="Enter first team name", example="Delhi Daredevils"),
    team2: str = Query(..., description="Enter second team name", example="Rajasthan Royals"),
):
    return find_matches(team1.lower(), team2.lower())

# Player stats API
@app.get("/player/{name}")
async def get_player_stats(name: str = Path(...  , description= " Enter Player Name " , example= "V Kohli")):
    return player_stats(name.lower())

# Player vs Player API
@app.get("/pvp")
async def get_player_matchhup(
    batsman: str = Query(... , description="Enter Batsmen Name " , example = "V Kohli" ),
    bowler: str = Query(... , description= "Enter Bowler Name " , example = "JJ Bumrah")
):
    return pvp(batsman.lower(), bowler.lower())

# Player Venue API
@app.get("/playervenue")
async def player_in_venue_stats(
    player: str = Query(... , description = "Enter Player Name " , example = "V Kohli"), 
    venue: str = Query(... , description ="Enter Venue " , example = "m chinnaswamy stadium")
):
    return player_stats(player_name=player.lower(), venue=venue.lower())

# Venue API
@app.get("/venue/{name}")
async def venue_stats(name: str = Path(... , description = "Enter Venue Name " , example = "m chinnaswamy stadium")):
    return ven_info(name.lower())

# Season API
@app.get("/season/{name}")
async def season_stats(name: str = Path(... , description = "Enter Season " , example ="2019" )):
    return season_info(name)
