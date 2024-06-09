
Protect the privacy of your sqlite databases (i.e. for analysis). 
These files can more safely be sent to other people, without fear of interception. You can also more safely work 
with sensitive data, as the data is encrypted with AES-256

## Example usage:

```
from sqlitesec import SqliteSec
import os

# Usage example
if os.path.exists("test.db"):
    os.remove("test.db")

key = b'blabla'
sqs = SqliteSec(key)

conn = sqs.connect("test.db")
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, data TEXT)')
cursor.execute('INSERT INTO test (data) VALUES (?)', ('Hei, verden!',))
conn.commit()
sqs.close(conn, "test.db")


# Step 2: Read the data back

conn = sqs.connect("test.db")
cursor = conn.cursor()
cursor.execute('SELECT data FROM test WHERE id=1')
fetched_data = cursor.fetchone()[0]
print(fetched_data)
sqs.close(conn, "test.db")
```
