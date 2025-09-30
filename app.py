from fastapi import FastAPI, Request, Path , Query , HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fuzzywuzzy import process

from aux_cd import (
    team_info, find_matches, match_details, player_stats,
    pvp, ven_info, season_info, info 
)

from aux_cd import VALID_PLAYERS , VALID_VENUES

VALID_TEAMS = {
    'chennai super kings', 'deccan chargers', 'delhi capitals', 'delhi daredevils',
    'gujarat lions', 'gujarat titans', 'kings xi punjab', 'kochi tuskers kerala',
    'kolkata knight riders', 'lucknow super giants', 'mumbai indians', 'pune warriors',
    'punjab kings', 'rajasthan royals', 'rising pune supergiant',
    'royal challengers bangalore', 'sunrisers hyderabad'
}

VALID_SEASONS = {
    '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', 
    '2018', '2019', '2020', '2021', '2022', '2023', '2024'
}

# ---------------- Validation Helpers ---------------- #

def validate_team(team: str) -> str:
    """Validate team name or raise with fuzzy suggestion."""
    team = team.lower()
    if team in VALID_TEAMS:
        return team

    # Fuzzy suggestion if not found
    suggestion, score = process.extractOne(team, VALID_TEAMS)
    raise HTTPException(
        status_code=400,
        detail={
            "error": f"Invalid team '{team}'",
            "suggestion": f"Did you mean '{suggestion}'?" if score > 70 else "No close match found"
        }
    )


def validate_season(season: str) -> str:
    """Validate season year."""
    if season in VALID_SEASONS:
        return season
    raise HTTPException(
        status_code=400,
        detail={
            "error": f"Invalid season '{season}'",
            "valid_seasons":  sorted(VALID_SEASONS)
        }
    )


def validate_player(player: str) -> str:
    player = player.lower()
    if player in VALID_PLAYERS:
        return player

    # Fuzzy match
    suggestion, score = process.extractOne(player, VALID_PLAYERS)
    raise HTTPException(
        status_code=400,
        detail={
            "error": f"Invalid player '{player}'",
            "suggestion": f"Did you mean '{suggestion}'?" if score > 70 else "No close match found"
        }
    )

def validate_venue(venue: str) -> str:
    venue = venue.lower()
    if venue in VALID_VENUES:
        return venue

    suggestion, score = process.extractOne(venue, VALID_VENUES)
    raise HTTPException(
        status_code=400,
        detail={
            "error": f"Invalid venue '{venue}'",
            "suggestion": f"Did you mean '{suggestion}'?" if score > 70 else "No close match found"
        }
    )


app = FastAPI(title="Cricket API", version="1.0")
templates = Jinja2Templates(directory="templates")

# Serve static files if you have (css/js/img)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ---------------------- INFO ENDPOINT ----------------------
@app.get("/info")
async def info_func():
    return info()

# ---------------------- TEAM ENDPOINT ----------------------
@app.get("/team/{name}")
async def team_stats(
    name: str = Path(..., description="Enter Team Name", example="Royal Challengers Bangalore")
):
    team = validate_team(name)
    return team_info(team)  


# ---------------------- MATCHUP ENDPOINT ----------------------
@app.get("/vs")
async def get_matchup(
    team1: str = Query(..., description="Enter first team name", example="Delhi Daredevils"),
    team2: str = Query(..., description="Enter second team name", example="Rajasthan Royals"),
):
    t1 = validate_team(team1)
    t2 = validate_team(team2)
    return find_matches(t1, t2)


# ----------------------  PLAYER STATS ENDPOINT ----------------------
@app.get("/player/{name}")
async def get_player_stats(
    name: str = Path(..., description="Enter Player Name", example="V Kohli")
):
    player = validate_player(name)
    return player_stats(player)   



# ---------------------- PLAYER VS PLAYER ENDPOINT ----------------------
@app.get("/pvp")
async def get_player_matchup(
    batsman: str = Query(..., description="Enter Batsman Name", example="V Kohli"),
    bowler: str = Query(..., description="Enter Bowler Name", example="JJ Bumrah"),
):
    batsman = validate_player(batsman)
    bowler = validate_player(bowler)
    return pvp(batsman, bowler)   



# ---------------------- PLAYER AT VENUE ENDPOINT ----------------------
@app.get("/playervenue")
async def player_in_venue_stats(
    player: str = Query(..., description="Enter Player Name", example="V Kohli"),
    venue: str = Query(..., description="Enter Venue", example="M Chinnaswamy Stadium"),
):
    player = validate_player(player)
    venue = validate_venue(venue)
    return player_stats(player_name=player, venue=venue)


# ---------------------- VENUE ENDPOINT ----------------------
# Venue API
@app.get("/venue/{name}")
async def venue_stats(
    name: str = Path(..., description="Enter Venue Name", example="M Chinnaswamy Stadium")
):
    venue = validate_venue(name)
    return ven_info(venue)


# ---------------------- SEASON ENDPOINT ----------------------
@app.get("/season/{name}")
async def season_stats(
    name: str = Path(... , description = "Enter Season " , example ="2019" )
):
    season = validate_season(name)
    return season_info(season)
