def Log_Cadastro(cursor):
    cursor.execute("INSERT INTO log (logfk) VALUES (SELECT logpk FROM logtypes WHERE logtype = 'cadastro')")
    