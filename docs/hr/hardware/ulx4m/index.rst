ULX4M hardverski vodič
=======================

**Arhitektura, komponente, sučelja i njihova uporaba u Hazard3-Doomu.**

ULX4M je mnogo više od FPGA-a na kojem radi Hazard3. To je modularna open
hardware računalna platforma s Lattice ECP5 FPGA-om, vanjskom memorijom, SPI
flashom za konfiguraciju, video i brzim sučeljima, vezama za izmjenjivu pohranu,
programiranjem i debug putovima te s dva gusto postavljena konektora kompatibilna
s CM4 formatom.

Ovaj vodič prati signale od fizičkih komponenti pločice preko FPGA pinova i
ograničenja do Veriloga, memorijskih kontrolera i, gdje je primjenjivo, softvera
koji se izvršava na Hazard3 procesoru.

.. important::

   Ovo je Hazard3-Doom hardverski vodič, a ne autoritativna zamjena za službenu
   ULX4M dokumentaciju. Prije oslanjanja na broj dijela, kapacitet memorije,
   napajanje ili pin uvijek provjerite PCB reviziju i stvarno ugrađene komponente.

To je važno jer javni ULX4M izvori opisuju više revizija i različite populacije
komponenata. Hazard3-Doom zato reviziju pločice i ugrađeni memorijski dio tretira
kao konfiguracijske ulaze.

.. toctree::
   :maxdepth: 2

   overview-and-variants
   fpga-and-clocking
   memory
   boot-and-flash
   video-and-storage
   interfaces
   pinout-and-revisions
   sources

Koristan mentalni model
-----------------------

.. code-block:: text

   +---------------------------------------------------------------+
   | Carrier pločica / vanjski svijet                              |
   | USB, zaslon, SD, Ethernet, PCIe/SerDes, GPIO, napajanje       |
   +-------------------------------+-------------------------------+
                                   |
                         CM4-kompatibilni konektori
                                   |
   +-------------------------------v-------------------------------+
   | ULX4M modul                                                   |
   |  SPI flash <--> Lattice ECP5 FPGA <--> video/JTAG/SD/SerDes  |
   |                    |                                          |
   |                 SDR/DDR3                                      |
   +---------------------------------------------------------------+

Hazard3-Doom danas ne koristi svaki dostupni ULX4M periferni blok. Vodič zato
odvaja **hardver prisutan na pločici** od **hardvera koji je trenutačno
implementiran ili kvalificiran u Hazard3-Doomu**.
