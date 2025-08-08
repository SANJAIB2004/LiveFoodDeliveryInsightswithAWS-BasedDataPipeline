import streamlit as st
import pandas as pd
import requests
import random
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Food Service Data Pipeline",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2E8B57;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #F0F8FF;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #FF6B35;
    }
    .sidebar .sidebar-content {
        background-color: #FFF8DC;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_customers():
    try:
        response = requests.get('https://randomuser.me/api/?results=100')
        return response.json()['results']
    except:
        return generate_mock_customers(100)


@st.cache_data(ttl=300)
def generate_mock_customers(num_customers):
    """Generate mock customer data if API fails"""
    mock_customers = []
    first_names = ['Rahul', 'Priya', 'Amit', 'Sneha', 'Vikram', 'Anita', 'Ravi', 'Kavya', 'Suresh', 'Meera']
    last_names = ['Sharma', 'Patel', 'Singh', 'Kumar', 'Reddy', 'Gupta', 'Jain', 'Shah', 'Verma', 'Rao']
    cities = ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad']

    for i in range(num_customers):
        mock_customers.append({
            'login': {'uuid': f'mock-{i}-{random.randint(1000, 9999)}'},
            'name': {'first': random.choice(first_names), 'last': random.choice(last_names)},
            'email': f'user{i}@example.com',
            'dob': {'age': random.randint(18, 80)},
            'gender': random.choice(['male', 'female']),
            'phone': f'+1-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}',
            'location': {'city': random.choice(cities), 'country': 'India'}
        })
    return mock_customers


@st.cache_data
def generate_food_menu_data(num_records):
    menu_items = [
        'Pizza Margherita', 'Chicken Burger', 'Caesar Salad', 'Spaghetti Carbonara',
        'Fish Tacos', 'Beef Steak', 'Vegetable Curry', 'Chocolate Cake', 'Grilled Salmon',
        'Mushroom Risotto', 'BBQ Ribs', 'Greek Salad', 'Pad Thai', 'Chicken Wings',
        'Lasagna', 'Fish & Chips', 'Taco Bowl', 'Cheesecake', 'Fried Rice', 'Pasta Primavera'
    ]
    categories = ['Main Course', 'Appetizer', 'Dessert', 'Salad', 'Beverage', 'Side Dish']
    cuisines = ['Italian', 'American', 'Mexican', 'Asian', 'Mediterranean', 'Indian']

    data = []
    for _ in range(num_records):
        item_name = random.choice(menu_items)
        data.append({
            'item_id': random.randint(1000, 9999),
            'item_name': item_name,
            'category': random.choice(categories),
            'cuisine_type': random.choice(cuisines),
            'price': round(random.uniform(8.99, 35.99), 2),
            'preparation_time': random.randint(10, 45),
            'calories': random.randint(200, 1200),
            'is_vegetarian': random.choice([True, False]),
            'is_gluten_free': random.choice([True, False]),
            'popularity_score': round(random.uniform(1, 10), 1),
            'date_added': (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
        })
    return pd.DataFrame(data)


@st.cache_data
def generate_ingredient_data(num_records):
    ingredients = [
        'Tomatoes', 'Cheese', 'Chicken Breast', 'Lettuce', 'Onions', 'Bell Peppers',
        'Mushrooms', 'Garlic', 'Pasta', 'Rice', 'Beef', 'Salmon', 'Shrimp', 'Potatoes',
        'Carrots', 'Broccoli', 'Spinach', 'Eggs', 'Milk', 'Flour', 'Olive Oil', 'Butter'
    ]
    suppliers = ['Fresh Foods Co.', 'Garden Supply', 'Organic Farms', 'Local Market', 'Premium Ingredients Ltd.']
    units = ['kg', 'lbs', 'pieces', 'liters', 'dozen']

    data = []
    for _ in range(num_records):
        data.append({
            'ingredient_id': random.randint(1000, 9999),
            'ingredient_name': random.choice(ingredients),
            'supplier': random.choice(suppliers),
            'cost_per_unit': round(random.uniform(0.50, 25.00), 2),
            'unit': random.choice(units),
            'expiry_date': (datetime.now() + timedelta(days=random.randint(1, 60))).strftime('%Y-%m-%d'),
            'stock_quantity': random.randint(10, 500),
            'minimum_stock': random.randint(5, 50),
            'is_organic': random.choice([True, False]),
            'storage_temperature': random.choice(['Room Temperature', 'Refrigerated', 'Frozen'])
        })
    return pd.DataFrame(data)


@st.cache_data(ttl=300)
def fetch_restaurants():
    try:
        response = requests.get('https://jsonplaceholder.typicode.com/users')
        return response.json()
    except:
        return generate_mock_restaurants(20)


@st.cache_data
def generate_mock_restaurants(num_restaurants):
    restaurant_names = ['Bella Vista', 'Golden Spoon', 'Urban Bistro', 'Coastal Kitchen', 'Mountain View']
    return [{'id': i, 'name': f'{random.choice(restaurant_names)} #{i}',
             'address': {'city': f'City{i}'}, 'phone': f'555-{i:04d}', 'website': f'restaurant{i}.com'}
            for i in range(1, num_restaurants + 1)]


def transform_customers(data):
    customers = []
    cuisines = ['North Indian', 'South Indian', 'Gujarati', 'Punjabi', 'Bengali', 'Maharashtrian', 'Rajasthani']
    dietary_prefs = ['None', 'Vegetarian', 'Vegan', 'Jain Food', 'No Onion-Garlic', 'Gluten-Free']

    for customer in data:
        customers.append({
            'customer_id': customer['login']['uuid'],
            'name': f"{customer['name']['first']} {customer['name']['last']}",
            'email': customer['email'],
            'age': customer['dob']['age'],
            'gender': customer['gender'],
            'phone': customer['phone'],
            'city': customer['location']['city'],
            'country': customer['location']['country'],
            'preferred_cuisine': random.choice(cuisines),
            'dietary_preference': random.choice(dietary_prefs),
            'loyalty_tier': random.choice(['Bronze', 'Silver', 'Gold', 'Platinum']),
            'total_orders': random.randint(1, 50),
            'registration_date': (datetime.now() - timedelta(days=random.randint(30, 1000))).strftime('%Y-%m-%d')
        })
    return pd.DataFrame(customers)


def transform_restaurants(data):
    cuisine_types = ['North Indian', 'South Indian', 'Gujarati', 'Punjabi', 'Bengali', 'Maharashtrian', 'Rajasthani']
    restaurants = []
    for restaurant in data:
        restaurants.append({
            'restaurant_id': restaurant['id'],
            'name': f"{restaurant['name']}'s Restaurant",
            'cuisine_type': random.choice(cuisine_types),
            'rating': round(random.uniform(3.0, 5.0), 1),
            'city': restaurant['address']['city'] if 'address' in restaurant else f"City{restaurant['id']}",
            'phone': restaurant['phone'],
            'website': restaurant['website'] if 'website' in restaurant else f"restaurant{restaurant['id']}.com",
            'delivery_available': random.choice([True, False]),
            'avg_delivery_time': random.randint(20, 60),
            'seating_capacity': random.randint(50, 200),
            'established_year': random.randint(2010, 2023)
        })
    return pd.DataFrame(restaurants)


def generate_orders_data(customers_df, menu_df):
    orders = []
    for _ in range(len(customers_df) * 2):  # Generate multiple orders per customer
        customer = customers_df.sample(1).iloc[0]
        item = menu_df.sample(1).iloc[0]
        quantity = random.randint(1, 5)
        order_date = datetime.now() - timedelta(days=random.randint(0, 90))

        orders.append({
            'order_id': random.randint(10000, 99999),
            'customer_id': customer['customer_id'],
            'customer_name': customer['name'],
            'item_id': item['item_id'],
            'item_name': item['item_name'],
            'category': item['category'],
            'cuisine_type': item['cuisine_type'],
            'price': item['price'],
            'quantity': quantity,
            'total_price': round(item['price'] * quantity, 2),
            'order_date': order_date.strftime('%Y-%m-%d'),
            'order_time': order_date.strftime('%H:%M'),
            'delivery_method': random.choice(['Dine-in', 'Takeout', 'Delivery']),
            'payment_method': random.choice(['Credit Card', 'Cash', 'Digital Wallet']),
            'order_status': random.choice(['Completed', 'In Progress', 'Cancelled'])
        })
    return pd.DataFrame(orders)


def load_data():
    """Load all data with caching"""
    if 'data_loaded' not in st.session_state:
        with st.spinner('Loading data...'):
            # Fetch raw data
            customers_data = fetch_customers()
            restaurants_data = fetch_restaurants()

            # Generate processed data
            menu_df = generate_food_menu_data(150)
            ingredient_df = generate_ingredient_data(200)
            customers_df = transform_customers(customers_data)
            restaurants_df = transform_restaurants(restaurants_data)
            orders_df = generate_orders_data(customers_df, menu_df)

            # Store in session state
            st.session_state.menu_df = menu_df
            st.session_state.ingredient_df = ingredient_df
            st.session_state.customers_df = customers_df
            st.session_state.restaurants_df = restaurants_df
            st.session_state.orders_df = orders_df
            st.session_state.data_loaded = True


def home_page():
    st.markdown('<h1 class="main-header">🍽️ Food Service Data Pipeline Dashboard</h1>', unsafe_allow_html=True)

    st.markdown("""
    ### Welcome to the Real-Time Food Service Analytics Platform

    This comprehensive dashboard provides insights into your food service operations with real-time data processing and visualization capabilities.

    **Key Features:**
    - 📊 **Real-time Data Processing**: Live updates from multiple data sources
    - 🔍 **Data Screening**: Advanced filtering and data quality checks
    - 📈 **Advanced Visualizations**: Interactive charts and analytics
    - 🍕 **Menu Analytics**: Performance tracking for menu items
    - 👥 **Customer Insights**: Behavior analysis and segmentation
    - 📦 **Inventory Management**: Real-time stock monitoring
    """)

    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total Customers",
            value=len(st.session_state.customers_df),
            delta=f"+{random.randint(5, 15)} this week"
        )

    with col2:
        st.metric(
            label="Total Orders",
            value=len(st.session_state.orders_df),
            delta=f"+{random.randint(20, 50)} today"
        )

    with col3:
        total_revenue = st.session_state.orders_df['total_price'].sum()
        st.metric(
            label="Total Revenue",
            value=f"₹{total_revenue:,.2f}",
            delta=f"+₹{random.randint(500, 2000):,} this week"
        )

    with col4:
        avg_order = st.session_state.orders_df['total_price'].mean()
        st.metric(
            label="Avg Order Value",
            value=f"₹{avg_order:.2f}",
            delta=f"+{random.uniform(0.5, 2.0):.2f}%"
        )

    # Quick Overview Charts
    st.markdown("### 📊 Quick Overview")
    col1, col2 = st.columns(2)

    with col1:
        # Orders by category
        category_counts = st.session_state.orders_df['category'].value_counts()
        fig = px.pie(values=category_counts.values, names=category_counts.index,
                     title="Orders by Category")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Daily revenue trend
        daily_revenue = st.session_state.orders_df.groupby('order_date')['total_price'].sum().reset_index()
        fig = px.line(daily_revenue, x='order_date', y='total_price',
                      title="Daily Revenue Trend")
        st.plotly_chart(fig, use_container_width=True)


def data_screening_page():
    st.markdown('<h2 class="sub-header">🔍 Data Screening & Quality Control</h2>', unsafe_allow_html=True)

    # Data selection
    data_type = st.selectbox(
        "Select Data Type to Screen:",
        ["Customer Data", "Menu Items", "Ingredients", "Orders", "Restaurants"]
    )

    if data_type == "Customer Data":
        df = st.session_state.customers_df
        st.markdown("### Customer Database")

    elif data_type == "Menu Items":
        df = st.session_state.menu_df
        st.markdown("### Menu Items Database")

    elif data_type == "Ingredients":
        df = st.session_state.ingredient_df
        st.markdown("### Ingredients Inventory")

    elif data_type == "Orders":
        df = st.session_state.orders_df
        st.markdown("### Orders Database")

    else:  # Restaurants
        df = st.session_state.restaurants_df
        st.markdown("### Restaurant Database")

    # Data overview
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Records", len(df))
    with col2:
        st.metric("Columns", len(df.columns))
    with col3:
        missing_values = df.isnull().sum().sum()
        st.metric("Missing Values", missing_values)
    with col4:
        duplicates = df.duplicated().sum()
        st.metric("Duplicate Records", duplicates)

    # Filtering options
    st.markdown("### 🔧 Data Filters")

    # Dynamic filters based on data type
    if data_type == "Customer Data":
        col1, col2, col3 = st.columns(3)
        with col1:
            age_range = st.slider("Age Range", int(df['age'].min()), int(df['age'].max()),
                                  (int(df['age'].min()), int(df['age'].max())))
        with col2:
            selected_cities = st.multiselect("Cities", df['city'].unique())
        with col3:
            loyalty_tiers = st.multiselect("Loyalty Tiers", df['loyalty_tier'].unique())

        # Apply filters
        filtered_df = df[df['age'].between(age_range[0], age_range[1])]
        if selected_cities:
            filtered_df = filtered_df[filtered_df['city'].isin(selected_cities)]
        if loyalty_tiers:
            filtered_df = filtered_df[filtered_df['loyalty_tier'].isin(loyalty_tiers)]

    elif data_type == "Menu Items":
        col1, col2, col3 = st.columns(3)
        with col1:
            price_range = st.slider("Price Range (₹)", float(df['price'].min()), float(df['price'].max()),
                                    (float(df['price'].min()), float(df['price'].max())))
        with col2:
            categories = st.multiselect("Categories", df['category'].unique())
        with col3:
            cuisines = st.multiselect("Cuisine Types", df['cuisine_type'].unique())

        # Apply filters
        filtered_df = df[df['price'].between(price_range[0], price_range[1])]
        if categories:
            filtered_df = filtered_df[filtered_df['category'].isin(categories)]
        if cuisines:
            filtered_df = filtered_df[filtered_df['cuisine_type'].isin(cuisines)]

    elif data_type == "Ingredients":
        col1, col2 = st.columns(2)
        with col1:
            suppliers = st.multiselect("Suppliers", df['supplier'].unique())
        with col2:
            storage_temp = st.multiselect("Storage Temperature", df['storage_temperature'].unique())

        # Apply filters
        filtered_df = df.copy()
        if suppliers:
            filtered_df = filtered_df[filtered_df['supplier'].isin(suppliers)]
        if storage_temp:
            filtered_df = filtered_df[filtered_df['storage_temperature'].isin(storage_temp)]

    elif data_type == "Orders":
        col1, col2, col3 = st.columns(3)
        with col1:
            date_range = st.date_input("Order Date Range",
                                       value=[datetime.now() - timedelta(days=30), datetime.now()])
        with col2:
            order_status = st.multiselect("Order Status", df['order_status'].unique())
        with col3:
            delivery_method = st.multiselect("Delivery Method", df['delivery_method'].unique())

        # Apply filters
        filtered_df = df.copy()
        if len(date_range) == 2:
            filtered_df = filtered_df[
                (pd.to_datetime(filtered_df['order_date']) >= pd.to_datetime(date_range[0])) &
                (pd.to_datetime(filtered_df['order_date']) <= pd.to_datetime(date_range[1]))
                ]
        if order_status:
            filtered_df = filtered_df[filtered_df['order_status'].isin(order_status)]
        if delivery_method:
            filtered_df = filtered_df[filtered_df['delivery_method'].isin(delivery_method)]

    else:  # Restaurants
        col1, col2 = st.columns(2)
        with col1:
            rating_range = st.slider("Rating Range", float(df['rating'].min()), float(df['rating'].max()),
                                     (float(df['rating'].min()), float(df['rating'].max())))
        with col2:
            cuisine_types = st.multiselect("Cuisine Types", df['cuisine_type'].unique())

        # Apply filters
        filtered_df = df[df['rating'].between(rating_range[0], rating_range[1])]
        if cuisine_types:
            filtered_df = filtered_df[filtered_df['cuisine_type'].isin(cuisine_types)]

    # Display filtered data
    st.markdown(f"### Filtered Data ({len(filtered_df)} records)")
    st.dataframe(filtered_df, use_container_width=True, height=400)

    # Data quality insights
    st.markdown("### 📋 Data Quality Report")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Data Completeness**")
        completeness = (1 - filtered_df.isnull().sum() / len(filtered_df)) * 100
        completeness_df = pd.DataFrame({
            'Column': completeness.index,
            'Completeness %': completeness.values
        })
        fig = px.bar(completeness_df, x='Column', y='Completeness %',
                     title="Data Completeness by Column")
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**Statistical Summary**")
        numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            st.dataframe(filtered_df[numeric_cols].describe(), use_container_width=True)
        else:
            st.info("No numeric columns available for statistical summary.")

    # Export options
    st.markdown("### 💾 Export Data")
    col1, col2, col3 = st.columns(3)

    with col1:
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name=f"{data_type.lower().replace(' ', '_')}_filtered.csv",
            mime="text/csv"
        )

    with col2:
        json_data = filtered_df.to_json(orient='records', indent=2)
        st.download_button(
            label="Download as JSON",
            data=json_data,
            file_name=f"{data_type.lower().replace(' ', '_')}_filtered.json",
            mime="application/json"
        )


def visualization_page():
    st.markdown('<h2 class="sub-header">📈 Advanced Analytics & Visualizations</h2>', unsafe_allow_html=True)

    # Visualization selection
    viz_type = st.selectbox(
        "Select Visualization Type:",
        ["Sales Analytics", "Customer Analytics", "Menu Performance", "Inventory Analytics", "Operational Metrics"]
    )

    if viz_type == "Sales Analytics":
        st.markdown("### 💰 Sales Performance Dashboard")

        # Sales metrics
        orders_df = st.session_state.orders_df
        total_sales = orders_df['total_price'].sum()
        avg_order = orders_df['total_price'].mean()
        total_orders = len(orders_df)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Sales", f"₹{total_sales:,.2f}")
        with col2:
            st.metric("Average Order Value", f"₹{avg_order:.2f}")
        with col3:
            st.metric("Total Orders", f"{total_orders:,}")

        # Sales visualizations
        col1, col2 = st.columns(2)

        with col1:
            # Daily sales trend
            daily_sales = orders_df.groupby('order_date')['total_price'].sum().reset_index()
            fig = px.line(daily_sales, x='order_date', y='total_price',
                          title="Daily Sales Trend", markers=True)
            fig.update_layout(xaxis_title="Date", yaxis_title="Sales (₹)")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Sales by delivery method
            delivery_sales = orders_df.groupby('delivery_method')['total_price'].sum().reset_index()
            fig = px.bar(delivery_sales, x='delivery_method', y='total_price',
                         title="Sales by Delivery Method", color='delivery_method')
            st.plotly_chart(fig, use_container_width=True)

        # Sales heatmap by day and hour
        orders_df['hour'] = pd.to_datetime(orders_df['order_time']).dt.hour
        orders_df['day_of_week'] = pd.to_datetime(orders_df['order_date']).dt.day_name()

        heatmap_data = orders_df.groupby(['day_of_week', 'hour'])['total_price'].sum().reset_index()
        heatmap_pivot = heatmap_data.pivot(index='day_of_week', columns='hour', values='total_price').fillna(0)

        fig = px.imshow(heatmap_pivot, title="Sales Heatmap (Day vs Hour)",
                        labels=dict(x="Hour of Day", y="Day of Week", color="Sales (₹)"))
        st.plotly_chart(fig, use_container_width=True)

    elif viz_type == "Customer Analytics":
        st.markdown("### 👥 Customer Insights Dashboard")

        customers_df = st.session_state.customers_df
        orders_df = st.session_state.orders_df

        # Customer metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Customers", len(customers_df))
        with col2:
            avg_age = customers_df['age'].mean()
            st.metric("Average Age", f"{avg_age:.1f}")
        with col3:
            avg_orders = customers_df['total_orders'].mean()
            st.metric("Avg Orders per Customer", f"{avg_orders:.1f}")
        with col4:
            loyalty_gold = len(customers_df[customers_df['loyalty_tier'].isin(['Gold', 'Platinum'])])
            st.metric("Premium Customers", loyalty_gold)

        col1, col2 = st.columns(2)

        with col1:
            # Age distribution
            fig = px.histogram(customers_df, x='age', bins=20, title="Customer Age Distribution")
            fig.update_layout(xaxis_title="Age", yaxis_title="Number of Customers")
            st.plotly_chart(fig, use_container_width=True)

            # Loyalty tier distribution
            loyalty_counts = customers_df['loyalty_tier'].value_counts()
            fig = px.pie(values=loyalty_counts.values, names=loyalty_counts.index,
                         title="Customer Loyalty Distribution")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Preferred cuisine
            cuisine_pref = customers_df['preferred_cuisine'].value_counts()
            fig = px.bar(x=cuisine_pref.values, y=cuisine_pref.index, orientation='h',
                         title="Customer Cuisine Preferences")
            fig.update_layout(xaxis_title="Number of Customers", yaxis_title="Cuisine Type")
            st.plotly_chart(fig, use_container_width=True)

            # Gender distribution
            gender_counts = customers_df['gender'].value_counts()
            fig = px.pie(values=gender_counts.values, names=gender_counts.index,
                         title="Customer Gender Distribution")
            st.plotly_chart(fig, use_container_width=True)

    elif viz_type == "Menu Performance":
        st.markdown("### 🍕 Menu Item Performance Analysis")

        menu_df = st.session_state.menu_df
        orders_df = st.session_state.orders_df

        # Menu performance metrics
        menu_performance = orders_df.groupby(['item_id', 'item_name']).agg({
            'quantity': 'sum',
            'total_price': 'sum',
            'order_id': 'count'
        }).rename(columns={'order_id': 'order_count'}).reset_index()

        # Merge with menu data
        menu_performance = menu_performance.merge(menu_df[['item_id', 'category', 'price', 'popularity_score']],
                                                  on='item_id', how='left')

        col1, col2 = st.columns(2)

        with col1:
            # Top selling items
            top_items = menu_performance.nlargest(10, 'quantity')
            fig = px.bar(top_items, x='quantity', y='item_name', orientation='h',
                         title="Top 10 Best Selling Items")
            fig.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Revenue by category
            category_revenue = orders_df.groupby('category')['total_price'].sum().reset_index()
            fig = px.pie(category_revenue, values='total_price', names='category',
                         title="Revenue by Menu Category")
            st.plotly_chart(fig, use_container_width=True)

        # Price vs Popularity scatter
        fig = px.scatter(menu_df, x='price', y='popularity_score', color='category',
                         size='calories', hover_data=['item_name'],
                         title="Menu Items: Price vs Popularity")
        fig.update_layout(xaxis_title="Price (₹)", yaxis_title="Popularity Score")
        st.plotly_chart(fig, use_container_width=True)

    elif viz_type == "Inventory Analytics":
        st.markdown("### 📦 Inventory Management Dashboard")

        ingredient_df = st.session_state.ingredient_df

        # Inventory alerts
        low_stock = ingredient_df[ingredient_df['stock_quantity'] <= ingredient_df['minimum_stock']]
        expiring_soon = ingredient_df[
            pd.to_datetime(ingredient_df['expiry_date']) <= pd.to_datetime(datetime.now() + timedelta(days=7))
            ]

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Ingredients", len(ingredient_df))
        with col2:
            st.metric("Low Stock Items", len(low_stock), delta=-len(low_stock))
        with col3:
            st.metric("Expiring Soon", len(expiring_soon), delta=-len(expiring_soon))
        with col4:
            total_value = (ingredient_df['cost_per_unit'] * ingredient_df['stock_quantity']).sum()
            st.metric("Total Inventory Value", f"₹{total_value:,.2f}")

        # Stock level alerts
        if len(low_stock) > 0:
            st.warning(f"⚠️ {len(low_stock)} items are running low on stock!")
            st.dataframe(low_stock[['ingredient_name', 'stock_quantity', 'minimum_stock', 'supplier']])

        if len(expiring_soon) > 0:
            st.error(f"🚨 {len(expiring_soon)} items are expiring within 7 days!")
            st.dataframe(expiring_soon[['ingredient_name', 'expiry_date', 'stock_quantity', 'supplier']])

        col1, col2 = st.columns(2)

        with col1:
            # Stock levels by supplier
            supplier_stock = ingredient_df.groupby('supplier').agg({
                'stock_quantity': 'sum',
                'cost_per_unit': 'mean'
            }).reset_index()
            fig = px.bar(supplier_stock, x='supplier', y='stock_quantity',
                         title="Total Stock Quantity by Supplier")
            fig.update_xaxis(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Inventory value by storage temperature
            temp_value = ingredient_df.groupby('storage_temperature').apply(
                lambda x: (x['cost_per_unit'] * x['stock_quantity']).sum()
            ).reset_index(name='total_value')
            fig = px.pie(temp_value, values='total_value', names='storage_temperature',
                         title="Inventory Value by Storage Type")
            st.plotly_chart(fig, use_container_width=True)

        # Stock quantity distribution
        fig = px.histogram(ingredient_df, x='stock_quantity', bins=20,
                           title="Stock Quantity Distribution")
        fig.update_layout(xaxis_title="Stock Quantity", yaxis_title="Number of Ingredients")
        st.plotly_chart(fig, use_container_width=True)

    else:  # Operational Metrics
        st.markdown("### ⚙️ Operational Performance Dashboard")

        orders_df = st.session_state.orders_df
        restaurants_df = st.session_state.restaurants_df

        # Operational metrics
        completed_orders = len(orders_df[orders_df['order_status'] == 'Completed'])
        completion_rate = (completed_orders / len(orders_df)) * 100
        avg_delivery_time = restaurants_df['avg_delivery_time'].mean()

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Order Completion Rate", f"{completion_rate:.1f}%")
        with col2:
            st.metric("Avg Delivery Time", f"{avg_delivery_time:.0f} min")
        with col3:
            restaurants_with_delivery = len(restaurants_df[restaurants_df['delivery_available'] == True])
            st.metric("Restaurants with Delivery", restaurants_with_delivery)
        with col4:
            avg_rating = restaurants_df['rating'].mean()
            st.metric("Average Restaurant Rating", f"{avg_rating:.2f}")

        col1, col2 = st.columns(2)

        with col1:
            # Order status distribution
            status_counts = orders_df['order_status'].value_counts()
            fig = px.pie(values=status_counts.values, names=status_counts.index,
                         title="Order Status Distribution")
            st.plotly_chart(fig, use_container_width=True)

            # Payment method preferences
            payment_counts = orders_df['payment_method'].value_counts()
            fig = px.bar(x=payment_counts.values, y=payment_counts.index, orientation='h',
                         title="Payment Method Usage")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Restaurant ratings distribution
            fig = px.histogram(restaurants_df, x='rating', bins=10,
                               title="Restaurant Rating Distribution")
            fig.update_layout(xaxis_title="Rating", yaxis_title="Number of Restaurants")
            st.plotly_chart(fig, use_container_width=True)

            # Seating capacity vs rating
            fig = px.scatter(restaurants_df, x='seating_capacity', y='rating',
                             color='cuisine_type', title="Seating Capacity vs Rating")
            st.plotly_chart(fig, use_container_width=True)

        # Hourly order distribution
        if 'hour' not in orders_df.columns:
            orders_df['hour'] = pd.to_datetime(orders_df['order_time']).dt.hour

        hourly_orders = orders_df['hour'].value_counts().sort_index()
        fig = px.bar(x=hourly_orders.index, y=hourly_orders.values,
                     title="Orders by Hour of Day")
        fig.update_layout(xaxis_title="Hour", yaxis_title="Number of Orders")
        st.plotly_chart(fig, use_container_width=True)


def main():
    # Initialize session state
    load_data()

    # Sidebar navigation
    st.sidebar.title("🍽️ Navigation")

    # Data refresh button
    if st.sidebar.button("🔄 Refresh All Data", type="primary"):
        # Clear cached data
        st.cache_data.clear()
        if 'data_loaded' in st.session_state:
            del st.session_state.data_loaded
        st.experimental_rerun()

    # Page selection
    page = st.sidebar.radio(
        "Select Page:",
        ["🏠 Home Dashboard", "🔍 Data Screening", "📊 Advanced Analytics"],
        index=0
    )

    # Data status in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📋 Data Status")
    if 'data_loaded' in st.session_state:
        st.sidebar.success("✅ Data Loaded Successfully")
        st.sidebar.info(f"📊 {len(st.session_state.customers_df)} Customers")
        st.sidebar.info(f"🍕 {len(st.session_state.menu_df)} Menu Items")
        st.sidebar.info(f"📦 {len(st.session_state.ingredient_df)} Ingredients")
        st.sidebar.info(f"🛍️ {len(st.session_state.orders_df)} Orders")
        st.sidebar.info(f"🏪 {len(st.session_state.restaurants_df)} Restaurants")

        # Last updated time
        st.sidebar.markdown(f"**Last Updated:** {datetime.now().strftime('%H:%M:%S')}")
    else:
        st.sidebar.warning("⏳ Loading Data...")

    # Quick actions
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚡ Quick Actions")
    if st.sidebar.button("📈 View Sales Summary"):
        st.sidebar.success(f"💰 Today's Revenue: ₹{st.session_state.orders_df['total_price'].sum():.2f}")

    if st.sidebar.button("⚠️ Check Inventory Alerts"):
        ingredient_df = st.session_state.ingredient_df
        low_stock = len(ingredient_df[ingredient_df['stock_quantity'] <= ingredient_df['minimum_stock']])
        if low_stock > 0:
            st.sidebar.error(f"🚨 {low_stock} items low on stock!")
        else:
            st.sidebar.success("✅ All items in stock")

    # Footer info
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ System Info")
    st.sidebar.markdown("**Version:** 2.1.0")
    st.sidebar.markdown("**Environment:** Production")
    st.sidebar.markdown("**Uptime:** 99.9%")

    # Route to appropriate page
    if page == "🏠 Home Dashboard":
        home_page()
    elif page == "🔍 Data Screening":
        data_screening_page()
    else:  # Advanced Analytics
        visualization_page()

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; padding: 20px;'>
            <p>🍽️ Food Service Data Pipeline Dashboard | Built with Streamlit & Plotly</p>
            <p>Real-time data processing and analytics for restaurant operations</p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()