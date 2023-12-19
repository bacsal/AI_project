import os
import pandas as pd

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(script_dir, 'result.csv')
df = pd.read_csv(csv_file_path, encoding='cp949')
setname = set()
for i in df['MY_CHAMPION']:
    setname.add(i)
name = pd.DataFrame(setname)
name.to_csv("name.csv")

data = pd.read_csv('name.csv')
print(data.head())