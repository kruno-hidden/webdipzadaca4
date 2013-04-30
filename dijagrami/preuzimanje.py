from datetime import datetime
from random import randint
import urllib
import urllib2
import os

preuzmi = []
preuzmi.append('http://www.kupime.hr/grad/zagreb')
preuzmi.append('http://www.kupime.hr/grad/osijek')
preuzmi.append('http://www.kupime.hr/grad/zadar')
preuzmi.append('http://www.kupime.hr/grad/makarska')
preuzmi.append('http://www.kupime.hr/grad/split')
preuzmi.append('http://www.kupime.hr/grad/rijeka')
preuzmi.append('http://www.kupime.hr/grad/sibenik')
preuzmi.append('http://www.kupime.hr/grad/varazdin')

ponude = {}         #linkovi na ponude
id_ponude = 0
id_akcije = 0
kategorije = {}
kat_num = 1
prodavatelji = {}
prod_num = 1
gradovi = {}
gr_num = 1
ime_foldera = '/home/kruno/Desktop/automat/ponuda_' #za slike
broj_foldera = 1

ukupno_linkova = 0
trenutni_link = 1

def provjeri_oib(oib):
    a = 10
    for i in range(0,10):
        a = a + int(oib[i:i+1])
        a = a % 10
        if a == 0:
            a = 10
        a *= 2
        a = a % 11
                
    kontrolni = 11 - a
    if kontrolni == 10:
        kontrolni = 0
    return kontrolni == int(oib[10:11])

def izaberi_oib():
    i = ''
    while 1==1:        
        i = str(randint(10000,99999)) + str(randint(10000,99999)) + str(randint(0,9))
        if provjeri_oib(i):
            return i


def extract_url(url):
    #print "Ucitavam: " + url
    global ukupno_linkova
    link = urllib2.urlopen(url)
    dopusti = 0
    for red in link:
        if red.find('ndxmid_title')!=-1:
            dopusti = 1
            continue
        if dopusti==1:
            dopusti = 0
            value = "http://www.kupime.hr"+red.rstrip().split("\"")[1]
            key = value.split("/")[4]
            if not key in ponude:
                ponude[key] = value
                ukupno_linkova = ukupno_linkova+1

    link.close()    

def trazi_linkove():
    global ukupno_linkova
    for url in preuzmi:
        extract_url(url)
    print "UKUPNO LINKOVA: " + str(ukupno_linkova)

def ispis_linkove():
    for k,v in ponude.items():
        print v

def analiziraj_ponudu(url):
    global ukupno_linkova
    global trenutni_link
    naslov = ''         #1
    podnaslov = ''      #2
    vrijednost = ''     #3
    popust = ''         #4
    kategorija = ''     
    grad = ''               #jedna ponuda moze se odnositi na vise gradova
    desc_title = ''
    shortdesc_text = '' #5
    napomene = ''       #6
    desc_text = ''      #7
    karta_x = ''
    karta_y = ''
    poduzece_ime = ''   #8
    poduzece_adr = ''   #9
    poduzece_kont = ''  #10
    poduzece_info = ''  #11
    
    print str(trenutni_link) + "({}) : ".format(str(float(trenutni_link)/float(ukupno_linkova)*100)) + url
    trenutni_link = trenutni_link +1
    link = urllib2.urlopen(url)
    line = 0 #govori koja linija se ceka
    tip = 0  #govori sto se cita
    slike = []
    
    for red in link:
        if red.find('.jpg')!=-1:
            if red.find('ndxmain_img')!=-1:
                s = red.split('src=\"/')[1].strip().split(".axd?")[0]
                slike.append("http://www.kupime.hr/"+s)
            if red.find('<li')!=-1 and red.find('http')==-1:
                s = red.split("href=\"/")[1].strip().split("\"")[0]
                slike.append("http://www.kupime.hr/"+s)
        if red.find('ndxoffer_title')!=-1:
            line = -2
            tip = 1
        if line<0:
            line = line+1
            continue
        if tip==1:
            naslov = red.strip().split('!')[0]
            line = -1
            tip = 2
            continue
        if tip==2:
            podnaslov = red.strip().split('!')[0]
            if podnaslov.find('<')!=-1:
                podnaslov = podnaslov.split('<')[0];
            line = 0
            tip = 0
            continue
        
        if red.find('ndxprice_info')!=-1:
            line = -3
            tip = 3
            continue
        if tip==3:
            vrijednost = red.strip().split('<')[0]
            vrijednost = vrijednost.replace(",","")
            line = -3
            tip = 4
            continue

        if tip==4:
            popust = red.strip().split('%')[0]
            line = 0
            tip = 0
            continue

        if red.find('selected')!=-1:
            grad = red.strip().split('/')[2]
            kategorija = red.strip().split('/')[3]
            continue

        if red.find('desc_title')!=-1:
            desc_title = red.split('>')[1].split('<')[0].strip()
            continue
        
        if red.find('shortdesc_text')!=-1:
            shortdesc_text = '<ul>\n'
            tip = 5
            continue
        if tip==5:
            if red.find('</ul>')!=-1:
                shortdesc_text = shortdesc_text + '</ul>'
                tip = 0
            else:
                shortdesc_text = shortdesc_text + red.strip()          
            continue

        if red.find('Napomene')!=-1:
            line = -1
            tip = 6
            continue
        if tip==6:
            if red.find('</ul>')!=-1:
                napomene = napomene + '</ul>'
                tip = 7
            else:
                napomene = napomene + red.strip()
            continue

        if tip==7 and red.find('desc_text')!=-1:
            tip=71
            continue
        if tip==71:
            if red.find('location')!=-1:
                desc_text = desc_text[:-6]
                tip = 0
            else:
                desc_text = desc_text + red.strip()
            continue
        
        if red.find('var lat')!=-1:
            karta_x = red.split("=")[1].strip().split(";")[0]
            continue

        if red.find('var lang')!=-1:
            karta_y = red.split("=")[1].strip().split(";")[0]
            continue

        if red.find('company_info')!=-1:
            tip = 8
            continue
        if tip==8:
            poduzece_ime = red.split(">")[1].strip().split("<")[0]
            tip=9
            line = -1
            continue
        if tip==9:
            poduzece_adr = red.strip().split(">")[2].split("<")[0]
            tip = 10
            continue
        if tip==10:
            poduzece_kont = red.split(":")[1].strip().split("<")[0].replace("(","").replace(")","").replace(" ","")
            tip = 11
            line = -1
            continue
        if tip==11:
            poduzece_info = red.split("href=\"")[2].strip().split("\"")[0]
            tip = 0
            continue
    '''   
    print "Naslov: \t" + naslov
    print "Podnaslov: \t" + podnaslov
    print "Vrijednost: \t" + vrijednost
    print "Popust: \t" + popust
    print "Kategorija: \t" + kategorija
    print "Grad: \t" + grad
    print "desc_title: \t" + desc_title
    print "shortdesc_text: \t" + shortdesc_text
    print "napomene: \t" + napomene
    print "\ndesc_text: " + desc_text
    print "x: \t"  + karta_x
    print "y: \t" + karta_y
    print "ime: \t" + poduzece_ime
    print "adr: \t" + poduzece_adr
    print "kon: \t" + poduzece_kont
    print "info: \t" + poduzece_info
    '''
    
    #PREUZIMANJE SLINA
    global broj_foldera
    folder_name = ime_foldera + str(broj_foldera).zfill(5)
    broj_foldera = broj_foldera + 1
    os.makedirs(folder_name)
    i = 1
    for red in slike:
        path = folder_name + "/" + str(i).zfill(2) + ".jpg"
        urllib.urlretrieve(str(red), str(path))
        i = i+1

    #SQL
    #KATEGORIJE
    global kategorije
    global kat_num
    if not kategorija in kategorije:
        kategorije[kategorija] = kat_num        
        f = open('/home/kruno/Desktop/kategorije.sql', 'a')        
        insert = "INSERT INTO `kategorije`(`id`, `naziv`, `aktivna`) VALUES ( "
        insert = insert + "'{}', ".format(str(kategorije[kategorija]))
        insert = insert + "'{}', ".format(kategorija)
        insert = insert + "'{}'".format('1')
        insert = insert + " );\n"
        f.write(insert)
        f.close()
        kat_num = kat_num + 1

    #SQL
    #PRODAVATELJI
    global prodavatelji
    global prod_num
    if not poduzece_ime in prodavatelji:
        prodavatelji[poduzece_ime] = prod_num
        f = open('/home/kruno/Desktop/prodavatelji.sql', 'a')
        insert = "INSERT INTO `prodavatelji`(`id`, `id_korisnika`, `naziv`, `adresa`, `kontakt`, `info`, `oib`, `aktivan`) VALUES ( "        
        insert = insert + "'{}', ".format(str(prodavatelji[poduzece_ime]))
        insert = insert + "'{}', ".format(str(randint(1,5)))
        insert = insert + "'{}', ".format(poduzece_ime)
        insert = insert + "'{}', ".format(poduzece_adr)
        insert = insert + "'{}', ".format(poduzece_kont)
        insert = insert + "'{}', ".format(poduzece_info)
        insert = insert + "'{}', ".format(izaberi_oib())
        insert = insert + "'{}'".format('1')
        insert = insert + " );\n"
        f.write(insert)
        f.close()
        prod_num = prod_num + 1
        

    #SQL
    #PONUDE
    global id_ponude
    f = open('/home/kruno/Desktop/ponude.sql', 'a')
    insert = "INSERT INTO `ponude`(`id_prodavatelja`, `id_kategorije`, `naslov`, `podnaslov`, `cijena`, `opis_naslov`, `opis_kratki`, `opis`, `napomena`, `karta_x`, `karta_y`) VALUES ( "    
    insert = insert + "'{}', ".format(str(prodavatelji[poduzece_ime]))
    insert = insert + "'{}', ".format(str(kategorije[kategorija]))#treba provjeriti - kategorija
    insert = insert + "'{}', ".format(naslov)
    insert = insert + "'{}', ".format(podnaslov)
    insert = insert + "'{}', ".format(vrijednost)
    insert = insert + "'{}', ".format(desc_title)
    insert = insert + "'{}', ".format(shortdesc_text)
    insert = insert + "'{}', ".format(desc_text)
    insert = insert + "'{}', ".format(napomene)
    insert = insert + "'{}', ".format(karta_x)
    insert = insert + "'{}'".format(karta_y)
    insert = insert + " );\n"
    f.write(insert)
    f.close()
    id_ponude = id_ponude + 1

    #SQL
    #MJESTA
    global gradovi
    global gr_num
    if not grad in gradovi:
        gradovi[grad]=gr_num
        f = open('/home/kruno/Desktop/gradovi.sql', 'a')
        insert = "INSERT INTO `gradovi`(`id`, `ime`) VALUES ( "
        insert = insert + "'{}', ".format(str(gradovi[grad]))
        insert = insert + "'{}'".format(grad)
        insert = insert + " );\n";
        f.write(insert)
        f.close()
        gr_num = gr_num + 1

    #SQL
    #AKCIJE
    global id_akcije
    f = open('/home/kruno/Desktop/akcije.sql', 'a')
    insert = "INSERT INTO `akcije`(`id_ponude`, `popust`, `datum_pocetka`, `datum_zavrsetka`, `limit`, `istaknuto`) VALUES ( "    
    insert = insert + "'{}', ".format(id_ponude)
    insert = insert + "'{}', ".format(popust)
    insert = insert + "'{}', ".format(datetime.fromordinal(datetime.now().toordinal()+randint(1,3)).strftime("%Y-%m-%d %H:%M:%S")) 
    insert = insert + "'{}', ".format(datetime.fromordinal(datetime.now().toordinal()+randint(4,7)).strftime("%Y-%m-%d %H:%M:%S")) 
    insert = insert + "'{}', ".format(randint(3,10))
    insert = insert + "'{}'".format('0')
    insert = insert + " );\n"
    f.write(insert)
    f.close()
    id_akcije = id_akcije + 1

    #SQL
    #GRADOVI_AKCIJE
    f = open('/home/kruno/Desktop/gradovi_akcije.sql', 'a')
    insert = "INSERT INTO `gradovi_akcije`(`id_grada`, `id_akcije`) VALUES ( "
    insert = insert + "'{}', ".format(str(gradovi[grad]))
    insert = insert + "'{}'".format(id_akcije)
    insert = insert + " );\n"
    f.write(insert)
    f.close()


def korisnici():
    imena = ["Nikola", "Nika", "Karlo", "Mia", "Sara", "Filip", "Lara", "Mirjana", "Lucija", "Petra", "Dragica", "Fran", "Nada", "Luka", "Josip", "Mario", "Marija", "Dora", "Ljubica", "Marko", "Ema", "Lana", "Željko", "David", "Tomislav", "Ivan", "Marica", "Ivica", "Stjepan", "Ana", "Leon", "Ivana", "Petar", "Ante", "Kata", "Katarina"]
    prezimena = ["Božić", "Jukić", "Blažević", "Grgić", "Filipović", "Marković", "Kovač", "Marić", "Horvat", "Vidović", "Pavić", "Šimić", "Šarić", "Tomić", "Matić", "Babić", "Knežević", "Vuković", "Perić", "Kovačević", "Bošnjak", "Perković", "Kovačić", "Radić", "Petrović", "Lovrić", "Popović", "Pavlović", "Novak", "Jurić"]
    adrese = ["Maksimir", "Kaptol", "Dolac", "Gundulićeva ulica", "Cvjetni trg", "Trg bana Josipa Jelačića", "Trg žrtava fašizma", "Nova cesta", "Gornji grad", "Trg Petra Krešimira Četvrtog"]
    mjesta = ["Zagreb","Split","Rijeka","Osjek","Pula","Pazin","Poreč","Varaždin","Slavnosni Brod", "Dubrovnik"]
    pbr = ["10000","21000","51000","31000","52100","52000","52440","42000","35000", "20000"]
    #SQL
    #KORISNICI
    f = open('/home/kruno/Desktop/korisnici.sql', 'a')
    f2 = open('/home/kruno/Desktop/logovi.sql', 'a')
    for i in range (0,30):
        insert = "INSERT INTO `korisnici`(`id`, `ime`, `prezime`, `adresa`, `pbr`, `mjesto`, `telefon`, `email`, `oib`, `open_id`, `opomena`, `deaktiviran`, `zamrznut`, `blokiran`, `datum_registracije`, `email_potvrda`, `username`, `password`, `ovlasti`) VALUES ( "
        insert = insert + "'{}', ".format(str(i+1))
        insert = insert + "'{}', ".format(imena[i])
        insert = insert + "'{}', ".format(prezimena[i])
        insert = insert + "'{}', ".format(adrese[randint(0,9)] + " " + str(randint(1,100)))
        ind = randint(0,9)
        insert = insert + "'{}', ".format(pbr[ind])
        insert = insert + "'{}', ".format(mjesta[ind])
        tel = '0' + pbr[ind][0:2] + str(randint(100,999)) + str(randint(100,999))
        insert = insert + "'{}', ".format(tel)
        insert = insert + "'{}', ".format(imena[i].lower()+"@nekimail.com")
        insert = insert + "'{}', ".format(izaberi_oib())
        insert = insert + "'{}', ".format('0')
        insert = insert + "'{}', ".format('0')
        insert = insert + "'{}', ".format('0')
        insert = insert + "'{}', ".format('0')
        insert = insert + "'{}', ".format('0')
        insert = insert + "'{}', ".format(datetime.fromordinal(datetime.now().toordinal()+randint(0,7)).strftime("%Y-%m-%d %H:%M:%S"))
        insert = insert + "'{}', ".format('aktiviran')
        insert = insert + "'{}', ".format(imena[i].lower())
        insert = insert + "'{}', ".format('lozinka')
        insert = insert + "'{}'".format('1')
        insert = insert + " );\n"
        f.write(insert)
        insert = "INSERT INTO `logovi`(`id_korisnika`, `id_tip`, `kljuc`, `datum`) VALUES ( "
        insert = insert + "'{}', ".format('1')
        insert = insert + "'{}', ".format('1')
        insert = insert + "'{}', ".format(str(i+1))
        insert = insert + "'{}'".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        insert = insert + " );\n"
        f2.write(insert)
        insert = "INSERT INTO `logovi`(`id_korisnika`, `id_tip`, `kljuc`, `datum`) VALUES ( "
        insert = insert + "'{}', ".format('1')
        insert = insert + "'{}', ".format('3')
        insert = insert + "'{}', ".format(str(i+1))
        insert = insert + "'{}'".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        insert = insert + " );\n"
        f2.write(insert)
    f.close()
    f2.close()

def ostali_zapisi():
    #SQL
    #TIP_LOGA
    log_tip = []
    log_tip.append("Korisnik registriran");
    log_tip.append("Korisnik aktiviran putem Emaila");
    log_tip.append("Korisnik aktiviran od strane administratora");
    log_tip.append("Izmjena korisničkih podataka");
    log_tip.append("Prijava korisnika");
    log_tip.append("Opomena korisniku");
    log_tip.append("Zamrzavanje računa");
    log_tip.append("Odmrzavanje računa");
    log_tip.append("Blokada računa");
    log_tip.append("Deblokada računa");
    log_tip.append("Promjena razine ovlasti");
    log_tip.append("Pretplata na newsletter");
    log_tip.append("Ukinuta pretplata na newsletter");
    log_tip.append("Kategorija dodana moderatoru");
    log_tip.append("Kategorija oduzeta moderatoru");
    log_tip.append("Dodana nova kategorija");
    log_tip.append("Izmjena kategorije");
    log_tip.append("Dodaja novog proizvoda");
    log_tip.append("Izmjena proizvoda");
    log_tip.append("Akcija dodana");
    log_tip.append("Akcija promjenjena");
    log_tip.append("Dodan vaucher");
    log_tip.append("Izmjenjen vaucher");
    log_tip.append("Iskoristen vaucher");
    log_tip.append("Prodavatelj dodan");
    log_tip.append("Prodavatelj izmjenjen");
    log_tip.append("Prodavatelj uklonjen");
    log_tip.append("Transakcija uspjela");
    log_tip.append("Transakcija neuspejla");
    log_tip.append("Izmjena sistemskog vremena");
    f = open('/home/kruno/Desktop/log_tip.sql', 'a')
    for red in log_tip:
        f.write("INSERT INTO `log_tip`(`opis`) VALUES ( '{}' );\n".format(red))
    f.close()
    #SQL
    #OPOMENE
    f = open('/home/kruno/Desktop/opomene.sql', 'a')
    insert = "INSERT INTO `opomene`(`id_korisnika`, `id_moderatora`, `datum`, `opis`) VALUES ( "
    insert = insert + "'{}', ".format('2')
    insert = insert + "'{}', ".format('1')
    insert = insert + "'{}', ".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    insert = insert + "'{}'".format('Izriće se opomena radi testiranja sustava')
    insert = insert + " );\n"
    f.write(insert)
    f.close()

    #SQL
    #MODERATORI
    f = open('/home/kruno/Desktop/moderatori.sql', 'a')
    insert = "INSERT INTO `moderatori`(`id_korisnika`, `id_kategorije`, `aktivan`) VALUES ( "
    insert = insert + "'{}', ".format('1')
    insert = insert + "'{}', ".format('1')
    insert = insert + "'{}'".format('1')
    insert = insert + " );\n"
    f.write(insert)
    insert = "INSERT INTO `moderatori`(`id_korisnika`, `id_kategorije`, `aktivan`) VALUES ( "
    insert = insert + "'{}', ".format('1')
    insert = insert + "'{}', ".format('2')
    insert = insert + "'{}'".format('1')
    insert = insert + " );\n"
    f.write(insert)
    f.close()

    #SQL
    #NEWSLETTER
    f = open('/home/kruno/Desktop/newsletter.sql', 'a')
    insert = "INSERT INTO `newsletter`(`id_korisnika`, `aktivan`) VALUES ( "
    insert = insert + "'{}', ".format('25')
    insert = insert + "'{}'".format('1')
    insert = insert + " );\n"
    f.write(insert)
    insert = "INSERT INTO `newsletter`(`id_korisnika`, `aktivan`) VALUES ( "
    insert = insert + "'{}', ".format('26')
    insert = insert + "'{}'".format('1')
    insert = insert + " );\n"
    f.write(insert)
    insert = "INSERT INTO `newsletter`(`id_korisnika`, `aktivan`) VALUES ( "
    insert = insert + "'{}', ".format('27')
    insert = insert + "'{}'".format('1')
    insert = insert + " );\n"
    f.write(insert)
    f.close()
    
    #SQL
    #KOSARICA
    f = open('/home/kruno/Desktop/kosarica.sql', 'a')
    insert = "INSERT INTO `kosarica`(`id_korisnika`, `id_akcije`, `operacija`, `datum`) VALUES ( "
    insert = insert + "'{}', ".format('1')
    insert = insert + "'{}', ".format('1')
    insert = insert + "'{}', ".format('0') #0dodano 1izbaceno 2kupljeno
    insert = insert + "'{}'".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    insert = insert + " );\n"
    f.write(insert)
    insert = "INSERT INTO `kosarica`(`id_korisnika`, `id_akcije`, `operacija`, `datum`) VALUES ( "
    insert = insert + "'{}', ".format('1')
    insert = insert + "'{}', ".format('1')
    insert = insert + "'{}', ".format('1') #0dodano 1izbaceno 2kupljeno
    insert = insert + "'{}'".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    insert = insert + " );\n"
    f.write(insert)
    insert = "INSERT INTO `kosarica`(`id_korisnika`, `id_akcije`, `operacija`, `datum`) VALUES ( "
    insert = insert + "'{}', ".format('1')
    insert = insert + "'{}', ".format('2')
    insert = insert + "'{}', ".format('0') #0dodano 1izbaceno 2kupljeno
    insert = insert + "'{}'".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    insert = insert + " );\n"
    f.write(insert)
    insert = "INSERT INTO `kosarica`(`id_korisnika`, `id_akcije`, `operacija`, `datum`) VALUES ( "
    insert = insert + "'{}', ".format('1')
    insert = insert + "'{}', ".format('2')
    insert = insert + "'{}', ".format('2') #0dodano 1izbaceno 2kupljeno
    insert = insert + "'{}'".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    insert = insert + " );\n"
    f.write(insert)
    f.close()

    #SQL
    #RACUNI
    f = open('/home/kruno/Desktop/racuni.sql', 'a')
    insert = "INSERT INTO `racuni`(`id_korisnika`, `datum`, `placeno`) VALUES ( "
    insert = insert + "'{}', ".format('1')
    insert = insert + "'{}', ".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")).format('1')
    insert = insert + "'{}'".format(1)
    insert = insert + " );\n"
    f.write(insert)
    f.close()

    #SQL
    #RACUNI_AKCIJE
    f = open('/home/kruno/Desktop/racuni_akcije.sql', 'a')
    insert = "INSERT INTO `racuni_akcije`(`id_racuna`, `id_akcije`, `kolicina`) VALUES ( "
    insert = insert + "'{}', ".format('1')
    insert = insert + "'{}', ".format('2')
    insert = insert + "'{}'".format(1)
    insert = insert + " );\n"
    f.write(insert)
    f.close()    
    
    #SQL
    #DODATNI
    f = open('/home/kruno/Desktop/dodatno.sql', 'a')
    #- promoviraj korisnika 1 u administratora
    insert = "UPDATE  `korisnici` SET  `ovlasti` =  '3' WHERE  `korisnici`.`id` =1;\n"
    f.write(insert)
    #- log da je user 1 adin
    insert = "INSERT INTO `logovi`(`id_korisnika`, `id_tip`, `kljuc`, `datum`) VALUES ( "
    insert = insert + "'{}', ".format('1')
    insert = insert + "'{}', ".format('11')
    insert = insert + "'{}', ".format('1')
    insert = insert + "'{}'".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    insert = insert + " );\n"
    f.write(insert)
    #- updejtadi usera 2 i staviti mu opomenu
    insert = "UPDATE  `WebDiP2012_013`.`korisnici` SET  `opomena` =  '1' WHERE  `korisnici`.`id` =2;\n"
    f.write(insert)
    #- log da je user 1 dodan kao moderator kategorije 1
    insert = "INSERT INTO `logovi`(`id_korisnika`, `id_tip`, `kljuc`, `datum`) VALUES ( "
    insert = insert + "'{}', ".format('1')
    insert = insert + "'{}', ".format('14')
    insert = insert + "'{}', ".format('1')
    insert = insert + "'{}'".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    insert = insert + " );\n"
    f.write(insert)
    #- log da je user 1 dodan kao moderator kategorije 2
    insert = "INSERT INTO `logovi`(`id_korisnika`, `id_tip`, `kljuc`, `datum`) VALUES ( "
    insert = insert + "'{}', ".format('1')
    insert = insert + "'{}', ".format('14')
    insert = insert + "'{}', ".format('2')
    insert = insert + "'{}'".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    insert = insert + " );\n"
    f.write(insert)
    #- korisnik 25 se pretpaltio na newsletter
    insert = "INSERT INTO `logovi`(`id_korisnika`, `id_tip`, `kljuc`, `datum`) VALUES ( "
    insert = insert + "'{}', ".format('25')
    insert = insert + "'{}', ".format('12')
    insert = insert + "'{}', ".format('1')
    insert = insert + "'{}'".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    insert = insert + " );\n"
    f.write(insert)
    #- korisnik 26 se pretpaltio na newsletter
    insert = "INSERT INTO `logovi`(`id_korisnika`, `id_tip`, `kljuc`, `datum`) VALUES ( "
    insert = insert + "'{}', ".format('26')
    insert = insert + "'{}', ".format('12')
    insert = insert + "'{}', ".format('1')
    insert = insert + "'{}'".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    insert = insert + " );\n"
    f.write(insert)
    #- korisnik 27 se pretpaltio na newsletter
    insert = "INSERT INTO `logovi`(`id_korisnika`, `id_tip`, `kljuc`, `datum`) VALUES ( "
    insert = insert + "'{}', ".format('27')
    insert = insert + "'{}', ".format('12')
    insert = insert + "'{}', ".format('1')
    insert = insert + "'{}'".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    insert = insert + " );\n"
    f.write(insert)
    #-log transakcija korisnika 1 računa 1 uspješna
    insert = "INSERT INTO `logovi`(`id_korisnika`, `id_tip`, `kljuc`, `datum`) VALUES ( "
    insert = insert + "'{}', ".format('1')
    insert = insert + "'{}', ".format('28')
    insert = insert + "'{}', ".format('1')
    insert = insert + "'{}'".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    insert = insert + " );\n"
    f.write(insert)
    f.close()

def spoji():
    datoteke = ['log_tip.sql','korisnici.sql','kategorije.sql','prodavatelji.sql','ponude.sql','gradovi.sql','akcije.sql','gradovi_akcije.sql', 'logovi.sql', 'opomene.sql', 'moderatori.sql', 'newsletter.sql', 'kosarica.sql', 'racuni.sql', 'racuni_akcije.sql', 'dodatno.sql']    
    f = open('/home/kruno/Desktop/kupime.sql', 'w')
    for dat in datoteke:
        o = open('/home/kruno/Desktop/'+dat, 'r')
        f.write('--\n-- {}\n--\n\n'.format(dat))
        for red in o:
            f.write(red)
        f.write('\n\n')
        o.close()
        os.remove('/home/kruno/Desktop/'+dat)
    f.close()

#main

print datetime.now()
trazi_linkove()
#ispis_linkove()
for k,v in ponude.items():
    analiziraj_ponudu(v)

korisnici()
ostali_zapisi()
spoji()
'''
analiziraj_ponudu('http://www.kupime.hr/ponuda/kompletan-ginekoloski-pregled/4793');
analiziraj_ponudu('http://www.kupime.hr/ponuda/dovedite-se-do-atomske-kondicije-i-eksplozivnosti-uz-insanity-workout/4765')
analiziraj_ponudu('http://www.kupime.hr/ponuda/kazalisna-predstava-diplomac-u-komediji/4792')
analiziraj_ponudu('http://www.kupime.hr/ponuda/svijet-wellness-uzitaka/4843')
'''

print datetime.now()
print "--- KRAJ ---"
