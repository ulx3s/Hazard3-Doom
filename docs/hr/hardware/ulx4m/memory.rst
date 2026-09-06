Vanjska memorija: SDRAM i DDR3
==============================

Vanjska memorija najveća je arhitekturna razlika između ULX4M-LS i ULX4M-LD.
Hazard3 i dalje izvršava obične RISC-V load/store operacije, ali se logika između
AHB sabirnice i fizičkog memorijskog čipa znatno razlikuje.

Vidi i :doc:`../../architecture/hazard3/memory-and-bus`.

ULX4M-LS: nativni SDR SDRAM
---------------------------

Trenutačni LS wrapper opisuje 32 MiB, 16-bitni SDR SDRAM i koristi istu obitelj
nativnih kontrolera kao ULX3S:

.. code-block:: text

   Hazard3/AHB -> ahb_sdram.v -> ulx3s_sdram_controller.v -> 16-bitni SDR SDRAM

Profil radi na 50 MHz i koristi 9-bitnu SDRAM column geometriju. Kontroler vodi
activate/precharge, CAS, refresh, byte maskiranje i arbitražu s videom.

ULX4M-LD: LiteDRAM DDR3
-----------------------

.. code-block:: text

   Hazard3 40 MHz -> AHB5 -> ahb_litedram.v -> CDC
       -> 128-bitni Wishbone 60 MHz -> LiteDRAM -> ECP5DDRPHY -> x16 DDR3

Generirani LiteDRAM core upravlja geometrijom, inicijalizacijom, rasporedom
naredbi, refreshem i DDR PHY-em. ``ahb_litedram.v`` namjerno zadržava isto
procesorsko sučelje kada se promijeni fizički DDR3 dio.

Podržane DDR3 obitelji profila
------------------------------

.. list-table::
   :header-rows: 1
   :widths: 29 20 20 31

   * - Projektni odabir
     - Gustoća
     - Kapacitet
     - LiteDRAM klasa
   * - ``MT41K512M16HA``
     - 8 Gbit x16
     - 1 GiB
     - ``MT41K512M16``
   * - ``AS4C256M16D3``
     - 4 Gbit x16
     - 512 MiB
     - ``AS4C256M16D3A``

Doom softverski profil trenutačno namjerno izlaže samo 64 MiB vanjske memorije;
preostali fizički kapacitet ne mora biti mapiran.

Trenutačno generirani profil
----------------------------

Uključeni SERV i VexRisc metapodaci odgovaraju Micron
``MT41K512M16HA`` obitelji i bilježe LiteDRAM/LiteX 2024.12, 25 MHz
referencu/init, Hazard3 40 MHz, LiteDRAM user port 60 MHz, DDR sat 120 MHz,
128-bitni Wishbone, command buffer depth 2 i uključen auto-precharge.

SERV ili minimalni VexRiscv služe kao LiteX inicijalizacijski CPU unutar
generiranog DDR okruženja. To nije Hazard3 procesor koji pokreće Doom.

Regeneriranje za ugrađeni RAM
-----------------------------

Ne mijenjajte ručno generirani LiteDRAM Verilog. Koristite YAML profile:

.. code-block:: bash

   cd third_party/Hazard3/example_soc/third_party/LiteDRAM
   ./regenerate-ulx4m.sh MT41K512M16HA

ili:

.. code-block:: bash

   ./regenerate-ulx4m.sh AS4C256M16D3

Generator stvara ``generated-serv/`` i ``generated-vexrisc/`` i bilježi
provenance.

.. important::

   Generirani core mora odgovarati DDR3 dijelu na stvarnoj pločici. Campaign
   stranica, stara shema ili tuđa pločica nisu dovoljne za identifikaciju.

Kvalifikacija
-------------

LiteDRAM kalibracija ili timing PASS nisu dovoljni. Kvalificirani Micron put
prošao je destruktivne uzorke, alias/adresne provjere, pseudorandom testove,
punu monitor kvalifikaciju, heap stress, Doom platform smoke test i izvršavanje
RV32 koda kopiranog u DDR.

Fizičko LD sučelje uključuje adrese, banke, RAS/CAS/WE, CKE, CS, ODT, reset,
dva data mask signala, 16 bidirekcijskih DQ bitova, dvije DQS byte lane i
diferencijalni sat. I LiteDRAM YAML i LPF nužni su dijelovi ispravnog dizajna.
