import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import time

st.set_page_config(page_title="NFT Vesting Calculator", page_icon="🐻", layout="wide")
st.markdown("""
<style>
    .stAppHeader {
        display: none;
    }
    header[data-testid="stHeader"] {
        display: none;
    }
    .stToolbar {
        display: none;
    }
    div[data-testid="stToolbar"] {
        display: none;
    }
    .stActionButton {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<script>
setTimeout(function(){
    window.location.reload(1);
}, 300000);
</script>
""", unsafe_allow_html=True)




st.markdown("""
<script>
setTimeout(function(){
    window.location.reload(1);
}, 300000);
</script>
""", unsafe_allow_html=True)

collections = {
    "Bong Bears": 107,
    "Bond Bears": 126,
    "Boo Bears": 271,
    "Baby Bears": 570,
    "Band Bears": 1166,
    "Bit Bears": 2303
}

nft_prices_bera = {
    "Bond Bears": 159320,
    "Bong Bears": 45775,
    "Boo Bears": 57788,
    "Baby Bears": 38191,
    "Band Bears": 19626,
    "Bit Bears": 319
}

nft_images = {
    "Bond Bears": "images/1.png",
    "Bong Bears": "images/2.png",
    "Boo Bears": "images/3.png",
    "Baby Bears": "images/4.png",
    "Band Bears": "images/5.png",
    "Bit Bears": "images/6.png"
}

total_vesting_tokens = 9_500_000
total_collections = 6
tokens_per_collection = total_vesting_tokens / total_collections
total_nfts = sum(collections.values())

unlock_start_date = datetime(2026, 2, 6)
cliff_duration = 365
unlock_percentage = 1 / 6
linear_vesting_months = 24

current_date = datetime.now()
days_since_unlock = (current_date - unlock_start_date).days

def format_time_remaining(target_date):
    now = datetime.now()
    if target_date <= now:
        return "Event has passed"

    time_diff = target_date - now
    days = time_diff.days

    if days > 0:
        return f"{days} days"
    else:
        return "Less than 1 day"


def get_next_milestone():
    now = datetime.now()
    cliff_end = unlock_start_date + timedelta(days=cliff_duration)
    vesting_end = cliff_end + timedelta(days=linear_vesting_months * 30)

    if now < unlock_start_date:
        return "Unlock Start", unlock_start_date
    elif now < cliff_end:
        return "First Token Unlock (1/6)", cliff_end
    elif now < vesting_end:
        return "Full Vesting Complete", vesting_end
    else:
        return "Vesting Completed", vesting_end


st.title("🐻 NFT Collection Vesting Calculator")

milestone_name, milestone_date = get_next_milestone()
time_remaining = format_time_remaining(milestone_date)

st.markdown(f"""
<div style="background: linear-gradient(90deg, #FF6B6B, #4ECDC4); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
    <h2 style="color: white; margin: 0; text-align: center;">⏰ {milestone_name}</h2>
    <h1 style="color: white; margin: 10px 0 0 0; text-align: center; font-family: monospace;">{time_remaining}</h1>
    <p style="color: white; margin: 5px 0 0 0; text-align: center; opacity: 0.9;">Target Date: {milestone_date.strftime('%B %d, %Y')}</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    st.subheader("💰 Donate - EVM")
    st.code("0x33AcB469Aefc9e63825305145dc1a87097347dc4", language="text")
with col2:
    st.subheader("💰 Donate - Solana")
    st.code("BrMJxk2cZYoHf55cMvc7oHHuaqkKBNGjSLjZNZpYwsV3", language="text")



st.markdown("---")


def calculate_vested_amount(days_since_unlock, total_tokens):
    if days_since_unlock < cliff_duration:
        return 0
    elif days_since_unlock == cliff_duration:
        return total_tokens * unlock_percentage
    else:
        days_after_cliff = days_since_unlock - cliff_duration
        linear_vesting_days = linear_vesting_months * 30
        if days_after_cliff >= linear_vesting_days:
            return total_tokens
        else:
            remaining_after_unlock = total_tokens * (1 - unlock_percentage)
            linear_vested = remaining_after_unlock * (days_after_cliff / linear_vesting_days)
            return total_tokens * unlock_percentage + linear_vested



collection_data = []
for name, supply in collections.items():
    tokens_per_nft = tokens_per_collection / supply
    total_collection_tokens = tokens_per_collection
    vested_tokens = calculate_vested_amount(days_since_unlock, total_collection_tokens)
    remaining_tokens = total_collection_tokens - vested_tokens
    remaining_tokens_per_nft = remaining_tokens / supply
    vesting_progress = (vested_tokens / total_collection_tokens) * 100

    # Calculate vesting end date and total tokens per NFT
    vesting_end_date = unlock_start_date + timedelta(days=cliff_duration + linear_vesting_months * 30)
    total_tokens_per_nft = tokens_per_collection / supply
    current_price_bera = nft_prices_bera.get(name, 0)
    image_path = nft_images.get(name, "images/1.png")

    collection_data.append({
        "name": name,
        "supply": supply,
        "remaining_per_nft": remaining_tokens_per_nft,
        "progress": vesting_progress,
        "total_tokens_per_nft": total_tokens_per_nft,
        "current_price_bera": current_price_bera,
        "vesting_end_date": vesting_end_date,
        "image_path": image_path
    })

for i in range(0, len(collection_data), 2):
    cols = st.columns([1, 3, 1, 3])

    for j in range(2):
        if i + j < len(collection_data):
            collection = collection_data[i + j]
            image_col = cols[j * 2]
            card_col = cols[j * 2 + 1]

            with image_col:
                try:
                    st.image(collection["image_path"], width=120, caption=collection["name"])
                except:
                    st.markdown(f"""
                    <div style="display: flex; align-items: center; justify-content: center; height: 120px; width: 120px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; border: 3px solid #667eea; margin: auto;">
                        <span style="color: white; font-size: 48px;">🐻</span>
                    </div>
                    """, unsafe_allow_html=True)

            with card_col:
                progress_color = "#FF6B6B" if collection["progress"] < 20 else "#FFA726" if collection[
                                                                                                "progress"] < 70 else "#4CAF50"
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 15px; margin-bottom: 20px; box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37); backdrop-filter: blur(4px); border: 1px solid rgba(255, 255, 255, 0.18);">
                    <h3 style="color: white; margin: 0 0 15px 0; text-align: center; font-size: 1.4em;">🐻 {collection["name"]}</h3>
                    <div style="background: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                        <p style="color: white; margin: 0; font-size: 0.9em; opacity: 0.8;">NFT Supply</p>
                        <p style="color: white; margin: 5px 0 0 0; font-size: 1.8em; font-weight: bold;">{collection["supply"]:,}</p>
                    </div>
                    <div style="background: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                        <p style="color: white; margin: 0; font-size: 0.9em; opacity: 0.8;">Remaining Tokens per NFT</p>
                        <p style="color: white; margin: 5px 0 0 0; font-size: 1.6em; font-weight: bold;">{collection["remaining_per_nft"]:,.0f}</p>
                    </div>
                    <div style="background: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                        <p style="color: white; margin: 0; font-size: 0.9em; opacity: 0.8;">Current Price (updated every few days)</p>
                        <p style="color: white; margin: 5px 0 0 0; font-size: 1.4em; font-weight: bold;">{collection["current_price_bera"]:,} BERA</p>
                    </div>
                    <div style="background: rgba(34, 139, 34, 0.2); padding: 15px; border-radius: 10px; margin-bottom: 15px; border: 2px solid #228B22;">
                        <p style="color: #90EE90; margin: 0; font-size: 0.9em; font-weight: bold;">💰 Buy Now Deal</p>
                        <p style="color: #FFFFFF; margin: 5px 0 0 0; font-size: 1.1em; font-weight: bold;">Buy for {collection["current_price_bera"]:,} BERA</p>
                        <p style="color: #90EE90; margin: 5px 0 0 0; font-size: 1.2em; font-weight: bold;">→ Get total of {collection["total_tokens_per_nft"]:,.0f} tokens</p>
                        <p style="color: white; margin: 5px 0 0 0; font-size: 0.9em; opacity: 0.9;">by {collection["vesting_end_date"].strftime('%b %d, %Y')}</p>
                    </div>
                    <div style="background: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 10px;">
                        <p style="color: white; margin: 0 0 10px 0; font-size: 0.9em; opacity: 0.8;">Vesting Progress</p>
                        <div style="background: rgba(255, 255, 255, 0.2); border-radius: 10px; overflow: hidden;">
                            <div style="background: {progress_color}; height: 8px; width: {collection["progress"]:.1f}%; transition: width 0.3s ease;"></div>
                        </div>
                        <p style="color: white; margin: 5px 0 0 0; font-size: 1.2em; font-weight: bold;">{collection["progress"]:.1f}%</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

st.header("📈 Vesting Timeline")

dates = []
current_date_iter = unlock_start_date
end_date = unlock_start_date + timedelta(days=cliff_duration + linear_vesting_months * 30)

while current_date_iter <= end_date:
    dates.append(current_date_iter)
    current_date_iter += timedelta(days=30)

timeline_data = []
for collection_name, supply in collections.items():
    total_collection_tokens = tokens_per_collection
    tokens_per_nft = total_collection_tokens / supply
    collection_timeline = []

    for date in dates:
        days_from_start = (date - unlock_start_date).days
        total_vested = calculate_vested_amount(days_from_start, total_collection_tokens)
        total_remaining = total_collection_tokens - total_vested

        remaining_per_nft = total_remaining / supply
        vested_per_nft = total_vested / supply

        collection_timeline.append({
            "Date": date,
            "Collection": collection_name,
            "Remaining Tokens per NFT": remaining_per_nft,
            "Vested Tokens per NFT": vested_per_nft,
            "Remaining Tokens": total_remaining,
            "Vested Tokens": total_vested
        })

    timeline_data.extend(collection_timeline)

timeline_df = pd.DataFrame(timeline_data)

st.subheader("Remaining Tokens per NFT Over Time")
fig_remaining_per_nft = px.line(timeline_df, x="Date", y="Remaining Tokens per NFT",
                                color="Collection", title="Remaining Tokens per NFT - All Collections")
fig_remaining_per_nft.update_layout(height=500,
                                    xaxis_title="Date",
                                    yaxis_title="Remaining Tokens per NFT",
                                    font=dict(size=24, color='black'),
                                    title_font_size=32,
                                    xaxis=dict(title_font=dict(size=28, color='black'),
                                               tickfont=dict(size=22, color='black')),
                                    yaxis=dict(title_font=dict(size=28, color='black'),
                                               tickfont=dict(size=22, color='black')),
                                    legend=dict(font=dict(size=22, color='black')))
fig_remaining_per_nft.update_traces(
    hovertemplate="<b>%{fullData.name}</b><br>" +
                  "Date: %{x}<br>" +
                  "Remaining Tokens: %{y:,.0f}<br>" +
                  "<extra></extra>",
    hoverlabel=dict(
        bgcolor="white",
        bordercolor="black",
        font_size=18,
        font_family="Arial"
    )
)
st.plotly_chart(fig_remaining_per_nft, use_container_width=True)
