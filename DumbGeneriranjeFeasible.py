import random
import numpy as np
import pandas as pd


file = "instanca1.txt"

with open(file, "r") as infile:
    nj = infile.readlines()

lj = []
for i in nj[:]:
    lj.append(i.split())

broj_vozila = float(lj[0][0])
broj_traka = float(lj[1][0])

print(broj_vozila)
print(broj_traka)

duljina_vozila = np.array(lj[3], dtype = float)
duljina_vozila


serija_vozila = np.array(lj[5], dtype = int)
serija_vozila


ogranicenja_trake = np.array(lj[7:7+int(broj_vozila)], dtype = int)
ogranicenja_trake



ogranicenja_trake.shape


assert ogranicenja_trake.shape[0] == broj_vozila
assert ogranicenja_trake.shape[1] == broj_traka



duljina_trake =  np.array(lj[7+int(broj_vozila)+1], dtype = float)
duljina_trake



vrijeme_izlaska = np.array(lj[7+int(broj_vozila)+3], dtype = int)
vrijeme_izlaska



tip_rasporeda = np.array(lj[7+int(broj_vozila)+5], dtype = int)
tip_rasporeda



ogranicenja = lj[7+int(broj_vozila)+5+2:]
ogranicenja



blokirane_trake = []

for lista in ogranicenja:
    # preskoci prvi element, tj id prve trake
    for i in range(1,len(lista)):
        blokirane_trake.append(int(lista[i]))
blokirane_trake        
        


# In[16]:


vozilo = {}

for key1 in range(0, int(broj_vozila)):
    # jer id od 1 ide..
    vozilo[key1+1] = {"duljina": duljina_vozila[key1], "serija": serija_vozila[key1], "izlazak": vrijeme_izlaska[key1], "raspored":tip_rasporeda[key1]}


# In[17]:


traka = {}

for key1 in range(0, int(broj_traka)):
    # jer id od 1 ide..
    traka[key1+1] = {"duljina": duljina_trake[key1], 
                     "blokirana_od": [], 
                     "blokira":[],
                     "ogranicenje": ogranicenja_trake [:, key1]} # 0.element je boolean jeli traka dopusta vozilo 1 parkiranje}
    


# In[18]:


# za svaku listu citaj prvi element i update traka

for lista in ogranicenja:
    
    # prvi element naznacuje id trake, ostali elementi blokirane trake
    # za svaku blokiranu stavi koja ju blokira
    for id_blokirane in lista[1:]:
        traka[int(id_blokirane)]["blokirana_od"].append(lista[0])


# In[19]:


for lista in ogranicenja:
    
    # prvi element naznacuje id trake
    for id_blokirane in lista[1:]:
        traka[int(lista[0])]["blokira"].append(int(id_blokirane))


# In[20]:


with open("instanca1rj.txt", "r") as infile:
    primjer_rjesenja = []
    for i in infile.readlines():
        primjer_rjesenja.append(i.split())
primjer_rjesenja  


# In[21]:


traka[22]


# # Objective kao jedna funkcija

# In[22]:


uk_kapacitet_svih_traka = np.sum(duljina_trake)
uk_duljina_svih_vozila = np.sum(duljina_vozila)


# In[23]:


def nagrada_penal(v1, v2):
    vr = abs(v1-v2)
    if vr >= 10 and vr <= 20:
        return 15
    if vr > 20:
        return 10
    if vr < 10:
        return -4*(10-vr)


# In[24]:


# ulazi rjesenje i dict vozila, trake?

# otprije trebi biti definirana: uk_kapacitet_svih_traka, uk_duljina_svih_vozila (f3), broj_vozila (g1)

def evaluation_function(rjesenje):
    
    broj_traka = len(rjesenje)
    
    #f2
    broj_koristenih_traka = 0
    
    #f3
    iskoristeni_kapacitet = 0
    ukupni_koristeni_kapacitet = 0
    
    #f1
    razlika_serija = 0
    serija = 0 # OPREZ ,PRETPOSTAVKA DA NEMA NULTE SERIJE!!!
    
    #g1
    br_isti_raspored = 0
    
    #g2
    g2 = -1 # jer sam brojil prvu traku..
    tmp_prvi_id = -9999
    tmp_zadnji_id = -9999 
    
    #g3
    n_p_uk = 0
    br_parova = 0
    
    # za svaku TRAKU u rjesenju (po poziciji, i je list index) ''''''''''''''
    for i in range(broj_traka):
        
        # ako je koristena traka, tj nije prazna
        if rjesenje[i] != []:
            
            # F2 ********
            broj_koristenih_traka += 1
            
            # G2 ********
            # id prvog vozila u trenutnoj traci
            vozilo_prvo_id = int(rjesenje[i][0])

            # id zadnjeg vozila u trenutnoj traci
            vozilo_zadnje_id = int(rjesenje[i][-1])
        
            # postavi inicijalne id-ove vozila
            if tmp_prvi_id == -9999:
                tmp_prvi_id = vozilo_prvo_id
                tmp_zadnji_id = vozilo_zadnje_id 

            if vozilo[vozilo_prvo_id]["raspored"] == vozilo[tmp_zadnji_id]["raspored"]:
                g2 += 1
                tmp_prvi_id = vozilo_prvo_id
                tmp_zadnji_id = vozilo_zadnje_id   
            else:
                tmp_prvi_id = vozilo_prvo_id
                tmp_zadnji_id = vozilo_zadnje_id   

                    
            # F1 ********
            # NE PROVJERAVA  OGRANICENJE DA U TRACI ISTA SERIJA VOZILA
            # ako je prva traka, odredi inicijalnu seriju
            if serija == 0:
                serija = vozilo[int(rjesenje[i][0])]["serija"]
            else:
                # odredi seriju prvog vozila u svakoj traci
                serija2 = vozilo[int(rjesenje[i][0])]["serija"]
                
                # ukoliko se serije iz prosle i trenutne trake ne slazu
                if serija2 != serija:
                    razlika_serija += 1
                    serija = serija2
                    
            # G3
            # ako je duljina trake veca od 2 elemenata treba iterirati po njima
            if len(rjesenje[i]) > 2:

                tmp_v = -9999
                # nagrada/penal po traci
                n_p_traka = 0
                  
            tmp_raspored = -9999 # za g1
            
            # za svako vozilo u traci ''''''''''''''''''''''''''''''''''''''''''
            for vozilo_id in rjesenje[i]:
                
                # F3 ********
                iskoristeni_kapacitet += vozilo[int(vozilo_id)]["duljina"]
                
                # G1 ********
                # odredi raspored prvog vozila u traci i spremi za usporedbu
                if tmp_raspored == -9999:
                    tmp_raspored = vozilo[int(vozilo_id)]["raspored"]
                else:
                    # raspored sljedeceg vozila u istoj traci
                    raspored = vozilo[int(vozilo_id)]["raspored"]

                    if tmp_raspored == raspored:
                        br_isti_raspored += 1
                    else:
                        tmp_raspored = raspored
                        
                # G3 *********
                if len(rjesenje[i]) > 2:
                    if tmp_v == -9999:
                        tmp_v = vozilo[int(vozilo_id)]["izlazak"]
                    else:     
                        vrijeme = vozilo[int(vozilo_id)]["izlazak"]
                        n_p_traka += nagrada_penal(tmp_v, vrijeme)
                        br_parova += 1
                        tmp_v = vrijeme

            # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
            # G3
            if len(rjesenje[i]) == 2:
                id1 = int(rjesenje[i][0])
                id2 = int(rjesenje[i][1])
            
                v1 = vozilo[id1]["izlazak"]
                v2 = vozilo[id2]["izlazak"]

                n_p_traka_2 = nagrada_penal(v1, v2)
                n_p_uk += n_p_traka_2
                br_parova += 1
                
            if len(rjesenje[i]) > 2:                
                n_p_uk += n_p_traka # g3
            
            # ako je duljina trake veca od 2 dodaj razmak 0.5 izmedu vozila za (br_vozila -1)*razmak
            if len(rjesenje[i]) >= 2:
                iskoristeni_kapacitet += (len(rjesenje[i]) -1)*0.5
                
            # ukupni kapacitet svih koristenih traka
            ukupni_koristeni_kapacitet += traka[i+1]["duljina"]
            
            
    F1 = (razlika_serija)/(broj_koristenih_traka-1)
    F2 = broj_koristenih_traka/len(rjesenje) # tu sam mogel broj_traka
    F3 = (ukupni_koristeni_kapacitet - iskoristeni_kapacitet)/(uk_kapacitet_svih_traka-uk_duljina_svih_vozila)
    
    G1 = br_isti_raspored/(broj_vozila-broj_koristenih_traka)
    G2 = g2/(broj_koristenih_traka-1)
    G3 = n_p_uk/(15*br_parova)
    
    g_uk = G1+G2+G3
    f_uk = F1+F2+F3
    
    return F1, F2, F3, G1, G2, G3, g_uk/f_uk
    


# In[25]:


evaluation_function(primjer_rjesenja)


# # DUMB Feasible

# ### restart

# In[26]:


# id traka od 0 do broj traka-1, idx
njnj = {"serija_po_trakama": np.zeros(int(broj_traka)),
        "zadnje_vrijeme_izlaska": np.zeros(int(broj_traka)),
        "vozila_po_trakama":[[] for i in range(int(broj_traka))],
        "dostupan_kapacitet":duljina_trake.copy()}
njnj


# In[27]:


sorted_by_izlazak = sorted(vozilo.items(), key=lambda kv: kv[1]["izlazak"])


# ### initial solution
# 
# nekad 48, umjesto 49 vozila parkirano...

# In[ ]:





# In[28]:


# while nisu iskoristena sva vozila


# izgleda da su ove for petlje redundantne
    
# za svako vozilo prema vremenu izlaska
for vozilo_el in sorted_by_izlazak:
    vozilo_id = vozilo_el[0] # uzmi id vozila iz tuple

    
    trake = list(range(int(broj_traka)))
    random.shuffle(trake)
    
    # za svaku traku
    for i in trake:
        # ako nije blokirana
        traka_id = i+1
        if traka_id not in blokirane_trake:


            # nadji prvu koja nema ogranicenja za vozilo
            if traka[traka_id]["ogranicenje"][vozilo_id-1]:

                # ako kapacitet trake veci od duljine vozila, dopusti parkiranje
                if njnj["dostupan_kapacitet"][i] > vozilo[vozilo_id]["duljina"]:

                    # ako se parkira prvo vozilo u traku, ne umanji kapacitet za 0.5 
                    if njnj["serija_po_trakama"][i] == 0:


                        # umanji kapacitet za duljinu vozila
                        njnj["dostupan_kapacitet"][i] -= vozilo[vozilo_id]["duljina"]
                        # dodaj vozilo u traku
                        njnj["vozila_po_trakama"][i].append(vozilo_id)
                        # stavi seriju cijele trake onog vozila koje prvo parkirano
                        njnj["serija_po_trakama"][i] = vozilo[vozilo_id]["serija"]   
                        # postavi zadnje vrijeme izlaska trake na izlazak zadgnje vozila
                        njnj["zadnje_vrijeme_izlaska"][i] = vozilo[vozilo_id]["izlazak"]
                        

                        ogranicenja_trake[vozilo_id-1, :] = 0

                        break

                        #traka[traka_id]["ogranicenje"][vozilo_id-1] = 0

                    # ako je serija trake jednaka seriji vozila
                    elif njnj["serija_po_trakama"][i] == vozilo[vozilo_id]["serija"]:  
                        if njnj["zadnje_vrijeme_izlaska"][i] < vozilo[vozilo_id]["izlazak"]:

                            # dodaj vozilo u traku
                            njnj["vozila_po_trakama"][i].append(vozilo_id)
                            # umanji kapacitet za duljinu vozila + 0.5
                            njnj["dostupan_kapacitet"][i] -= vozilo[vozilo_id]["duljina"] + 0.5
                            # postavi zadnje vrijeme izlaska trake na izlazak zadgnje vozila
                            njnj["zadnje_vrijeme_izlaska"][i] = vozilo[vozilo_id]["izlazak"]
                            
                            # ograniciti postavljanje vozila u sve ostale trake
                            ogranicenja_trake[vozilo_id-1, :] = 0
                            break
                            #traka[traka_id]["ogranicenje"][vozilo_id-1] = 0
                    # vozilo je u nekoj traci, na ostale trake postavi ogranicenje 

print(njnj["vozila_po_trakama"])

# izgleda da su ove for petlje redundantne
    
for vozilo_el in sorted_by_izlazak:
    vozilo_id = vozilo_el[0] # uzmi id vozila iz tuple

    trake = list(range(int(broj_traka)))
    random.shuffle(trake)
    
    # za svaku traku
    for i in trake:

        traka_id = i+1
            # nadji prvu koja nema ogranicenja za vozilo
        if traka[traka_id]["ogranicenje"][vozilo_id-1]:

            # ako kapacitet trake veci od duljine vozila, dopusti parkiranje
            if njnj["dostupan_kapacitet"][i] > vozilo[vozilo_id]["duljina"]:

                # ako se parkira prvo vozilo u traku, ne umanji kapacitet za 0.5 *********************''''''''''''''''''''
                if njnj["serija_po_trakama"][i] == 0:

                    
                    najkasniji_izlazak_blokirajucih = 0
                    for blokirajuce_tr in traka[traka_id]["blokirana_od"]:
                        
                        if njnj["zadnje_vrijeme_izlaska"][int(blokirajuce_tr)-1] > najkasniji_izlazak_blokirajucih:
                            najkasniji_izlazak_blokirajucih = njnj["zadnje_vrijeme_izlaska"][int(blokirajuce_tr)-1]
                    
                    # vozilo koje ulazi u traku mora imati izlazak nakon izlaska vozila u traci koja ju blokira
                    if vozilo[vozilo_id]["izlazak"] > najkasniji_izlazak_blokirajucih:
                        
                    # i mora imati izlazak prije svih blokiranih traka!
                    # ako stavljam vozila u blokirajucu traku
                    
                        najraniji_izlazak_blokiranih = 999
                        for blokirane_tr in traka[traka_id]["blokira"]:
                            
                            print(blokirane_tr)
                            
                            if njnj["zadnje_vrijeme_izlaska"][int(blokirane_tr)-1] < najraniji_izlazak_blokiranih:
                                najraniji_izlazak_blokiranih = njnj["vozila_po_trakama"][int(blokirane_tr)-1]
                                
                        if vozilo[vozilo_id]["izlazak"] < najraniji_izlazak_blokiranih:
                        
                            
                            print("vozilo ID = ",vozilo_id)
                            # umanji kapacitet za duljinu vozila
                            njnj["dostupan_kapacitet"][i] -= vozilo[vozilo_id]["duljina"]
                            # dodaj vozilo u traku
                            njnj["vozila_po_trakama"][i].append(vozilo_id)
                            # stavi seriju cijele trake onog vozila koje prvo parkirano
                            njnj["serija_po_trakama"][i] = vozilo[vozilo_id]["serija"]   
                            # postavi zadnje vrijeme izlaska trake na izlazak zadgnje vozila
                            njnj["zadnje_vrijeme_izlaska"][i] = vozilo[vozilo_id]["izlazak"]

                            ogranicenja_trake[vozilo_id-1, :] = 0

                            break

                    #traka[traka_id]["ogranicenje"][vozilo_id-1] = 0

                # ako je serija trake jednaka seriji vozila *********************''''''''''''''''''''
                elif njnj["serija_po_trakama"][i] == vozilo[vozilo_id]["serija"]:  
                    
                    
                    najkasniji_izlazak_blokirajucih = 0
                    for blokirajuce_tr in traka[traka_id]["blokirana_od"]:
                        
                        if njnj["zadnje_vrijeme_izlaska"][int(blokirajuce_tr)-1] > najkasniji_izlazak_blokirajucih:
                            najkasniji_izlazak_blokirajucih = njnj["zadnje_vrijeme_izlaska"][int(blokirajuce_tr)-1]
                    
                    # vozilo koje ulazi u traku mora imati izlazak nakon izlaska vozila u traci koja ju blokira
                    if vozilo[vozilo_id]["izlazak"] > najkasniji_izlazak_blokirajucih:

                            najraniji_izlazak_blokiranih = 999
                            for blokirane_tr in traka[traka_id]["blokira"]:

                                if njnj["zadnje_vrijeme_izlaska"][int(blokirane_tr)-1] < najraniji_izlazak_blokiranih:
                                    najraniji_izlazak_blokiranih = njnj["vozila_po_trakama"][int(blokirane_tr)-1]

                            if vozilo[vozilo_id]["izlazak"] < najraniji_izlazak_blokiranih:
                                
                                print("vozilo ID = ",vozilo_id)
                                # dodaj vozilo u traku
                                njnj["vozila_po_trakama"][i].append(vozilo_id)
                                # umanji kapacitet za duljinu vozila + 0.5
                                njnj["dostupan_kapacitet"][i] -= vozilo[vozilo_id]["duljina"] + 0.5
                                # postavi zadnje vrijeme izlaska trake na izlazak zadgnje vozila
                                njnj["zadnje_vrijeme_izlaska"][i] = vozilo[vozilo_id]["izlazak"]

                                # ograniciti postavljanje vozila u sve ostale trake
                                ogranicenja_trake[vozilo_id-1, :] = 0
                                break
                                
print(njnj["vozila_po_trakama"])


# In[29]:


njnj["zadnje_vrijeme_izlaska"][9]


# In[30]:


njnj["zadnje_vrijeme_izlaska"][11]


# In[31]:


njnj["vozila_po_trakama"][9]


# In[32]:


for j in njnj["vozila_po_trakama"][9]:
    print(vozilo[j]["izlazak"])


# In[33]:


njnj["vozila_po_trakama"][10]


# In[34]:


for j in njnj["vozila_po_trakama"][10]:
    print(vozilo[j]["izlazak"])


# ### rjesenje

# In[35]:


njnj


# In[36]:


njnj["vozila_po_trakama"][21]  # traka 22


# In[37]:


vozilo[49]["izlazak"] # prvo u traci 22


# In[38]:


njnj["vozila_po_trakama"][20] # traka 21


# In[39]:


vozilo[12]["izlazak"] # zadnje u 21 trea biti prije prvog u 22


# In[40]:


# traka 22 se puni nakon trake 21, jer je 22 blokirana


# In[ ]:





# In[41]:


evaluation_function(njnj["vozila_po_trakama"])


# In[42]:


iskoristena_vozila = list(np.unique(j for lista in njnj["vozila_po_trakama"] for j in lista)[0])


# In[43]:


len(iskoristena_vozila)


# In[44]:


vozilo[22]["izlazak"]


# In[45]:


traka[22]["blokirana_od"]


# In[46]:


njnj["zadnje_vrijeme_izlaska"]


# # pomocno

# In[47]:


yolo = np.array([[1,2],[3,4]])
yolo


# In[48]:


yolo2 = {"nj": yolo[:,0]}
yolo2


# In[49]:


yolo[0][0] = 10


# In[50]:


yolo


# In[51]:


yolo2


# In[ ]:




