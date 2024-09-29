import streamlit as st
with open("st_app/lda_visualization_unigram.html", 'r') as lda:
    plot=lda.read()
st.write("## LDA Unigram")
st.components.v1.html(plot, height=1000, width=1200)

with open("st_app/lda_visualization_bigram.html", 'r') as lda:
    plot=lda.read()
st.write("## LDA Bigram")
st.components.v1.html(plot, height=1000, width=1200)
