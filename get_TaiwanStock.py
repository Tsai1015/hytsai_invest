import pandas as pd

test2
def create_TaiwanStock(month):
# 取得台股上市 & 上櫃公司名單
    twseurl_1 = 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=2'
    twseurl_2 = 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=4'

    print(f'抓取 {month:02d} 月份上市公司清單')
    Listed_company = pd.read_html(twseurl_1, header = 0, encoding = 'big5hkscs')[0]
    Listed_company = Listed_company.drop(0)
    print(f'抓取 {month:02d} 月份上櫃公司清單')
    OTC_company = pd.read_html(twseurl_2, header = 0, encoding = "big5hkscs")[0]
    OTC_company = OTC_company.drop(0)

    Listed_OTC_company = pd.concat([Listed_company, OTC_company], ignore_index=True)
    Listed_OTC_company[['證券代號', '公司名稱']] = Listed_OTC_company['有價證券代號及名稱'].str.split('　', expand=True)
    Listed_OTC_company = Listed_OTC_company.drop(['國際證券辨識號碼(ISIN Code)', '上市日', 'CFICode', '備註', '有價證券代號及名稱'], axis=1)

    # 處理特殊資料
    special_data = Listed_OTC_company[Listed_OTC_company['公司名稱'].isna()]
    special_data = special_data.drop(['公司名稱'], axis=1)
    special_data = special_data.rename(columns={'證券代號': '有價證券代號及名稱'})
    special_data[['證券代號', '公司名稱']] = special_data['有價證券代號及名稱'].str.split(' ', expand=True)
    special_data = special_data.drop(['有價證券代號及名稱'], axis=1)
    special_data = special_data.dropna(subset=['公司名稱'])
    Listed_OTC_company = Listed_OTC_company.dropna(subset=['公司名稱'])
    Listed_OTC_company = pd.concat([Listed_OTC_company, special_data], ignore_index=True)
    Taiwan_stock = Listed_OTC_company["證券代號"].tolist()
    
    return Taiwan_stock