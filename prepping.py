#%%библиотеки
import pandas as pd
import seaborn as sb
#%%читаем csv смотрим, что есть
df=pd.read_csv("main.csv")
df.info()
#%%смотрим чего не хватает
sb.heatmap(df.isnull())
#%%сносим маловлияющие на цену колонки и дубликаты
print(df["deal_type"].value_counts(),
      df["accommodation_type"].value_counts(),
      df["object_type"].value_counts(),
      df["house_material_type"].value_counts(),
      df["finish_type"].value_counts(),
      df["street"].value_counts(),#много пропусков, заменить нечем
      df["house_number"].value_counts(),
      df["heating_type"].value_counts())
useless_columns=["author","author_type","url","deal_type",
                 "accommodation_type","object_type",
                 "house_material_type","finish_type","phone",
                 "heating_type","street","house_number",
                 "residential_complex"]
df=df.drop(columns=useless_columns).drop_duplicates()
#%%заполняем или удаляем пропуски
df.dropna(subset=["location","price"],inplace=True)
df.loc[df["district"].isna(),"district"]=df["location"]
df.loc[df["underground"].isna(),"underground"]=df["location"]
df.loc[df["living_meters"]=="-1","living_meters"]=df["total_meters"]
df.loc[df["kitchen_meters"]=="-1","kitchen_meters"]=0
#%%приводим в порядок числа
df["living_meters"]=df["living_meters"].str.replace("\xa0м²","").str.replace(",",".").astype(float)
df["kitchen_meters"]=df["kitchen_meters"].str.replace("\xa0м²","").str.replace(",",".").astype(float)
#%%проверяем, всё ли в порядке
df.info()
#%%у-у-у, матрица корреляций
sb.heatmap(df.select_dtypes(include=['number']).corr(),
                            annot=True,
                            cmap='summer_r',
                            fmt='.2f',
                            linewidths=0.5)