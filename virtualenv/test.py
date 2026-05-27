import pandas as pd
sample_data = {
    "a": [4,5,6],
    "b": [7,8,9],
    "c": [10,11,12]
}

df = pd.DataFrame(sample_data)
df_index = pd.DataFrame(sample_data, index=[1,2,3])

# print(df)
print(df_index)