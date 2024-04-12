from collections import defaultdict
import pandas as pd
from sklearn.linear_model import LinearRegression

class SistemaTransporte:
    def __init__(self, reglas, paradas, conexiones):
        self.reglas = reglas
        self.paradas = paradas
        self.conexiones = conexiones
        self.grafo = self._construir_grafo()
        
    def _construir_grafo(self):
        grafo = defaultdict(list)
        for parada in self.paradas:
            for conexion in self.conexiones:
                if parada == conexion[0]:
                    grafo[parada].append((conexion[1], conexion[2]))
        return grafo
    
    def _aplicar_reglas(self, camino):
        for regla in self.reglas:
            if regla.aplica(camino):
                return regla.modifica(camino)
        return camino
    
    def _mejor_ruta(self, origen, destino):
        visitados = set()
        rutas = [(origen, 0, [])]
        while rutas:
            actual, costo, ruta = rutas.pop(0)
            if actual == destino:
                return ruta
            if actual in visitados:
                continue
            visitados.add(actual)
            for vecino, costo_adyacente in self.grafo[actual]:
                nueva_ruta = ruta + [vecino]
                if self._aplicar_reglas(nueva_ruta):
                    rutas.append((vecino, costo + costo_adyacente, nueva_ruta))
        return None
    
    def buscar_ruta(self, origen, destino):
        ruta = self._mejor_ruta(origen, destino)
        if ruta is None:
            print("No hay ruta disponible entre", origen, "y", destino)
        else:
            coste_total = self._calcular_coste_total(ruta)
            print("La mejor ruta es:", end=" ")
            for parada in ruta[:-1]:
                print(parada, end=" -> ")
            print(ruta[-1])
            print(f"Coste total: {coste_total}")
            return ruta
    
    def _calcular_coste_total(self, ruta):
        coste_total = 0
        for i in range(len(ruta) - 1):
            origen = ruta[i]
            destino = ruta[i + 1]
            for conexion in self.conexiones:
                if origen == conexion[0] and destino == conexion[1]:
                    coste_total += conexion[2]
        return coste_total

class Regla:
    def __init__(self, aplica, modifica):
        self.aplica = aplica
        self.modifica = modifica

reglas = [
    Regla(lambda camino: len(camino) > 2, lambda camino: camino[1:]),
]

paradas = ["A", "B", "C", "D", "E"]

conexiones = [
    ("A", "B", 10),
    ("A", "C", 20),
    ("B", "D", 30),
    ("C", "D", 40),
    ("D", "E", 50),
]

sistema = SistemaTransporte(reglas, paradas, conexiones)

def obtener_demanda_transport_publico(origen, destino):
    # Simulación de obtención de datos climáticos
    weather_data = {
        'temperature': [25],
        'precipitation': [0.05]
    }
    weather_df = pd.DataFrame(weather_data, columns=['temperature', 'precipitation'])
    return model.predict(weather_df)

# Entrenar modelo de regresión lineal usando datos de tráfico histórico
traffic_data = {
    'stop_id': ['A', 'B', 'C', 'D', 'E'],
    'temperature': [20, 21, 22, 23, 24],
    'precipitation': [0, 0, 0.1, 0, 0.2],
    'passenger_volume': [100, 120, 80, 90, 110]
}
traffic_df = pd.DataFrame(traffic_data, columns=['stop_id', 'temperature', 'precipitation', 'passenger_volume'])
X_train = traffic_df[['temperature', 'precipitation']]
y_train = traffic_df['passenger_volume']

# Ajustar modelo de regresión lineal
model = LinearRegression()
model.fit(X_train, y_train)

# Solicitar origen y destino
origen = input("Ingrese la parada de origen: ")
destino = input("Ingrese la parada de destino: ")

# Buscar ruta y obtener demanda de transporte público
ruta = sistema.buscar_ruta(origen, destino)
if ruta:
    demanda_predicha = obtener_demanda_transport_publico(origen, destino)
    print("Demanda de transporte público predicha:", demanda_predicha)
