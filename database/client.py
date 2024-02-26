import aiomysql
import config

'''
create table if not exists user(
Id DECIMAL(15, 0),
Username TEXT,
Date datetime,
Status tinyint);
'''
class User:
    async def add_user(self, user_id, username):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''SELECT * FROM user WHERE Id = %s''', (user_id,))
        check = await cursor.fetchone()
        if not bool(check):
            await cursor.execute('''INSERT INTO user VALUES(%s, %s, CURRENT_DATE(), 1)''', (user_id, username))
            await connect.commit()
        connect.close()

    async def get_all_user(self):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''SELECT ID FROM user''')
        result = await cursor.fetchall()

        user_ids = [int(row[0]) for row in result]
        connect.close()
        return user_ids

    async def disactive_user(self, user_id):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''UPDATE user SET Status = 0 WHERE Id = %s''', (user_id,))
        await connect.commit()
        await cursor.close()
        connect.close()

    async def active_user(self, user_id):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''UPDATE user SET Status =1 WHERE Id = %s''', (user_id,))
        await connect.commit()
        await cursor.close()
        connect.close()

    async def stat_text(self):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''SELECT COUNT(Id) as count FROM user WHERE DATEDIFF(CURRENT_DATE(), Date)<=1''')
        day_users = await cursor.fetchone()
        await cursor.execute('''SELECT COUNT(Id) as count FROM user WHERE DATEDIFF(CURRENT_DATE(), Date)<=7''')
        week_users = await cursor.fetchone()
        await cursor.execute('''SELECT COUNT(Id) as count FROM user WHERE DATEDIFF(CURRENT_DATE(), Date)<=30''')
        moth_users = await cursor.fetchone()

        await cursor.execute('''SELECT COUNT(Id) as count FROM user''')
        all_users = await cursor.fetchone()
        await cursor.execute('''SELECT COUNT(Id) as count FROM user WHERE Status = 1''')
        active_users = await cursor.fetchone()
        await cursor.execute('''SELECT COUNT(Id) as count FROM user WHERE Status = 0''')
        disactive_users = await cursor.fetchone()
        return f'👥 Пользователи\n' \
               f'├ Всего: {all_users[0]}\n' \
               f'├ Живые: {active_users[0]}\n' \
               f'└ Мёртвые: {disactive_users[0]}\n\n' \
               f'📈 Динамика\n' \
               f'├ За день: +{day_users[0]}\n' \
               f'├ За неделю: +{week_users[0]}\n' \
               f'└ За месяц: +{moth_users[0]}\n'