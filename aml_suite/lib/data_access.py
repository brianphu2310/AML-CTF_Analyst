"""
data_access.py
Single source of truth for loading customers/transactions and applying the
risk engine, cached so every page sees the same numbers.
"""

import os
import pandas as pd
import streamlit as st
from . import risk_engine

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


@st.cache_data
def load_customers():
    df = pd.read_csv(os.path.join(DATA_DIR, "customers.csv"), parse_dates=["onboarded_date"])
    df["onboarded_date"] = df["onboarded_date"].dt.date
    df = risk_engine.apply_customer_ratings(df)
    return df


@st.cache_data
def load_transactions():
    df = pd.read_csv(os.path.join(DATA_DIR, "transactions.csv"), parse_dates=["txn_date"])
    df["txn_date"] = df["txn_date"].dt.date
    return df


@st.cache_data
def load_alerts():
    customers = load_customers()
    transactions = load_transactions()
    return risk_engine.build_alerts(transactions, customers)


@st.cache_data
def load_typology_hits():
    customers = load_customers()
    transactions = load_transactions()
    return risk_engine.detect_typologies(transactions, customers)
