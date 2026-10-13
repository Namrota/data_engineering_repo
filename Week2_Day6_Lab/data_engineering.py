import pandas as pd

# Inspect Three Small Input Batches
b1_df= pd.read_csv('batch_1.csv')
b2_df= pd.read_csv('batch_2.csv')
b3_df= pd.read_csv('batch_3.csv')

print(f"Row count for batch 1: {b1_df.shape[0]} ")
print(f"Row count for batch 1: {b2_df.shape[0]} ")
print(f"Row count for batch 1: {b3_df.shape[0]} ")

new_df= pd.concat([b1_df, b2_df, b3_df], ignore_index=True)
print(f"Row count for new concatenated dataframe: {new_df.shape[0]} ")

print(f"Total sales: {new_df['amount_gbp'].sum().round(2)}")



# Q. 7 — Process Three Batches and Keep the Counts
b1_df['batch_id']= 1
b2_df['batch_id']= 2
b3_df['batch_id']= 3

concat_df= pd.concat([b1_df, b2_df, b3_df], ignore_index=True)
summary= concat_df.groupby('batch_id').agg(
    {"order_id": ["count"], 
    "amount_gbp": ["sum"]})

print(f"Summary:\n {summary}")


# Q. 9 — Clean a Batch of Orders
orders = pd.DataFrame({
    "order_id": [201, 202, 203, 204],
    "city": [" London ", "Manchester", "Leeds", None],
    "amount_gbp": [45.50, -5.00, 30.00, 20.00],
})

rejected_orders= ((orders['city'].isna())|(orders['amount_gbp'] < 0))
reject_df= orders.loc[rejected_orders].copy()
valid_orders= orders.loc[~rejected_orders].copy()
valid_orders['city']= valid_orders['city'].str.strip()

print(valid_orders)
print(reject_df)


# Q. 11 — Simulate Three Batch Runs
batch_1 = [10, 20, 30]
batch_2 = [40, 50]
batch_3 = [60, 70, 80, 90]

batches=[batch_1, batch_2, batch_3]
cumulative_total= 0

for key, val in enumerate(batches, start= 1):
    batch_total= sum(val)
    cumulative_total+= batch_total

    print(key,
          len(batches),
          batch_total,
          cumulative_total)