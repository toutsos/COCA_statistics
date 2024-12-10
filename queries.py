import sqlite3
import pandas as pd

if __name__ == "__main__":
    conn = sqlite3.connect('word_pairs.db')
    cursor = conn.cursor()

    query = '''
            SELECT root, count
            FROM WordPair wp, Word w1
            WHERE wp.word2_id = w1.id
            AND word1_id = (SELECT id FROM Word WHERE root='listen')
            ORDER BY count desc
            '''
    try:
        # Load the query result into a DataFrame
        df = pd.read_sql_query(query, conn)
        # Display the DataFrame as a table
        # print(df)

        # Write the DataFrame to a CSV file
        df.to_csv('output.csv', index=False)

    except sqlite3.Error as e:
        print("SQLite error:", e)
    finally:
        conn.close()