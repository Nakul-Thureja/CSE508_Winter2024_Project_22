from utils import *
from CompetitiveAnalysis import *
import streamlit as st
import time

st.markdown('### Group 22 IR Project')
st.markdown('#### E-Commerce Competitive Analysis System')
st.markdown('Search for a product on Amazon')
key = st.text_input('Enter the product name')

from concurrent.futures import ThreadPoolExecutor
import requests
from PIL import Image
from io import BytesIO
import concurrent.futures

def process_element(index, element):
    try:
        item, url = get_item_from_star_element(element)
        image = item.find('img', class_='s-image')
        response = requests.get(image['src'])
        img_pil = Image.open(BytesIO(response.content))

        soup = scrape_data(url)
        product_details = get_product_details(soup)

        description = get_about_this_item(soup)

        reviews = scrape_reviews(url)
        average_compound_score = analyze_reviews(reviews)
        product_detail = [product_details['name'], " ".join(description[1]), img_pil, url]
        all_detail = [product_details['name'], product_details['price'], description[0], description[1], average_compound_score, reviews,url, image['src']]
        return index, product_detail, all_detail
    except:
        return index, [], []
    
def get_data(key):
    with st.spinner('Searching for products...'):
        params = {
        'k': key,
        }
        page = get_soup(params, 1)

        elements = get_star_elements(page)
        
        product_dict = {}
        all_detail_product = {}

        # Create a ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=10) as executor:
            # Use list comprehension to create a list of futures
            futures = [executor.submit(process_element, index, element) for index, element in enumerate(elements)]

            # Wait for all futures to complete
            for future in concurrent.futures.as_completed(futures):
                index, product_detail, all_detail = future.result()
                product_dict[index] = product_detail
                all_detail_product[index] = all_detail
        max_index, top_k_recommendations = get_top_k_recommendations(key, product_dict)
        print("returned")
        # reviews = scrape_reviews(product_dict[max_index][3])
        # average_compound_score = analyze_reviews(reviews)
        # price, image_url = get_price_and_image_url(product_dict[max_index][3])
        # df = pd.DataFrame(reviews, columns=['Review'])
    
    with st.sidebar:
        try:
            st.title("Your Product")
            st.markdown(f"<div style='text-align: center; padding: 10px;'><img src='{all_detail_product[max_index][7]}' style='width: 80%;'></div>",unsafe_allow_html=True)    
            st.markdown(f'<div style="text-align: center;"><a href="{all_detail_product[max_index][6]}" target="_blank">Go to product page</a>', unsafe_allow_html=True)   

            st.markdown(f"## {all_detail_product[max_index][0]}")
            st.markdown(f"### Price: {all_detail_product[max_index][1]}")
            st.markdown(f"### Average sentiment score: {all_detail_product[max_index][4]:.2f}")
            st.markdown(f"### Overall sentiment: {'positive' if all_detail_product[max_index][4] > 0 else 'negative' if all_detail_product[max_index][4] < 0 else 'neutral'}")
            with st.expander("About the Product"):
                st.write(pd.DataFrame(all_detail_product[max_index][3], columns=['About the Product']))
            with st.expander("Show Reviews"):
                st.dataframe(pd.DataFrame(all_detail_product[max_index][5], columns=['Review']))
        except:
            st.write("No product found")
    
    st.markdown(f"### Top {len(top_k_recommendations)} products by Competition")
    tab_labels = [f"Product {i+1}" for i in range(len(top_k_recommendations))]

    try:
        tabs = st.tabs(tab_labels)
        count = 0
        for index in top_k_recommendations:
            with tabs[count]:
                count+=1
                with st.spinner(f"Fetching data for {product_dict[index][0]}..."):
    
                    left_co, cent_co,last_co = st.columns(3)
                    with left_co:
                        st.image(all_detail_product[index][7], width=300)
                        st.markdown(f'<a href="{all_detail_product[index][6]}" target="_blank">Go to product page</a>', unsafe_allow_html=True)
                    with last_co:
                        st.markdown(f"##### {all_detail_product[index][0]}")
                        st.markdown(f"**Price:** {all_detail_product[index][1]}")
                        st.markdown(f"**Average sentiment score:** {all_detail_product[index][4]:.2f}")
                        st.markdown(f"**Overall sentiment:** {'positive' if all_detail_product[index][4] > 0 else 'negative' if all_detail_product[index][4] < 0 else 'neutral'}")
                    with st.expander("About the Product"):
                        st.write(pd.DataFrame(all_detail_product[index][3], columns=['About the Product']))
                    with st.expander("Show Reviews"):
                        st.dataframe(pd.DataFrame(all_detail_product[index][5], columns=['Review']))
    except:
        pass
            

    
    # st.sidebar.title("Your Product")
    # st.sidebar.markdown(f"<div style='text-align: center; padding: 10px;'><img src='{image['src']}'></div>",unsafe_allow_html=True)           
    # st.sidebar.markdown(f"## {product_details['name']}")
    # st.sidebar.markdown(f"### Price: {product_details['price']}")
    # st.sidebar.markdown(f"### Average sentiment score: {average_compound_score:.2f}")
    # st.sidebar.markdown(f"### Overall sentiment: {'positive' if average_compound_score > 0 else 'negative' if average_compound_score < 0 else 'neutral'}")
            


if st.button('Find'):
    get_data(key)


