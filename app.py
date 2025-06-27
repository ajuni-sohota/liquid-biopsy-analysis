"""
Liquid Biopsy ctDNA Analysis Platform
Clinical Genomics Pipeline for Precision Oncology

Author: Ajuni Sohota
Purpose: Portfolio demonstration of clinical bioinformatics capabilities
Focus: Low-input ctDNA analysis, quality control, and clinical interpretation
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import gc  # Garbage collection for memory management

# Configure page with memory optimization
st.set_page_config(
    page_title="ctDNA Analysis Platform",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Memory-optimized CSS (minimal styling)
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        border: 1px solid #ddd;
        border-radius: 0.3rem;
        padding: 0.8rem;
        margin: 0.3rem 0;
        background-color: #f8f9fa;
    }
    .high-conf { border-left: 4px solid #28a745; }
    .low-conf { border-left: 4px solid #dc3545; }
</style>
""", unsafe_allow_html=True)

@st.cache_data(max_entries=3)  # Limit cache to save memory
def generate_demo_data():
    """Generate minimal demo dataset for ctDNA analysis"""
    # Small dataset to minimize memory usage
    np.random.seed(42)  # Reproducible results
    
    variants = []
    genes = ['EGFR', 'KRAS', 'TP53', 'PIK3CA', 'BRAF']
    cancer_types = ['NSCLC', 'CRC', 'Breast', 'Pancreatic']
    
    for i in range(8):  # Small dataset
        gene = np.random.choice(genes)
        vaf = np.random.lognormal(-2.5, 1.2)  # Realistic ctDNA VAFs
        depth = np.random.randint(5000, 15000)
        
        variants.append({
            'gene': gene,
            'variant_id': f'var_{i+1:03d}',
            'vaf_percent': max(0.01, vaf),
            'depth': depth,
            'alt_reads': int(depth * vaf / 100),
            'cancer_type': np.random.choice(cancer_types),
            'signal_to_noise': np.random.uniform(1.5, 8.0),
            'ctdna_fraction': np.random.uniform(0.001, 0.2),
            'artifact_prob': np.random.uniform(0.05, 0.6),
            'clinical_actionable': np.random.choice([True, False], p=[0.6, 0.4]),
            'validation_status': np.random.choice(['Confirmed', 'Pending', 'Failed'], p=[0.7, 0.2, 0.1])
        })
    
    return pd.DataFrame(variants)

@st.cache_data(max_entries=2)
def generate_qc_data():
    """Generate minimal QC monitoring data"""
    dates = pd.date_range(start='2024-01-15', end='2024-01-25', freq='D')
    
    qc_data = []
    for date in dates:
        qc_data.append({
            'date': date,
            'samples_processed': np.random.randint(40, 80),
            'avg_depth': np.random.normal(8000, 1000),
            'validation_rate': np.random.uniform(0.85, 0.98),
            'artifact_rate': np.random.uniform(0.02, 0.08)
        })
    
    return pd.DataFrame(qc_data)

def display_technical_metrics():
    """Display core technical analysis with minimal memory usage"""
    st.subheader("🔬 Technical Analysis")
    
    df = generate_demo_data()
    
    # Basic metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        high_conf = len(df[df['signal_to_noise'] > 3.0])
        st.metric("High Confidence", high_conf, f"{high_conf/len(df):.0%}")
    
    with col2:
        actionable = len(df[df['clinical_actionable'] == True])
        st.metric("Actionable", actionable, f"{actionable/len(df):.0%}")
    
    with col3:
        avg_vaf = df['vaf_percent'].mean()
        st.metric("Avg VAF", f"{avg_vaf:.2f}%")
    
    # Single optimized plot
    fig = px.scatter(
        df, 
        x='vaf_percent', 
        y='signal_to_noise',
        color='artifact_prob',
        hover_data=['gene'],
        title="VAF vs Signal-to-Noise Analysis",
        labels={'vaf_percent': 'VAF (%)', 'signal_to_noise': 'S/N Ratio'}
    )
    fig.add_hline(y=3.0, line_dash="dash", annotation_text="Quality Threshold")
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Clear memory
    del df
    gc.collect()

def display_quality_control():
    """Display QC monitoring with memory optimization"""
    st.subheader("📊 Quality Control Monitoring")
    
    qc_df = generate_qc_data()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.line(
            qc_df, 
            x='date', 
            y='validation_rate',
            title="Validation Rate Trend",
            labels={'validation_rate': 'Validation Rate'}
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.line(
            qc_df, 
            x='date', 
            y='artifact_rate',
            title="Artifact Rate Monitoring", 
            labels={'artifact_rate': 'Artifact Rate'}
        )
        fig.add_hline(y=0.05, line_dash="dash", annotation_text="Threshold")
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    # Clear memory
    del qc_df
    gc.collect()

def display_variant_details():
    """Display variant analysis with minimal data"""
    st.subheader("🧬 Variant Analysis")
    
    df = generate_demo_data()
    
    # Filter for demonstration
    show_count = st.slider("Number of variants to display:", 1, len(df), min(5, len(df)))
    display_df = df.head(show_count)
    
    for _, variant in display_df.iterrows():
        with st.expander(f"{variant['gene']} - {variant['variant_id']}"):
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**VAF:** {variant['vaf_percent']:.3f}%")
                st.write(f"**Depth:** {variant['depth']:,}x")
                st.write(f"**Alt Reads:** {variant['alt_reads']}")
                st.write(f"**S/N Ratio:** {variant['signal_to_noise']:.1f}")
            
            with col2:
                st.write(f"**Cancer Type:** {variant['cancer_type']}")
                st.write(f"**ctDNA Fraction:** {variant['ctdna_fraction']:.2%}")
                st.write(f"**Artifact Prob:** {variant['artifact_prob']:.1%}")
                st.write(f"**Status:** {variant['validation_status']}")
            
            # Quality assessment
            if variant['signal_to_noise'] > 3.0 and variant['artifact_prob'] < 0.3:
                st.success("✅ High Confidence Call")
            else:
                st.warning("⚠️ Requires Additional Validation")
    
    # Clear memory
    del df, display_df
    gc.collect()

def main():
    # Header
    st.markdown('<div class="main-header">🧬 Liquid Biopsy Analysis Platform</div>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    **Clinical ctDNA Analysis Pipeline for Precision Oncology**
    
    *Demonstrating bioinformatics capabilities for clinical genomics applications*
    
    **Features:** Low-VAF detection • Quality control • Clinical interpretation • Database integration
    """)
    
    # Sidebar with minimal controls
    st.sidebar.header("🔧 Analysis Settings")
    
    vaf_threshold = st.sidebar.slider(
        "VAF Threshold (%)", 
        0.01, 1.0, 0.05, 0.01,
        help="Minimum VAF for reporting"
    )
    
    sn_threshold = st.sidebar.slider(
        "S/N Threshold", 
        1.0, 10.0, 3.0, 0.1,
        help="Signal-to-noise ratio cutoff"
    )
    
    # Memory usage indicator
    if st.sidebar.button("🔍 Check Memory Usage"):
        import psutil
        memory_percent = psutil.virtual_memory().percent
        st.sidebar.info(f"Memory Usage: {memory_percent:.1f}%")
    
    # Main analysis sections
    display_technical_metrics()
    display_quality_control() 
    display_variant_details()
    
    # Capabilities summary
    st.subheader("🚀 Platform Capabilities")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🔬 Technical Features:**
        - Ultra-low VAF detection (>0.01%)
        - Signal-to-noise optimization
        - Artifact filtering algorithms  
        - Quality control pipelines
        - Real-time monitoring
        - Statistical validation
        """)
    
    with col2:
        st.markdown("""
        **👩‍⚕️ Clinical Applications:**
        - Treatment selection support
        - Biomarker discovery
        - Resistance monitoring  
        - Prognostic assessment
        - Clinical reporting
        - Physician decision support
        """)
    
    # Contact information
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    **📧 Contact**
    
    **Ajuni Sohota**  
    Bioinformatics Scientist  
    ajunisohota@gmail.com  
    
    🔗 [LinkedIn](https://linkedin.com/in/ajuni-sohota)  
    🐙 [GitHub](https://github.com/ajuni-sohota)
    """)
    
    # Force garbage collection at end
    gc.collect()

if __name__ == "__main__":
    main()
