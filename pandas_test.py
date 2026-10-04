import pandas as pd

data = {
    "Name": ["Shristi", "Rahul", "Priya"],
    "Python": [85, 78, 92],
    "DBMS": [78, 82, 88],
    "Maths": [90, 75, 95]
}

df = pd.DataFrame(data)

print("----- Student Data -----")
print(df)

print("\n----- Average Marks -----")
print(df[["Python", "DBMS", "Maths"]].mean())