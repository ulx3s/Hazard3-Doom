Guide matériel ULX4M
=====================

**Architecture, composants, interfaces et utilisation par Hazard3-Doom.**

L'ULX4M est bien plus que le FPGA qui exécute Hazard3. C'est une plate-forme de
calcul modulaire et open hardware comprenant un FPGA Lattice ECP5, de la mémoire
externe, une mémoire flash SPI de configuration, des interfaces vidéo et haut
débit, des connexions de stockage amovible, des chemins de programmation et de
débogage, ainsi que deux connecteurs d'extension haute densité compatibles avec
le format CM4.

Ce guide suit les signaux depuis les composants physiques de la carte, à
travers les broches et contraintes FPGA, jusqu'au Verilog, aux contrôleurs
mémoire et, lorsque cela s'applique, au logiciel exécuté sur le processeur
Hazard3.

.. important::

   Ce document est un guide matériel Hazard3-Doom, et non un remplacement
   autoritatif de la documentation du fabricant ULX4M. Vérifiez toujours la
   révision du PCB et les composants réellement montés avant de vous fier à une
   référence, une capacité mémoire, une hypothèse d'alimentation ou une broche.

Cette distinction est importante car les sources ULX4M publiques décrivent
plusieurs révisions et populations de composants. Hazard3-Doom traite donc la
révision de la carte et la mémoire montée comme des paramètres de configuration.

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

Modèle mental utile
-------------------

.. code-block:: text

   +---------------------------------------------------------------+
   | Carte porteuse / monde extérieur                              |
   | USB, affichage, SD, Ethernet, PCIe/SerDes, GPIO, alimentation |
   +-------------------------------+-------------------------------+
                                   |
                         connecteurs compatibles CM4
                                   |
   +-------------------------------v-------------------------------+
   | Module ULX4M                                                  |
   |  flash SPI <--> FPGA Lattice ECP5 <--> vidéo/JTAG/SD/SerDes  |
   |                    |                                          |
   |                 SDR/DDR3                                      |
   +---------------------------------------------------------------+

Hazard3-Doom n'utilise pas encore tous les périphériques disponibles. Le guide
sépare donc le **matériel présent sur la carte** du **matériel actuellement
implémenté ou qualifié par Hazard3-Doom**.
