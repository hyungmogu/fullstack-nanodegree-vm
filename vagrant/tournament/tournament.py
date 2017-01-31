#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connects to PostgreSQL database. The object is to be used for 
    performing queries. 
    """
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Removes all entries from a table named 'matches'.

    @Args:
      None

    @Returns:
      None
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM matches;")
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
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM players;")
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
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM players")
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
    conn = connect()
    cursor = conn.cursor()
    query1 = "INSERT INTO players (name) VALUES (%s);"
    data = (name,)
    cursor.execute(query1, data)
    conn.commit()
    cursor.execute("INSERT INTO matches (wins,losses,matches) VALUES (0,0,0);")
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
    conn = connect()
    cursor = conn.cursor()
    query1 = "SELECT COUNT(*) FROM matches;"
    cursor.execute(query1)
    result1 = cursor.fetchone()

    # Win and match columns filled with zeros because no match has been done.
    if (result1[0] == 0): 
        query2 = """SELECT id, name, 0 AS wins, 0 AS matches FROM players;"""  
    # After first round, query normally.
    else: 
        query2 = """SELECT players.id, players.name, matches.wins,
                    matches.matches FROM players JOIN matches 
                    ON players.id = matches.id ORDER BY wins DESC;"""
    cursor.execute(query2)
    result2 = cursor.fetchall()
    return result2

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    @Args:
       winner,[INTEGER]:the id number of the player who won
       loser,[INTEGER]:the id number of the player who lost
    
    @Returns:
       None
    """
    conn = connect()
    cursor = conn.cursor()
    # Raise win-count for winner.
    query1 = "UPDATE matches SET wins = wins + 1 WHERE id = %s;" 
    data1 = (winner,)
    cursor.execute(query1,data1)
    conn.commit()
    # Raise lose-count for loser.
    query2 = "UPDATE matches SET losses = losses + 1 WHERE id = %s;"
    data2 = (loser,)
    cursor.execute(query2,data2)
    conn.commit()
    # Raise match-count for both loser and winner.
    query3 = "UPDATE matches SET matches = matches + 1 WHERE id = %s;"
    data3 = (winner,)
    cursor.execute(query3,data3)
    conn.commit()
    query4 = "UPDATE matches SET matches = matches + 1 WHERE id = %s;"
    data4 = (loser,)
    cursor.execute(query4,data4)
    conn.commit()
    conn.close();
    print("""Successfully updated the outcome of a single match between 
            player1_id = {0} and player2_id = {1}""".format(winner,loser))
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
