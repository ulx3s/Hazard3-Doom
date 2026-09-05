FPGA, horloges et domaines d'E/S
=================================

La cible ULX4M-LD de Hazard3-Doom est construite pour
``LFE5UM-85F-8BG381C``. La classe ``UM`` fournit les ressources SerDes ECP5,
alors que les variantes ``LFE5U`` ordinaires n'offrent pas les mêmes
transceivers haut débit. Le makefile ULX4M-LS actuel cible un ECP5 85K en
``CABGA381`` afin de disposer de suffisamment de blocs RAM pour le SoC Doom.

Référence de 25 MHz
-------------------

Les contraintes définissent ``clk_osc`` comme une entrée 25 MHz. Cette référence
alimente plusieurs domaines indépendants.

.. list-table:: Domaines importants sur ULX4M-LD
   :header-rows: 1
   :widths: 28 20 52

   * - Domaine
     - Horloge
     - Rôle
   * - Référence/initialisation
     - 25 MHz
     - Oscillateur direct et référence LiteDRAM.
   * - Système Hazard3/AHB
     - 40 MHz qualifié
     - CPU, bus SoC et côté AHB de l'adaptateur DDR.
   * - Utilisateur LiteDRAM
     - 60 MHz qualifié
     - Port Wishbone 128 bits.
   * - DDR
     - 120 MHz dans les métadonnées actuelles
     - Horloge physique DDR3.
   * - Pixel vidéo
     - 50 MHz
     - Pipeline vidéo.
   * - Sérialisation TMDS
     - 250 MHz
     - Sérialiseur GPDI/HDMI.

Le wrapper LD garde LiteDRAM sur la référence directe de 25 MHz tandis que
Hazard3 peut utiliser une PLL système distincte. Changer l'horloge CPU ne change
donc pas automatiquement le profil DDR3 généré.

Le wrapper autorise actuellement 25, 40 ou 50 MHz pour Hazard3, mais 40 MHz est
le point de qualification de la version avec le port LiteDRAM à 60 MHz.

ULX4M-LS
---------

Le wrapper LS génère un système Hazard3/SDRAM à 50 MHz à partir de la même
référence 25 MHz. Une seconde PLL est réservée à la vidéo. L'horloge SDRAM est
transmise avec une relation de phase contrôlée afin de respecter la fenêtre de
timing du composant SDR.

Pourquoi les domaines comptent
------------------------------

Sur LD, Hazard3 émet des transactions AHB à 40 MHz alors que le port utilisateur
LiteDRAM fonctionne à 60 MHz. ``ahb_litedram.v`` doit donc traduire le bus et
franchir correctement la frontière d'horloge.

Il faut vérifier séparément le timing du système 40 MHz, celui de LiteDRAM à
60 MHz, les contraintes PHY DDR et enfin les tests réels de mémoire. Un PASS
nextpnr sur une seule horloge ne qualifie pas toute la mémoire. Voir
:doc:`../../reference/timing-sweeps`.

Normes d'E/S
------------

Le LPF contient aussi les caractéristiques électriques. La DDR3 LD utilise des
normes SSTL et des contraintes différentielles adaptées aux lignes DQ/DQS et à
l'horloge. La SDRAM LS et de nombreux signaux ordinaires utilisent LVCMOS 3,3 V.
Une broche correcte avec une mauvaise norme d'E/S reste une conception
matériellement incorrecte.
