#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all match records from database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM matches;""")
    conn.commit() # commit used to persist the effect of any data manipulation 
    conn.close()
    print("Deleted all match records from database")
    return

def deletePlayers():
    """Remove all player records from database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM players;""")
    conn.commit()
    conn.close()
    print("Deleted all player records from database")
    return

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""SELECT COUNT(*) FROM players """)
    result = cursor.fetchone()
    conn.close()
    return result[0] 

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cursor = conn.cursor()
    query1 = "INSERT INTO players (name) VALUES (%s);"
    data = (name,)
    cursor.execute(query1,data)
    conn.commit()
    cursor.execute("INSERT INTO matches (wins,losses,matches) VALUES (0,0,0);")
    conn.commit()
    conn.close()
    print("Player named %s successfully added to database" % name)
    return 

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cursor = conn.cursor()
    query1 = "SELECT COUNT(*) FROM matches;"
    cursor.execute(query1)
    result1 = cursor.fetchone()
    if (result1[0] == 0):
        query2 = "SELECT id,name,0 AS wins, 0 AS matches FROM players;"
    else:
        query2 = "SELECT players.id,players.name,matches.wins,matches.matches FROM players JOIN matches ON players.id = matches.id ORDER BY wins DESC;"
    cursor.execute(query2)
    result2 = cursor.fetchall()
    return result2


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    conn = connect()
    cursor = conn.cursor()
    query1 = "UPDATE matches SET wins = wins + 1 WHERE id = %s;"
    data1 = (winner,)
    cursor.execute(query1,data1)
    conn.commit()
    query2 = "UPDATE matches SET losses = losses + 1 WHERE id = %s;"
    data2 = (loser,)
    cursor.execute(query2,data2)
    conn.commit()
    query3 = "UPDATE matches SET matches = matches + 1 WHERE id = %s;"
    data3 = (winner,)
    cursor.execute(query3,data3)
    conn.commit()
    query4 = "UPDATE matches SET matches = matches + 1 WHERE id = %s;"
    data4 = (loser,)
    cursor.execute(query4,data4)
    conn.commit()
    conn.close();
    print("Successfully updated the outcome of a single match between player1_id = {0} and player2_id = {1}".format(winner,loser))
    return
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    count = countPlayers()
    standings = playerStandings()
    result = []    
    i = 0
    while i < count:
        pair = (standings[i][0],standings[i][1],standings[i+1][0],standings[i+1][1])
        result.append(pair)
        i += 2

    return result     

