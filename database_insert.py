import sqlite3
from match_generator import match_list


for match in match_list:
    try:
        sqliteConnection = sqlite3.connect('royalbetsproject/db.sqlite3')
        cursor = sqliteConnection.cursor()
        print("Connection to DB acquired")

        insert_query = """INSERT INTO royalbetsapp_fixture (team_home_id, team_away_id, odds_team_home, 
        odds_draw, odds_team_away, match_num, week, date, played, result_home, result_away, winner_home, winner_away, table_updated) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?);"""

        count = cursor.execute(insert_query, match)
        sqliteConnection.commit()
        print("Record inserted")
        cursor.close()

    except sqlite3.Error as error:
        print("Insertion failed", error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("Connection to DB closed")
