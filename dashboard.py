import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick

# Load the DataFrame
all_df = pd.read_csv('all_data.csv')

# Load additional datasets
customer_df = pd.read_csv('customers_dataset.csv')
geolocation_df = pd.read_csv('geolocation_dataset.csv')
order_items_df = pd.read_csv('order_items_dataset.csv')
order_payments_df = pd.read_csv('order_payments_dataset.csv')
order_reviews_df = pd.read_csv('order_reviews_dataset.csv')
orders_df = pd.read_csv('orders_dataset.csv')
product_category_name_df = pd.read_csv('product_category_name_translation.csv')

st.title('E-Commerce Sales Dashboard')
st.markdown("""
    This dashboard provides insights into e-commerce sales data.
    The data is sourced from various datasets including customer, order,
    payment, and product category information.
""")

# Pertanyaan 1: Which product is the most popular and which one is the least purchased?
st.header('Most and Least Sold Products')

product_counts = all_df.groupby('product_category_name_english')['product_id'].count().reset_index()
sorted_df = product_counts.sort_values(by='product_id', ascending=False)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))
colors = ["#FFB6C1", "#FF69B4", "#FF1493", "#DB7093", "#C71585"]

# Most sold products
sns.barplot(x="product_id", y="product_category_name_english", hue="product_category_name_english",
            data=sorted_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Products with the highest sales", loc="center", fontsize=19)
ax[0].tick_params(axis='y', labelsize=15)

# Least sold products
sns.barplot(x="product_id", y="product_category_name_english", hue="product_category_name_english",
            data=sorted_df.sort_values(by="product_id", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Products with the lowest sales", loc="center", fontsize=19)
ax[1].tick_params(axis='y', labelsize=15)

plt.suptitle("Most and Least Sold Products", fontsize=28)
st.pyplot(fig)

# Explanation
st.markdown("""
    The chart above illustrates the sales volume of products in different categories.
    The left bar chart shows the top 5 best-selling products, while the right bar
    chart displays the 5 least sold products. Understanding which products are
    popular helps in inventory management and marketing strategies.
""")

# Conclusion
st.markdown("**Conclusion:** The analysis reveals which products are performing well and which are not, providing insights for future marketing and stock decisions.")

# Pertanyaan 2: How do customers rate their satisfaction with the service?
st.header('Customer Satisfaction')

rating_service = all_df['review_score'].value_counts().sort_values(ascending=False)
max_score = rating_service.idxmax()

colors = ["#FF69B4" if score == max_score else "#FFB6C1" for score in rating_service.index]

plt.figure(figsize=(10, 5))
sns.barplot(x=rating_service.index,
            y=rating_service.values,
            order=rating_service.index,
            palette=colors)

plt.title("Rating customers for service", fontsize=15)
plt.xlabel("Rating")
plt.ylabel("Number of Customers")
plt.xticks(fontsize=12)

st.pyplot(plt)

# Explanation
st.markdown("""
    This chart displays customer satisfaction ratings for the service.
    A higher rating indicates better customer satisfaction, which is
    crucial for maintaining a positive brand image and customer loyalty.
""")

# Conclusion
st.markdown("**Conclusion:** Monitoring customer satisfaction is vital for business success, allowing for adjustments in service delivery and customer engagement.")

# Pertanyaan 3: Which city has the most sellers and buyers?
st.header('Cities with the Most Customers')

city_customer = all_df.customer_city.value_counts().sort_values(ascending=False).rename_axis('City').reset_index(name='Number of Customers')

top_5_cities_customer = city_customer.head(5)

plt.figure(figsize=(10, 6))

colors = ["#FF69B4" if city == top_5_cities_customer['City'].iloc[0] else "#FFB6C1" for city in top_5_cities_customer['City']]

sns.barplot(x="Number of Customers", y="City", data=top_5_cities_customer, palette=colors, legend=False)

plt.xlabel('Number of Customers')
plt.ylabel('City')
plt.title('Top 5 Cities with the Most Customers')

st.pyplot(plt)

# Explanation
st.markdown("""
    This bar chart illustrates the cities with the highest number of customers.
    Identifying key markets can guide targeted marketing campaigns and resource allocation.
""")

# Conclusion
st.markdown("**Conclusion:** Understanding geographical distribution of customers enables effective marketing strategies and tailored customer experiences.")

# Pertanyaan 4: What payment method is used for the largest transaction? What is the total value of that transaction?
st.header('Total Payment Value by Payment Type')

total_payment_type = all_df.groupby('payment_type')['payment_value'].sum().reset_index()
total_payment_type['payment_value_million'] = total_payment_type['payment_value'] / 1e6

plt.figure(figsize=(10, 6))

pink_palette = ["#FFB6C1", "#FF69B4", "#FF1493", "#DB7093", "#C71585"]
sns.barplot(x="payment_type", y="payment_value_million", data=total_payment_type, palette=pink_palette)

plt.xlabel('Payment Type')
plt.ylabel('Total Payment Value (Million)')
plt.title('Total Payment Value by Payment Type')

fmt = '{x:,.0f}M'
tick = mtick.StrMethodFormatter(fmt)
plt.gca().yaxis.set_major_formatter(tick)

st.pyplot(plt)

# Explanation
st.markdown("""
    This chart displays the total transaction value by payment type.
    Understanding payment preferences can help in optimizing payment
    gateways and enhancing customer convenience.
""")

# Conclusion
st.markdown("**Conclusion:** Analyzing payment methods is essential for financial planning and improving user experience in payment processing.")

# End of the dashboard
st.markdown("### Thank you for exploring the E-Commerce Sales Dashboard!")
