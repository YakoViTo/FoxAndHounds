Implementación de un juego llamado "El Zorro y los Cazadores" utilizando la biblioteca Pygame en Python. El juego consiste en un tablero cuadriculado donde un zorro (representado por una imagen) debe intentar evitar ser capturado por los cazadores (también representados por imágenes) que se mueven por el tablero. El objetivo del zorro es llegar a la parte superior del tablero, mientras que los cazadores intentan bloquear su camino.

![image](https://github.com/YakoViTo/FoxAndHounds/assets/135473233/1b89adae-bde4-46ee-b2d1-ee1f34b09c9c)

El juego permite a los jugadores alternar turnos entre el zorro y los cazadores. El zorro puede moverse diagonalmente hacia arriba o hacia abajo en el tablero, mientras que los cazadores solo se mueven diagonalmente hacia abajo. El zorro puede evadir a los cazadores moviéndose estratégicamente y aprovechando las oportunidades para avanzar hacia la parte superior.

El programa utiliza el algoritmo Minimax para tomar decisiones automáticas para los movimientos de los cazadores. El algoritmo evalúa las posibles jugadas y selecciona la mejor opción en función de una función de evaluación que considera varios factores, como la posición del zorro, la distancia entre las piezas y la posibilidad de victoria.

En general, el programa implementa la lógica del juego "El Zorro y los Cazadores" y ofrece una interfaz gráfica mediante la biblioteca Pygame para que los jugadores interactúen con el juego y jueguen tanto contra la computadora (cazadores controlados por el algoritmo Minimax) como entre sí.
