import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

# ---------------------------------------------------------
# Page Configurations
# ---------------------------------------------------------
st.set_page_config(
    page_title="Advertising Sales Predictor",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Custom Styling (Premium Glassmorphism & Neon Highlights)
# ---------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

/* Apply globally */
html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
    background-color: #0e1117;
}

/* Main Container spacing */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 95%;
}

/* Custom header container with premium gradient */
.header-container {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
    padding: 3rem 2rem;
    border-radius: 24px;
    border: 1px solid rgba(0, 240, 255, 0.15);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.1);
    margin-bottom: 2.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.header-container::before {
    content: "";
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(112, 0, 255, 0.1) 0%, transparent 60%);
    pointer-events: none;
}

.header-title {
    font-size: 3.5rem;
    font-weight: 700;
    margin: 0;
    background: linear-gradient(90deg, #00f0ff, #7000ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -1px;
}

.header-subtitle {
    font-size: 1.2rem;
    color: #cbd5e1;
    margin-top: 0.75rem;
    font-weight: 300;
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
    line-height: 1.6;
}

/* Tab menu customization (larger font sizes) */
.stTabs [data-baseweb="tab-list"] {
    gap: 32px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    padding-bottom: 8px;
}

.stTabs [data-baseweb="tab"] {
    height: auto;
    padding: 12px 16px !important;
    background-color: transparent !important;
    border-radius: 8px;
    color: #94a3b8 !important;
    transition: all 0.3s ease;
}

.stTabs [data-baseweb="tab"]:hover {
    color: #00f0ff !important;
    background-color: rgba(255, 255, 255, 0.02) !important;
}

/* Targeted selection of paragraph and tab wrapper to increase font size */
.stTabs [data-baseweb="tab"] p, 
.stTabs [data-baseweb="tab"] span,
.stTabs [data-baseweb="tab"] div {
    font-size: 1.4rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.3px;
}

.stTabs [aria-selected="true"] {
    color: #00f0ff !important;
    border-bottom-color: #00f0ff !important;
}

.stTabs [aria-selected="true"] p {
    color: #00f0ff !important;
}

/* Glassmorphism Metric Card */
.metric-card {
    background: rgba(30, 41, 59, 0.45);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 1.75rem 1.5rem;
    text-align: center;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.25);
    transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), border-color 0.3s ease, box-shadow 0.3s ease;
}

.metric-card:hover {
    transform: translateY(-6px);
    border-color: rgba(0, 240, 255, 0.35);
    box-shadow: 0 12px 40px 0 rgba(0, 240, 255, 0.1);
}

.metric-card-label {
    font-size: 0.9rem;
    font-weight: 600;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}

.metric-card-value {
    font-size: 2.8rem;
    font-weight: 700;
    color: #00f0ff;
    margin: 0.6rem 0;
    text-shadow: 0 0 12px rgba(0, 240, 255, 0.4);
}

.metric-card-desc {
    font-size: 0.85rem;
    color: #64748b;
    line-height: 1.4;
}

/* Premium Full-Width Horizontal Prediction Bar */
.predict-bar-full {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: linear-gradient(90deg, #1e1b4b 0%, #0f172a 100%);
    border: 2px solid #00f0ff;
    box-shadow: 0 0 35px rgba(0, 240, 255, 0.3);
    border-radius: 20px;
    padding: 2rem 3rem;
    margin-bottom: 2.5rem;
    width: 100%;
}

.predict-bar-title-full {
    font-size: 1.4rem;
    font-weight: 700;
    color: #ffffff;
    text-transform: uppercase;
    letter-spacing: 2.5px;
}

.predict-bar-price-full {
    font-size: 3.8rem;
    font-weight: 800;
    color: #00f0ff;
    text-shadow: 0 0 20px rgba(0, 240, 255, 0.7);
    white-space: nowrap;
}

.predict-desc {
    font-size: 1rem;
    color: #94a3b8;
    margin-top: 0.4rem;
    line-height: 1.6;
}

/* Custom styled section title */
.section-title {
    font-size: 2rem;
    font-weight: 700;
    color: #ffffff;
    margin-top: 1rem;
    margin-bottom: 1.5rem;
    border-bottom: 2px solid rgba(255, 255, 255, 0.08);
    padding-bottom: 0.6rem;
    letter-spacing: -0.5px;
}

/* Increase font size of characteristics labels in Streamlit */
.stSlider label, .stNumberInput label {
    font-size: 1.25rem !important;
    font-weight: 600 !important;
    color: #f8fafc !important;
}

/* Sidebar Customization */
section[data-testid="stSidebar"] {
    background-color: #0f172a !important;
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}

div[data-testid="stSidebarUserContent"] {
    padding-top: 2rem;
}

/* Sidebar simulation card container */
.sidebar-simulation-box {
    background: rgba(30, 41, 59, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Data & Model Processing (Cached)
# ---------------------------------------------------------
@st.cache_resource
def load_and_train_model():
    # Load dataset
    df = pd.read_csv("advertising.csv")
    
    # Features and Target
    X = df[['TV', 'Radio', 'Newspaper']]
    y = df['Sales']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Create polynomial features (Degree = 2)
    poly = PolynomialFeatures(degree=2)
    X_train_poly = poly.fit_transform(X_train)
    X_test_poly = poly.transform(X_test)
    
    # Train the Polynomial Regression model
    model = LinearRegression()
    model.fit(X_train_poly, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test_poly)
    
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    
    metrics = {
        "R2": r2,
        "MAE": mae,
        "MSE": mse,
        "RMSE": rmse
    }
    
    return df, poly, model, metrics, X_train, X_test, y_train, y_test, y_pred

# Load data and build model
df, poly, model, metrics, X_train, X_test, y_train, y_test, y_pred = load_and_train_model()

# ---------------------------------------------------------
# Sidebar - Inputs for Prediction (in $ currency)
# ---------------------------------------------------------
st.sidebar.markdown("""
<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 1rem;">
    <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM13 17H11V15H13V17ZM13 13H11V7H13V13Z" fill="url(#paint0_linear)"/>
        <defs>
            <linearGradient id="paint0_linear" x1="2" y1="2" x2="22" y2="22" gradientUnits="userSpaceOnUse">
                <stop stop-color="#00f0ff"/>
                <stop offset="1" stop-color="#7000ff"/>
            </linearGradient>
        </defs>
    </svg>
    <h2 style="margin: 0; font-size: 1.8rem; font-weight: 700; color: #ffffff;">Controls</h2>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div class="sidebar-simulation-box">
    <span style="color: #94a3b8; font-size: 0.95rem;">Configure the active budgets below to simulate channel distributions and predict units sold.</span>
</div>
""", unsafe_allow_html=True)

# Sliders configured in absolute dollar values ($) instead of thousands ($K)
# Default values scaled up to reflect the original data defaults (e.g. 150.0 -> $150,000)
tv_input = st.sidebar.slider("TV Advertising Budget ($)", min_value=0, max_value=300000, value=150000, step=1000)
radio_input = st.sidebar.slider("Radio Advertising Budget ($)", min_value=0, max_value=50000, value=25000, step=500)
newspaper_input = st.sidebar.slider("Newspaper Advertising Budget ($)", min_value=0, max_value=120000, value=30000, step=500)

st.sidebar.markdown("<br>", unsafe_allow_html=True)

# Compute Model-scaled values (dividing by 1000 to match model inputs)
tv_model = tv_input / 1000.0
radio_model = radio_input / 1000.0
newspaper_model = newspaper_input / 1000.0

total_budget = tv_input + radio_input + newspaper_input

# Budget allocations and premium pie visualization
st.sidebar.markdown(f"""
<div style="background: rgba(0, 240, 255, 0.05); border: 1px solid rgba(0, 240, 255, 0.2); border-radius: 12px; padding: 1rem; text-align: center;">
    <div style="font-size: 0.85rem; font-weight: 600; color: #94a3b8; text-transform: uppercase;">Total Spend Allocation</div>
    <div style="font-size: 1.8rem; font-weight: 700; color: #00f0ff; margin-top: 0.25rem;">${total_budget:,.2f}</div>
</div>
""", unsafe_allow_html=True)

# Pie chart in sidebar for budget allocation percentages
fig_allocation = go.Figure(data=[go.Pie(
    labels=['TV', 'Radio', 'Newspaper'],
    values=[tv_input, radio_input, newspaper_input],
    hole=.45,
    marker=dict(colors=['#00f0ff', '#7000ff', '#f43f5e']),
    textinfo='percent',
    hoverinfo='label+value'
)])
fig_allocation.update_layout(
    margin=dict(l=0, r=0, t=10, b=10),
    height=200,
    showlegend=False,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#ffffff')
)
st.sidebar.plotly_chart(fig_allocation, use_container_width=True)

# ---------------------------------------------------------
# Header Section
# ---------------------------------------------------------
st.markdown("""
<div class="header-container">
    <h1 class="header-title">Advertising Sales Predictor</h1>
    <p class="header-subtitle">Analyze multi-channel marketing campaigns. Interactively balance your budget allocations and monitor live sales performance outputs.</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Tabbed Interface
# ---------------------------------------------------------
tab_predict, tab_data, tab_diagnostics = st.tabs([
    "🔮 Predictor & Insights",
    "📊 Dataset Explorer",
    "🧪 Model Diagnostics & Formula"
])

# ---------------------------------------------------------
# Tab 1: Predictor & Insights
# ---------------------------------------------------------
with tab_predict:
    # Compute prediction with scaled values
    input_data = pd.DataFrame([[tv_model, radio_model, newspaper_model]], columns=['TV', 'Radio', 'Newspaper'])
    input_poly = poly.transform(input_data)
    prediction = model.predict(input_poly)[0]
    
    # Display premium horizontal prediction bar
    st.markdown(f"""
    <div class="predict-bar-full">
        <div>
            <div class="predict-bar-title-full">Predicted Sales Revenue</div>
            <div class="predict-desc">Estimated sales response for TV: <b>${tv_input:,.2f}</b>, Radio: <b>${radio_input:,.2f}</b>, Newspaper: <b>${newspaper_input:,.2f}</b></div>
        </div>
        <div class="predict-bar-price-full">{prediction:.3f}M units</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 class='section-title'>Visualizing your Budget in Context</h2>", unsafe_allow_html=True)
    
    # 2D scatter plots mapping user input (scaled back for the charts) against actual dataset distribution
    col_tv, col_radio, col_news = st.columns(3)
    
    with col_tv:
        st.subheader("TV vs Sales")
        fig_tv = px.scatter(df, x="TV", y="Sales", opacity=0.4, labels={"TV": "TV Spend ($K)", "Sales": "Sales (Units)"},
                            color_discrete_sequence=['#94a3b8'])
        # Add prediction point (using scaled model value to align with dataset ranges)
        fig_tv.add_trace(go.Scatter(x=[tv_model], y=[prediction], mode='markers',
                                    marker=dict(color='#00f0ff', size=16, symbol='star', line=dict(color='#ffffff', width=2)),
                                    name='Prediction Point'))
        fig_tv.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            showlegend=False,
            height=320
        )
        st.plotly_chart(fig_tv, use_container_width=True)
        
    with col_radio:
        st.subheader("Radio vs Sales")
        fig_radio = px.scatter(df, x="Radio", y="Sales", opacity=0.4, labels={"Radio": "Radio Spend ($K)", "Sales": "Sales (Units)"},
                               color_discrete_sequence=['#94a3b8'])
        # Add prediction point (using scaled model value to align with dataset ranges)
        fig_radio.add_trace(go.Scatter(x=[radio_model], y=[prediction], mode='markers',
                                       marker=dict(color='#7000ff', size=16, symbol='star', line=dict(color='#ffffff', width=2)),
                                       name='Prediction Point'))
        fig_radio.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            showlegend=False,
            height=320
        )
        st.plotly_chart(fig_radio, use_container_width=True)
        
    with col_news:
        st.subheader("Newspaper vs Sales")
        fig_news = px.scatter(df, x="Newspaper", y="Sales", opacity=0.4, labels={"Newspaper": "Newspaper Spend ($K)", "Sales": "Sales (Units)"},
                              color_discrete_sequence=['#94a3b8'])
        # Add prediction point (using scaled model value to align with dataset ranges)
        fig_news.add_trace(go.Scatter(x=[newspaper_model], y=[prediction], mode='markers',
                                      marker=dict(color='#f43f5e', size=16, symbol='star', line=dict(color='#ffffff', width=2)),
                                      name='Prediction Point'))
        fig_news.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            showlegend=False,
            height=320
        )
        st.plotly_chart(fig_news, use_container_width=True)

    st.markdown("---")
    
    col_lhs, col_rhs = st.columns([1, 1])
    
    with col_lhs:
        st.markdown("### 🔍 Model Dynamics & Interactions")
        st.write("""
        This engine runs a **Polynomial Features Regression model** to predict product demand based on investment across three channels. 
        Instead of a standard linear regression, it computes secondary effects and channel synergies:
        
        - **Interaction effects** are captured dynamically (e.g. how $TV \times Radio$ combined budgets amplify final sales).
        - **Diminishing returns** are represented by the negative quadratic coefficients ($TV^2$, $Radio^2$) which penalize over-spending in a single area.
        """)
        
    with col_rhs:
        st.markdown("### 📊 Allocations & Distribution Summary")
        df_summary = pd.DataFrame({
            "Marketing Channel": ["TV Campaign", "Radio Campaign", "Newspaper Campaign", "Joint Budget"],
            "Allocated Spend": [tv_input, radio_input, newspaper_input, total_budget],
            "Relative Percentage": [
                (tv_input/total_budget)*100 if total_budget > 0 else 0,
                (radio_input/total_budget)*100 if total_budget > 0 else 0,
                (newspaper_input/total_budget)*100 if total_budget > 0 else 0,
                100.0 if total_budget > 0 else 0
            ]
        })
        st.dataframe(df_summary.style.format({
            "Allocated Spend": "${:,.2f}",
            "Relative Percentage": "{:.1f}%"
        }), hide_index=True, use_container_width=True)

# ---------------------------------------------------------
# Tab 2: Dataset Explorer
# ---------------------------------------------------------
with tab_data:
    st.markdown("<h2 class='section-title'>Interactive Dataset Explorer</h2>", unsafe_allow_html=True)
    
    col_grid_lhs, col_grid_rhs = st.columns([2, 3])
    
    with col_grid_lhs:
        st.subheader("Historical Sales Database")
        st.write("Examine underlying training records:")
        
        # Display clean styled table
        st.dataframe(df, use_container_width=True, height=450)
        
        # Download button
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Dataset (CSV)",
            data=csv_data,
            file_name="advertising_dataset.csv",
            mime="text/csv"
        )
        
    with col_grid_rhs:
        st.subheader("3D Joint Target Space")
        st.write("Rotate the 3D space to see where higher sales cluster. The cyan diamond represents your active budget selection.")
        
        # Color dataset by sales
        fig_3d = px.scatter_3d(
            df, x="TV", y="Radio", z="Newspaper",
            color="Sales",
            color_continuous_scale="Viridis",
            labels={"TV": "TV ($K)", "Radio": "Radio ($K)", "Newspaper": "Newspaper ($K)"},
            opacity=0.6,
            height=450
        )
        
        # Plot predictions on scaled inputs to place it correctly on the 3D axes
        fig_3d.add_trace(go.Scatter3d(
            x=[tv_model], y=[radio_model], z=[newspaper_model],
            mode='markers',
            marker=dict(
                size=12,
                color='#00f0ff',
                symbol='diamond',
                line=dict(color='#ffffff', width=3)
            ),
            name='User Configuration'
        ))
        
        fig_3d.update_layout(
            margin=dict(l=0, r=0, b=0, t=0),
            scene=dict(
                xaxis=dict(backgroundcolor="rgba(0, 0, 0, 0)", gridcolor="rgba(255, 255, 255, 0.1)"),
                yaxis=dict(backgroundcolor="rgba(0, 0, 0, 0)", gridcolor="rgba(255, 255, 255, 0.1)"),
                zaxis=dict(backgroundcolor="rgba(0, 0, 0, 0)", gridcolor="rgba(255, 255, 255, 0.1)")
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff')
        )
        st.plotly_chart(fig_3d, use_container_width=True)

    st.markdown("---")
    
    col_corr, col_desc = st.columns([2, 1])
    
    with col_corr:
        st.subheader("Feature Correlation Heatmap")
        corr_matrix = df[['TV', 'Radio', 'Newspaper', 'Sales']].corr()
        fig_heat = px.imshow(
            corr_matrix,
            text_auto=".3f",
            aspect="auto",
            color_continuous_scale="Blues",
            labels=dict(color="Correlation")
        )
        fig_heat.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff'),
            height=300
        )
        st.plotly_chart(fig_heat, use_container_width=True)
        
    with col_desc:
        st.subheader("Descriptive Statistics")
        st.write(df[['TV', 'Radio', 'Newspaper', 'Sales']].describe().T)

# ---------------------------------------------------------
# Tab 3: Model Diagnostics & Formula
# ---------------------------------------------------------
with tab_diagnostics:
    st.markdown("<h2 class='section-title'>Model Fit & Evaluation</h2>", unsafe_allow_html=True)
    
    # 4 Metric Cards for Performance
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-card-label">R² Score (Accuracy)</div>
            <div class="metric-card-value">{metrics['R2']:.4f}</div>
            <div class="metric-card-desc">Explains {metrics['R2']*100:.2f}% of sales variance.</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-card-label">MAE (Mean Abs Error)</div>
            <div class="metric-card-value">{metrics['MAE']:.4f}</div>
            <div class="metric-card-desc">Average absolute unit prediction error.</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-card-label">MSE (Mean Sq Error)</div>
            <div class="metric-card-value">{metrics['MSE']:.4f}</div>
            <div class="metric-card-desc">Penalizes larger outliers.</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-card-label">RMSE (Root MSE)</div>
            <div class="metric-card-value">{metrics['RMSE']:.4f}</div>
            <div class="metric-card-desc">Standard deviation of residual errors.</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    
    col_plot1, col_plot2 = st.columns(2)
    
    with col_plot1:
        st.subheader("Predicted vs Actual Sales")
        fig_fit = px.scatter(
            x=y_test, y=y_pred,
            labels={"x": "Actual Sales", "y": "Predicted Sales"},
            opacity=0.7,
            color_discrete_sequence=['#00f0ff']
        )
        # Add diagonal perfect prediction line
        min_val = min(y_test.min(), y_pred.min())
        max_val = max(y_test.max(), y_pred.max())
        fig_fit.add_trace(go.Scatter(
            x=[min_val, max_val], y=[min_val, max_val],
            mode='lines',
            line=dict(color='#f43f5e', dash='dash', width=2),
            name='Ideal Fit'
        ))
        fig_fit.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            showlegend=False,
            height=350
        )
        st.plotly_chart(fig_fit, use_container_width=True)
        
    with col_plot2:
        st.subheader("Residual Distribution")
        residuals = y_test - y_pred
        fig_res = px.histogram(
            x=residuals,
            nbins=15,
            labels={"x": "Residual Value (Actual - Predicted)"},
            color_discrete_sequence=['#7000ff']
        )
        fig_res.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            height=350
        )
        st.plotly_chart(fig_res, use_container_width=True)
        
    st.markdown("---")
    
    st.subheader("📐 Model Formula Explorer")
    st.write("Below is the exact mathematical equation of the trained model, mapping how linear and interaction terms combine to predict sales:")
    
    # Gather coefficients
    coefs = model.coef_
    intercept = model.intercept_
    feature_names = poly.get_feature_names_out(['TV', 'Radio', 'Newspaper'])
    
    # Print equation formatted as LaTeX
    terms = []
    # Index 0 is the bias (if include_bias is True). But LinearRegression fits its own intercept
    # so coefs[0] is typically 0. We'll skip terms with coefficients very close to 0.
    for i, name in enumerate(feature_names):
        # Format name for LaTeX
        name_latex = name.replace(" ", " \\times ")
        name_latex = name_latex.replace("^2", "^2")
        
        coef_val = coefs[i]
        if abs(coef_val) > 1e-5:
            sign = " + " if coef_val >= 0 else " - "
            val = abs(coef_val)
            if name == "1":
                terms.append(f"{sign}{val:.4f}")
            else:
                terms.append(f"{sign}{val:.4f} \\cdot \\text{{{name_latex}}}")
                
    equation_latex = f"\\text{{Sales}} = {intercept:.4f}" + "".join(terms)
    st.latex(equation_latex)
    
    st.write("### Polynomial Coefficients Details")
    df_coef = pd.DataFrame({
        "Feature Term": feature_names,
        "Coefficient": coefs
    })
    # Replace index 0 coefficient if it is effectively zero
    df_coef.iloc[0, 1] = intercept
    # Convert index to string to avoid mixed types (string/int) in pyarrow serialization
    df_coef.index = df_coef.index.astype(str)
    df_coef.rename(index={"0": "Intercept (Baseline)"}, inplace=True)
    st.dataframe(df_coef.style.format({"Coefficient": "{:.6f}"}), use_container_width=True)
