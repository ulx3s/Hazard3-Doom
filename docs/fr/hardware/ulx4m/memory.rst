Mémoire externe : SDRAM et DDR3
===============================

La mémoire externe est la principale différence architecturale entre ULX4M-LS
et ULX4M-LD. Hazard3 exécute toujours des chargements et stockages RISC-V
ordinaires, mais le chemin jusqu'au composant mémoire change complètement.

Voir aussi :doc:`../../architecture/hazard3/memory-and-bus`.

ULX4M-LS : SDR SDRAM native
---------------------------

Le wrapper LS actuel décrit une interface SDR SDRAM 16 bits de 32 MiB et utilise
la même famille de contrôleurs natifs que l'ULX3S :

.. code-block:: text

   Hazard3/AHB -> ahb_sdram.v -> ulx3s_sdram_controller.v -> SDR SDRAM 16 bits

Le profil utilise une horloge système de 50 MHz et une géométrie de 9 bits de
colonne. Le contrôleur gère activation, précharge, CAS, rafraîchissement, masques
d'octets et arbitrage avec la vidéo.

ULX4M-LD : DDR3 LiteDRAM
------------------------

.. code-block:: text

   Hazard3 40 MHz -> AHB5 -> ahb_litedram.v -> CDC
       -> Wishbone 128 bits 60 MHz -> LiteDRAM -> ECP5DDRPHY -> DDR3 x16

Le coeur généré LiteDRAM possède la géométrie, l'initialisation, la planification
des commandes, le rafraîchissement et le PHY DDR. ``ahb_litedram.v`` conserve
la même interface côté processeur lorsque la puce DDR change.

Profils DDR3 pris en charge
---------------------------

.. list-table::
   :header-rows: 1
   :widths: 29 20 20 31

   * - Sélection projet
     - Densité
     - Capacité
     - Classe LiteDRAM
   * - ``MT41K512M16HA``
     - 8 Gbit x16
     - 1 GiB
     - ``MT41K512M16``
   * - ``AS4C256M16D3``
     - 4 Gbit x16
     - 512 MiB
     - ``AS4C256M16D3A``

Le profil logiciel Doom actuel n'expose volontairement que 64 MiB de mémoire
externe; la capacité physique supplémentaire n'a pas besoin d'être mappée.

Profil généré actuel
--------------------

Les métadonnées SERV et VexRisc incluses dans cette version correspondent à la
famille Micron ``MT41K512M16HA`` et enregistrent LiteDRAM/LiteX 2024.12, une
référence 25 MHz, Hazard3 à 40 MHz, un port LiteDRAM à 60 MHz, une horloge DDR à
120 MHz, un port Wishbone 128 bits, une profondeur de tampon de commandes 2 et
l'auto-précharge activée.

SERV ou VexRiscv minimal sert de CPU d'initialisation LiteX dans le coeur généré.
Ce n'est pas le processeur Hazard3 qui exécute Doom.

Régénération pour la RAM montée
-------------------------------

Ne modifiez pas manuellement le Verilog LiteDRAM généré. Utilisez les profils
YAML :

.. code-block:: bash

   cd third_party/Hazard3/example_soc/third_party/LiteDRAM
   ./regenerate-ulx4m.sh MT41K512M16HA

ou :

.. code-block:: bash

   ./regenerate-ulx4m.sh AS4C256M16D3

Le générateur produit les variantes ``generated-serv/`` et
``generated-vexrisc/`` et enregistre leur provenance.

.. important::

   Le coeur généré doit correspondre à la DDR3 réellement montée. Une page de
   campagne, un vieux schéma ou la carte d'un autre utilisateur ne suffit pas à
   identifier votre composant.

Qualification
-------------

Une calibration LiteDRAM ou un PASS de timing ne suffit pas. Le chemin Micron
qualifié a été testé avec motifs destructifs, tests d'alias/adresse, séquences
pseudo-aléatoires, suite de qualification du moniteur, stress du tas, test de la
plate-forme Doom et exécution de code RV32 copié dans la DDR.

L'interface physique LD comprend adresse, banques, RAS/CAS/WE, CKE, CS, ODT,
reset, deux masques, seize DQ bidirectionnels, deux voies DQS et une horloge
différentielle. Le LPF et le YAML LiteDRAM sont tous deux indispensables à une
conception correcte.
