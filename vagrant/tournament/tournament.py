#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connects to PostgreSQL database. The method is to be used for 
    performing queries. 
    """
    conn = psycopg2.connect("dbname=tournament")
    cursor = conn.cursor()
    return conn, cursor

def deleteMatches():
    """Removes all entries from a table named 'matches'.

    @Args:
      None

    @Returns:
      None
    """
    conn, cursor = connect()
    cursor.execute("TRUNCATE TABLE match_result;")
    conn.commit() 
    conn.close()
    print("Deleted all match records from table")
    return

def deletePlayers():
    """Removes all entries from a table named 'players'.

    @Args:
      None

    @Returns:
      None
    """
    conn, cursor = connect()
    cursor.execute("TRUNCATE TABLE player CASCADE;")
    conn.commit()
    conn.close()
    print("Deleted all player records from table")
    return

def countPlayers():
    """Returns the number of registered players. 

    @Args:
      None

    @Returns
      [INT] Number of Players 
    """
    conn, cursor = connect()
    cursor.execute("SELECT COUNT(*) FROM player")
    result = cursor.fetchone()
    conn.close()
    num_of_players = result[0]
    return num_of_players 

def registerPlayer(name):
    """Adds a player to the tournament database.

    @Args:
      name,[STRING]: the player's full name.

    @Returns:
      None
    """
    conn, cursor = connect()
    query = "INSERT INTO player (name) VALUES (%s);"
    data = (name,)
    cursor.execute(query, data)
    conn.commit()
    conn.close()
    print("Player named %s successfully added to database" % name)
    return 

def playerStandings():
    """Returns player standings sorted by wins.

    @Args:
      None   

    @Returns:
      A list of tuples, containing
        id,[INTEGER]: player's unique id
        name,[STRING]: player's full name
        wins,[INTEGER]: the number of matches player has won
        matches,[INTEGER]: the number of matches player has played
    """
    conn, cursor = connect()
    query = """SELECT * FROM player_standings;"""
    cursor.execute(query)
    result2 = cursor.fetchall()
    conn.close()
    return result2

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    @Args:
       winner,[INTEGER]:the id number of the player who won
       loser,[INTEGER]:the id number of the player who lost
    
    @Returns:
       None
    """
    conn, cursor = connect()
    cursor.execute("INSERT INTO match_result (winner_id,loser_id) VALUES (%s,%s)",(winner,loser))
    conn.commit()
    conn.close()
    print("Successfully updated the outcome of a single match between" 
            + " player1_id = {0} (winner) and player2_id = {1} (loser)".format(winner,loser))
    return

def swissPairings():
    """Pairs players for the next round of a match.
  
    @Args:
        None
  
    @Returns:
        A list of tuples, containing
            id1,[INTEGER]: the first player's unique id
            name1,[STRING]: the first player's name
            id2,[INTEGER]: the second player's unique id
            name2,[STRING]: the second player's name
    """
    count = countPlayers()
    standings = playerStandings()
    result = []    
    i = 0
    # Pairs people with similar standings. Note that
    # standings[i][0]: the id of first player
    # standings[i][1]: the name of first player
    # standings[i+1][0]: the id of second player
    # standings[i+1][0]: the name of second player
    while i < count:
        pair = (standings[i][0],standings[i][1],
                standings[i+1][0],standings[i+1][1])
        result.append(pair)
        i += 2

    return result     
