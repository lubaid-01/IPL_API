from fastapi import FastAPI, Request
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
    return JSONResponse(content=info())

# Team API
@app.get("/team/{name}")
async def t_func(name: str):
    return JSONResponse(content=team_info(name.lower()))

# Match API
@app.get("/vs/{t1}/{t2}")
async def m_func(t1: str, t2: str):
    return JSONResponse(content=find_matches(t1.lower(), t2.lower()))

# Player stats API
@app.get("/player/{name}")
async def p_func(name: str):
    return JSONResponse(content=player_stats(name.lower()))

# Player vs Player API
@app.get("/pvp/{batsman}/{bowler}")
async def pvp_func(batsman: str, bowler: str):
    return JSONResponse(content=pvp(batsman.lower(), bowler.lower()))

# Player Venue API
@app.get("/playervenue/{player}/{venue}")
async def p_venue_func(player: str, venue: str):
    return JSONResponse(content=player_stats(player_name=player.lower(), venue=venue.lower()))

# Venue API
@app.get("/venue/{name}")
async def venue_fun(name: str):
    return JSONResponse(content=ven_info(name.lower()))

# Season API
@app.get("/season/{name}")
async def season_fun(name: str):
    return JSONResponse(content=season_info(name))
