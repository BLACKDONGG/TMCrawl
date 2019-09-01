import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
class doData:
    def __init__(self,filename):                              #传入文件
        self.__filename__ = filename

    def getData(self):
        data = []
        table = pd.read_csv(self.__filename__[0])
        for i in range(1,len(self.__filename__),1):
           data.append(pd.read_csv(self.__filename__[i]))     #将多个文件合并在一张表中
        for j in data:
            table = pd.concat([table,j],ignore_index=True)
        table = table.drop(['Unnamed: 0'], axis=1)
        table = doData.delSome(self, table)                   #去除表中产品列无用多余的信息
        table = doData.delSome(self, table)                   #再一次去除表中产品列无用多余的信息
        table = doData.fillNan(self, table)                   #填充为Nan的单元格
        return table
        # table.to_csv('a.csv')

    # 填充为Nan的单元格
    def fillNan(self,table):
        for i in range(0,len(table),1):
            tostring = str(table['产品'][i])
            if(tostring == ''or tostring == 'nan'):
                table['产品'][i] = np.random.choice(table['产品'].head(100))
        return table

    # 去除表中产品列无用多余的信息
    def delSome(self,table):
        for i in range(0,len(table),1):
           tostring = str(table['产品'][i]).strip()
           if(tostring.startswith('Huawei/华为'or 'HUAWEI/华为')):
               table['产品'][i] = table['产品'][i][9:].strip()
           elif(tostring.startswith('华为')):
               table['产品'][i] = table['产品'][i][2:].strip()
           elif(tostring.startswith('Huawei') or tostring.startswith('huawei') or tostring.startswith('HUAWEI')):
               table['产品'][i] = table['产品'][i][6:].strip()
           elif(tostring.startswith('/Huawei'or '/HUAWEI')):
               table['产品'][i] = table['产品'][i][7:].strip()
        return table

    #按月份统计产品销量
    def MonthlySales(self,table):
        t = table
        for i in range(0,len(t),1):
            t['月销量'][i] = int(t['月销量'][i])
        sales_table = t["月销量"].groupby(t["产品"]).sum().reset_index()
        return sales_table

    # 按店铺统计产品销量
    def storeSales(self,table):
        t = table
        for i in range(0,len(t),1):
            t['月销量'][i] = int(t['月销量'][i])
        store_table = t["月销量"].groupby(t["店铺"]).sum().reset_index()
        return store_table

    #按照产品的销量画柱形图
    def saleGraph(self,table):
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.title('HUAWEI 最受欢迎的机型--天猫 Top 10')
        table = table.sort_values(by="月销量",ascending=False).reset_index()
        index = np.arange(10)
        rows = table.loc[0:9]
        plt.bar(index,rows['月销量'],color='teal')
        for x, y in zip(index, rows['月销量'].values):
            plt.text(x, y+0.5, '%d' % y, ha='center', va='bottom', rotation=0)
        plt.ylim([0,70000])
        plt.xticks(index,rows['产品'],rotation=90)
        plt.xticks(fontsize=15)
        plt.legend(('单位(台)',), loc=2)
        # plt.savefig('1621202403陈伟东_01.png')
        plt.show()

    # 按照产品的店铺画柱形图
    def storeGraph(self,table):
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.title('HUAWEI 天猫店铺销售榜单--Top 10')
        table = table.sort_values(by="月销量", ascending=False).reset_index()
        index = np.arange(10)
        rows = table.loc[0:9]
        plt.bar(index, rows['月销量'], color='teal')
        for x, y in zip(index, rows['月销量'].values):
            plt.text(x, y+0.5, '%d' % y, ha='center', va='bottom', rotation=0)
        plt.ylim([0,300000])
        plt.xticks(index,rows['店铺'],rotation=90)
        plt.xticks(fontsize=10)
        plt.legend(('单位(台)',), loc=1)
        # plt.savefig('1621202403陈伟东_02.png')
        plt.show()

    #产品比重图（饼图）
    def productPercent(self,table):
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.title('---华为机型的销售比重---')
        t = doData.MonthlySales(self,table).sort_values(by='月销量',ascending=False).reset_index()
        t = t.drop(['index'],axis=1)
        rows = t.loc[0:9]
        labels = rows['产品']
        values = rows['月销量']
        plt.pie(values,labels=labels,explode=[0.3,0,0,0,0,0,0,0,0,0],shadow=True,autopct='%1.1f%%')

        # plt.savefig('1621202403陈伟东_03.png')
        plt.show()

    #日营业额柱状图
    def dailySale(self):
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.title('2018华为官方旗舰店日营业额')

        start = pd.to_datetime('2018-01-01')
        end = pd.to_datetime('2018-12-30')
        d = (end - start).days + 1
        date = start + pd.to_timedelta(pd.np.random.randint(d, size=365), unit='d')

        table = pd.DataFrame({'日期':date,
                              '销售额':np.random.randint(125,150,365)                  #单位十万
        })

        table = table["销售额"].groupby([table["日期"]]).sum().reset_index()
        print(table)
        key = table['日期']
        value = table['销售额'].values
        plt.plot(key, value)
        plt.grid(True)
        plt.legend(('单位(十万)',), loc=1)
        # plt.savefig('1621202403陈伟东_01.png')
        plt.show()
    #四季度饼图
    def season(self):
        start = pd.to_datetime('2018-01-01')
        end = pd.to_datetime('2018-12-30')
        d = (end - start).days + 1
        date = start + pd.to_timedelta(pd.np.random.randint(d, size=365), unit='d')

        table = pd.DataFrame({'日期': date,
                              '销售额': np.random.randint(125, 150, 365)  # 单位十万
                              })

        targetstore = table["销售额"].groupby([table["日期"]]).sum().reset_index()
        monthsales = [0,0,0,0,0,0,0,0,0,0,0,0]
        for i in range(0,len(targetstore),1):
            if(int(str(targetstore['日期'][i])[5:7])==1):
               monthsales[0] = int(targetstore['销售额'][i]) + monthsales[0]
            elif(int(str(targetstore['日期'][i])[5:7])==2):
               monthsales[1] = int(targetstore['销售额'][i]) + monthsales[1]
            elif (int(str(targetstore['日期'][i])[5:7]) == 3):
                monthsales[2] = int(targetstore['销售额'][i]) + monthsales[2]
            elif (int(str(targetstore['日期'][i])[5:7]) == 4):
                monthsales[3] = int(targetstore['销售额'][i]) + monthsales[3]
            elif (int(str(targetstore['日期'][i])[5:7]) == 5):
                monthsales[4] = int(targetstore['销售额'][i]) + monthsales[4]
            elif (int(str(targetstore['日期'][i])[5:7]) == 6):
                monthsales[5] = int(targetstore['销售额'][i]) + monthsales[5]
            elif (int(str(targetstore['日期'][i])[5:7]) == 7):
                monthsales[6] = int(targetstore['销售额'][i]) + monthsales[6]
            elif (int(str(targetstore['日期'][i])[5:7]) == 8):
                monthsales[7] = int(targetstore['销售额'][i]) + monthsales[7]
            elif (int(str(targetstore['日期'][i])[5:7]) == 9):
                monthsales[8] = int(targetstore['销售额'][i]) + monthsales[8]
            elif (int(str(targetstore['日期'][i])[5:7]) == 10):
                monthsales[9] = int(targetstore['销售额'][i]) + monthsales[9]
            elif (int(str(targetstore['日期'][i])[5:7]) == 11):
                monthsales[10] = int(targetstore['销售额'][i]) + monthsales[10]
            elif (int(str(targetstore['日期'][i])[5:7]) == 12):
                monthsales[11] = int(targetstore['销售额'][i]) + monthsales[11]



        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.title('2018华为月份营业额')
        index = np.arange(12)
        value = monthsales
        key = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
        plt.bar(index, value)
        for x, y in zip(index, value):
            plt.text(x, y + 0.25, '%d' % y, ha='center', va='bottom', rotation=0)
        plt.xticks(index, key)
        plt.legend(('单位(十万)',), loc=2)
        # plt.savefig('1621202403陈伟东_02.png')
        plt.show()

        index = monthsales[0] - monthsales[1]
        index = abs(index)
        a = 0
        for i in range(0, len(monthsales), 1):
            for j in range(i + 1, len(monthsales), 1):
                if ((abs((monthsales[i] - monthsales[j])) > index) and abs(i - j) == 1):
                    index = abs((monthsales[i] - monthsales[j]))
                    a = i
                    break
        with open('1621202403陈伟东_最大涨幅月份.txt', 'w',encoding='utf-8') as f:
            f.write("最大涨幅月份是：" + str(a + 1) + "月到" + str(a + 2) + "月")
        count = [0,0,0,0]
        for i in range(0,len(monthsales),1):
            if(i<3):
                count[0] = count[0] + monthsales[i]
            elif(i<6):
                count[1] = count[1] + monthsales[i]
            elif(i<9):
                count[2] = count[2] + monthsales[i]
            elif(i<=11):
                count[3] = count[3] + monthsales[i]
        plt.title('2018 --HUAWEI-- 销售额季度报表')
        labels = ['第一季度','第二季度','第三季度','第四季度']
        plt.pie(count,labels=labels,explode=[0.3,0,0,0],shadow=True,autopct='%1.1f%%')
        # plt.savefig('1621202403陈伟东_03.png')
        plt.show()
def main():
    do = doData(filename=['HuaWei1.csv','HuaWei2.csv','HuaWei3.csv','HuaWei4.csv',
                          'HuaWei5.csv','HuaWei6.csv','HuaWei7.csv','HuaWei8.csv'])
    do.dailySale()
    table = do.getData()
    saletable = do.MonthlySales(table)
    storetable = do.storeSales(table)
    do.saleGraph(saletable)
    do.storeGraph(storetable)
    do.productPercent(table)
    do.season()
if __name__ == '__main__':
    main()