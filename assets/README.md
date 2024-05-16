# /assets
Direktorij namenjen slikam, videoposnetkom, zvocnim posnetkom,...

# Dodajanje direktorija:
primer:
- assets/photos
- assets/videos
- assets/audio
- assets/random
- ...

# Poimenovanje in dodajanje meritev
1. Za vsak videposnetek naj bodo svoje meritve.
2. Za vsak videoposnetek ustvari mapo z imenom **video_<ime_videoposnetka>**
3. Ta mapa pa naj vsebuje:
    - mapo **frames**

        ![Vsebina frames](/assets/random/vsebina_frames.PNG)

    - mapo **labels**

        ![Vsebina labels](/assets/random/vsebina_labels.PNG)

    - dokument **classes.txt**
    - dokument **info.txt** in
    - dokument **notes.json**

4. ***Na github NE pushaj originalnih videoposnetkov!***

# Poimenovanje meritev
- mm = minuta zajema
- ss = sekunda zajema

## Frames:
- slika_<mm>_<ss>.PNG


## Labels:
- oznaka_<mm>_<ss>.txt