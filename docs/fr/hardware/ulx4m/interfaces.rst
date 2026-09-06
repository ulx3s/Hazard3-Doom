Interfaces externes et extension
================================

Les deux connecteurs compatibles CM4 transportent l'alimentation et de nombreux
signaux entre le module et une carte porteuse. « compatible CM4 » décrit surtout
un objectif mécanique, de connectique et de mappage; cela ne signifie pas que
tout logiciel Raspberry Pi ou toute fonction d'une carte porteuse CM4 fonctionne
automatiquement avec un FPGA.

Ethernet
--------

Les variantes publiées incluent Ethernet, mais le PHY dépend des sources et des
révisions. Crowd Supply indique ``KSZ9031RNXCA`` pour les configurations LS et
LD promues, tandis qu'une documentation LS plus ancienne mentionne
``LAN8720A``. Hazard3-Doom ne dépend pas actuellement d'Ethernet pour Doom, le
moniteur, la programmation ou le débogage.

CSI/DSI et SerDes
-----------------

Les sources amont décrivent des groupes de connecteurs caméra/affichage et des
routes SerDes vers PCIe x1 et d'autres connecteurs. Certaines voies utilisent
des E/S ordinaires « faussement différentielles »; d'autres exigent une variante
ECP5 disposant réellement de SerDes et le bon routage PCB.

Avant d'utiliser ces voies, vérifiez le composant FPGA monté et la révision PCB.
Le ``LFE5UM-85F-8BG381C`` actuel est de classe SerDes, mais le SoC Doom n'utilise
pas encore PCIe ni un autre périphérique SerDes.

GPIO, boutons, interrupteurs et LED
-----------------------------------

Les descriptions publiques mentionnent GPIO, trois boutons, deux interrupteurs
DIP et huit LED sur des configurations représentatives. Le top-level LD actuel
expose huit LED et les utilise aussi comme instrumentation de démarrage DDR :
heartbeat, verrouillage PLL, état d'initialisation, horloge utilisateur et
activité de l'adaptateur. Le top-level LS actuel en expose quatre.

UART et JTAG
------------

UART reste le chemin de diagnostic logiciel le plus simple : moniteur résident,
logs, transfert d'images et Web Serial. JTAG est complémentaire pour arrêt,
pas-à-pas, registres, mémoire et débogage source.

Alimentation
------------

La documentation amont indique un besoin d'au moins 500 mA et décrit des chemins
d'alimentation différents selon la carte porteuse. Il faut donc nommer la carte
porteuse dans les instructions et vérifier l'entrée d'alimentation, les rails
FPGA/mémoire, les tensions des banques d'E/S et la fonction exacte des broches.
La forme d'un connecteur ne garantit jamais la compatibilité électrique.
