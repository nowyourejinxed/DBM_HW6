import psycopg

class ConnectionManager:
        def __init__(self, dbname, user, password, host, port):
            self.conn = psycopg.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            self.cursor = self.conn.cursor()

        def insert_food(self, selected_date, food_id):
            try:
                self.cursor.execute("""
                    INSERT INTO entry (date,)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                selected_date, food_id))
                self.conn.commit()
            except Exception as e:
                self.conn.rollback()
                return str(e)

        def pull_entries(self, selected_date):
            try:
                self.cursor.execute("""
                    SELECT food.description, SUM(food_calorie_conversion_factor.protein_value) as protein, SUM(food_calorie_conversion_factor.fat_value) as fat, SUM(food_calorie_conversion_factor.carbohydrate_value) as carbs
                    FROM (("users" JOIN "user_entry" ON email = user_email) JOIN "entry" ON entry.entryid = user_entry.entryid)
                    JOIN "food" ON food.fdc_id = entry.foodid
                    JOIN food_nutrient_conversion_factor ON food.fdc_id = food_nutrition_conversion_factor.fdc_id
                    JOIN food_calorie_conversion_factor ON food_nutrient_conversion_factor.id = food_calorie_conversion_factor.food_nutrient_conversion_factor_id
                    WHERE entry.date = %s
                    GROUP BY food.description;
                """, (selected_date,))
                return self.cursor.fetchall()
            except Exception as e:
                return str(e)

        def close(self):
            self.cursor.close()
            self.conn.close()