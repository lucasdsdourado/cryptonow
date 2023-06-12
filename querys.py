sql = [
["""
    CREATE TABLE IF NOT EXISTS MARKETATUAL (
        id INTEGER NOT NULL,
        starttime TEXT,
        moeda TEXT, 
        vlatual TEXT, 
        vlanter TEXT, 
        percent TEXT, 
        PRIMARY KEY(id AUTOINCREMENT)
    )"""],
["""
    INSERT INTO MARKETATUAL (starttime,moeda,vlatual,vlanter,percent) 
    VALUES ('{}','{}','{}','{}','{}')"""],
["""
    CREATE TABLE IF NOT EXISTS LOGERROS (
        id INTEGER NOT NULL,
        ERRO TEXT,
        PRIMARY KEY(id AUTOINCREMENT)
    )"""],
['DROP TABLE IF EXISTS MARKETANTIG'],
['CREATE TABLE IF NOT EXISTS MARKETANTIG AS SELECT * FROM MARKETATUAL'],
['DELETE FROM MARKETATUAL'],
['INSERT INTO LOGERROS (ERRO) VALUES({})'],
['DELETE FROM LOGERROS'],
["""
    CREATE TABLE IF NOT EXISTS FAVORITAS (
        MOEDA TEXT
    )"""],
["INSERT INTO FAVORITAS (MOEDA) VALUES('{}')"],
["DELETE FROM FAVORITAS WHERE MOEDA = '{}'"],
["UPDATE FAVORITAS SET MOEDA = '{}' WHERE MOEDA = '{}'"]
]