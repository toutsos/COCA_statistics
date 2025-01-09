import sqlite3
import sys
import pandas as pd





if __name__=="__main__":

    if len(sys.argv) == 5:

        word1 = sys.argv[1].lower()
        word1_type = sys.argv[2].lower()
        word2 = sys.argv[3].lower()
        word2_type = sys.argv[4].lower()

        conn = sqlite3.connect('word_pairs.db')
        cursor = conn.cursor()

        query = '''
                    SELECT sum(count) AS total_count
                    FROM WordPair wp JOIN Word w ON w.Id=wp.Word2_id OR w.Id=wp.Word1_id
                    WHERE (wp.Word1_id=(SELECT Id FROM Word WHERE Root=? AND pos=?)
                    OR wp.Word2_id=(SELECT Id FROM Word WHERE Root=? AND pos=?))
                    AND w.pos=?;
                '''

        query_1 = '''
                    WITH VerbId AS (
                        SELECT Id FROM Word WHERE Root=? AND pos=?
                    ),
                    NounId AS (
                        SELECT Id FROM Word WHERE Root=? AND pos=?
                    )
                    SELECT SUM(total_count) AS overall_sum
                    FROM (
                        SELECT SUM(wp.count) AS total_count
                        FROM WordPair wp
                        WHERE wp.Word1_id = (SELECT Id FROM VerbId)
                          AND wp.Word2_id = (SELECT Id FROM NounId)

                        UNION ALL

                        SELECT SUM(wp.count)
                        FROM WordPair wp
                        WHERE wp.Word2_id = (SELECT Id FROM VerbId)
                          AND wp.Word1_id = (SELECT Id FROM NounId)
                    ) AS union_sums;
        '''

        try:
            cursor.execute(query, (word1, word1_type, word1, word1_type, word2_type,))
            result1 = cursor.fetchall()
            print(f'Total \033[1m{word2_type}s\033[0m associated with the {word1_type} \033[1m{word1}\033[0m: \033[1m{result1[0][0]}\033[0m')

            cursor.execute(query, (word2, word2_type, word2, word2_type, word1_type,))
            result3 = cursor.fetchall()
            print(f'Total \033[1m{word1_type}s\033[0m associated with the {word2_type} \033[1m{word2}\033[0m: \033[1m{result3[0][0]}\033[0m')

            if result1[0][0] == None or result3[0][0] == None:
                print(f'Probability of \033[1m{word1}\033[0m and \033[1m{word2}\033[0m co-occurring in the same sentence: \033[1m0%\033[0m')
            else:
                cursor.execute(query_1, (word1, word1_type, word2, word2_type,))
                result2 = cursor.fetchall()
                print(f'Occurrences of \033[1m{word1}\033[0m and \033[1m{word2}\033[0m appearing together in the same sentence: \033[1m{result2[0][0]}\033[0m')

                probability1 = (result2[0][0]/result1[0][0])*100
                probability2 = (result2[0][0] / result3[0][0]) * 100
                probability = max(probability1, probability2)

                print(f'Probability of \033[1m{word1}\033[0m and \033[1m{word2}\033[0m co-occurring in the same sentence: \033[1m{probability:.6f}%\033[0m')


        except sqlite3.Error as e:
            print("SQLite error:", e)
        finally:
            conn.close()

    elif len(sys.argv) == 4:

        word1 = sys.argv[1].lower()
        word1_type = sys.argv[2].lower()
        types = sys.argv[3].lower()

        conn = sqlite3.connect('word_pairs.db')
        cursor = conn.cursor()

        query_1 = '''
            WITH VerbId AS (
                SELECT Id FROM Word WHERE Root=? AND pos=?
            )
            SELECT word, count
            FROM (
                SELECT w.root as word, count
                FROM WordPair wp, Word w, Word w1
                WHERE wp.Word1_id = (SELECT Id FROM VerbId)
                  AND wp.Word2_id = w.Id
                  AND w.pos = ?
                  AND wp.Word1_id = w1.id
                UNION ALL

                SELECT w.root as word_id , count
                FROM WordPair wp, Word w, Word w1
                WHERE wp.Word2_id = (SELECT Id FROM VerbId)
                  AND wp.Word1_id = w.Id
                  AND w.pos = ?
                  AND wp.Word2_id = w1.id
            ) AS union_sums
            ORDER BY count DESC
            LIMIT 10;
        '''

        try:
            cursor.execute(query_1, (word1, word1_type, types, types,))
            results = cursor.fetchall()

            # Display the results
            print("Word ID | Count")
            print("------------------")
            for word_id, count in results:
                print(f"{word_id} | {count}")


        except sqlite3.Error as e:
            print("SQLite error:", e)
        finally:
            conn.close()