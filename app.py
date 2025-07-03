import streamlit as st
from datetime import datetime

def validar_fecha(dia, mes, anio):
    try:
        fecha = datetime(anio, mes, dia)
        if 2000 <= anio <= 2025:
            return True
        else:
            return False
    except ValueError:
        return False

def cargar_ventas(matriz_ventas):
    st.header("Cargar Ventas")
    cantidad = st.number_input("¿Cuántas ventas desea cargar?", min_value=1, step=1, key="cantidad_ventas")
    ventas_nuevas = []
    for i in range(cantidad):
        with st.expander(f"Venta #{len(matriz_ventas) + i + 1}", expanded=True):
            id_prod = st.number_input("ID del producto", key=f"id_prod_{i}", format="%d")
            cat = st.text_input("Categoría del producto", key=f"cat_{i}")
            producto = st.text_input("Producto", key=f"producto_{i}")
            precio = st.number_input("Precio del producto", min_value=0.0, format="%.2f", key=f"precio_{i}")
            cant = st.number_input("Cantidad vendida", min_value=1, step=1, key=f"cant_{i}")

            col1, col2, col3 = st.columns(3)
            with col1:
                dia = st.number_input("Día", min_value=1, max_value=31, key=f"dia_{i}")
            with col2:
                mes = st.number_input("Mes", min_value=1, max_value=12, key=f"mes_{i}")
            with col3:
                anio = st.number_input("Año", min_value=2000, max_value=2025, key=f"anio_{i}")

            fecha_valida = validar_fecha(dia, mes, anio)
            if fecha_valida:
                fecha = f"{int(dia):02d}-{int(mes):02d}-{int(anio)}"
                st.success(f"Fecha válida: {fecha}")
                agregar = st.button("Agregar esta venta", key=f"add_{i}")
                if agregar:
                    venta = [int(id_prod), cat, producto, float(precio), int(cant), fecha]
                    ventas_nuevas.append(venta)
                    st.success("Venta agregada correctamente.")
            else:
                st.error("Fecha inválida. Corrija los datos.")
    if ventas_nuevas:
        matriz_ventas.extend(ventas_nuevas)
    return matriz_ventas

def modificar_venta(matriz_ventas):
    st.header("Modificar Venta")
    if not matriz_ventas:
        st.warning("No hay ventas registradas.")
        return

    ids = [venta[0] for venta in matriz_ventas]
    id_abuscar = st.number_input("Ingrese el ID de la venta a modificar", min_value=1, step=1)
    if id_abuscar not in ids:
        st.info("Ingrese un ID presente en la tabla de ventas.")
        return

    index = ids.index(id_abuscar)
    venta = matriz_ventas[index]

    st.subheader("Datos actuales de la venta")
    st.write(f"ID: {venta[0]}")
    st.write(f"Categoría: {venta[1]}")
    st.write(f"Producto: {venta[2]}")
    st.write(f"Precio: {venta[3]}")
    st.write(f"Cantidad: {venta[4]}")
    st.write(f"Fecha: {venta[5]}")

    with st.form(key="modificar_venta_form"):
        nuevo_id = st.text_input("Nuevo ID", value=str(venta[0]))
        nueva_cat = st.text_input("Nueva Categoría", value=venta[1])
        nuevo_prod = st.text_input("Nuevo Producto", value=venta[2])
        nuevo_precio = st.text_input("Nuevo Precio", value=str(venta[3]))
        nueva_cant = st.text_input("Nueva Cantidad", value=str(venta[4]))
        nueva_fecha = st.text_input("Nueva Fecha (dd-mm-aaaa)", value=venta[5])
        submit = st.form_submit_button("Modificar venta")

        if submit:
            try:
                venta[0] = int(nuevo_id)
                venta[1] = nueva_cat if nueva_cat else venta[1]
                venta[2] = nuevo_prod if nuevo_prod else venta[2]
                venta[3] = float(nuevo_precio)
                venta[4] = int(nueva_cant)
                # Validación de fecha simple
                try:
                    d, m, a = map(int, nueva_fecha.split("-"))
                    if validar_fecha(d, m, a):
                        venta[5] = nueva_fecha
                    else:
                        st.warning("Fecha inválida, se mantiene la anterior.")
                except:
                    st.warning("Formato de fecha inválido, se mantiene la anterior.")
                st.success("Venta modificada correctamente.")
            except Exception as e:
                st.error(f"Error al modificar la venta: {e}")

def eliminar_venta(matriz_ventas):
    st.header("Eliminar Venta")
    if not matriz_ventas:
        st.warning("No hay ventas registradas.")
        return

    ids = [venta[0] for venta in matriz_ventas]
    id_eliminar = st.number_input("Ingrese el ID de la venta a eliminar", min_value=1, step=1)
    if id_eliminar not in ids:
        st.info("Ingrese un ID presente en la tabla de ventas.")
        return

    index = ids.index(id_eliminar)
    venta = matriz_ventas[index]
    st.write("Venta a eliminar:")
    st.write(f"ID: {venta[0]}, Categoría: {venta[1]}, Producto: {venta[2]}, Precio: {venta[3]}, Cantidad: {venta[4]}, Fecha: {venta[5]}")
    if st.button("Confirmar eliminación"):
        matriz_ventas.pop(index)
        st.success("Venta eliminada correctamente.")

def mostrar_ventas(matriz_ventas):
    st.header("Ventas Registradas")
    if not matriz_ventas:
        st.info("No hay ventas registradas.")
        return
    import pandas as pd
    df = pd.DataFrame(matriz_ventas, columns=["ID", "Categoría", "Producto", "Precio", "Cantidad", "Fecha"])
    st.dataframe(df)

def total_ingresos(matriz_ventas):
    total = sum(venta[3] * venta[4] for venta in matriz_ventas)
    return total

def total_prod_cat_vend(matriz_ventas, categoria):
    total = sum(venta[4] for venta in matriz_ventas if categoria.lower() == venta[1].lower())
    return total

def productos_por_categoria(matriz_ventas):
    st.header("Cantidad de productos vendidos por categoría")
    categoria = st.text_input("Ingrese la categoría")
    if categoria:
        total = total_prod_cat_vend(matriz_ventas, categoria)
        st.info(f"Productos vendidos en '{categoria}': {total}")

def promedio_por_ventas_en_fecha(matriz_ventas):
    st.header("Promedio de ingresos por fecha")
    fecha = st.text_input("Ingrese la fecha a consultar (dd-mm-aaaa)")
    if fecha:
        total_ingresos_fecha = 0
        cantidad_ventas = 0
        for venta in matriz_ventas:
            if venta[5] == fecha:
                ingreso = venta[3] * venta[4]
                total_ingresos_fecha += ingreso
                cantidad_ventas += 1
        if cantidad_ventas > 0:
            promedio = total_ingresos_fecha / cantidad_ventas
            st.info(f"Ventas en {fecha}: {cantidad_ventas}\nIngresos totales: ${total_ingresos_fecha:.2f}\nPromedio de ventas: ${promedio:.2f}")
        else:
            st.warning(f"No se registraron ventas en la fecha {fecha}.")

def mostrar_ingresos_totales(matriz_ventas):
    st.header("Ingresos Totales")
    ingresos = total_ingresos(matriz_ventas)
    st.info(f"Total de ingresos generados: ${ingresos:.2f}")

def main():
    st.set_page_config(page_title="Gestionador de Ventas Online", layout="centered")
    st.title("Gestionador de Ventas Online")
    st.caption("Demo interactiva para portfolio con Streamlit")

    if "matriz_ventas" not in st.session_state:
        st.session_state.matriz_ventas = []

    menu = st.sidebar.selectbox(
        "Menú Principal",
        [
            "Cargar Ventas",
            "Modificar Venta",
            "Eliminar Venta",
            "Ver Ventas",
            "Productos por Categoría",
            "Ingresos Totales",
            "Promedio de Ingresos por Fecha",
        ]
    )
    if menu == "Cargar Ventas":
        cargar_ventas(st.session_state.matriz_ventas)
    elif menu == "Modificar Venta":
        modificar_venta(st.session_state.matriz_ventas)
    elif menu == "Eliminar Venta":
        eliminar_venta(st.session_state.matriz_ventas)
    elif menu == "Ver Ventas":
        mostrar_ventas(st.session_state.matriz_ventas)
    elif menu == "Productos por Categoría":
        productos_por_categoria(st.session_state.matriz_ventas)
    elif menu == "Ingresos Totales":
        mostrar_ingresos_totales(st.session_state.matriz_ventas)
    elif menu == "Promedio de Ingresos por Fecha":
        promedio_por_ventas_en_fecha(st.session_state.matriz_ventas)

if __name__ == "__main__":
    main()
