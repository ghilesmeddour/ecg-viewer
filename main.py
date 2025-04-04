import io

import aecg
import streamlit as st

st.set_page_config(
    page_title="aECG Viewer",
    page_icon="🫀",
    layout="wide",
)

st.markdown("# 🫀 Annotated ECG Viewer")

uploaded_file = st.file_uploader("Load an aECG file", type=["xml"])

c1, c2 = st.columns(2)

plot_mode = c1.selectbox("Plot mode", ["multiple", "one"])
time_mode = c2.selectbox("Time mode", ["relative", "absolute"])

if uploaded_file is None:
    if st.button("Load `Example aECG.xml`", type="secondary"):
        with open("res/Example aECG.xml", "rb") as in_file:
            bytes_data = in_file.read()
    else:
        st.stop()
else:
    bytes_data = uploaded_file.getvalue()

aecg_o = aecg.read(io.BytesIO(bytes_data))

summar_dict = aecg_o.summary()

st.markdown("## Summary")
st.json(summar_dict)

st.markdown("## Waveforms")

for serie in aecg_o.series:
    st.markdown(f"### Serie: {serie.id}")

    st.markdown("### Sequences")
    for i, seq_set in enumerate(serie.sequence_sets, 1):
        title = f"Serie {serie.id} | Sequence set {i}"
        df = seq_set.get_sequences_df()
        fig = aecg.plotter.plot_seq_set(
            df, plot_mode=plot_mode, time_mode=time_mode, title=title
        )

        st.markdown(f"**{title}**")

        with st.expander("Show data"):
            st.dataframe(df)

        st.plotly_chart(fig)

    st.markdown("### Derived sequences")
    for i, seq_set in enumerate(serie.derived_sequence_sets, 1):
        title = f"Serie {serie.id} | Derived sequence set {i}"
        df = seq_set.get_sequences_df()
        fig = aecg.plotter.plot_seq_set(
            df, plot_mode=plot_mode, time_mode=time_mode, title=title
        )

        st.markdown(f"**{title}**")

        with st.expander("Show data"):
            st.dataframe(df)

        st.plotly_chart(fig)
