1)Scraper.py içine tüm sitelerin linkleri eklenecek ve otomasyon yapılarak düzenli olarak veri çekilmesi sağlanacak. (Bitmedi)

2)hatbet ve meridianbet gibi dosyalar oluşacak (Bitmedi)

3)oddsmeridian.py ve oddshatbet.py gibi tüm siteler için sitenin içeriğine ve nasıl kodlandığına bağlı olarak veriyi çekmek adına kod yazılacak ve meridianbet.json, hatbet.json gibi dosyalar oluşmuş olacak. (Diğer sitelerden gelen tablo formatlarının oluşturduğum tablo formatıyla aynı olmasına dikkat edilmeli.) (Bitmedi)  (Şu scrape dosyalarının adı odds ile başlarsa script çalışır ve başka birşey yapmaya gerek kalmaz.  yani xbet isimli sitenin scraperi oddsxbet.py olsun)

4)Yapılması gerekenler aslında sadece scraperi yazmak ve scrape edilen datalardan maçlar için data json tablelarını çekmek için her siteye özgü oddsmeridian.py veya oddshatbet.py gibi dosyalar oluşacak.Oluşan tableların ve dosya isimlerinin benim oluşturduklarımla consistent olmasına dikkat edilmeli.
Scraper.py dışında hiçbir dosyanın içeriğiyle oynanmasına gerek yok.

5)Ana scraperi yazdıktan sonra runlamak için klasörün içine girip ./run.sh yazmak yeterli olacaktır.



EN İYİ PRACTİCE ANA SCRAPERİN İÇİNE SİTELERİ ÇEKMEK VE ANA SCRAPER DATALARI ÇEKTİKTEN SONRA PYTHON DOSYASI İÇİNDE ./run.sh scriptini çalıştırmak.
