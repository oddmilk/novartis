# Master
master = pd.read_excel('master.xlsx') # HCP master data
master['ETMSID'] = master['DETMS ID'].apply(lambda x: x[1:])  # a bit initial cleaning
hosp_sub = hosp_level[['HospitalID', 'Standard Level']].drop_duplicates()
master[['HosID','ETMSID']] = master[['HosID','ETMSID']].astype(int)
master = master.merge(hosp_sub, left_on = 'HosID', right_on = 'HospitalID', how = 'inner')


mst_cols = ['Prvnc','ETMSID','Title','sr_name','Standard Level'] # leave Product for now
mst = master[mst_cols].drop_duplicates()
mst['ETMSID'] = mst['ETMSID'].astype(int)
brand_cols = ['ETMSID','Product','Tier']
brand_potential = master[brand_cols].drop_duplicates()
brand_potential['ETMSID'] = brand_potential['ETMSID'].astype(int)


mst.columns = ['Prv', 'ETMSID', 'Title', 'Dept', 'HospLevel']
mst['HospLevel'] = mst['HospLevel'].fillna('无等级')
mst['HospLevel'] = mst['HospLevel'].str.replace('0','无等级')
mst['Dept'] = mst['Dept'].fillna('无科室')
mst.head()
hcp_dup = mst.ETMSID.value_counts().reset_index()
mst = mst.groupby('ETMSID').apply(lambda x: x.iloc[-1:]).reset_index(drop = True)


# Content 
raw = pd.ExcelFile('raw.xlsx')
hcp_content = pd.read_excel(raw, '文章link to HCP')
content_reception = pd.read_excel(raw, '阅读量统计by文章')
interaction = pd.read_excel(raw, '互动问题统计')
master = pd.read_excel('master.xlsx') # HCP master data




main = hcp_content[hcp_content['疾病领域'] == 35]
main['author_type'] = (main['作者医院'].notnull()).astype(int)
    # Remove unwanted cols
s1 = main.drop(['MCC审核号码','ETMSID','作品名称'],1).drop_duplicates()
    # Content table generation: each row is a unique content piece
a0 = main['作品ID'].value_counts().reset_index()
a0.columns = ['作品ID', 'hcp_viewed']
s2 = s1.merge(a0, how = 'inner')
    # Filter content reception data by TA (35 only)
reception = content_reception.merge(s2, how = 'inner')
reception['p_date'] = reception['推送时间'].dt.date
reception['p_weekday'] = reception['p_date'].apply(lambda x: x.weekday())
reception['p_hour'] = reception['推送时间'].dt.hour

a1 = guruGroupby(reception, 'author_type', measures).sort_values(by = 'author_type', ascending = False)
a2 = guruGroupby(reception, ['author_type', 'p_weekday'], measures).sort_values(by = ['author_type','微信阅读量'], ascending = False)
a3 = guruGroupby(reception, ['author_type', 'p_hour'], measures).sort_values(by = ['author_type','微信阅读量'], ascending = False)
a4 = guruGroupby(reception, ['author_type', '作品类型'], measures).sort_values(by = ['author_type','微信阅读量'], ascending = False)
a5 = guruGroupby(reception, ['author_type', '对应产品'], measures).sort_values(by = ['author_type','微信阅读量'], ascending = False)


# Author type
reception['author_type'] = reception['']

HCP_aut = reception[reception['author_type'] == 1]
Novartis_aut = reception[reception['author_type'] == 0]



measures = ['微信阅读量','微信转发量','微信收藏量','原文阅读量','原文点赞量']


HCP_pop = []
for i in range(len(measures)):
        x = getPopContent(HCP_aut, measures[i], 10)
        HCP_pop.append(x)



c_top10 = [HCP_aut, Novartis_aut]
