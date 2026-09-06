Sources de conception et lectures complémentaires
=================================================

Ce guide conserve volontairement la visibilité des sources amont. Hazard3-Doom
ajoute une interprétation et des notes d'intégration, mais ne remplace pas la
documentation de la conception ULX4M.

Sources ULX4M principales
-------------------------

* `ULX4M sur Crowd Supply <https://www.crowdsupply.com/intergalaktik/ulx4m>`_
* `Dépôt matériel Intergalaktik ULX4M <https://github.com/intergalaktik/ulx4m>`_
* `Documentation Intergalaktik ULX4M <https://github.com/intergalaktik/ulx4m-documentation>`_
* `Exemples ULX4M <https://github.com/lawrie/ulx4m_examples>`_

Sources Hazard3-Doom
--------------------

.. code-block:: text

   third_party/Hazard3/example_soc/fpga/
   third_party/Hazard3/example_soc/synth/
   third_party/Hazard3/example_soc/soc/
   third_party/Hazard3/example_soc/third_party/LiteDRAM/
   bootloader/
   openocd/

Pour résoudre une divergence, utilisez l'ordre de confiance suivant : la carte
physique, le schéma/PCB/BOM correspondant, le LPF et le wrapper du build, la
fiche technique du composant monté, puis les pages de campagne/README/exemples.
Documentez toute divergence qui influence un build.

Documentation liée
------------------

* :doc:`../../reference/board-profiles`
* :doc:`../../architecture/hazard3/memory-and-bus`
* :doc:`../../architecture/video`
* :doc:`../../user-guide/bootloader`
* :doc:`../../user-guide/sd-card`
* :doc:`../../user-guide/jtag-debugging`
* :doc:`../../reference/timing-sweeps`
