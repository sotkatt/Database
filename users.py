import requests, os, psycopg2, random
os.system('clear')

URL = "https://randomuser.me/api/?nat=ru"


def get_user_data():
    response = requests.get(URL)
    
    if response.status_code != 200:
        return None
    
    return response.json()


def proccessing():
    data = get_user_data()['results'][0]

    professions = [
        "engineer", "teacher", "scientist", 
        "developer", "programmer", "artist", 
        "designer", "nurse", "doctor", "lawyer"
    ]

    salary = random.randint(200000, 1400000)

    return {
        "first_name": data['name']['first'],
        "last_name": data['name']['last'],
        "gender": data['gender'],
        "email": data['email'],
        "date": data['dob']['date'],
        "age": data['dob']['age'],
        "phone_number": data['phone'],
        "username": data['login']['username'],
        "password": data['login']['password'],
        "street": data['location']['street']['name'],
        "city": data['location']['city'],
        "country": data['location']['country'],
        "profession": random.choice(professions),
        "salary": salary
    }


def post_database(count_person=999):
    connection = psycopg2.connect( 
        host="localhost", 
        user="mereke", 
        password="123", 
        database="wake_up", 
        port="5432"
    )
    cursor = connection.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS persons(\
            id SERIAL PRIMARY KEY,\
            first_name VARCHAR(125) DEFAULT 'неизвестно',\
            last_name VARCHAR(125) DEFAULT 'неизвестно',\
            gender VARCHAR(20) DEFAULT 'неизвестно',\
            email VARCHAR(155) DEFAULT 'неизвестно',\
            date VARCHAR(125) DEFAULT 'неизвестно',\
            age INT DEFAULT 18,\
            phone_number VARCHAR(25) DEFAULT 'неизвестно',\
            username VARCHAR(60) DEFAULT 'неизвестно',\
            password VARCHAR(125) DEFAULT 'неизвестно',\
            street VARCHAR(255) DEFAULT 'неизвестно',\
            city VARCHAR(100) DEFAULT 'неизвестно',\
            country VARCHAR(100) DEFAULT 'неизвестно',\
            profession VARCHAR(100) DEFAULT 'неизвестно',\
            salary INT DEFAULT 200000)"
    )

    for person in range(count_person + 1):
        user = proccessing()

        try:
            cursor.execute(
                "INSERT INTO persons(\
                    first_name, last_name, gender, email, date, age,\
                    phone_number, username, password, street, city,\
                    country, profession, salary)\
                VALUES(\
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\
                )", (
                    user['first_name'], user['last_name'], user['gender'],
                    user['email'], user['date'], user['age'],
                    user['phone_number'], user['username'], user['password'],
                    user['street'], user['city'], user['country'],
                    user['profession'], user['salary']
                )
            )
            print(
                f"{person}: Данные пользователя {user['first_name']} {user['last_name']} добавлены в базу данных"
            )
        except Exception:
            continue
    
    connection.commit()
    cursor.close()
    connection.close()

    return f"Данные пользователей добавлены в базу данных"

print(post_database())