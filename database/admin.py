import aiomysql
import config


class Text:
    async def edit_text(self, text_id, text):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''UPDATE text SET Text = %s WHERE Id = %s''', (text, text_id))
        await connect.commit()
        await cursor.close()
        connect.close()

    async def get_text(self, text_id):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''SELECT Text FROM text WHERE Id = %s''', (text_id,))
        result = await cursor.fetchone()
        await cursor.close()
        connect.close()
        return result[0]
