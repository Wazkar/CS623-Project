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

        conn.rollback()
        #conn.commit()
        print(success_message)

    except Exception as e:
        conn.rollback()
        print("ERROR:", e)

    finally:
        conn.close()


# -----------------------------
# 1. DELETE PRODUCT (p1)
# -----------------------------
def delete_product():
    run_transaction(
        [
            ("DELETE FROM Product WHERE prodid = %s", ("p1",))
        ],
        "Product p1 deleted (Stock auto-updated via CASCADE)"
    )


# -----------------------------
# 2. DELETE DEPOT (d1)
# -----------------------------
def delete_depot():
    run_transaction(
        [
            ("DELETE FROM Depot WHERE depid = %s", ("d1",))
        ],
        "Depot d1 deleted (Stock auto-updated via CASCADE)"
    )


# -----------------------------
# 3. RENAME PRODUCT (p1 -> pp1)
# -----------------------------
def rename_product():
    run_transaction(
        [
            ("UPDATE Product SET prodid = %s WHERE prodid = %s", ("p1", "pp1"))
        ],
        "Product renamed from p1 to pp1"
    )


# -----------------------------
# 4. RENAME DEPOT (d1 -> dd1)
# -----------------------------
def rename_depot():
    run_transaction(
        [
            ("UPDATE Depot SET depid = %s WHERE depid = %s", ("dd1", "d1"))
        ],
        "Depot renamed from d1 to dd1"
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
        "Product p100 and Stock inserted"
    )


# -----------------------------
# 6. ADD DEPOT + STOCK
# -----------------------------
def add_depot_and_stock():
    run_transaction(
        [
            ("INSERT INTO Depot VALUES (%s, %s, %s)", ("d100", "Chicago", 100)),
            ("INSERT INTO Stock VALUES (%s, %s, %s)", ("p1", "d100", 100))
        ],
        "Depot d100 and Stock inserted"
    )


# -----------------------------
# DEMO CONTROLLER (STEP-BY-STEP)
# -----------------------------
def main():
    print("\n===== DATABASE TRANSACTION DEMO START =====\n")

    input("Step 1: Delete Product p1 (press Enter)")
    delete_product()

    input("\nStep 2: Delete Depot d1 (press Enter)")
    delete_depot()

    input("\nStep 3: Rename Product p1 -> pp1 (press Enter)")
    rename_product()

    input("\nStep 4: Rename Depot d1 -> dd1 (press Enter)")
    rename_depot()

    input("\nStep 5: Add Product + Stock (press Enter)")
    add_product_and_stock()

    input("\nStep 6: Add Depot + Stock (press Enter)")
    add_depot_and_stock()

    print("\n===== DEMO COMPLETE =====\n")


if __name__ == "__main__":
    main()
