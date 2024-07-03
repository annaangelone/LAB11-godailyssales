from database.DB_connect import DBConnect
from model.prodotto import Prodotto
from model.connessione import Connessione

class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getColors():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor()
        query = ("""SELECT DISTINCT Product_color as color
                    FROM go_products
                    order by color""")
        cursor.execute(query,)

        for row in cursor:
            result.append(row[0])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getProducts(colore):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = ("""SELECT DISTINCT *
                    from go_products
                    where product_color = %s""")
        cursor.execute(query, (colore,))

        for row in cursor:
            result.append(Prodotto(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(p1, p2, anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = ("""SELECT gds1.Product_number as prod1, gds2.Product_number as prod2, count(distinct gds1.Date) as peso
                    from go_daily_sales gds1, go_daily_sales gds2
                    where gds1.Product_number = %s and gds2.Product_number = %s
                    and gds1.Retailer_code = gds2.Retailer_code and gds1.Date = gds2.Date
                    and YEAR(gds1.Date) = %s
                    group by prod1, prod2""")
        cursor.execute(query, (p1, p2, anno))

        for row in cursor:
            result.append(row["peso"])

        cursor.close()
        conn.close()
        return result