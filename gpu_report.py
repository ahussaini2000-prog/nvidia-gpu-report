import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="NVIDIA GPU Interactive Report 2026", layout="wide")

# --- DATASET ---
# A curated list of top NVIDIA GPUs as of Jan 2026
data = [
    {"Model": "NVIDIA B200", "Series": "Data Center", "Arch": "Blackwell", "VRAM_GB": 192, "Mem_Type": "HBM3e", "Bandwidth_TB_s": 8.0, "TDP_W": 1000, "Price_USD": 45000, "Cores": "N/A (Flux)", "Use_Case": "AI Training (Massive)"},
    {"Model": "NVIDIA H200", "Series": "Data Center", "Arch": "Hopper", "VRAM_GB": 141, "Mem_Type": "HBM3e", "Bandwidth_TB_s": 4.8, "TDP_W": 700, "Price_USD": 40000, "Cores": 16896, "Use_Case": "AI Inference/Training"},
    {"Model": "NVIDIA H100 NVL", "Series": "Data Center", "Arch": "Hopper", "VRAM_GB": 94, "Mem_Type": "HBM3", "Bandwidth_TB_s": 3.9, "TDP_W": 400, "Price_USD": 30000, "Cores": 16896, "Use_Case": "AI Training"},
    {"Model": "NVIDIA H100 SXM", "Series": "Data Center", "Arch": "Hopper", "VRAM_GB": 80, "Mem_Type": "HBM3", "Bandwidth_TB_s": 3.35, "TDP_W": 700, "Price_USD": 28000, "Cores": 16896, "Use_Case": "AI Training"},
    {"Model": "NVIDIA A100 (80GB)", "Series": "Data Center", "Arch": "Ampere", "VRAM_GB": 80, "Mem_Type": "HBM2e", "Bandwidth_TB_s": 2.0, "TDP_W": 400, "Price_USD": 15000, "Cores": 6912, "Use_Case": "Legacy AI/HPC"},
    {"Model": "NVIDIA L40S", "Series": "Data Center", "Arch": "Ada Lovelace", "VRAM_GB": 48, "Mem_Type": "GDDR6", "Bandwidth_TB_s": 0.86, "TDP_W": 350, "Price_USD": 8000, "Cores": 18176, "Use_Case": "Omniverse/Inference"},
    {"Model": "RTX 6000 Ada", "Series": "Workstation", "Arch": "Ada Lovelace", "VRAM_GB": 48, "Mem_Type": "GDDR6", "Bandwidth_TB_s": 0.96, "TDP_W": 300, "Price_USD": 6800, "Cores": 18176, "Use_Case": "Rendering/AI Dev"},
    {"Model": "RTX A6000", "Series": "Workstation", "Arch": "Ampere", "VRAM_GB": 48, "Mem_Type": "GDDR6", "Bandwidth_TB_s": 0.77, "TDP_W": 300, "Price_USD": 4500, "Cores": 10752, "Use_Case": "Rendering/Data Sci"},
    {"Model": "RTX 5090", "Series": "Consumer", "Arch": "Blackwell", "VRAM_GB": 32, "Mem_Type": "GDDR7", "Bandwidth_TB_s": 1.5, "TDP_W": 500, "Price_USD": 2200, "Cores": 21760, "Use_Case": "Hardcore Gaming/Local AI"},
    {"Model": "RTX 4090", "Series": "Consumer", "Arch": "Ada Lovelace", "VRAM_GB": 24, "Mem_Type": "GDDR6X", "Bandwidth_TB_s": 1.0, "TDP_W": 450, "Price_USD": 1800, "Cores": 16384, "Use_Case": "Gaming/Local AI"},
    {"Model": "RTX 5080", "Series": "Consumer", "Arch": "Blackwell", "VRAM_GB": 16, "Mem_Type": "GDDR7", "Bandwidth_TB_s": 1.0, "TDP_W": 400, "Price_USD": 1200, "Cores": 10752, "Use_Case": "High-End Gaming"},
    {"Model": "RTX 4080 Super", "Series": "Consumer", "Arch": "Ada Lovelace", "VRAM_GB": 16, "Mem_Type": "GDDR6X", "Bandwidth_TB_s": 0.74, "TDP_W": 320, "Price_USD": 1000, "Cores": 10240, "Use_Case": "Gaming"},
]

df = pd.DataFrame(data)

# --- HEADER & INTRODUCTION ---
st.title("🟢 NVIDIA GPU Interactive Intelligence Report (2026)")
st.markdown("""
This tool helps you analyze and compare the latest NVIDIA GPUs based on **VRAM**, **Bandwidth**, **Price**, and **Application**.
Use the sidebar to filter the dataset.
""")

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filter Options")

series_filter = st.sidebar.multiselect(
    "Product Series",
    options=df["Series"].unique(),
    default=df["Series"].unique()
)

min_vram = st.sidebar.slider("Minimum VRAM (GB)", 0, 200, 12)
max_price = st.sidebar.slider("Maximum Price (USD)", 500, 50000, 50000)

# Apply filters
filtered_df = df[
    (df["Series"].isin(series_filter)) &
    (df["VRAM_GB"] >= min_vram) &
    (df["Price_USD"] <= max_price)
]

# --- MAIN CONTENT ---

# 1. KPI Metrics
col1, col2, col3 = st.columns(3)
col1.metric("GPUs Available", len(filtered_df))
if not filtered_df.empty:
    cheapest = filtered_df.loc[filtered_df["Price_USD"].idxmin()]
    most_powerful = filtered_df.loc[filtered_df["Bandwidth_TB_s"].idxmax()]
    col2.metric("Best Value Option", cheapest["Model"], f"${cheapest['Price_USD']:,}")
    col3.metric("Highest Bandwidth", most_powerful["Model"], f"{most_powerful['Bandwidth_TB_s']} TB/s")

# 2. Detailed Data Table
st.subheader("📋 GPU Specifications Table")
st.dataframe(
    filtered_df.style.format({"Price_USD": "${:,}", "Bandwidth_TB_s": "{:.2f} TB/s"}),
    use_container_width=True
)

# 3. Visualizations
st.subheader("📊 Comparative Analysis")

tab1, tab2, tab3 = st.tabs(["Price vs. VRAM", "Memory Bandwidth Leaders", "Applications"])

with tab1:
    st.markdown("**Why this matters:** For AI Fine-tuning, you often pay a premium purely for VRAM capacity.")
    fig_scatter = px.scatter(
        filtered_df,
        x="Price_USD",
        y="VRAM_GB",
        size="Bandwidth_TB_s",
        color="Series",
        hover_name="Model",
        log_x=True,
        title="Price vs. VRAM Capacity (Size = Memory Bandwidth)",
        labels={"Price_USD": "Price (USD, Log Scale)", "VRAM_GB": "VRAM (GB)"}
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with tab2:
    st.markdown("**Why this matters:** Bandwidth (TB/s) is often the bottleneck for Large Language Model (LLM) inference speed.")
    fig_bar = px.bar(
        filtered_df.sort_values("Bandwidth_TB_s", ascending=False),
        x="Bandwidth_TB_s",
        y="Model",
        color="Series",
        orientation="h",
        title="Memory Bandwidth Comparison (Higher is Better)"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with tab3:
    st.markdown("### Primary Use Cases by Model")
    for series in filtered_df["Series"].unique():
        st.caption(f"**{series}**")
        subset = filtered_df[filtered_df["Series"] == series]
        for _, row in subset.iterrows():
            st.text(f"- {row['Model']}: {row['Use_Case']}")

# 4. Recommendation Logic
st.subheader("💡 Quick Recommendations")
user_need = st.selectbox("What is your primary goal?", 
                         ["I want to play games in 4K", 
                          "I want to run/fine-tune 70B LLMs locally", 
                          "I want to train massive AI models from scratch",
                          "I do 3D Rendering (Blender/Maya)"])

if user_need == "I want to play games in 4K":
    st.info("Recommendation: **RTX 5090** or **RTX 4090**. These offer the highest clock speeds and rasterization performance.")
elif user_need == "I want to run/fine-tune 70B LLMs locally":
    st.info("Recommendation: **Dual RTX 3090/4090s** or a single **RTX 6000 Ada**. You need at least 48GB VRAM to run a 70B model comfortably at 4-bit/8-bit quantization.")
elif user_need == "I want to train massive AI models from scratch":
    st.info("Recommendation: **H100/H200 Cluster**. You cannot do this efficiently on consumer hardware. Look into cloud rental (Lambda/AWS) rather than buying.")
elif user_need == "I do 3D Rendering (Blender/Maya)":
    st.info("Recommendation: **RTX 4090** (Best Value) or **RTX 6000 Ada** (If scenes exceed 24GB VRAM). The RTX 4090 is often faster than the 6000 Ada in raw rendering if VRAM isn't the limit.")
