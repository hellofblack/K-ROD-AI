# EĞİTİM HAZIRLIĞI
Eğitim için Darknet kullandım (https://github.com/AlexeyAB/darknet) ve seçtiğim algoritma da yolov4-tiny oldu.Bunu seçmemdeki amaç pi den tam performans ve verim alabilmek. 

Eğitim için gerekli olan verileri de OIDv4(https://github.com/EscVM/OIDv4_ToolKit) üzerinden toplu halde çekip, çektiğim fotografları ayıklayıp data seti oluşturdum.

İlk olarak çalışma alanımızı seçmekle başladım ben GOOGLE Colab kullanmayı tercih ettim. Sonra bir mail açıp drive ı colab e bağladım ve drive a OIDv4 tool'unu clone ederek krulumuna başladım.

---> kurulum aşaması şöyle olmakta;


     !git clone https://github.com/EscVM/OIDv4_ToolKit.git  (drive a clone etme işlemi)
     !pip3 install -r requirements.txt  (txt içerisindeki kütüphanelerin kısa kurulumu) 
     !python3 main.py downloader --classes <istediğiniz nesneler(ingilizce)> --type_csv train --limit <istediğiniz miktar(1 nesne için)>
     
Burada label dosyalarını eğitim için düzenlememiz lazım bunun için de classes.txt de istediğimiz sırada(!) alt alta yazmamız gerek.
     
     örnek:
     Tree
     Person
     Street light
     
Yukarıdaki örnekte label dosyalarında Tree yerine 0 Person yerine 1 yazılacaktır. Bu sıralamaya mutlaka dikkat etmemiz gerekli çünkü kod satırında bu sıra ile yazmamız gerekecek. Classes dosyasına yazdıktan sonra sırayı aşadaki kod satırını çalıştırarak etiketleri bize lazım olan biçime getirdik.     
     
     !python3 convert_annotations
     
     
Daha sonrasında tüm dosyaları düzenli bir şekilde adlandırma uyguladım.(örneğin: 1 den 1000 e kadar).
Bunu yaparken yine bir koddan yararlandım.(yukarıdan ulaşabilirsiniz.)

Daha sonrasında data dosyasını oluşturmaya başladım (Darknet için). Öncelikle CFG dosyasını düzenledim. Darknet dosyasında bulunna cfg dosyaları arasından bulabilirsiniz ben oradan aldım.
      
      
      batch=64
      subdivisions=16

      max_batches = 20000
      policy=steps
      steps=16000,18000
      
-->  Değerleri şu şekilde ayarladım.       
Max_batches= class sayısı x 2.000
steps = (max_batches.80)/100 , (max_batches.90)/100 

       filters=45 ((class + 5)*3)
       activation=linear



       [yolo]
       mask = 3,4,5
       anchors = 10,14,  23,27,  37,58,  81,82,  135,169,  344,319
       classes=10  (kendi class sayınız)
       


MAKEFİLE da ise şu ayarları yaptım:

         GPU=1
         CUDNN=1
         CUDNN_HALF=0
         OPENCV=1  
  
ayarlamalardan sonra darknet dosyası içerisinde bir adet backup dosyası açıp bıraktım.

Data setini oluşturmaya başlarken ilk önce bir adet boş bir dosya açtım adına da spot_data dedim. Daha sonrasında topladığımız fotograf ve ekiletlerin hepsini images adında bir dosya açarak içine attım. Sonra etiketler için ayrı bir dosya açarak adını labels koydum. Bu dosyaya etiketkeri kopyaladım. 2 Adet farklı uzantıya sahip dosyalar oluşturdum. spot.data ve spor.names 



--> SPOT.DATA
Burada bize lazım olacak olan data dosyalarının ve class sayısının bilgisi ve konumları yazmakta.Kendinize uygun şekilde bilgileri düzenlemeniz gerekli(!)

    classes=10
    train=/content/drive/MyDrive/darknet/spot_data/training.txt
    testing=/content/drive/MyDrive/darknet/spot_data/testing.txt
    names=/content/drive/MyDrive/darknet/spot_data/spot.names
    backup=/content/drive/MyDrive/darknet/backup
    
--> SPOT.NAMES  
Burada nesnelerin classes.txt deki konumları yazmakta.Bu çok önemli bir işlem çünkü label dosyasında 0 bizim için Tree anlamına gelmekteydi ve biz burada ilk satıra (index numaralarına göre ilerlemekte) Tree yazmak zorundayız. Etiketler ingilizce olabilir biz eğitimi yaparken burada hangi index değeri için hangi çıktıyı vericeğini aslında söylemekteyiz bu yüzden ben türkçe adları ile bu öğrenimi gerçekleştirdim.



--> TRAINING VE TESTING DOSYALARI

 Ek olarak da training.txt ve testing.txt olmak üzere 2 adet daha dosya oluşturdum. Bunları olauşturma sebebim eğitim de öğrenmesi ve bu öğrendiklerini test etmesi için kullanacağı fotograf konumlarını söylemekti.
 Bu konumları tek tek elle yazmak yerine yukarıda vereceğim kod sayfası ile kolayca yapabilirsiniz. Bu konumların %20 si test %80 i train için kullanılmalı.
 
 örnek konum;
 
     /content/drive/MyDrive/darknet/spot_data/images/1.jpg
     
En son yolov4-tiny için uygun olan conv dosyasını da darknet dosyasına atıyoruz.
Bu işlemler bittikten sonra eğitim için herşey hazır oluyor.

# EĞİTİM AŞAMASI
öncelikle sistemimiz COLAB ise çalışma zamanımızı GPU olarak ayarlıyoruz.

daha sonrasında sırası ile bu kodları çalıştırdım.
     
     %cat /etc/lsb-release                          --> sistem durumu
     !apt-get update                                --> sistem güncelleştirme
     !sudo apt install dos2unix                     --> dos2unix kurulumu
     !find . -type f -print0 | xargs -0 dos2unix    --> dos2unix formatına dönüştürme
     !chmod +x /content/drive/MyDrive/darknet       --> darknet dosyasına çalıştırma yetkisi
     !make                                          --> makefile ayarlarını yaptırmak
     !./darknet detector train /content/drive/MyDrive/darknet/spot_data/spot.data yolov4-tiny.cfg yolov4-tiny.conv.29 -mAP -dont_show    --> eğitim
     
     
Bu işlemler sırasıyla uyguladığımda eğitim işlemini başarılı bir şekilde başlatmış oldum. 100. iterasyondan sonra chart grafiği gelecek ve bu grafikte zaman, yanılma payı gibi değerler gösterecek. Dosyayı drive üzerinden çalıştırdığımız için hiç bir veri kaybı olmadan işlem devam edecek. Herhangi bir hata veya GPU atılması sonucunda dosyalar silinmeden kalacaktır. 

Tavsiyem çok büyük eğitimleri buradan yapmak yerine iyi bir bilgisayarda yapmanız daha verimli olacaktır.

https://youtu.be/DjO9UtSON6U  bu videodaki aşamaları takip ederek yapabilirsiniz.


Proje için düzenlemiş olduğum kod yukarıda k-rod.py dosyasından ulaşabilirsiniz.
