wb = openpyxl.load_workbook("amazon_product.xlsx")
server_list = ['Japan #527','Japan #553','Japan #573','Japan #543','Japan #531','Japan #535','Japan #587','Japan #530','Japan #526','Japan #574']

already_list_before = []

for server in server_list:
    ws = wb[server]
    for excel_i in range(1,200):
        for excel_j in range(1,200):
            if ws.cell(column=excel_i,row=excel_j).value != None:
                already_list_before.append(ws.cell(column=excel_i,row=excel_j).value)
counter = collections.Counter(already_list_before)
already_list = []
for key in counter.most_common():
    if key[1] >= 10:
        already_list.append(key[0])
    else:
        break
letter = 'select * from Amazon.freebooks'
df = pd.read_sql(letter,conn)
for i in range(len(df)):
    asin = df['asin'][i]
    if asin in already_list:
        letter = 'update Amazon.freebooks set buy_flag = TRUE where asin = "'+asin+'"'
        conn.execute(letter)
for server in server_list:
    ws = wb[server]
    le= 'select * from Amazon.Rua'+server[-3:]+';'
    df = pd.read_sql(le, conn)
    berfore = []
    for i in range(len(df)):
        before.append(df['asin'][i])
    for excel_i in range(1,200):
        for excel_j in range(1,200):
            if ws.cell(column=excel_i,row=excel_j).value != None:
                asin = ws.cell(column=excel_i,row=excel_j).value
                if not asin in before:
                    letter = 'insert into Amazon.Rua'+server[-3:]+' values("'+asin+'")'
                    try:
                        conn.execute(letter)
                    except:
                        print('error')
