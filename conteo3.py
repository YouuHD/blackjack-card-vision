# Inicializar el contador
conteo = 0

# Definir valores de las cartas
valores_cartas = {'2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 0, '8': 0, '9': 0, '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1}

def contar_carta(cartas):
    """
    Función para contar el valor total de un conjunto de cartas.
    """
    total = 0
    for carta in cartas:
        total += valores_cartas[carta]
    
    print("Total: ",total)
    return total

def evaluar_conteo(conteo):
    """
    Función para evaluar si el conteo es beneficioso para apostar.
    """
    mensaje = ""
    if conteo > 0:
        mensaje = "El conteo es beneficioso para apostar."
    elif conteo == 0:
        mensaje = "El conteo es neutral."
    else:
        mensaje = "El conteo no es beneficioso para apostar."
    
    return mensaje

#Impresión de 
def prueba(player):
    print("Desde función impresión del arreglo: ",player)

# Juego
def do_conteo(mano_jugador, carta_desconocida_repartidor):
    while True:
        #Declaración de variable conteo
        conteo = 0
        # Actualizar el conteo basado en las cartas repartidas
        if len(mano_jugador) > 1:
            try:
                conteo += contar_carta(mano_jugador)
                conteo += contar_carta(carta_desconocida_repartidor)
            
                # Evaluar el conteo
                mensaje = evaluar_conteo(conteo)
            except:
                mensaje = "El conteo no es beneficioso para apostar."
                return mensaje
                break

            # Comprobar si algún jugador tiene 21
            if 'A' in mano_jugador and conteo == -1:
                mensaje = "¡Blackjack! ¡El jugador gana!"
                break
            elif 'A' in mano_jugador and conteo == 0:
                mensaje = "¡Blackjack! ¡El repartidor gana!"
                break

            if mano_jugador and conteo == 21:
                mensaje = "El jugador ha alcanzado 21. ¡El jugador gana!"
            elif mano_jugador and conteo > 21:
                mensaje = "El jugador a superado 21 el repartidor gana"
                break

            # Reiniciar el conteo para la próxima ronda
            conteo = 0
            return mensaje
            break
        else: 
            mensaje = "Solo se ha registrado una carta del jugador"
            break