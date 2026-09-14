import requests
import json
import sqlite3

class TursoRow:
    """Mimics sqlite3.Row - acts like a tuple but allows dict-like and attribute access."""
    def __init__(self, cols, values):
        self._cols = cols
        self._values = tuple(values)
        self._col_map = {col.lower(): i for i, col in enumerate(cols)}

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._values[key]
        if isinstance(key, str):
            idx = self._col_map.get(key.lower())
            if idx is not None:
                return self._values[idx]
            raise KeyError(key)
        raise TypeError("Index must be int or string")

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __iter__(self):
        return iter(self._values)

    def __len__(self):
        return len(self._values)

    def keys(self):
        return self._cols

class TursoCursor:
    def __init__(self, conn):
        self.conn = conn
        self.lastrowid = None
        self._rows = []
        self.rowcount = -1

    def execute(self, query, params=None):
        return self._execute_stmt(query, params)

    def executemany(self, query, params_seq):
        for params in params_seq:
            self._execute_stmt(query, params)
        return self

    def _execute_stmt(self, query, params=None):
        if params:
            args = []
            if isinstance(params, (tuple, list)):
                for p in params:
                    if p is None:
                        args.append({"type": "null"})
                    elif isinstance(p, int):
                        args.append({"type": "integer", "value": str(p)})
                    elif isinstance(p, float):
                        args.append({"type": "float", "value": float(p)})
                    else:
                        args.append({"type": "text", "value": str(p)})
            else:
                pass
            stmt = {"sql": query, "args": args}
        else:
            stmt = {"sql": query}

        payload = {
            "requests": [
                {"type": "execute", "stmt": stmt},
                {"type": "close"}
            ]
        }
        try:
            resp = requests.post(self.conn.url, headers=self.conn.headers, json=payload, timeout=20)
            if resp.status_code != 200:
                print(f"HTTP ERROR: {resp.status_code}")
                print(resp.text)
            resp_data = resp.json()
        except Exception as e:
            print("Request exception:", e)
            return self
        
        try:
            res = resp_data["results"][0]["response"]["result"]
            cols = [c["name"] for c in res["cols"]]
            
            parsed_rows = []
            for row in res["rows"]:
                values = []
                for i, col in enumerate(cols):
                    val = row[i].get("value")
                    val_type = row[i].get("type")
                    if val_type == "integer":
                        val = int(val) if val else 0
                    elif val_type == "float":
                        val = float(val) if val else 0.0
                    elif val_type == "null":
                        val = None
                    values.append(val)
                parsed_rows.append(TursoRow(cols, values))
            
            self._rows = parsed_rows
            self.lastrowid = res.get("last_insert_rowid")
            self.rowcount = res.get("affected_row_count", -1)
        except Exception as e:
            print("Turso Error:", resp_data, e)
            self._rows = []
            self.rowcount = -1

        return self

    def fetchone(self):
        if self._rows:
            return self._rows.pop(0)
        return None

    def fetchall(self):
        res = self._rows
        self._rows = []
        return res

class TursoConnection:
    def __init__(self, db_url, auth_token):
        if not db_url.endswith("/v2/pipeline"):
            if db_url.startswith("libsql://"):
                db_url = db_url.replace("libsql://", "https://")
            db_url = db_url.rstrip("/") + "/v2/pipeline"
            
        self.url = db_url
        self.headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        }
        self.row_factory = None

    def cursor(self):
        return TursoCursor(self)

    def commit(self):
        pass

    def close(self):
        pass

def connect(url, token):
    return TursoConnection(url, token)
