import psycopg2
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import axes3d
import datetime


# 1
def no_of_movies_per_year(cur):
    cur.execute('''
        SELECT date_trunc('year', release_date) AS release_year, COUNT(*)
        FROM movie
        GROUP BY release_year
        ORDER BY release_year ASC;
    ''')

    rows = cur.fetchall()

    years = []
    no_of_movies = []
    for row in rows:
        if row[0] is None:
            continue

        years.append(row[0].year)
        no_of_movies.append(row[1])

    x = np.array(years)
    y = np.array(no_of_movies)

    plt.xlabel('Year')
    plt.ylabel('Number of Movies')
    # plt.scatter(x, y, s = 1)
    plt.plot(x, y)
    plt.show()


# 2
def no_of_movies_per_genre(cur):
    cur.execute('''
            SELECT g.name, COUNT(mg.movie_id)
            FROM movie_genres as mg
            INNER JOIN genre g
            ON mg.genre_id = g.id
            GROUP BY g.name;
        ''')

    rows = cur.fetchall()

    genre_names = []
    no_of_movies = []
    for row in rows:
        genre_names.append(row[0])
        no_of_movies.append(row[1])

    x = np.array(genre_names)
    y = np.array(no_of_movies)

    plt.xlabel('Genre')
    plt.ylabel('Number of Movies')
    plt.xticks(rotation=45)
    plt.bar(x, y)
    plt.subplots_adjust(bottom=0.25)
    plt.show()


# 3
def no_of_movies_per_genre_per_year(cur):
    cur.execute('''
                SELECT COUNT(m.title), g.name, date_trunc('year', release_date) AS release_year FROM Movie m
                INNER JOIN Movie_genres mg ON m.id = mg.movie_id
                INNER JOIN Genre g ON mg.genre_id = g.id
                GROUP BY g.name, release_year
                ORDER BY release_year;
            ''')

    rows = cur.fetchall()
    unique_genres = set()
    unique_years = set()
    for row in rows:
        if row[2] is None:
            continue

        unique_genres.add(row[1])
        unique_years.add(row[2].year)

    years = list(unique_years)

    x_genres = []
    for genre in unique_genres:
        for _ in years:
            x_genres.append(genre)

    i = 0
    x_dict = {}
    x = []
    for genre in x_genres:
        if genre not in x_dict:
            x_dict[genre] = i
            x.append(i)
            i += 1
        else:
            x.append(x_dict[genre])

    y = years * len(unique_genres)
    z = np.zeros(len(x))
    dx = np.ones(len(x)) * 0.25
    dy = np.ones(len(x)) * 0.25

    data = {}
    for row in rows:
        if row[2] is None:
            continue

        if row[2].year in data:
            data[row[2].year][row[1]] = row[0]
        else:
            data[row[2].year] = {row[1]: row[0]}

    dz = []

    for i in range(len(x)):
        if x_genres[i] in data[y[i]]:
            dz.append(data[y[i]][x_genres[i]])
        else:
            dz.append(0)

    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection='3d')
    ax1.set_facecolor((1.0, 1.0, 1.0))

    ax1.bar3d(x, y, z, dx, dy, dz)

    plt.xticks(range(len(x_dict.values())), x_dict.keys())
    plt.show()


# 4
def max_budget_per_year(cur):
    cur.execute('''
        SELECT date_trunc('year', release_date) AS release_year, MAX(budget)
        FROM movie
        GROUP BY release_year
        ORDER BY release_year;
    ''')

    rows = cur.fetchall()

    years = []
    max_budgets = []
    for row in rows:
        if row[0] is None:
            continue
        years.append(row[0].year)
        max_budgets.append(row[1])

    x = np.array(years)
    y = np.array(max_budgets)

    plt.xlabel('Year')
    plt.ylabel('Max Budget')
    plt.xticks(rotation=45)
    plt.plot(x, y)
    plt.subplots_adjust(bottom=0.15)
    plt.show()


# 5
def total_revenue_per_year_for_actor(cur):
    cur.execute('''
            SELECT date_trunc('year', m.release_date) AS release_year, SUM(m.revenue) FROM Actor a 
            INNER JOIN Person p ON a.person_id = p.person_id 
            INNER JOIN Movie_Cast mc ON a.person_id = mc.person_id
            INNER JOIN Movie m ON mc.movie_id = m.id
            WHERE p.name = 'Leonardo DiCaprio'
            GROUP BY release_year
            ORDER BY release_year ASC;
        ''')

    rows = cur.fetchall()

    years = []
    total_revenue_per_year = []
    for row in rows:
        years.append(row[0].year)
        total_revenue_per_year.append(row[1])

    x = np.array(years)
    y = np.array(total_revenue_per_year)

    plt.xlabel('Year')
    plt.ylabel('Total Revenue')
    plt.xticks(rotation=45)
    plt.bar(x, y)
    plt.subplots_adjust(bottom=0.25)
    plt.show()


# 6
def average_rating_per_user(cur):
    cur.execute('''
            SELECT user_id, AVG(rating)
            FROM ratings
            GROUP BY user_id
            ORDER BY user_id ASC;
        ''')

    rows = cur.fetchall()

    users = []
    avgs = []
    for row in rows:
        users.append(row[0])
        avgs.append(row[1])

    x = np.array(users)
    y = np.array(avgs)

    plt.xlabel('User Id')
    plt.ylabel('Average')
    plt.scatter(x, y, s=1)
    plt.show()


# 7
def no_of_ratings_per_user(cur):
    cur.execute('''
        SELECT user_id, COUNT(rating)
        FROM ratings
        GROUP BY user_id
        ORDER BY user_id ASC;
        ''')

    rows = cur.fetchall()

    users = []
    count = []
    for row in rows:
        users.append(row[0])
        count.append(row[1])

    x = np.array(users)
    y = np.array(count)

    plt.xlabel('User Id')
    plt.ylabel('Number of Ratings')
    plt.scatter(x, y, s=1)
    plt.show()


# 8
def no_of_ratings_avg_rating(cur):
    cur.execute("""
        SELECT user_id, COUNT(rating), AVG(rating)
        FROM ratings
        GROUP BY user_id
        ORDER BY user_id ASC;
    """)

    rows = cur.fetchall()

    count = []
    avgs = []
    for row in rows:
        count.append(row[1])
        avgs.append(row[2])

    x = np.array(count)
    y = np.array(avgs)

    plt.xlabel('Number of Ratings')
    plt.ylabel('Average Rating')
    plt.scatter(x, y, s=1)
    plt.show()


# 9
def avg_rating_per_genre(cur):
    cur.execute("""
        SELECT g.name, AVG(rating) 
        FROM ratings r
        INNER JOIN movie m
        ON r.movie_id = m.id
        INNER JOIN movie_genres mg
        ON m.id = mg.movie_id
        INNER JOIN genre g
        ON mg.genre_id = g.id
        GROUP BY g.name;
        """)

    rows = cur.fetchall()

    genres = []
    avgs = []
    for row in rows:
        genres.append(row[0])
        avgs.append(row[1])

    x = np.array(genres)
    y = np.array(avgs)

    plt.xlabel('Genres')
    plt.ylabel('Average Rating')
    plt.xticks(rotation=45)
    plt.bar(x, y)
    plt.subplots_adjust(bottom=0.25)
    plt.show()


if __name__ == '__main__':
    # Update connection string information
    host = "databases2022.postgres.database.azure.com"
    dbname = "MovieLens"
    user = "examiner@databases2022"
    password = "oursuperduperpassword0912"
    sslmode = "require"

    # Construct connection string
    conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
    conn = psycopg2.connect(conn_string)
    print("Connection established")

    cursor = conn.cursor()

    avg_rating_per_genre(cursor)
