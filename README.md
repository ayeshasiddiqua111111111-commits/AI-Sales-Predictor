# 📈 AI Sales Predictor

An interactive marketing analytics and machine learning web application predicting product sales from multi-channel advertising investments (TV, Radio, and Newspaper) using 2nd-degree Polynomial Regression.

---

## 🚀 Features

- **Next.js Real-Time Engine**: Instant sales forecasting with non-linear polynomial modeling.
- **Cross-Channel Synergy Simulation**: Measures the combined interaction lift (TV × Radio interaction effect).
- **Interactive Budget Sliders**: Test any combination of advertising channel allocations.
- **Strategy Presets**: One-click scenario simulations (Balanced Mix, Radio Synergy Blitz, Prime-Time TV Dominant, Lean Budget).
- **Interactive Scatter Plot**: Current allocation plotted against 200 historical campaign records.
- **Dataset Explorer**: Full searchable, sortable, and paginated campaign dataset.
- **Model Diagnostics**: Detailed mathematical equation, fitted regression weights, and accuracy metrics (R² = 95.33%, MAE = 0.903).
- **Dual Architecture**: Includes both the modern **Next.js Web App** and the original **Streamlit Python App**.

---

## 🛠️ Deploy to Vercel

### Step 1: Push to GitHub
1. Create a new repository on [GitHub](https://github.com/new).
2. Push your project to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: AI Sales Predictor Next.js web application"
   git branch -M main
   git remote add origin https://github.com/<YOUR-USERNAME>/<YOUR-REPO-NAME>.git
   git push -u origin main
   ```

### Step 2: Connect to Vercel
1. Go to [vercel.com](https://vercel.com) and log in with your GitHub account.
2. Click **"Add New..."** → **"Project"**.
3. Select your GitHub repository.
4. In the configuration settings:
   - **Root Directory**: Click **Edit** and choose `frontend`.
   - **Framework Preset**: Next.js (automatically detected).
5. Click **"Deploy"**.

Vercel will build and assign you a live, production HTTPS domain (e.g., `https://ai-sales-predictor.vercel.app`).

---

## 💻 Running Locally

### 1. Next.js Web App
- Double-click `run_web.bat` OR run:
  ```bash
  cd frontend
  npm install
  npm run build
  npm run start
  ```
- Accessible at: **http://localhost:3000**

### 2. Streamlit Python App
- Double-click `run_app.bat` OR run:
  ```bash
  python -m streamlit run app.py --server.port 8501
  ```
- Accessible at: **http://localhost:8501**
