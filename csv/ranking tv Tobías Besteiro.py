import pandas as pd
import os

RUTA_CSV = os.path.expanduser("~/Escritorio/csv/tv_accesos_provincias.csv")

def cargar_datos():
    try:
        df = pd.read_csv(RUTA_CSV)
        print(f"Archivo cargado ({len(df)} registros).")
        return df
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None

def pedir_opcion(mensaje, opciones):
    """Muestra opciones y valida que el usuario elija una existente."""
    print(f"\nOpciones disponibles: {', '.join(map(str, opciones))}")
    while True:
        try:
            valor = int(input(mensaje))
            if valor in opciones:
                return valor
        except ValueError:
            pass
        print("Opción inválida. Intente nuevamente.")

def main():
    os.system('clear')
    print("=== RANKING TV POR SUSCRIPCIÓN ===\n")
    df = cargar_datos()
    if df is None:
        return

    # Preguntar orden
    orden = input("¿Ordenar de 'mayor a menor' o 'menor a mayor'? ").lower()
    ascendente = "menor" in orden

    # Pedir año y trimestre
    anios = sorted(df["anio"].unique())
    anio = pedir_opcion("Ingrese el año: ", anios)

    trimestres = sorted(df[df["anio"] == anio]["trimestre"].unique())
    trimestre = pedir_opcion("Ingrese el trimestre (1-4): ", trimestres)

    # Filtrar y procesar
    df_f = df[(df["anio"] == anio) & (df["trimestre"] == trimestre)]
    if df_f.empty:
        print("No se encontraron datos con los filtros seleccionados.")
        return

    ranking = (
        df_f.groupby("provincia", as_index=False)["tv_suscripcion"]
        .sum()
        .sort_values(by="tv_suscripcion", ascending=ascendente)
        .reset_index(drop=True)
    )
    ranking.insert(0, "Posición", range(1, len(ranking) + 1))

    print(f"\nRanking de provincias - Año {anio} / Trimestre {trimestre}\n")
    print(ranking.to_string(index=False))
    print("\nProceso finalizado.")

if __name__ == "__main__":
    main()