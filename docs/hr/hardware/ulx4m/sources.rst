Izvorni dizajn i dodatna literatura
===================================

Ovaj vodič namjerno zadržava vidljivost upstream izvora. Hazard3-Doom dodaje
tumačenje i projektne integracijske bilješke, ali ne zamjenjuje izvornu ULX4M
hardversku dokumentaciju.

Glavni ULX4M izvori
-------------------

* `ULX4M na Crowd Supplyu <https://www.crowdsupply.com/intergalaktik/ulx4m>`_
* `Intergalaktik ULX4M hardverski repo <https://github.com/intergalaktik/ulx4m>`_
* `Intergalaktik ULX4M dokumentacija <https://github.com/intergalaktik/ulx4m-documentation>`_
* `ULX4M primjeri <https://github.com/lawrie/ulx4m_examples>`_

Hazard3-Doom izvori
-------------------

.. code-block:: text

   third_party/Hazard3/example_soc/fpga/
   third_party/Hazard3/example_soc/synth/
   third_party/Hazard3/example_soc/soc/
   third_party/Hazard3/example_soc/third_party/LiteDRAM/
   bootloader/
   openocd/

Kod neslaganja izvora koristite ovaj prioritet: fizička pločica, odgovarajuća
shema/PCB/BOM revizija, LPF i wrapper za konkretni build, datasheet ugrađene
komponente, a zatim campaign/README/example materijal. Neslaganje koje utječe na
build treba dokumentirati u projektu.

Povezana Hazard3-Doom dokumentacija
-----------------------------------

* :doc:`../../reference/board-profiles`
* :doc:`../../architecture/hazard3/memory-and-bus`
* :doc:`../../architecture/video`
* :doc:`../../user-guide/bootloader`
* :doc:`../../user-guide/sd-card`
* :doc:`../../user-guide/jtag-debugging`
* :doc:`../../reference/timing-sweeps`
