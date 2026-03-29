import streamlit as st
import random
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Cafe Management System",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .calculator-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .total-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'calc_display' not in st.session_state:
    st.session_state.calc_display = ""
if 'bill_generated' not in st.session_state:
    st.session_state.bill_generated = False
if 'current_bill' not in st.session_state:
    st.session_state.current_bill = None

# Define items and prices
items = {
    "Fries Meal": 25,
    "Lunch Meal": 40,
    "Burger Meal": 35,
    "Pizza Meal": 50,
    "Cheese Burger": 30,
    "Drinks": 35,
    "Sandwich": 30,
    "Pasta": 45,
    "Ice Cream": 25
}

# Initialize quantities in session state
if 'quantities' not in st.session_state:
    st.session_state.quantities = {item: 0 for item in items}

# Calculator function
def calculator_click(value):
    if value == 'C':
        st.session_state.calc_display = ""
    elif value == '⌫':
        st.session_state.calc_display = st.session_state.calc_display[:-1]
    elif value == '=':
        try:
            expression = st.session_state.calc_display.replace('%', '/100')
            result = eval(expression)
            st.session_state.calc_display = str(round(result, 10))
        except:
            st.session_state.calc_display = "Error"
    else:
        st.session_state.calc_display += value
    st.rerun()

# Header Section
st.markdown('<div class="main-header">', unsafe_allow_html=True)
st.title("☕ Cafe Management System")
st.markdown("### By Rashmi Kumari")
st.markdown('</div>', unsafe_allow_html=True)

# Main content area
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("## 📝 Order Management")
    tab1, tab2 = st.tabs(["Menu Items", "Price List"])
    
    with tab1:
        st.markdown("### Select Your Items")
        # Organize items in columns
        col_item1, col_item2, col_item3 = st.columns(3)
        item_list = list(items.items())
        
        for i, (item, price) in enumerate(item_list):
            col = [col_item1, col_item2, col_item3][i % 3]
            with col:
                st.markdown(f"**{item}**")
                qty = st.number_input(
                    "Quantity",
                    min_value=0,
                    value=st.session_state.quantities[item],
                    key=f"qty_{item}",
                    step=1,
                    label_visibility="collapsed"
                )
                st.session_state.quantities[item] = qty
                st.markdown(f"*₹{price} each*")
        
        st.markdown("---")
        
        # Buttons
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        
        with col_btn1:
            if st.button("💰 Generate Bill", use_container_width=True, type="primary"):
                selected_items = {item: qty for item, qty in st.session_state.quantities.items() if qty > 0}
                if selected_items:
                    # Calculate bill
                    subtotal = sum(items[item] * qty for item, qty in selected_items.items())
                    tax = subtotal * 0.33
                    service_charge = subtotal / 99
                    total = subtotal + tax + service_charge
                    order_number = random.randint(12980, 50876)
                    
                    # Store bill
                    st.session_state.current_bill = {
                        'order_number': order_number,
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'time': datetime.now().strftime('%I:%M:%S %p'),
                        'items': selected_items,
                        'subtotal': subtotal,
                        'tax': tax,
                        'service_charge': service_charge,
                        'total': total
                    }
                    st.session_state.bill_generated = True
                    st.success(f"✅ Bill Generated Successfully!")
                    st.balloons()
                else:
                    st.warning("⚠️ Please select at least one item!")
        
        with col_btn2:
            if st.button("🗑️ Reset All", use_container_width=True):
                # Reset all quantities to 0
                for item in st.session_state.quantities:
                    st.session_state.quantities[item] = 0
                st.session_state.bill_generated = False
                st.session_state.current_bill = None
                st.success("✅ All items reset successfully!")
                st.rerun()
        
        with col_btn3:
            if st.button("❌ Exit", use_container_width=True):
                st.warning("Thank you for using Cafe Management System!")
                st.stop()
        
        # Display bill only when Generate Bill is clicked
        if st.session_state.bill_generated and st.session_state.current_bill:
            bill = st.session_state.current_bill
            st.markdown('<div class="total-box">', unsafe_allow_html=True)
            st.markdown("## 🧾 Bill Summary")
            
            col_bill1, col_bill2 = st.columns(2)
            with col_bill1:
                st.markdown(f"**Order Number:** #{bill['order_number']}")
                st.markdown(f"**Date:** {bill['date']}")
                st.markdown(f"**Time:** {bill['time']}")
                st.markdown("---")
                st.markdown("### Order Details:")
                for item, qty in bill['items'].items():
                    st.markdown(f"• {item}: {qty} x ₹{items[item]} = ₹{items[item]*qty}")
            
            with col_bill2:
                st.markdown("### Cost Breakdown:")
                st.markdown(f"**Subtotal:** ₹{bill['subtotal']:.2f}")
                st.markdown(f"**Tax (33%):** ₹{bill['tax']:.2f}")
                st.markdown(f"**Service Charge:** ₹{bill['service_charge']:.2f}")
                st.markdown("---")
                st.markdown(f"### **Total Amount:** ₹{bill['total']:.2f}")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Add a button to generate new bill
            if st.button("🔄 New Bill", use_container_width=True):
                st.session_state.bill_generated = False
                st.session_state.current_bill = None
                st.rerun()
    
    with tab2:
        st.markdown("## 📋 Menu Price List")
        price_data = {
            "Item": list(items.keys()),
            "Price (₹)": list(items.values())
        }
        st.table(price_data)

with col_right:
    st.markdown("## 🧮 Calculator")
    st.markdown('<div class="calculator-box">', unsafe_allow_html=True)
    
    # Calculator display
    display_value = st.session_state.calc_display if st.session_state.calc_display else "0"
    st.markdown(f"### {display_value}")
    
    # Calculator buttons layout
    calc_buttons = [
        ['C', '⌫', '%', '/'],
        ['7', '8', '9', '*'],
        ['4', '5', '6', '-'],
        ['1', '2', '3', '+'],
        ['0', '00', '.', '=']
    ]
    
    # Create calculator buttons
    for row in calc_buttons:
        cols = st.columns(len(row))
        for idx, btn in enumerate(row):
            with cols[idx]:
                if st.button(btn, key=f"calc_{btn}_{idx}", use_container_width=True):
                    calculator_click(btn)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Tip calculator
    st.markdown("### 💰 Tip Calculator")
    col_t1, col_t2, col_t3 = st.columns(3)
    subtotal = sum(items[item] * qty for item, qty in st.session_state.quantities.items() if qty > 0)
    
    with col_t1:
        if st.button("10% Tip", use_container_width=True):
            if subtotal > 0:
                tip = subtotal * 0.10
                st.session_state.calc_display = f"{tip:.2f}"
                st.rerun()
            else:
                st.warning("Add items first!")
    
    with col_t2:
        if st.button("15% Tip", use_container_width=True):
            if subtotal > 0:
                tip = subtotal * 0.15
                st.session_state.calc_display = f"{tip:.2f}"
                st.rerun()
            else:
                st.warning("Add items first!")
    
    with col_t3:
        if st.button("20% Tip", use_container_width=True):
            if subtotal > 0:
                tip = subtotal * 0.20
                st.session_state.calc_display = f"{tip:.2f}"
                st.rerun()
            else:
                st.warning("Add items first!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; padding: 1rem;'>
    <p>© 2024 Cafe Management System | Developed by Rashmi Kumari</p>
</div>
""", unsafe_allow_html=True)