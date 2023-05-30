.. MOOD documentation master file, created by
   sphinx-quickstart on Thu Apr  6 16:23:38 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to MOOD's documentation!
================================
Добавить на сервере MUD поддержку бродячих монстров:

* один раз в 30 секунд выбирается случайный монстр, и он перемещается на одну клетку в случайно выбранном направлении (вправо/влево/вверх/вниз; помним, что поле "закольцовано").
* если в результате перемещения монстр попал бы на клетку, где уже есть монстр, то перемещение НЕ ПРОИСХОДИТ, и проводится повторный выбор монстра и направления; и так пока не будет выполнено успешное перемещение монстра.
* при перемещении сервер выдаёт всем игрокам сообщение "<имя_монстра> moved one cell <направление>", где <направление> это right, left, up, down. Например: "manticore moved one cell right".
* если монстр попадает на клетку, где есть игрок (или игроки), происходит "энкаунтер" - как если бы игрок(и) сам зашел(ли) на клетку с монстром. В т.ч. монстр отрисовывается у столкнувшихся с ним игроков, с произнесением приветственной фразы.

.. toctree::
   :maxdepth: 1
   :caption: Documentation:
    
   modules
   
.. automodule:: moodserver.moodserver
   :members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
