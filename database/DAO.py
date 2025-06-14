from database.DB_connect import DBConnect
from model.seasons import Season
from model.nodes import Node
from model.edges import Edge

class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllAnni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """Select * from seasons"""

        cursor.execute(query)

        for row in cursor:
            result.append(Season(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """select distinct(r.driverId), d.forename, d.surname
                   from results r, races ra, drivers d
                   where r.raceId = ra.raceId and ra.`year` = %s and r.`position` > 0 and d.driverId = r.driverId"""

        cursor.execute(query, (year,))

        for row in cursor:
            result.append(Node(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """select r1.driverId as driverId1, r2.driverId as driverId2, count(*) as peso
                    from results r1, results r2, races ra
                    where r1.raceId = ra.raceId and r1.raceId = r2.raceId and ra.`year` = %s and r1.driverId != r2.driverId and r1.position > r2.position and r2.position > 0
                    group by r1.driverId, r2.driverId"""

        cursor.execute(query, (year,))

        for row in cursor:
            result.append(Edge(**row))

        cursor.close()
        conn.close()
        return result

    #Due piloti sono collegati se hanno condiviso nella stessa stagione la stessa posizione finale in gara
    #il peso è il numero di occorrenze
    @staticmethod
    def getAllEdges2(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """select least(r1.driverId, r2.driverId) as driverId1, greatest(r1.driverId, r2.driverId) as driverId2, count(*) as peso
                    from results r1, results r2, races ra1, races ra2
                    where r1.driverId != r2.driverId and r1.position = r2.position AND r1.position IS NOT null and
                    ra1.raceId = r1.raceId and ra2.raceId = r2.raceId and ra1.year = ra2.year and ra1.year = %s
                    group by driverId1, driverId2"""

        cursor.execute(query, (year,))

        #for row in cursor:
            #result.append(Edge2(**row))

        cursor.close()
        conn.close()
        return result

    # Due piloti partono dalla stessa posizione in gare diverse
    # il peso è il numero di occorrenze
    @staticmethod
    def getAllEdges3():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """SELECT 
                    LEAST(r1.driverId, r2.driverId) AS d1,
                    GREATEST(r1.driverId, r2.driverId) AS d2,
                    COUNT(*) AS peso
                    FROM results r1
                    JOIN results r2 ON r1.grid = r2.grid AND r1.driverId < r2.driverId
                    WHERE r1.grid IS NOT NULL
                    GROUP BY d1, d2
                    """

        cursor.execute(query)

        # for row in cursor:
        # result.append(Edge3(**row))

        cursor.close()
        conn.close()
        return result

    # Due costruttori hanno gareggiato nella stessa stagione
    @staticmethod
    def getAllEdges4():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """SELECT DISTINCT 
                    LEAST(r1.constructorId, r2.constructorId) AS c1,
                    GREATEST(r1.constructorId, r2.constructorId) AS c2
                    FROM results r1
                    JOIN results r2 ON r1.raceId = r2.raceId
                    JOIN races ra ON r1.raceId = ra.raceId
                    WHERE r1.constructorId < r2.constructorId
                                        """

        cursor.execute(query)

        # for row in cursor:
        # result.append(Edge4(**row))

        cursor.close()
        conn.close()
        return result

    # Due piloti se hanno stessi millisecondi in best lap nella stessa gara
    # il peso è il numero di occorrenze
    @staticmethod
    def getAllEdges5():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """SELECT 
                    LEAST(l1.driverId, l2.driverId) AS d1,
                    GREATEST(l1.driverId, l2.driverId) AS d2,
                    COUNT(*) AS peso
                    FROM laptimes l1
                    JOIN laptimes l2 ON l1.raceId = l2.raceId AND l1.driverId < l2.driverId
                    WHERE l1.milliseconds = l2.milliseconds
                    GROUP BY d1, d2
                    """

        cursor.execute(query)

        # for row in cursor:
        # result.append(Edge5(**row))

        cursor.close()
        conn.close()
        return result

    # Due costruttori hanno gareggiato nella stessa stagione
    # il peso è il numero di occorrenze
    @staticmethod
    def getAllEdges6():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """SELECT 
                    LEAST(r1.constructorId, r2.constructorId) AS c1,
                    GREATEST(r1.constructorId, r2.constructorId) AS c2,
                    COUNT(DISTINCT ra.circuitId) AS peso
                    FROM results r1
                    JOIN results r2 ON r1.raceId = r2.raceId AND r1.constructorId < r2.constructorId
                    JOIN races ra ON r1.raceId = ra.raceId
                    GROUP BY c1, c2"""

        cursor.execute(query)

        # for row in cursor:
        # result.append(Edge6(**row))

        cursor.close()
        conn.close()
        return result

    # Due piloti sono collegati da quello ha fatto più sorpassi verso chi ne ha subiti
    # il peso è il numero di occorrenze
    @staticmethod
    def getAllEdges7():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """WITH sorpassi AS (
                      SELECT r1.driverId AS sorpassante, r2.driverId AS sorpassato
                      FROM results r1
                      JOIN results r2 ON r1.raceId = r2.raceId
                      WHERE r1.grid > r2.grid AND r1.position < r2.position
                    )
                    SELECT sorpassante, sorpassato, COUNT(*) AS peso
                    FROM sorpassi
                    GROUP BY sorpassante, sorpassato"""

        cursor.execute(query)

        # for row in cursor:
        # result.append(Edge7(**row))

        cursor.close()
        conn.close()
        return result

    # Due piloti sono legati se hanno effettuato pitstop nello stesso giro e nela stessa gara
    # il peso è il numero di occorrenze
    @staticmethod
    def getAllEdges8():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """SELECT 
                    LEAST(p1.driverId, p2.driverId) AS d1,
                    GREATEST(p1.driverId, p2.driverId) AS d2,
                    COUNT(*) AS peso
                    FROM pitstops p1
                    JOIN pitstops p2 ON p1.raceId = p2.raceId AND p1.lap = p2.lap
                    WHERE p1.driverId < p2.driverId
                    GROUP BY d1, d2"""

        cursor.execute(query)

        # for row in cursor:
        # result.append(Edge8(**row))

        cursor.close()
        conn.close()
        return result

    # Due piloti sono legati se hanno ricevuto la stessa penalità nella stessa gara
    # il peso è il numero di occorrenze
    @staticmethod
    def getAllEdges9():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """SELECT 
                    LEAST(r1.driverId, r2.driverId) AS d1,
                    GREATEST(r1.driverId, r2.driverId) AS d2,
                    COUNT(*) AS peso
                    FROM results r1
                    JOIN results r2 ON r1.raceId = r2.raceId AND r1.driverId < r2.driverId
                    WHERE r1.statusId = r2.statusId AND r1.statusId NOT IN (1) -- 1 = "Finished"
                    GROUP BY d1, d2"""

        cursor.execute(query)

        # for row in cursor:
        # result.append(Edge9(**row))

        cursor.close()
        conn.close()
        return result

    # Due costruttori sono legati ha avuto più punti verso chi ne ha avuti meno nella stessa gara
    # il peso è il numero di occorrenze
    @staticmethod
    def getAllEdges10():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """SELECT 
                    cs1.constructorId AS vincente,
                    cs2.constructorId AS sconfitto,
                    COUNT(*) AS peso
                    FROM constructorstandings cs1
                    JOIN constructorstandings cs2 
                      ON cs1.raceId = cs2.raceId AND cs1.constructorId <> cs2.constructorId
                    WHERE cs1.points > cs2.points
                    GROUP BY vincente, sconfitto"""

        cursor.execute(query)

        # for row in cursor:
        # result.append(Edge10(**row))

        cursor.close()
        conn.close()
        return result

    # Due costruttori sono legati se hanno preso lo stesso punteggio nelle stesse gare
    # il peso è il numero di occorrenze
    @staticmethod
    def getAllEdges11():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """SELECT 
                    LEAST(cr1.constructorId, cr2.constructorId) AS c1,
                    GREATEST(cr1.constructorId, cr2.constructorId) AS c2,
                    COUNT(*) AS peso
                    FROM constructorresults cr1
                    JOIN constructorresults cr2 
                      ON cr1.raceId = cr2.raceId AND cr1.constructorId < cr2.constructorId
                    WHERE cr1.points = cr2.points
                    GROUP BY c1, c2"""

        cursor.execute(query)

        # for row in cursor:
        # result.append(Edge11(**row))

        cursor.close()
        conn.close()
        return result