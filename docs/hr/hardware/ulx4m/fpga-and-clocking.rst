FPGA, satovi i I/O domene
=========================

Hazard3-Doom ULX4M-LD meta gradi se za ``LFE5UM-85F-8BG381C``. Klasa ``UM``
sadrži ECP5 SerDes resurse, dok obične ``LFE5U`` varijante nemaju istu brzu
transceiver funkcionalnost. Trenutačni ULX4M-LS makefile cilja ECP5 85K u
``CABGA381`` paketu kako bi bilo dovoljno blok RAM-a za Doom SoC.

Referentni sat od 25 MHz
------------------------

Ograničenja definiraju ``clk_osc`` kao 25 MHz ulaz. Ta referenca napaja više
logički odvojenih domena.

.. list-table:: Važne ULX4M-LD domene
   :header-rows: 1
   :widths: 28 20 52

   * - Domena
     - Sat
     - Svrha
   * - Referenca/inicijalizacija
     - 25 MHz
     - Izravni oscilator i LiteDRAM referenca.
   * - Hazard3/AHB sustav
     - kvalificiranih 40 MHz
     - CPU, SoC sabirnica i AHB strana DDR adaptera.
   * - LiteDRAM user
     - kvalificiranih 60 MHz
     - 128-bitni Wishbone port.
   * - DDR
     - 120 MHz u trenutačnim metapodacima
     - Fizički DDR3 sat.
   * - Video piksel
     - 50 MHz
     - Video pipeline.
   * - TMDS serijalizacija
     - 250 MHz
     - GPDI/HDMI serijalizator.

LD wrapper drži LiteDRAM na izravnoj 25 MHz referenci, dok Hazard3 koristi
zaseban sistemski PLL. Promjena CPU sata zato ne mijenja automatski generirani
DDR3 profil.

Wrapper trenutačno dopušta 25, 40 i 50 MHz za Hazard3, ali 40 MHz je kvalificiran
release checkpoint u paru s LiteDRAM user satom od 60 MHz.

ULX4M-LS
---------

LS wrapper iz iste 25 MHz reference generira Hazard3/SDRAM sustav od 50 MHz.
Video ima drugi PLL. SDRAM sat prosljeđuje se s kontroliranim faznim odnosom
prema sistemskom satu.

Zašto su clock domene važne
---------------------------

Na LD-u Hazard3 šalje AHB transakcije na 40 MHz, a LiteDRAM user port radi na
60 MHz. ``ahb_litedram.v`` zato mora i prevesti sabirnicu i sigurno prenijeti
zahtjeve/odgovore preko clock-domain granice.

Zasebno treba provjeriti 40 MHz timing, 60 MHz timing, DDR PHY ograničenja i
stvarne memorijske testove. nextpnr PASS jedne domene nije kvalifikacija cijelog
memorijskog sustava. Pogledajte :doc:`../../reference/timing-sweeps`.

I/O standardi
-------------

LPF nije samo popis pinova. LD DDR3 koristi odgovarajuće SSTL i diferencijalne
postavke za DQ/DQS i DDR sat, dok LS SDRAM i mnogi obični signali koriste 3,3 V
LVCMOS. Ispravan pin s pogrešnim električnim standardom i dalje je pogrešan
hardverski dizajn.
