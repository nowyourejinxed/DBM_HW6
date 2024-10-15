import psycopg


class ConnectionManager:
    def __init__(self, connection_string):
        self.conn = psycopg.connect(connection_string)

        self.cursor = self.conn.cursor()

    def grab_count(self):
        self.cursor.execute("""
            SELECT count(*) AS count FROM "entry";
        """)
        count = self.cursor.fetchone()[0]
        print(count)
        return count

    def search_foods(self):
        self.cursor.execute("""
                SELECT DISTINCT description, fdc_id FROM "food"
            """)
        return self.cursor.fetchall()

    def insert_food(self, selected_date, food_id, email):
        try:
            count = self.link_entry(email)
            self.cursor.execute("""
                INSERT INTO "entry" (entryid, foodid, amount, date) VALUES (%s, %s, %s, %s);
            """, (
                count, food_id, 1, selected_date))

            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            return str(e)

    def link_entry(self, email):
        email = str(email)
        count = self.grab_count()
        print(f"count{count}")
        self.cursor.execute("""
             INSERT INTO "user_entry" ("user_email", "entryid") VALUES (%s, %s);
         """, (email, count))
        self.conn.commit()
        return count

    def get_totals(self, selected_date):
        self.cursor.execute("""
            SELECT SUM(food_calorie_conversion_factor.protein_value) as protein, SUM(food_calorie_conversion_factor.fat_value) as fat, SUM(food_calorie_conversion_factor.carbohydrate_value) as carbs
            FROM (("users" JOIN "user_entry" ON email = user_email) JOIN "entry" ON entry.entryid = user_entry.entryid)
            JOIN "food" ON food.fdc_id = entry.foodid
            JOIN food_nutrient_conversion_factor ON food_nutrient_conversion_factor.fdc_id = food.fdc_id
            JOIN food_calorie_conversion_factor ON food_nutrient_conversion_factor.id = food_calorie_conversion_factor.food_nutrient_conversion_factor_id
            WHERE entry.date = %s;
        """, (selected_date,))
        print(self.cursor.fetchall())
        return self.cursor.fetchall()

    def pull_entries(self, selected_date):
        try:
            self.cursor.execute("""
                SELECT food.description, SUM(food_calorie_conversion_factor.protein_value) as protein, SUM(food_calorie_conversion_factor.fat_value) as fat, SUM(food_calorie_conversion_factor.carbohydrate_value) as carbs
                FROM (("users" JOIN "user_entry" ON email = user_email) JOIN "entry" ON entry.entryid = user_entry.entryid)
                JOIN "food" ON food.fdc_id = entry.foodid
                JOIN food_nutrient_conversion_factor ON food_nutrient_conversion_factor.fdc_id = food.fdc_id
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
