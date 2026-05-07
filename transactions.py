from psycopg2 import connect

# -----------------------------
# DATABASE CONNECTION
# -----------------------------
def get_connection():
    return connect(
        host="localhost",
        port=5432,
        database="project",
        user="postgres",
        password="password"
    )


# -----------------------------
# GENERIC TRANSACTION WRAPPER
# -----------------------------
def run_transaction(queries, success_message):
    conn = get_connection()
    cur = conn.cursor()

    try:
        for query, params in queries:
            cur.execute(query, params)

        conn.commit()
        print(success_message)

    except Exception as e:
        conn.rollback()
        print("ERROR:", e)

    finally:
        conn.close()


# -----------------------------
# 1. RENAME PRODUCT (p1 -> pp1)
# -----------------------------
def rename_product():
    run_transaction(
        [
            ("UPDATE Product SET prodid = %s WHERE prodid = %s", ("pp1", "p1"))
        ],
        "Product renamed: p1 → pp1"
    )


# -----------------------------
# 2. RENAME DEPOT (d1 -> dd1)
# -----------------------------
def rename_depot():
    run_transaction(
        [
            ("UPDATE Depot SET depid = %s WHERE depid = %s", ("dd1", "d1"))
        ],
        "Depot renamed: d1 → dd1"
    )


# -----------------------------
# 3. DELETE PRODUCT (pp1)
# -----------------------------
def delete_product():
    run_transaction(
        [
            ("DELETE FROM Product WHERE prodid = %s", ("pp1",))
        ],
        "Product pp1 deleted (CASCADE updates Stock)"
    )


# -----------------------------
# 4. DELETE DEPOT (dd1)
# -----------------------------
def delete_depot():
    run_transaction(
        [
            ("DELETE FROM Depot WHERE depid = %s", ("dd1",))
        ],
        "Depot dd1 deleted (CASCADE updates Stock)"
    )


# -----------------------------
# 5. ADD PRODUCT + STOCK
# -----------------------------
def add_product_and_stock():
    run_transaction(
        [
            ("INSERT INTO Product VALUES (%s, %s, %s)", ("p100", "cd", 5)),
            ("INSERT INTO Stock VALUES (%s, %s, %s)", ("p100", "d2", 50))
        ],
        "Inserted Product p100 + Stock entry"
    )


# -----------------------------
# 6. ADD DEPOT + STOCK
# -----------------------------
def add_depot_and_stock():
    run_transaction(
        [
            ("INSERT INTO Depot VALUES (%s, %s, %s)", ("d100", "Chicago", 100)),
            ("INSERT INTO Stock VALUES (%s, %s, %s)", ("p100", "d100", 100))
        ],
        "Inserted Depot d100 + Stock entry"
    )


# -----------------------------
# DEMO CONTROLLER (FIXED ORDER)
# -----------------------------
def main():
    print("\n===== DATABASE TRANSACTION DEMO START =====\n")

    input("Step 1: Rename Product p1 → pp1")
    rename_product()

    input("\nStep 2: Rename Depot d1 → dd1")
    rename_depot()

    input("\nStep 3: Delete Product pp1")
    delete_product()

    input("\nStep 4: Delete Depot dd1")
    delete_depot()

    input("\nStep 5: Add Product p100 + Stock")
    add_product_and_stock()

    input("\nStep 6: Add Depot d100 + Stock")
    add_depot_and_stock()

    print("\n===== DEMO COMPLETE =====\n")


if __name__ == "__main__":
    main()