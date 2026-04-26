import pandas as pd
import numpy as np
from sklearn.linear_model import ElasticNetCV
from sklearn.preprocessing import StandardScaler

# =============================================================
# 1. SETUP — replace these with your actual DataFrames
# =============================================================
# df_x = pd.read_csv("your_features.csv")
# df_y = pd.read_csv("your_targets.csv")
# If df_y has multiple columns, pick the one you want:
# y = df_y["your_target_column"].values

# For now, assuming df_x and df_y are already loaded:
X = df_x.values
y = df_y.values.ravel()  # flatten to 1D if needed
feature_names = df_x.columns.tolist()

# =============================================================
# 2. SCALE FEATURES
#    ElasticNet is sensitive to feature scale — standardize first.
# =============================================================
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# =============================================================
# 3. FIT ElasticNetCV
#    Searches over alpha values for each l1_ratio, using k-fold CV.
# =============================================================
l1_ratios = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.99, 1.0]

model = ElasticNetCV(
    l1_ratio=l1_ratios,
    n_alphas=100,          # 100 alpha candidates per l1_ratio
    cv=5,                  # 5-fold cross-validation
    random_state=42,
    max_iter=10_000,
)

# Fit ElasticNetCV on scaled data
model.fit(X_scaled, y)

# Back-transform coefficients to original feature units
beta_original = model.coef_ / scaler.scale_
intercept_original = model.intercept_ - np.sum(model.coef_ * scaler.mean_ / scaler.scale_)

# =============================================================
# 4. RESULTS
# =============================================================
print("=" * 60)
print("BEST HYPERPARAMETERS")
print("=" * 60)
print(f"  alpha    (penalty strength) : {model.alpha_:.6f}")
print(f"  l1_ratio (L1 vs L2 mix)     : {model.l1_ratio_:.2f}")
print(f"  intercept                   : {model.intercept_:.6f}")
print(f"  intercept ReScaled          : {intercept_original:.6f}")
print()

# Build a DataFrame of coefficients
coef_df = pd.DataFrame({
    "feature": feature_names,
    "beta_scaled": model.coef_,           # for ranking importance
    "beta_original": beta_original,       # for interpretation in original units
    "abs_beta_scaled": np.abs(model.coef_),
}).sort_values("abs_beta_scaled", ascending=False)

print("=" * 60)
print("MODEL COEFFICIENTS (sorted by magnitude)")
print("=" * 60)
print(coef_df.to_string(index=False))
print()

# Show which features were dropped (beta = 0)
dropped = coef_df[coef_df["beta_scaled"] == 0]["feature"].tolist()
kept = coef_df[coef_df["beta_scaled"] != 0]["feature"].tolist()
print(f"Features kept   : {len(kept)}")
print(f"Features dropped: {len(dropped)}")
if dropped:
    print(f"  Dropped: {dropped}")

# =============================================================
# 5. TRACKING ERROR & CORRELATION (original units)
# =============================================================
y_pred = X @ beta_original + intercept_original

tracking_error = np.std(y - y_pred, ddof=1) # ddof=1: divides by n-1 → sample std (Bessel's correction)
tracking_error_annualized = tracking_error * np.sqrt(252)
correlation    = np.corrcoef(y, y_pred)[0, 1]

print("=" * 60)
print("FIT DIAGNOSTICS")
print("=" * 60)
print(f"  Tracking error (std of residuals) : {tracking_error:.6f}")
print(f"  Tracking error (annualized) : {tracking_error_annualized:.6f}")
print(f"  Correlation (y vs y_pred)         : {correlation:.6f}")
