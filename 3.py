import mysql.connector

# З'єднання з базою даних
connection = mysql.connector.connect(
    host='localhost',  # або 'localhost' для локального сервера 134.249.176.108
    user='root',
    password='root',
    database='civilization3', # Sakila server_database
    port=2023  # порт, на якому працює MySQL
)

# Створення курсора для виконання SQL-запитів
cursor = connection.cursor()

# Перевірка підключення
if connection.is_connected():
    print('Підключено до бази даних')

# Виконання SQL-запиту
cursor.execute("SHOW TABLES")

# Отримання результатів та виведення їх на екран
tables = cursor.fetchall()
print("Список таблиць:")
for table in tables:
    print(table[0])




# Виведення вмісту кожної таблиці
for table in tables:
    table_name = table[0]
    
    # Виконання SQL-запиту для отримання вмісту таблиці
    cursor.execute(f"SELECT * FROM {table_name}")
    
    # Отримання результатів та виведення їх на екран
    table_content = cursor.fetchall()
    
    print(f"\nВміст таблиці {table_name}:")
    for row in table_content:
        print(row)



# Закриття курсора та з'єднання
cursor.close()
connection.close()



import asyncio
import aiomysql

async def handle_client(reader, writer):
    # Отримуємо дані від клієнта
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print(f"Received {message} from {addr}")

    # Підключаємось до бази даних
    async with aiomysql.connect(host='localhost', port=3306,
                                 user='user', password='password',
                                 db='database') as conn:
        async with conn.cursor() as cursor:
            # Виконуємо запит до бази даних
            await cursor.execute("SELECT * FROM table")
            result = await cursor.fetchall()
            print("Received data from database:", result)

    # Надсилаємо відповідь клієнту
    response = "Hello from server!"
    writer.write(response.encode())
    await writer.drain()

    # Закриваємо з'єднання
    writer.close()

async def main():
    server = await asyncio.start_server(
        handle_client, '127.0.0.1', 8888)

    async with server:
        await server.serve_forever()

asyncio.run(main())