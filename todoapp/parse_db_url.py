def parce_url(url):
    url = url.strip()
    if url.split(":")[0] == "postgres":
        return build_postgres_dic(url)
    else: 
        if url.split(":")[0] == "sqlite":
            return build_sqlite_dic(url)
        else:
            return {'ENGINE': 'engine not fount'}

def build_postgres_dic(url):
    url = url.replace("postgres://","")
    url, name = url.split("/")
    user, password = url.split("@")[0].split(":")
    host, port = url.split("@")[1].split(":")
    return {'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'USER': user,
            'PASSWORD': password,
            'HOST': host,
            'PORT': port,
            'NAME': name 
            }

def build_sqlite_dic(url):
    name = url.split("///")[1]
    return {'ENGINE': 'django.db.backends.sqlite3',
            'NAME': name
            }


print (parce_url("    sqlite:///C:/Users/admin/site_db.sqlite3   "))


# postgres://<USER>:<PASSWORD>@<HOST>:<PORT>/<NAME>


