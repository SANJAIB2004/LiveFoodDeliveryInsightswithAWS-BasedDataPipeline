# 🍽️ Live Food Delivery Data Pipeline Dashboard using the AWS

A comprehensive real-time data analytics platform designed specifically for Indian food service operations, including restaurants, food delivery services, and catering businesses.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0+-red.svg)
![Plotly](https://img.shields.io/badge/Plotly-5.17.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🚀 Features

### 🏠 **Home Dashboard**
- Real-time KPIs and metrics
- Sales overview and revenue tracking
- Quick performance indicators
- Interactive charts for immediate insights

### 🔍 **Data Screening & Quality Control**
- Multi-datasource filtering system
- Data quality reports and completeness metrics
- Export functionality (CSV/JSON)
- Missing data analysis and duplicate detection
- Dynamic filtering for all data types

### 📊 **Advanced Analytics & Visualizations**
- **Sales Analytics**: Revenue trends, delivery method analysis, sales heatmaps
- **Customer Analytics**: Demographics, loyalty distribution, cuisine preferences
- **Menu Performance**: Best sellers, category revenue, price vs popularity analysis
- **Inventory Analytics**: Stock alerts, supplier analysis, expiration tracking
- **Operational Metrics**: Order completion rates, payment methods, restaurant ratings

## 🇮🇳 **Indian Cuisine Focus**

This dashboard is specifically tailored for Indian food operations with:

### **Authentic Menu Items**
- Traditional dishes: Butter Chicken, Biryani, Dal Tadka, Paneer Tikka Masala
- Regional specialties: Dosa, Idli, Vada Pav, Chole Bhature
- Street food: Pani Puri, Bhel Puri, Samosa
- Desserts: Gulab Jamun, Rasgulla, Kulfi
- Beverages: Masala Chai, Lassi

### **Regional Cuisine Categories**
- North Indian, South Indian, Gujarati, Punjabi
- Bengali, Maharashtrian, Rajasthani

### **Indian Ingredients & Spices**
- Traditional spices: Turmeric, Garam Masala, Cumin Seeds
- Fresh herbs: Coriander, Mint, Curry Leaves
- Staples: Basmati Rice, Wheat Flour, various Lentils
- Cooking mediums: Ghee, Coconut Oil, Mustard Oil

### **Indian Dietary Preferences**
- Vegetarian, Vegan, Jain Food
- No Onion-Garlic restrictions
- Gluten-Free options

## 🛠️ **Installation**

### **Prerequisites**
- Python 3.8 or higher
- pip package manager

### **Step 1: Clone the Repository**
```bash
git clone https://github.com/SANJAIB2004/LiveFoodDeliveryInsightswithAWS-BasedDataPipeline.git
cd LiveFoodDeliveryInsightswithAWS-BasedDataPipeline.git
```

### **Step 2: Create Virtual Environment (Recommended)**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 4: Run the Application**
```bash
streamlit run review.py
```

The dashboard will open in your browser at `http://localhost:8501`

## 📦 **Project Structure**

```
indian-food-pipeline-dashboard/
│
├── review.py                 # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation


## 🔧 **Configuration**

API Endpoints
The dashboard uses the following APIs for data generation:
- `https://randomuser.me/api/` - For customer data generation
- `https://jsonplaceholder.typicode.com/users` - For restaurant data

🎯 Use Cases

Restaurant Chains
- Multi-location performance monitoring
- Menu optimization across regions
- Inventory management and cost control
- Customer preference analysis

Food Delivery Services
- Order pattern analysis
- Delivery performance tracking
- Customer retention insights
- Revenue optimization

Catering Businesses
- Event-based analytics
- Ingredient planning and procurement
- Cost analysis and profit margins
- Customer preference tracking

```


### **Adding New Regions**
```python
# In transform_customers() and transform_restaurants() functions
cuisines = ['Your Regional Cuisine', 'North Indian', ...]
```

### **Modifying Metrics**
Edit the respective functions in `main.py` to add custom KPIs and calculations.

## 📋 **Requirements**

### **Essential Dependencies**
```
streamlit>=1.28.0
pandas>=1.5.3
numpy>=1.24.0
requests>=2.31.0
plotly>=5.17.0
```
