#%%библиотеки
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
#%%читаем csv смотрим, что есть
df=pd.read_csv("main.csv")
df.info()
#%%смотрим чего не хватает
sb.heatmap(df.isnull())
#%%сносим маловлияющие на цену колонки и дубликаты
print(df["deal_type"].value_counts(),          #везде sale
      df["accommodation_type"].value_counts(), #везде flat
      df["object_type"].value_counts(),        #везде -1
      df["house_material_type"].value_counts(),#много пропусков, заменить нечем
      df["finish_type"].value_counts(),        #много пропусков, заменить нечем
      df["street"].value_counts(),             #много пропусков, заменить нечем
      df["house_number"].value_counts(),       #много пропусков, заменить нечем
      df["heating_type"].value_counts())       #везде -1
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
df.loc[df["living_meters"].isna(),"living_meters"]=df["total_meters"]
df.loc[df["kitchen_meters"]=="-1","kitchen_meters"]=0
df.loc[df["kitchen_meters"].isna(),"kitchen_meters"]=0
df.replace(["-1",-1,"-1.0",-1.0],df['year_of_construction'].median(),inplace=True)
df=df[df['rooms_count']!=2006.0]
#%%приводим в порядок числа
df["living_meters"]=df["living_meters"].str.replace("\xa0м²","").str.replace(",",".").astype(float)
df["kitchen_meters"]=df["kitchen_meters"].str.replace("\xa0м²","").str.replace(",",".").astype(float)
#%%проверяем, всё ли в порядке
df.isna().mean()*100
#%%заполняем цену за метр
df['meter_price']=round(df['price']/df['total_meters'].astype(float),2)
#%%смотрим сколько квартир по сколько комнат
plt.hist(df["rooms_count"],bins=range(int(df["rooms_count"].min()),
                                      int(df["rooms_count"].max())+2),
                           edgecolor="black",color="seagreen",
                           alpha=0.7)
plt.xticks(range(int(df["rooms_count"].min()),
                 int(df["rooms_count"].max())+2))
plt.xlabel("количество комнат")
plt.ylabel("количество объявлений")
plt.show()
#%%графики типа мы умные, типа мы анализируем
fig,axs=plt.subplots(2,2,figsize=(15, 15))
axs[0,0].scatter(y=df["meter_price"],x=df["floor"],
                 alpha=0.05,color="seagreen")
axs[0,0].grid(True,alpha=0.5)
axs[0,0].set_title("по этажу")

axs[1,1].scatter(y=df["meter_price"],x=df["year_of_construction"],
                 alpha=0.1,color="seagreen")
axs[1,1].grid(True,alpha=0.5)
axs[1,1].set_title("по году постройки")

axs[0,1].scatter(y=df["meter_price"],x=df["district"],
                 alpha=0.05,color="seagreen")
axs[0,1].grid(True,alpha=0.5)
axs[0,1].set_title("по району")

axs[1,0].scatter(y=df["price"],x=df["location"],
                 alpha=0.9,color="seagreen")
axs[1,0].grid(True,alpha=0.5)
axs[1,0].set_xticklabels(labels=df["location"].value_counts().index,
                         rotation=90)
axs[1,0].set_title('по автору')
plt.show()
#%%цена по городу
plt.figure(figsize=(10,10))
plt.scatter(x=df['location'], y=df['price'],color="seagreen")
plt.xticks(rotation = 90)
plt.show()
#%%у-у-у, матрица корреляций
sb.heatmap(df.select_dtypes(include=["number"]).corr(),
                            annot=True,
                            cmap="summer_r",
                            fmt=".2f",
                            linewidths=0.5)
#%%
df.to_csv("clean_main.csv")
# %%