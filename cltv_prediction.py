##############################################################
# BG-NBD ve Gamma-Gamma Submodel ile CLTV Prediction

# => Bu projecede Zaman Projeksiyonlu lifetime value tahmini gerçekleştireceğiz.

# => CLTV = Expected Number of Transactşon * Expected Average Profit

# => Conditional Expected = koşullu beklenti.

# => CLTV = BG/NBD Model * Gamma Gamma Submodel

# => BG/NBD ( Beta Geometric  / Negative Binomial distribution) bu dağılımı kullanarak Expected Number of Transaction
# değerlerini hesaplayacağız. Karlılık

# => Expected = Bir rastsal değişkenin beklenen değerini ifade etmek için kullanılır. Yani o rastsal değişkenin
# ortalaması demek.

# => Rastsal Değişken = Değerlerini bir deneyin sonuçlarından alan değere rastsal değişken denir.

# => Genel olarak kitleden bir dağılım yapısı öğreneceğiz, bu dağılım yapısı genel olarak insanların satın alma
# transaction davranışlarının dağılımı olacak, ki bu bir olasılık dağılımı, bu olasılık dağılımının beklenen bir değeri
# vardı, yani bir ortalaması vardır. Bu olasılık dağılımının beklenen değerini koşullandırarak yani bireyler özelinde
# biçimlendirerek her bir birey için beklenen işlem sayısını tahmin etmiş olacağız. Dolayısıyla amacımız olasılık
# dağılımları aracılığıyla genel kitlemizin satın alma davranışlarını modelleyip bunları kişilerin özeline indirgemek.

# => BG/NBD modeli diğer adıyla Buy Till You Die olarak anılmaktadır. Alış veriş süreçlerimiz iki basamaktan meydana
# gelir.
# 1. Basamak => Satın alma süreci yani Buy süreci
# 2. Basamak => Bırakma süreci, düşme, işlemi bitirme, yani drop olma, yani churn olma , Till You Die sürecidir.
# BG/NBD modeli bu süreci modellemektedir.


####   Transaction Process (Buy) + Dropout Process (Till You Die)   ####

# Transaction Process (Buy)
# => Transaction Process alive (haytta) olduğu sürece, belirli bir zaman periyodunda, bir müşteri tarafından
# gerçekleştirilecek işlem sayısı transaction rate parametresi ile possion dağılır.
# => Bir müşteri alive (hayatta) olduğu sürece kendi transaction rate i etrafında rastgele satın alma yapmaya devam
# edecektir.
# => Transaction rate ler her bir müşteriye göre değişir ve tüm kitle için gamma dağılır (r, a)
# => Satın alma süreçleri, işlem oranları bütün bir kitle açısından farklılıklar gösteriyor yani kişiden kişiye
# değişiyor, yani he bir kişye göre değişen bu satın alma davranışı tüm kitle için gamma dağılıyor.


# Dropout Process (Till You Die)

# => Her bir müşterinin p olasılığı ile dropout rate (dropout probability) i vardır. yani churn olma, aktif olmama,
# satın almayı bırakma olasılığı vardır.
# => Bir müşteri alış veriş yaptıktan sonra belirli bir olasıkla drop olur.
# => Dropout  rate ler he bir müşteriye göre değişir ve tüm kitle için beta dağılır (a, b)
# recency => Bir müşterinin ilk satın alması ile son satın alması arasındaki geçen süredir. Haftalık cinstendir. Bu
# müşteri özelinde bir recency dir. her bir müşterinin ilk ve son satınalması arasındaki geçen süredir.
# T = müşterinin ilk satın alması üzerinden geçen zamandır. Yani analiz günü ile müşterinin ilk alış veriş yaptığı gün
# arasındaki farktır. Müşterinin yaşıdır.


######        Gamma Gamma Submodel      #######

# => Bir müşterinin işlem başına ortalama ne kadar kar getirebileceğini tahmin etmek için kullanılır.

# CVTL = Expected Number of Transaction * Expected Average Profit

# CLTV = BG/NBD Model * Gamma Gamma Submodel

# Bir müşterinin işlemlerinin parasal değeri (monetary) transaction value'larının ortalaması etrafında rastgele dağılır.

# Ortalama transaction value, zaman içinde kullanıcılar arasında değişebilir fakat tek bir kullanıcı için değişmez.

# => Ortlama transaction value tüm müşteriler arasında gamma dağılır. Yani bu şu anlama gelir: Müşterilerimin satın alma
# frekanslarının dağılımını biliyordum, şimid bu gamma dağılımı ile bana bırakacakları ortalama karlılığın da dağılımını
# biliyorum. Yani gama dağılımı ile dağılıyormuş.

# => x = frequency değeri.tekrar eden satış sayısı. en az ikinci kez işlem yapmış lolma durumunu ifade ediyor.
# => monetary

# Sonuç olarak BD/NBD model ile Gamma Gamma Submodel bir araya getirildiğinde CLTV (customer Lifetime Value)  tahmini
# değerlerini belirli bir zaman projeksiyonu ile ele almış oluyoruz.

##############################################################
# Yol Haritası
# 1. Verinin Hazırlanması (Data Preperation)
# 2. BG-NBD Modeli ile Expected Number of Transaction
# 3. Gamma-Gamma Modeli ile Expected Average Profit
# 4. BG-NBD ve Gamma-Gamma Modeli ile CLTV'nin Hesaplanması
# 5. CLTV'ye Göre Segmentlerin Oluşturulması
# 6. Çalışmanın fonksiyonlaştırılması


##############################################################
# 1. Verinin Hazırlanması (Data Preperation)
##############################################################

# Bir e-ticaret şirketi müşterilerini segmentlere ayırıp bu segmentlere göre
# pazarlama stratejileri belirlemek istiyor.

# Veri Seti Hikayesi

# https://archive.ics.uci.edu/ml/datasets/Online+Retail+II

# Online Retail II isimli veri seti İngiltere merkezli online bir satış mağazasının
# 01/12/2009 - 09/12/2011 tarihleri arasındaki satışlarını içeriyor.

# Değişkenler

# InvoiceNo: Fatura numarası. Her işleme yani faturaya ait eşsiz numara. C ile başlıyorsa iptal edilen işlem.
# StockCode: Ürün kodu. Her bir ürün için eşsiz numara.
# Description: Ürün ismi
# Quantity: Ürün adedi. Faturalardaki ürünlerden kaçar tane satıldığını ifade etmektedir.
# InvoiceDate: Fatura tarihi ve zamanı.
# UnitPrice: Ürün fiyatı (Sterlin cinsinden)
# CustomerID: Eşsiz müşteri numarası
# Country: Ülke ismi. Müşterinin yaşadığı ülke.


##########################
# Gerekli Kütüphane ve Fonksiyonlar
##########################

# !pip install lifetimes ile kurulum yapmamız lazım. Çünkü dağılım modellerini kullanabilmez için bu kurulum şart.
import datetime as dt # burada datetime modülünü programa dahil ettik. Bu kütüphaneyi yüklememizin sebebi tipi boject
# görünüp fakat geröekte time olan verileri bu kütüphane ile tipini time çevirmek içindir.
import pandas as pd
import matplotlib.pyplot as plt # burada grafik olarak görmek istersek diye bu matplotlib içerisinden pyplot kuruldu.
from lifetimes import BetaGeoFitter # lifetimes içerisinden Beta modeli kuruldu.
from lifetimes import GammaGammaFitter # yukarıdaki gibi lifetimes içerisinden Gamma Gamma modeli kuruldu.
from lifetimes.plotting import plot_period_transactions

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.float_format', lambda x: '%.4f' % x)
from sklearn.preprocessing import MinMaxScaler # bunun amacı lifetime value hesaplandıktan sonra bu değeri 0-1 yada
# 0-100 arasına çekmek istediğimiz zaman bu kütüphane içerisindeki min max fonksiyonlarını kullanmak için yükledik.

# Aykırı değer = Bir değişkenin genel dağılımının oldukça dışında olan değerdir.
def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit

# quantile() fonksiyonu çeyreklik hesaplama fonksiyonudur.
# Yukarıdaki fonksiyonu yazmamızın temel amacı şudur: aykırı değerler ile ilgili çalıma yapamız lazım. boplot yada iqr
# olarak geçen önce aykırı değerleri tespit edeceğiz bu fonksiyon ile. aşağıdaki fonksiyon ile de aykırı değerleri eşik
# değerler ile değiştireceğiz.
# Yukarıdaki fonskiyonun görevi kendisine girilen değişken için eşik değer belirlemektir.
# öncelikle quartile1 ve quartile3 gibi iki tane değişken oluşturulıup bu dataframe in çeyrek değerleri hesaplanarak bu
# değişkenlere atanmıştır.
# Daha sonra bulunan bu çeyreklik değerlerinin farkı hesaplanarak interquantile_range (çeyrekler açıklığı) değişkenine
# atanıyor.
# Bu hesaplamalardan sonra alt ve üst limitler belirleniyor.
# üst limit = üçüncü çeyrek ile çeyrek açıklığının 1.5 katı toplanarak belirleniyor.
# alt limit = birinci çeyrekden çeyrek açıklığının 1.5 katı çıkarılarak elde ediliyor.
# fonksiyon bize bu işlemler sonucunda return ile alt ve üst limit değerlerini dönüyor.
# Bilgi :  quantile (0.01) ile quantile(0.99) değerlerini biz  veriyi inceleyip kendimiz belirledik. Ama normalde
# outlier eşik değerini belirlemek için çeyreklik eşik değerini 0.25 ile 0.75 olarak alırız.
# hesaplanan alt ve üst limitlerin dışında kalan veriler değerler bizi için artık aykırı değerdir.
# 0.01 ile 0.99 almamızın temel sebebi ise veri seti içerisinde en problemli en sıkıntılı değerleri atmak. olabildiğince
# az veri atmak aralığı geniş tutmak.


def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    # dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit # bu değişkenin değerlerinde eksi değerler
    # olmadığından dolayı buranın çalıştırılmasına gerek yoktur.
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit

# Yukarıdaki fonksiyonun amacı: aykırı değer olarak yakaladığımız değerler yerine belirlediğimiz alt ve üslt limit
# değerlerini bir önceki fonksiyonu kullanark değiştir demiş olduk.
# değerlerini yerleştir demiş olacağız.

# Yukarıdaki fonksiyonu kısaca özetlemek gerekirse: Bu fonksiyon bir dataframe ve değişken ile çağrıldığında bir önceki
# fonksiyonu çağırıp hesaplamış olduğu üst ve alt limitleri karşısında yer alan değişkeneler atayacak.
# Daha sonra ilgili değişkendeki değerlerde üst sınırda olanlar varsa,bunların yerine üst limit değerini ata demiş olduk
# aynı şekilde eğer ilgili değişkendeki değerlerde eğer alt sınırdan küçük olan değeler varsa bunların yerine al limit
# değerini ata demiş olduk.
# Örneğin 360 gibi bir değer bulunduysa bu değeri 300 ile değişterecektir.



#########################
# Verinin Okunması
#########################

df_ = pd.read_excel("Miuul/CRM/online_retail_II.xlsx",
                    sheet_name="Year 2010-2011")
df = df_.copy() # burada veri setinin bir kopyasını aldık. amacımız veri seti bozulur veya başka bir hata yaparsak en
# baştan veriyi okutmak vs gibidurumlar ile uğralmamak ve verinin ilk halini koruma altına almak.

df.shape

df.info() # burada veri ile ilgili genel bilgilere bakıyoruz. sütun  isimleri, veri tipi gibi...
# bu kod ile şunu görddük: InvoıceDate değişkenin tipini de kontrol etmiş olduk. tipi datetime olmamış olsa idi tipini
# değiştirmek zorunda kalacaktık.

df.describe().T # verinin betimsel istatistiklerine bakıyoruz.

df.head()

df.isnull().sum() # her değişkenden toplam kaçartane eksik değer olduğunu tespit ettik.

#########################
# Veri Ön İşleme
#########################

df.dropna(inplace=True) # burada eksik değerleri veri setinden attık. kalıcı hale getirdik.

df = df[~df["Invoice"].str.contains("C", na=False)] # burada faturanın içersinde C değeri olmayanları seçip df
# değişkenine atadık. Böylelikle iade edilen işlemleri veri setinden uzaklaştırmış olduk.

df = df[df["Quantity"] > 0] # burada ürün adedinin sıfırdan büyük olanları seçip df değişkeninin ilgili sütununa atadık.
# df  içinde df yaparak zatan ilgili sütunda çalıştığımızı belirtmiş olduk. sıfırdan büyük seçmemizin sebebi ise iade
# işlemlerinden kaynaklı eksi değerlerden kurtulmaktı.

df = df[df["Price"] > 0] # burada da yukarıda olduğu gibi iadelerden kaynaklı eksi değerlerden kurtulmak amacımız. fiyat
# değişkeninin sıfırdan farklı olanları seçmiş olduk.

df.describe().T

# Bizim için öenmli olan iki tane değişken var. birisi price diğeri ise quantitiy değerleridir. çünkü biz bu değişkenler
# üzierinden hesaplamalar yapacağız. Bu hesaplamaları yapabilmek için aykırı değerlerden kurtulmamız gerek. Bunu da daha
# önce yukarıda tanımladığımız fonksiyonlar ile yapacğız.

replace_with_thresholds(df, "Quantity") # burada şunu dedik. bu değişkendeki aykırı değerleri bu değişkendeki eşik
# değerler ile değiştirdik. replace_with_thresholds fonksiyonu bize şunu diyor bana bir dataframe ver ve bu df
# içerissinden hangi değişkenin eşik değerini değiştireyim diyor.

replace_with_thresholds(df, "Price") # yukarıdaki ile aynı mantıkla çalışıyor.

df.describe().T

df["TotalPrice"] = df["Quantity"] * df["Price"] # burada df içersine yeni bir değişken oluşturduk. bu değişkene de satış
# adedi ile birim fiyatın çarpımını atadık.
# Burada neden TotalPrize isminde bir değişken oluşturma ihtiyacı hissettik: çünkü ileriki aşamalarda bir müşterinin
# fatura başına ne kadar odediğni hesaplamamız gerektiği zaman kullanacağız bu sütunu

df.head()

today_date = dt.datetime(2011, 12, 11) # analizleri yaptığımız günü belirliyoruz. burada ki tarih en son alış veriş
# yapılan tarihten 2 gün sonraki tarihtir.

#########################
# Lifetime Veri Yapısının Hazırlanması
#########################

# recency: Son satın alma üzerinden geçen zaman. Haftalık. (kullanıcı özelinde)
# T: Müşterinin yaşı. Haftalık. (analiz tarihinden ne kadar süre önce ilk satın alma yapılmış)
# frequency: tekrar eden toplam satın alma sayısı (frequency>1)
# monetary: satın alma başına ortalama kazanç


cltv_df = df.groupby('Customer ID').agg(
    {'InvoiceDate': [lambda InvoiceDate: (InvoiceDate.max() - InvoiceDate.min()).days,
                     lambda InvoiceDate: (today_date - InvoiceDate.min()).days],
     'Invoice': lambda Invoice: Invoice.nunique(),
     'TotalPrice': lambda TotalPrice: TotalPrice.sum()})
# Yukarıda ki kodda şunu yaptık:  cltv_df isminde bir değişken oluşturduk. bu değişkene ise df içerisinden Customer ID
# groupby alarak agg fonksiyonu ile yaptığımız işlemlerden elde ettiğimiz sonuçları atadık.

# InvoiceDate (Recency) için iki işlem yapmamız gerekli
# 1. işlem (lambda InvoiceDate: (InvoiceDate.max() - InvoiceDate.min()).days) recency hesaplamamız gerekli. buradan her
# bir müşteri için recency hesaplanmış olduk. Gün cinsinden
# 2. işlem (lambda InvoiceDate: (today_date - InvoiceDate.min()).days) müşterinin yaşının hesaplanmsıdır.

# Invoice (Frequency) değerinin hesaplması işlemi için
# lambda Invoice: Invoice.nunique() ifadesi ile her bir müşterinin eşiz kaç tane faturası var bunun bilgisini aldık.
#

# TotalPrize (monetary) değerinin hesaplanması için ise
# lambda TotalPrice: TotalPrice.sum() ifadesi ile toplam fiyatlarım toplamını al dedik.


cltv_df.columns = cltv_df.columns.droplevel(0) # okunabilirliği artımak adına bu değişkenlerin isimlerindeki sıfırıncı
# seviye silinir.

cltv_df.columns = ['recency', 'T', 'frequency', 'monetary'] # burada bu değişkenin sütun isimlerini kendi istediğimiz
# isimler ile isimlendirdik.

# Biz hesaplamaları yapabilmemiz ve modeli de uygulayabilmiz için bu değerlerin türlerini dönüştürmemiz gerekecek.
# Recency = haftalık
# Monetary = Ortalama
# T = haftalık

cltv_df["monetary"] = cltv_df["monetary"] / cltv_df["frequency"] # burada istemiş olduğumuz müşteri özelinde ortalama
# değeri hesapladık. işlem başına kazanç değerlerini hesaplamış olduk.

cltv_df.describe().T

cltv_df = cltv_df[(cltv_df['frequency'] > 1)] # burada frequency değerini 1 den büyük olacak şekilde seçtik.

cltv_df["recency"] = cltv_df["recency"] / 7 # burada recency değerini haftalık cinse çevirdik.

cltv_df["T"] = cltv_df["T"] / 7 # burada müşteri yaşını da haftalık cinse çevirdik.

cltv_df.describe().T
##############################################################
# 2. BG-NBD Modelinin Kurulması
##############################################################

bgf = BetaGeoFitter(penalizer_coef=0.001) # bir model nesnesi oluşturduk.

bgf.fit(cltv_df['frequency'],
        cltv_df['recency'],
        cltv_df['T'])
#
################################################################
# 1 hafta içinde en çok satın alma beklediğimiz 10 müşteri kimdir?
################################################################

bgf.conditional_expected_number_of_purchases_up_to_time(1,
                                                        cltv_df['frequency'],
                                                        cltv_df['recency'],
                                                        cltv_df['T']).sort_values(ascending=False).head(10)

# Yukarıda 1 hafta içerisinde ne çok satın alma yapacak 10 müşteri ve satın alma sayılarını tahmin ettik.
# Aşağıda ise uzun uzun yazmak yerine predict ile de yazdığımızda aynı çıktıyı verecektir. ama bu durum sadece bg/nbd
# modeli için gereçrlidir bu gamma gamma submodel için geçerli değildir.

bgf.predict(1,
            cltv_df['frequency'],
            cltv_df['recency'],
            cltv_df['T']).sort_values(ascending=False).head(10)


cltv_df["expected_purc_1_week"] = bgf.predict(1,
                                              cltv_df['frequency'],
                                              cltv_df['recency'],
                                              cltv_df['T'])
# Yukarıda ise bir hafta içerisinde beklediğimiz satın almaları hesaplayıp bunu da cltv_df veri setine yeni bir sütun
# olarak ekledik.

################################################################
# 1 ay içinde en çok satın alma beklediğimiz 10 müşteri kimdir?
################################################################

bgf.predict(4,
            cltv_df['frequency'],
            cltv_df['recency'],
            cltv_df['T']).sort_values(ascending=False).head(10)
# yukarıda 1 ay yerine 4 yazılmasının sebebi ise hafatalık cinsten çalıştığımız için bir ay 4 hafta olduğu için 4
# yazılmıştır.

cltv_df["expected_purc_1_month"] = bgf.predict(4,
                                               cltv_df['frequency'],
                                               cltv_df['recency'],
                                               cltv_df['T'])
# Yukarıda ise bir ay içerisinde beklediğimiz satın almaların listesini cltv_df veri setine yeni bir sütun olarak ekledik.

bgf.predict(4,
            cltv_df['frequency'],
            cltv_df['recency'],
            cltv_df['T']).sum()

################################################################
# 3 Ayda Tüm Şirketin Beklenen Satış Sayısı Nedir?
################################################################

bgf.predict(4 * 3,
            cltv_df['frequency'],
            cltv_df['recency'],
            cltv_df['T']).sum()
# Yukarıda 3 aylık için beklene  satın almaları hesaplarken bir ay 4 hafta 3 ay ise 4*3 hafta olacağı için bu şekilde
# yazıldı.

cltv_df["expected_purc_3_month"] = bgf.predict(4 * 3,
                                               cltv_df['frequency'],
                                               cltv_df['recency'],
                                               cltv_df['T'])
# Yukarıda ise 3 ayda beklenen satın almaları cltv_df veri setine yeni bir sütun olarak ekledik.
################################################################
# Tahmin Sonuçlarının Değerlendirilmesi
################################################################

plot_period_transactions(bgf) # burada yaptığımız tahminleri görsel hale getirdik.
plt.show(block=True)

##############################################################
# 3. GAMMA-GAMMA Modelinin Kurulması
##############################################################
# Hatırlatma => BG-NBD satın alma sayısını(purhase frequency) modelliyor. Gama-Gamma ise average profit(beklenen kar) i
# modelliyor.

ggf = GammaGammaFitter(penalizer_coef=0.01) # model nesenesi oluşturuldu.

ggf.fit(cltv_df['frequency'], cltv_df['monetary']) # model fit edildi

ggf.conditional_expected_average_profit(cltv_df['frequency'],
                                        cltv_df['monetary']).head(10)
# Yukarıdaki kod ile biz her bir müşteri için bekelen karı getirmiş oldu.

ggf.conditional_expected_average_profit(cltv_df['frequency'],
                                        cltv_df['monetary']).sort_values(ascending=False).head(10)

cltv_df["expected_average_profit"] = ggf.conditional_expected_average_profit(cltv_df['frequency'],
                                                                             cltv_df['monetary'])
# Yukarıda ki kod ile de her bir müşteri için beklene karı yeni bir sütun olarak cltv_df veri seti içersine attık.

cltv_df.sort_values("expected_average_profit", ascending=False).head(10) # burada şunu yaptık:
# her bir müşteri için beklene kara göre veri setini büyükten küçüğe doğru sırala dedik

##############################################################
# 4. BG-NBD ve GG modeli ile CLTV'nin hesaplanması.
##############################################################

cltv = ggf.customer_lifetime_value(bgf,
                                   cltv_df['frequency'],
                                   cltv_df['recency'],
                                   cltv_df['T'],
                                   cltv_df['monetary'],
                                   time=3,  # 3 aylık
                                   freq="W",  # T'nin frekans bilgisi.
                                   discount_rate=0.01)

# Yukarıda kodda ise şunu yaptık: koda beklediği verileri yazdık. hesaplanacağı zaman değerini sıklık cinsini weak w,
# ve ileride olurda indirim yaparsak diye indirim oranını girdik.
cltv.head()

cltv = cltv.reset_index()

cltv_final = cltv_df.merge(cltv, on="Customer ID", how="left") # burada daha önce oluştuduğumuz cltv_df veri seti ile
# en son oluşturduğumuz cltv veri seti merge ile birleştiriliyor. bu birleştirme işlemi ise custome ıd baz alınarak sol
# tarafta olacak şekilde birleştiriliyor.

cltv_final.sort_values(by="clv", ascending=False).head(10) # burada ise clv ye göre cltv_final veri setini büyükten
# küçüğe dopru sıraladık.

# Bilgi: customer_lifetime_value fonksiyonu return ettiği data frame deki isimlendirmeyi (clv) bu şekilde yapmıştır.
# sıkıntı yok yani
# Bilgi : BG/NBD modelinde Churn olmamış, dropout olmamış bir müşterinin recency değeri arttıkça monetary değeri artabilir.
##############################################################
# 5. CLTV'ye Göre Segmentlerin Oluşturulması
##############################################################

cltv_final

cltv_final["segment"] = pd.qcut(cltv_final["clv"], 4, labels=["D", "C", "B", "A"])

cltv_final.sort_values(by="clv", ascending=False).head(50)

cltv_final.groupby("segment").agg(
    {"count", "mean", "sum"})



##############################################################
# 6. Çalışmanın Fonksiyonlaştırılması
##############################################################

def create_cltv_p(dataframe, month=3):
    # 1. Veri Ön İşleme
    dataframe.dropna(inplace=True)
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]
    dataframe = dataframe[dataframe["Quantity"] > 0]
    dataframe = dataframe[dataframe["Price"] > 0]
    replace_with_thresholds(dataframe, "Quantity")
    replace_with_thresholds(dataframe, "Price")
    dataframe["TotalPrice"] = dataframe["Quantity"] * dataframe["Price"]
    today_date = dt.datetime(2011, 12, 11)

    cltv_df = dataframe.groupby('Customer ID').agg(
        {'InvoiceDate': [lambda InvoiceDate: (InvoiceDate.max() - InvoiceDate.min()).days,
                         lambda InvoiceDate: (today_date - InvoiceDate.min()).days],
         'Invoice': lambda Invoice: Invoice.nunique(),
         'TotalPrice': lambda TotalPrice: TotalPrice.sum()})

    cltv_df.columns = cltv_df.columns.droplevel(0)
    cltv_df.columns = ['recency', 'T', 'frequency', 'monetary']
    cltv_df["monetary"] = cltv_df["monetary"] / cltv_df["frequency"]
    cltv_df = cltv_df[(cltv_df['frequency'] > 1)]
    cltv_df["recency"] = cltv_df["recency"] / 7
    cltv_df["T"] = cltv_df["T"] / 7

    # 2. BG-NBD Modelinin Kurulması
    bgf = BetaGeoFitter(penalizer_coef=0.001)
    bgf.fit(cltv_df['frequency'],
            cltv_df['recency'],
            cltv_df['T'])

    cltv_df["expected_purc_1_week"] = bgf.predict(1,
                                                  cltv_df['frequency'],
                                                  cltv_df['recency'],
                                                  cltv_df['T'])

    cltv_df["expected_purc_1_month"] = bgf.predict(4,
                                                   cltv_df['frequency'],
                                                   cltv_df['recency'],
                                                   cltv_df['T'])

    cltv_df["expected_purc_3_month"] = bgf.predict(12,
                                                   cltv_df['frequency'],
                                                   cltv_df['recency'],
                                                   cltv_df['T'])

    # 3. GAMMA-GAMMA Modelinin Kurulması
    ggf = GammaGammaFitter(penalizer_coef=0.01)
    ggf.fit(cltv_df['frequency'], cltv_df['monetary'])
    cltv_df["expected_average_profit"] = ggf.conditional_expected_average_profit(cltv_df['frequency'],
                                                                                 cltv_df['monetary'])

    # 4. BG-NBD ve GG modeli ile CLTV'nin hesaplanması.
    cltv = ggf.customer_lifetime_value(bgf,
                                       cltv_df['frequency'],
                                       cltv_df['recency'],
                                       cltv_df['T'],
                                       cltv_df['monetary'],
                                       time=month,  # 3 aylık
                                       freq="W",  # T'nin frekans bilgisi.
                                       discount_rate=0.01)

    cltv = cltv.reset_index()
    cltv_final = cltv_df.merge(cltv, on="Customer ID", how="left")
    cltv_final["segment"] = pd.qcut(cltv_final["clv"], 4, labels=["D", "C", "B", "A"])

    return cltv_final


df = df_.copy()

cltv_final2 = create_cltv_p(df)

cltv_final2.to_csv("cltv_prediction.csv")













