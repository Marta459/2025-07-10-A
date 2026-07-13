from database.DB_connect import DBConnect


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct (order_date) from orders o order by order_date"

        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def getTutteCategorie():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from categories"""

        cursor.execute(query)

        for row in cursor:
            results.append(row)

        cursor.close()
        conn.close()
        return results

# Faccio una query per prendermi i miei nodi

    @staticmethod
    def getProdotti(categoria):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct p.product_id , p.product_name, p.list_price  
                    from categories c, products p
                    where p.category_id = c.category_id and c.category_id = %s
                        """

        cursor.execute(query, (categoria,))

        for row in cursor:
            results.append(row)

        cursor.close()
        conn.close()
        return results

# Presi i nodi vado nel model per costruire il metodo def creaGrafo

#Ora devo pensare ai miei archi

    @staticmethod
    def getVendite(data1, data2):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT p.product_id, p.product_name, COUNT(oi.order_id) AS num_vendite
                   FROM products p, order_items oi, orders o
                   WHERE p.product_id = oi.product_id
                     AND oi.order_id = o.order_id
                     AND o.order_date BETWEEN %s AND %s
                   GROUP BY p.product_id, p.product_name"""
        cursor.execute(query, (data1, data2))
        for row in cursor:
            results.append(row)
        cursor.close()
        conn.close()
        return results