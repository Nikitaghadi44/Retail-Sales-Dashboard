import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Retail Sales Dashboard", layout="wide")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("retail_sales_1000_rows.csv")
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df["Month"] = df["Order_Date"].dt.month
    df["Year"] = df["Order_Date"].dt.year

    df["Age_Group"] = pd.cut(
        df["Age"],
        bins=[18, 25, 35, 45, 55, 65],
        labels=["18-25", "26-35", "36-45", "46-55", "56-65"]
    )
    return df

df = load_data()

# ---------------- TITLE ----------------
st.title("🛒 Retail Sales & Customer Insights Dashboard")

# ---------------- KPIs ----------------
total_revenue = df["Revenue"].sum()
total_orders = df["Order_ID"].nunique()
avg_order_value = total_revenue / total_orders

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Revenue", f"₹{total_revenue:,.0f}")
col2.metric("🧾 Total Orders", total_orders)
col3.metric("📦 Avg Order Value", f"₹{avg_order_value:,.0f}")

st.divider()

# ---------------- FILTERS ----------------
st.sidebar.header("🔍 Filter")

region_filter = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

category_filter = st.sidebar.multiselect(
    "Select Product Category",
    options=df["Product_Category"].unique(),
    default=df["Product_Category"].unique()
)

filtered_df = df[
    (df["Region"].isin(region_filter)) &
    (df["Product_Category"].isin(category_filter))
]

# ---------------- REVENUE BY CATEGORY ----------------
st.subheader("📊 Revenue by Product Category")

category_revenue = filtered_df.groupby("Product_Category")["Revenue"].sum()

fig1, ax1 = plt.subplots()
category_revenue.plot(kind="bar", ax=ax1)
ax1.set_xlabel("Category")
ax1.set_ylabel("Revenue")
st.pyplot(fig1)

# ---------------- MONTHLY TREND ----------------
st.subheader("📈 Monthly Revenue Trend")

monthly_revenue = filtered_df.groupby("Month")["Revenue"].sum()

fig2, ax2 = plt.subplots()
monthly_revenue.plot(kind="line", marker="o", ax=ax2)
ax2.set_xlabel("Month")
ax2.set_ylabel("Revenue")
st.pyplot(fig2)

# ---------------- CUSTOMER DEMOGRAPHICS ----------------
st.subheader("👥 Customer Demographics")

col4, col5 = st.columns(2)

with col4:
    gender_dist = filtered_df["Gender"].value_counts()
    fig3, ax3 = plt.subplots()
    gender_dist.plot(kind="pie", autopct="%1.1f%%", ax=ax3)
    ax3.set_ylabel("")
    st.pyplot(fig3)

with col5:
    age_dist = filtered_df["Age_Group"].value_counts().sort_index()
    fig4, ax4 = plt.subplots()
    age_dist.plot(kind="bar", ax=ax4)
    ax4.set_xlabel("Age Group")
    ax4.set_ylabel("Number of Customers")
    st.pyplot(fig4)

st.success("✅ Dashboard loaded successfully")
