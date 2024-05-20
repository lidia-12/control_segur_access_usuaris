import pigpio  # Importa la llibreria pigpio per controlar els pins GPIO de Raspberry Pi
from time import sleep  # Importa la funció sleep de la llibreria time per a pausar l'execució

class ControladorBuzzer:
    def __init__(self, pi, pin):
        self.pi = pi  # Inicialitza l'objecte pi com a connexió a pigpio
        self.pin = pin  # Assigna el pin del buzzer rebut com a paràmetre
        # Comprova si està connectat al daemon de pigpio
        if not self.pi.connected:
            raise Exception("No s'ha pogut connectar amb el daemon de pigpio.")
        # Defineix les cançons amb seqüències de tons i durades
        self.cançons = {
            "Cara al sol": ("edccccdedccffedced", "535555374646464648"),
            "The Lion Sleeps Tonight": ("cdedefedcdedced", "434434344343438"),
            "Game Of Thrones": ("adfgadfgadfge", "4422442244229"),
            "Foto": ("b", "3"),
            "La cucaracha": ("cccfacccfa", "2226322263"),
            "Fail": ("ad", "44")
        }
        # Defineix els tons associats a cada nota
        self.tons = {
            'C': 261,
            'D': 294,
            'E': 329,
            'F': 349,
            'G': 391,
            'A': 440,
            'B': 494,
            's': 0  # 's' per a silenci
        }

    def assegurar_connectat(self):
        # Reconnecta al daemon de pigpio si no està connectat
        if not self.pi.connected:
            self.pi = pigpio.pi()
            if not self.pi.connected:
                raise ConnectionError("No s'ha pogut reconectar amb el daemon de pigpio.")

    def tocar_ton(self, freqüència, durada):
        # Toca un ton amb una freqüència i durada especificades
        self.assegurar_connectat()
        if freqüència > 0:  # Només toca el ton si la freqüència és major que zero
            self.pi.hardware_PWM(self.pin, freqüència, 500000)  # Defineix el cicle de treball al 50%
            sleep(durada)
        self.pi.hardware_PWM(self.pin, 0, 0)  # Assegura't que s'aturi el ton

    def seleccionar_cançó(self, nom_cançó):
        # Toca la seqüència de tons d'una cançó seleccionada
        if nom_cançó in self.cançons:
            seqüència, tempos = self.cançons[nom_cançó]
            for nota, tempo in zip(seqüència, tempos):
                freqüència = self.tons[nota.upper()]
                durada = int(tempo) / 10  # Converteix el tempo a segons
                self.tocar_ton(freqüència, durada)
        else:
            print("Cançó no disponible.")

    def parar(self):
        # Atura la reproducció del buzzer i allibera els recursos de pigpio
        if self.pi.connected:
            self.pi.hardware_PWM(self.pin, 0, 0)  # Assegura't que no es toqui cap ton
            self.pi.stop()
            self.pi = None

# Configuració del pin GPIO per al buzzer
pin_buzzer = 12  # Assegura't de canviar això pel pin al qual està connectat el teu buzzer

# Inicialitza una connexió a pigpio
pi = pigpio.pi()
if pi.connected:
    instancia_buzzer = ControladorBuzzer(pi, pin_buzzer)
else:
    print("Error: No s'ha pogut connectar amb el daemon de pigpio.")


# Exemple d'ús
if __name__ == "__main__":
    try:
        while True:
            print("Llista de cançons disponibles:")
            # Mostra la llista de cançons disponibles per a la reproducció
            for index, song in enumerate(instancia_buzzer.cançons.keys(), 1):
                print(f"{index}. {song}")
            print("0. Sortir")
            selecció = input("Selecciona una cançó (número) o 0 per sortir: ")
            if selecció == "0":
                break
            noms_cançons = list(instancia_buzzer.cançons.keys())
            try:
                cançó_seleccionada = noms_cançons[int(selecció) - 1]
                instancia_buzzer.seleccionar_cançó(cançó_seleccionada)
            except (IndexError, ValueError):
                print("Selecció no vàlida. Torna-ho a intentar.")
    finally:
        instancia_buzzer.parar()

