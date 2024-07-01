# POTREBNE KNJIZNICE
```
pip install numpy opencv-python shapely matplotlib tkinter PIL
```

# UPORABA
*danger_detection_v1.py*\
Skripta je namenjena demonstraciji, kako se presodi nevarnost pesca/ kolesarja s pomocjo meje nevarnosti (crte).\
V skripti je potrebno rocno izbrati vhodno sliko.\
Po izvrseni skripti se prikaze slika z oznacbo pesca in izrisom meje nevarnosti (rdeca crta).\
Ce se oznacba pesca prekriva z mejo nevarnosti, se izpise opozorilo.\

*moving_line_demo.py*\
Skripta je namenjena demonstraciji, kako bo uporabnik v koncni aplikaciji s pomocjo "drag" lahko prosto premikal mejo nevarnosti (crto) in si jo tako prilagodil na svoje preference.\
Ce uporabnik ne spremeni meje nevarnosti, se bo upostevala standardna meja, ki je dolocena s koordinatami v kodi.\
Ob izvrseni skripti uporabnik izbere demo sliko in na njej lahko rocno prilagaja mejo nevarnosti.\
