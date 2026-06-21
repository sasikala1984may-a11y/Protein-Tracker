import streamlit as st
import mysql.connector
import pandas as pd


@st.cache_resource
def get_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='ridhan',
            database='protien_tracker'
        )
        return conn
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return None


def get_all_foods(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM pro_content")
    data = cur.fetchall()
    df = pd.DataFrame(data, columns=["Food", "Protein_per_100g_or_unit"])
    return df


def add_food(conn, food, protein):
    cur = conn.cursor()
    cur.execute("INSERT INTO pro_content VALUES (%s, %s)", (food, protein))
    conn.commit()


def update_food(conn, food, protein):
    cur = conn.cursor()
    cur.execute("UPDATE pro_content SET Protien_content=%s WHERE Food=%s", (protein, food))
    conn.commit()


def delete_food(conn, food):
    cur = conn.cursor()
    cur.execute("DELETE FROM pro_content WHERE Food=%s", (food,))
    conn.commit()


def calculate_total_protein(conn, lines):
    # lines: list of strings like 'food,quantity'
    cur = conn.cursor()
    cur.execute("SELECT * FROM pro_content")
    dt = cur.fetchall()
    food_map = {row[0].lower(): row[1] for row in dt}
    total = 0.0
    details = []
    for line in lines:
        if not line.strip():
            continue
        parts = [p.strip() for p in line.split(",")]
        if len(parts) != 2:
            details.append((line, "invalid format"))
            continue
        food, qty_str = parts[0], parts[1]
        key = food.lower()
        if key not in food_map:
            details.append((line, "food not found"))
            continue
        try:
            qty = float(qty_str)
        except ValueError:
            details.append((line, "invalid quantity"))
            continue
        prot_val = float(food_map[key])
        if key == 'egg':
            # original app treats egg as per-unit protein
            item_protein = prot_val * qty
        else:
            per_gram = prot_val / 100.0
            item_protein = per_gram * qty
        total += item_protein
        details.append((line, f"{item_protein:.2f} g"))

    return total, details


def main():
    st.title("Protein Tracker")
    conn = get_connection()
    if conn is None:
        st.stop()

    menu = st.sidebar.selectbox("Choose action", [
        "View foods",
        "Add food",
        "Update food",
        "Delete food",
        "Calculate intake",
    ])

    if menu == "View foods":
        st.header("All foods and protein content")
        df = get_all_foods(conn)
        st.dataframe(df)

    elif menu == "Add food":
        st.header("Add a new food")
        food = st.text_input("Food name")
        protein = st.number_input("Protein (per 100g or per unit for egg)", min_value=0.0, format="%.2f")
        if st.button("Add"):
            if food:
                add_food(conn, food, protein)
                st.success("Food added")
            else:
                st.error("Enter a food name")

    elif menu == "Update food":
        st.header("Update protein value")
        df = get_all_foods(conn)
        foods = df['Food'].tolist()
        if foods:
            sel = st.selectbox("Select food", foods)
            new_val = st.number_input("New protein value (per 100g or per unit)", min_value=0.0, format="%.2f")
            if st.button("Update"):
                update_food(conn, sel, new_val)
                st.success("Updated successfully")
        else:
            st.info("No foods in database")

    elif menu == "Delete food":
        st.header("Delete a food")
        df = get_all_foods(conn)
        foods = df['Food'].tolist()
        if foods:
            sel = st.selectbox("Select food to delete", foods)
            if st.button("Delete"):
                delete_food(conn, sel)
                st.success("Deleted")
        else:
            st.info("No foods in database")

    elif menu == "Calculate intake":
        st.header("Calculate daily protein intake")
        st.write("Enter lines in the format: food,quantity")
        st.write("For eggs enter number of eggs as the quantity (egg,2)")
        text = st.text_area("Meals (one per line)")
        if st.button("Calculate"):
            lines = text.splitlines()
            total, details = calculate_total_protein(conn, lines)
            st.write(f"Total protein: {total:.2f} g")
            st.write("Details:")
            for d in details:
                st.write(f"{d[0]} -> {d[1]}")


if __name__ == '__main__':
    main()
