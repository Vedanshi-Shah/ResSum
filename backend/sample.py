import streamlit as st
import time
from nltk.tokenize import sent_tokenize
import streamlit.components.v1 as components
import json

with open('sections.json', "r", encoding="utf-8") as f:
    data = json.loads(f.read())
    print(data.keys())
f.close()

# bootstrap 4 collapse example
st.title("Just out for a test")
hello = st.button("Introduction")
bye = st.button("References")

tabs = []
i = 0
for tab in data:
    print(tab)
    tabs.append(tab)
    i+=1

ts = st.tabs(tabs)
while i>0:
    with ts[i-1]:
        st.write(tabs[i-1])
        st.write(data[tabs[i-1]])
    i-=1

if (hello):
    st.write(data['1. INTRODUCTION '])
if (bye):
    st.write(data['9. ACKNOWLEDGMENTS '])

components.html(
    """
        <link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Dancing+Script&display=swap" rel="stylesheet">
    """, scrolling=True
)

text = """A cuckoo filter is a compact variant of a hash table that stores only fingerprints. this paper also applies partialkey cuckio hashing to serve set membership tests. it uses less space than bloom filters in many practical applications. Full keys are not stored, so a cuckoo filter cannot insert new items. standard cuckaboo hashing involves moving keys based on their hash values. a filter can only insert new keys if the full key set is not stored. Optimal bloom filter uses 1.44 log2 bits per item, for a 44% overhead. cuckoo filters are spaceoptimized and do not use semisorting. each filter consists of an array of blocks and each block is a small bloom filter. Cuckoo filters are asymptotically better (by a constant factor) than bloom filters. instead of checking each item’s two buckets one by one, our implementation applies a performance optimization that tries to issue two memory loads together. This property of cuckoo filters provides an approximate table lookup mechanism. it returns 1 +  values on average for each existing item and on average  for each nonexisting item. this is useful for matching more than one fingerprint due to false positive hits. A basic cuckoo hash table consists of an array of buckets where each item has two candidate buckets determined by hash functions h1(x) and h2(x). given an item x, the algorithm first calculates x’s fingerprint and two candidate. buckets according to eq. Partialkey cuckoo hashing is based on a hash table of 8 buckets. bucket size and number of buckets in the table can be varied. load factor can be increased or decreased depending on the bucket size. Cuckoo filters are not suitable for applications that insert the same item more than 2b times. the two buckets for this duplicated item will become overloaded. we choose cucktoo filter because it achieves the best space efficiency for false positive rates. A spaceoptimized bloom filter uses k = log2 hash functions. each item can be stored using 1.44 log2 bits. a counting bloom filter requires 4 more space than a standard bloom filter. This paper focuses on optimizing and analyzing the space efficiency when using partialkey cuckoo hashing with only fingerprints. cuckeroo filters are like counting bloom filters that can delete inserted items by removing corresponding fingerprints from the hash tables on deletion."""
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 500px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 500px;
        margin-left: -500px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.title("Sit tight while we garnish your summary")
for t in sent_tokenize(text):
    st.sidebar.markdown("""* <div style="background-color: #337def; margin-bottom: 5px; padding: 5px 5px; padding-left: 10px"><span style="color: #fcc729;"><b> %s <b></span></div>""" % t, unsafe_allow_html=True)

# def main():
    # if 'i' not in st.session_state:
    #     st.session_state.i = 0
    # if 'clicked' not in st.session_state:
    #     st.session_state.clicked = False
    # st.session_state.i+=1
    # st.session_state.i%=3
    # st.title("Testing Streamlit")
    # button = st.button("Stop it here!")
    # if (button):
    #     st.session_state.clicked = True
    # st.sidebar.title(text[st.session_state.i])
    # if (not(st.session_state.clicked)):
    #     time.sleep(2)
    #     st.experimental_rerun()
# t = st.empty()
# if 'i' not in st.session_state:
#     st.session_state.i = 0
# def on_update():
#     st.session_state.i+=1
#     st.session_state.i%=1
#     t.text(text[st.session_state.i])
# on_update()
# if __name__=="__main__":
#     main()
