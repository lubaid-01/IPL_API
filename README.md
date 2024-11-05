# IPL Dataset API

Welcome to the **IPL Dataset API**! 🚀🌐

## 📖 Overview
The **IPL Dataset API** provides structured access to a wide array of data from the Indian Premier League, offering easy integration for developers, analysts, and cricket enthusiasts. All data is returned in JSON format for seamless use in various applications.

**Access the API at:** [IPL Dataset API](https://ipl-api-ogdg.onrender.com/)

---

## 🔗 API Endpoints

### 1. **General Information**
- **`/info`**: Retrieve general metadata such as player names, stadium names, etc.
  - **Example**: `https://ipl-api-ogdg.onrender.com/info`

### 2. **Player Details**
- **`/player/{player_name}`**: Get player-specific statistics, profiles, and team affiliations.
  - **Example**: `https://ipl-api-ogdg.onrender.com/player/V Kohli`

### 3. **Player Venue Statistics**
- **`/playervenue/{player}/{venue}`**: Player performance data at a specific venue.
  - **Example**: `https://ipl-api-ogdg.onrender.com/playervenue/V Kohli/Chenna Swami Stadium`

### 4. **Team Information**
- **`/team/{team_name}`**: Access team details, including player rosters and performance metrics.
  - **Example**: `https://ipl-api-ogdg.onrender.com/team/Royal Challengers Bangalore`

### 5. **Venue Information**
- **`/venue/{venue_name}`**: Get details about IPL venues, including capacity and location.
  - **Example**: `https://ipl-api-ogdg.onrender.com/venue/Chenna Swami Stadium`

### 6. **Season Statistics**
- **`/season/{year}`**: Fetch information about a particular IPL season.
  - **Example**: `https://ipl-api-ogdg.onrender.com/season/2019`

### 7. **Player vs Player Stats**
- **`/pvp/{batsman}/{bowler}`**: Compare a batsman's performance against a bowler.
  - **Example**: `https://ipl-api-ogdg.onrender.com/pvp/V Kohli/J Bumrah`

### 8. **Team vs Team Match History**
- **`/vs/{team1}/{team2}`**: Detailed match history between two teams, sorted by season and date.
  - **Example**: `https://ipl-api-ogdg.onrender.com/vs/Delhi Daredevils/Rajasthan Royals`

---

## 🛠 Data Format
All responses are returned in **JSON**, making it easy to parse and work with in various programming languages.

---

## 🚀 Usage & Applications
- **Developers**: Integrate IPL stats into apps or websites.
- **Analysts**: Analyze player performance, team dynamics, and match trends.
- **Cricket Enthusiasts**: Gain insights into your favorite teams and players.

---

## 📚 Example Usage
```python
import requests

response = requests.get("https://ipl-api-ogdg.onrender.com/player/V Kohli")
data = response.json()
print(data)
