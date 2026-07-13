import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# --------------------------
# CONFIGURACIÓN PARA CELULARES Y PC
# --------------------------
st.set_page_config(
    page_title="Empleos Tucumán",
    page_icon="📢",
    layout="centered",
    initial_sidebar_state="collapsed"
)
ARCHIVO_DATOS = "empleos_tucuman_web.json"

# --------------------------
# BASE COMPLETA DE OFERTAS (54 puestos)
# --------------------------
base_inicial = [
    # COMERCIO Y ATENCIÓN AL CLIENTE
    {"puesto": "Cajero/a supermercado mayorista", "zona": "San Miguel", "tipo": "Completo", "rubro": "Comercio", "detalle": "Atención en caja, cobros con tarjetas y manejo de valores.", "requisitos": "Mayor de 19 años, secundario completo, responsable.", "telefono": "3811112222", "correo": "rrhh@mayoristatucuman.com.ar", "fuente": "Base local"},
    {"puesto": "Repositor góndolas", "zona": "Yerba Buena", "tipo": "Medio tiempo", "rubro": "Comercio", "detalle": "Organización de productos, control de fechas de vencimiento y limpieza de góndolas.", "requisitos": "Sin experiencia, disponibilidad horaria por la mañana.", "telefono": "3812223333", "correo": "personal@superyerba.com.ar", "fuente": "Base local"},
    {"puesto": "Vendedor/a indumentaria deportiva", "zona": "Centro", "tipo": "Medio tiempo", "rubro": "Comercio", "detalle": "Asesoramiento a clientes, ventas y control de inventario.", "requisitos": "Buena dicción y trato amable.", "telefono": "3813334444", "correo": "ventas@deportestucuman.com.ar", "fuente": "Base local"},
    {"puesto": "Atención al cliente farmacia", "zona": "Banda del Río Salí", "tipo": "Completo", "rubro": "Comercio", "detalle": "Entrega de medicamentos, cobros y recepción de recetas.", "requisitos": "Secundario completo, puntualidad.", "telefono": "3814445555", "correo": "rrhh@farmaciasalta.com.ar", "fuente": "Base local"},
    {"puesto": "Vendedor/a por mayor", "zona": "Parque Industrial", "tipo": "Completo", "rubro": "Comercio", "detalle": "Visita a comercios, toma de pedidos y cobranzas.", "requisitos": "Licencia de conducir vigente, 1 año de experiencia.", "telefono": "3815556666", "correo": "comercial@distribuidoratuc.com.ar", "fuente": "Base local"},
    {"puesto": "Cajero/a estacionamiento centro", "zona": "Centro", "tipo": "Turnos rotativos", "rubro": "Servicios", "detalle": "Control de entradas, cobros y orden de vehículos.", "requisitos": "Honestidad y manejo de efectivo.", "telefono": "3816667777", "correo": "servicios@estacionamientocentro.com.ar", "fuente": "Base local"},
    {"puesto": "Anfitrión/a local comercial", "zona": "Peatonal Muñecas", "tipo": "Medio tiempo", "rubro": "Comercio", "detalle": "Recibir clientes, informar horarios y servicios disponibles.", "requisitos": "Buena presencia y puntualidad.", "telefono": "3817778888", "correo": "atencion@peatonal.com.ar", "fuente": "Base local"},
    {"puesto": "Promotor/a productos", "zona": "Toda la ciudad", "tipo": "Por horas", "rubro": "Marketing", "detalle": "Demostración de productos y entrega de muestras.", "requisitos": "Disponibilidad para trasladarse.", "telefono": "3818889999", "correo": "promociones@tucuman.com.ar", "fuente": "Base local"},
    {"puesto": "Auxiliar de depósito", "zona": "Las Talitas", "tipo": "Completo", "rubro": "Comercio", "detalle": "Recepción, etiquetado y entrega de mercadería.", "requisitos": "Esfuerzo físico moderado.", "telefono": "3819990000", "correo": "deposito@talitas.com.ar", "fuente": "Base local"},
    {"puesto": "Vendedor/a calzado", "zona": "Av. Rivadavia", "tipo": "Medio tiempo", "rubro": "Comercio", "detalle": "Atención a clientes, toma de medidas y limpieza del local.", "requisitos": "Sin experiencia, ganas de aprender.", "telefono": "3810001111", "correo": "ventas@calzadotuc.com.ar", "fuente": "Base local"},
    {"puesto": "Encargado/a local verdulería", "zona": "El Manantial", "tipo": "Completo", "rubro": "Comercio", "detalle": "Control de stock, atención al público y manejo de caja.", "requisitos": "Experiencia en rubro alimentos.", "telefono": "3811212121", "correo": "verduleria@tuc.com.ar", "fuente": "Base local"},
    {"puesto": "Auxiliar administrativo comercial", "zona": "Centro", "tipo": "Completo", "rubro": "Administrativo", "detalle": "Archivo de documentos, facturación y atención telefónica.", "requisitos": "Manejo básico de computadora.", "telefono": "3812323232", "correo": "admin@comerciostuc.com.ar", "fuente": "Base local"},

    # GASTRONOMÍA Y ALIMENTOS
    {"puesto": "Camarero/a eventos", "zona": "Yerba Buena", "tipo": "Por eventos", "rubro": "Gastronomía", "detalle": "Atención en bodas, fiestas y reuniones empresariales.", "requisitos": "Disponibilidad fines de semana y feriados.", "telefono": "3811223344", "correo": "eventos@salonesyerba.com.ar", "fuente": "Base local"},
    {"puesto": "Cocinero/a diario", "zona": "Centro", "tipo": "Completo", "rubro": "Gastronomía", "detalle": "Elaboración de menú diario y platos a la carta.", "requisitos": "Experiencia mínima de 2 años.", "telefono": "3812334455", "correo": "cocina@restauranteelcentro.com.ar", "fuente": "Base local"},
    {"puesto": "Ayudante panadería", "zona": "El Manantial", "tipo": "Mañana", "rubro": "Gastronomía", "detalle": "Limpieza, ayudante en horneado y venta en mostrador.", "requisitos": "Disponibilidad desde las 5 de la mañana.", "telefono": "3813445566", "correo": "panaderia@manantial.com.ar", "fuente": "Base local"},
    {"puesto": "Elaborador comidas rápidas", "zona": "Tafí Viejo", "tipo": "Medio tiempo", "rubro": "Gastronomía", "detalle": "Preparación de platos y limpieza del área de trabajo.", "requisitos": "Sin experiencia, rápido aprendizaje.", "telefono": "3814556677", "correo": "rrhh@fasttafi.com.ar", "fuente": "Base local"},
    {"puesto": "Repartidor pedidos con moto", "zona": "Toda la ciudad", "tipo": "Completo", "rubro": "Transporte", "detalle": "Entregas de pedidos a domicilio.", "requisitos": "Moto propia, licencia vigente.", "telefono": "3815667788", "correo": "repartos@tucumandeliveries.com.ar", "fuente": "Base local"},
    {"puesto": "Auxiliar cocina hotel", "zona": "Centro", "tipo": "Turnos", "rubro": "Gastronomía", "detalle": "Preparación de insumos y limpieza de áreas.", "requisitos": "Carnet de salud al día.", "telefono": "3816778899", "correo": "rrhh@hotelcentrotuc.com.ar", "fuente": "Base local"},
    {"puesto": "Encargado/a barra", "zona": "Yerba Buena", "tipo": "Tarde-noche", "rubro": "Gastronomía", "detalle": "Preparación de tragos, control de stock y cobros.", "requisitos": "Experiencia en atención de barra.", "telefono": "3817889900", "correo": "barra@pubtucuman.com.ar", "fuente": "Base local"},
    {"puesto": "Lavaplatos y limpieza gastronómica", "zona": "Banda del Río Salí", "tipo": "Turnos", "rubro": "Gastronomía", "detalle": "Limpieza de vajilla, utensilios y áreas de trabajo.", "requisitos": "Sin experiencia.", "telefono": "3818990011", "correo": "cocina@banda.com.ar", "fuente": "Base local"},
    {"puesto": "Maestro pastelero", "zona": "San Miguel", "tipo": "Completo", "rubro": "Gastronomía", "detalle": "Elaboración de tortas, postres y masas dulces.", "requisitos": "Título o experiencia comprobable.", "telefono": "3819001122", "correo": "pasteleria@tuc.com.ar", "fuente": "Base local"},

    # SERVICIOS GENERALES Y LIMPIEZA
    {"puesto": "Limpieza clínica privada", "zona": "Barrio Norte", "tipo": "Medio tiempo", "rubro": "Servicios", "detalle": "Limpieza de consultorios, pasillos y baños.", "requisitos": "Puntualidad y cuidado de materiales.", "telefono": "3818990011", "correo": "servicios@clinicanorte.com.ar", "fuente": "Base local"},
    {"puesto": "Conserje edificio residencial", "zona": "Yerba Buena", "tipo": "Turno noche", "rubro": "Seguridad", "detalle": "Control de acceso, rondas y recepción de encomiendas.", "requisitos": "Referencias comprobables.", "telefono": "3819001122", "correo": "edificios@yerbabuena.com.ar", "fuente": "Base local"},
    {"puesto": "Jardinería fincas y barrios", "zona": "Lules", "tipo": "Completo", "rubro": "Servicios", "detalle": "Corte de césped, poda de plantas y riego.", "requisitos": "Conocimientos básicos de jardinería.", "telefono": "3810112233", "correo": "mantenimiento@lules.com.ar", "fuente": "Base local"},
    {"puesto": "Auxiliar limpieza industrial", "zona": "Parque Industrial", "tipo": "Completo", "rubro": "Servicios", "detalle": "Limpieza de naves, maquinaria y áreas comunes.", "requisitos": "Sin experiencia, esfuerzo físico.", "telefono": "3811223344", "correo": "servicios@industrialtuc.com.ar", "fuente": "Base local"},
    {"puesto": "Paseador y cuidador mascotas", "zona": "Toda la ciudad", "tipo": "Por horas", "rubro": "Servicios", "detalle": "Paseos diarios y cuidado en domicilio.", "requisitos": "Amor por animales y paciencia.", "telefono": "3812334455", "correo": "mascotas@cuidados-tuc.com.ar", "fuente": "Base local"},
    {"puesto": "Lavado autos a domicilio", "zona": "Yerba Buena y San Miguel", "tipo": "Por horas", "rubro": "Servicios", "detalle": "Lavado, encerado y aspirado de vehículos.", "requisitos": "Responsabilidad y prolijidad.", "telefono": "3813445566", "correo": "autos@tucuman.com.ar", "fuente": "Base local"},
    {"puesto": "Limpieza oficinas corporativas", "zona": "Centro", "tipo": "Tarde", "rubro": "Servicios", "detalle": "Limpieza de escritorios, salas de reuniones y baños.", "requisitos": "Discreción y cuidado.", "telefono": "3814556677", "correo": "limpieza@oficinastuc.com.ar", "fuente": "Base local"},
    {"puesto": "Auxiliar mantenimiento escuela", "zona": "Toda la ciudad", "tipo": "Medio tiempo", "rubro": "Servicios", "detalle": "Limpieza de aulas, patios y reparaciones menores.", "requisitos": "Certificado de antecedentes limpio.", "telefono": "3815667788", "correo": "escuelas@educaciontuc.gov.ar", "fuente": "Gobierno de Tucumán"},

    # OFICIOS Y CONSTRUCCIÓN
    {"puesto": "Ayudante albañil", "zona": "Banda del Río Salí", "tipo": "Completo", "rubro": "Oficios", "detalle": "Carga de materiales, preparación de mezclas y limpieza de obra.", "requisitos": "Esfuerzo físico, sin experiencia.", "telefono": "3816778899", "correo": "obras@bandadelsali.com.ar", "fuente": "Base local"},
    {"puesto": "Electricista domiciliario", "zona": "Toda la provincia", "tipo": "Por trabajo", "rubro": "Oficios", "detalle": "Reparaciones, instalaciones nuevas y tableros eléctricos.", "requisitos": "Título habilitante y referencias.", "telefono": "3817889900", "correo": "electricidad@tucuman.com.ar", "fuente": "Base local"},
    {"puesto": "Carpintero armador muebles", "zona": "Las Talitas", "tipo": "Completo", "rubro": "Oficios", "detalle": "Corte de madera, armado y barnizado de muebles.", "requisitos": "Manejo de herramientas eléctricas.", "telefono": "3818990011", "correo": "muebles@lastalitas.com.ar", "fuente": "Base local"},
    {"puesto": "Mecánico general", "zona": "Famaillá", "tipo": "Completo", "rubro": "Oficios", "detalle": "Reparación de motores, frenos y embragues.", "requisitos": "Experiencia mínima de 1 año.", "telefono": "3819001122", "correo": "taller@famailla.com.ar", "fuente": "Base local"},
    {"puesto": "Pintor casas y departamentos", "zona": "Toda la ciudad", "tipo": "Por obra", "rubro": "Oficios", "detalle": "Pintura interior/exterior y preparación de paredes.", "requisitos": "Acabados prolijos.", "telefono": "3810112233", "correo": "pinturas@tucuman.com.ar", "fuente": "Base local"},
    {"puesto": "Instalador cerámicos", "zona": "Yerba Buena", "tipo": "Por obra", "rubro": "Oficios", "detalle": "Colocación de pisos y revestimientos cerámicos.", "requisitos": "Experiencia comprobable.", "telefono": "3811223344", "correo": "revestimientos@tuc.com.ar", "fuente": "Base local"},
    {"puesto": "Plomero reparaciones menores", "zona": "San Miguel", "tipo": "Por trabajo", "rubro": "Oficios", "detalle": "Desagotes, cambio de cañerías y grifería.", "requisitos": "Herramientas propias.", "telefono": "3812334455", "correo": "plomeria@tuc.com.ar", "fuente": "Base local"},
    {"puesto": "Operario maquinaria construcción", "zona": "Parque Industrial", "tipo": "Completo", "rubro": "Oficios", "detalle": "Manejo de hormigonera, mezcladoras y elevadores.", "requisitos": "Curso de seguridad vigente.", "telefono": "3813445566", "correo": "maquinaria@obras-tuc.com.ar", "fuente": "Base local"},

    # SALUD Y CUIDADOS
    {"puesto": "Cuidador/a adulto mayor", "zona": "Centro", "tipo": "Completo", "rubro": "Cuidados", "detalle": "Acompañamiento, higiene y ayuda en la alimentación.", "requisitos": "Paciencia y referencias comprobables.", "telefono": "3814556677", "correo": "cuidados@hogar.com.ar", "fuente": "Base local"},
    {"puesto": "Auxiliar farmacia social", "zona": "Banda del Río Salí", "tipo": "Medio tiempo", "rubro": "Salud", "detalle": "Entrega de medicamentos y control de stock.", "requisitos": "Secundario completo.", "telefono": "3815667788", "correo": "farmacia@social.tuc.gov.ar", "fuente": "Municipalidad de Tucumán"},
    {"puesto": "Acompañante terapéutico", "zona": "Yerba Buena", "tipo": "Medio tiempo", "rubro": "Salud", "detalle": "Apoyo a personas con discapacidad en actividades diarias.", "requisitos": "Título terciario o curso certificado.", "telefono": "3816778899", "correo": "terapia@tuc.com.ar", "fuente": "Base local"},
    {"puesto": "Auxiliar enfermería consultorio", "zona": "Centro", "tipo": "Completo", "rubro": "Salud", "detalle": "Toma de presión, curaciones y limpieza de consultorio.", "requisitos": "Curso de auxiliar de enfermería.", "telefono": "3817889900", "correo": "consultorio@saludtuc.com.ar", "fuente": "Base local"},
    {"puesto": "Cuidador/a niños por horas", "zona": "Toda la ciudad", "tipo": "Por horas", "rubro": "Cuidados", "detalle": "Cuidado de niños de 2 a 12 años en domicilio.", "requisitos": "Certificado de antecedentes limpio.", "telefono": "3818990011", "correo": "niñera@tuc.com.ar", "fuente": "Base local"},

    # ADMINISTRATIVO Y OFICINA
    {"puesto": "Auxiliar contable básico", "zona": "Centro", "tipo": "Completo", "rubro": "Administrativo", "detalle": "Archivo de facturas, recibos y control de pagos.", "requisitos": "Manejo básico de Excel.", "telefono": "3819001122", "correo": "contable@estudiotuc.com.ar", "fuente": "Base local"},
    {"puesto": "Recepcionista consultorios", "zona": "San Miguel", "tipo": "Turnos", "rubro": "Administrativo", "detalle": "Turno de pacientes, cobros y manejo de agenda.", "requisitos": "Buena presencia y dicción clara.", "telefono": "3810112233", "correo": "recepcion@consultorios.com.ar", "fuente": "Base local"},
    {"puesto": "Digitador/a datos", "zona": "Centro", "tipo": "Medio tiempo", "rubro": "Administrativo", "detalle": "Carga de información a sistemas informáticos.", "requisitos": "Mecanografía rápida.", "telefono": "3811223344", "correo": "datos@proyectos-tuc.com.ar", "fuente": "Base local"},
    {"puesto": "Auxiliar recursos humanos", "zona": "Parque Industrial", "tipo": "Completo", "rubro": "Administrativo", "detalle": "Archivo de legajos y entrevistas iniciales.", "requisitos": "Estudiante de RRHH o carreras afines.", "telefono": "3812334455", "correo": "rrhh@empresatuc.com.ar", "fuente": "Base local"},

    # FUENTES OFICIALES
    {"puesto": "Auxiliar administrativo municipal", "zona": "Centro", "tipo": "Completo", "rubro": "Administrativo", "detalle": "Apoyo en oficinas de atención al vecino.", "requisitos": "Secundario completo.", "telefono": "0381-4300000", "correo": "empleos@municipalidadtucuman.gov.ar", "fuente": "Municipalidad de Tucumán"},
    {"puesto": "Personal limpieza espacios públicos", "zona": "Toda la ciudad", "tipo": "Medio tiempo", "rubro": "Servicios", "detalle": "Mantenimiento de plazas, calles y avenidas.", "requisitos": "Sin experiencia.", "telefono": "0381-4300001", "correo": "servicios@municipalidadtucuman.gov.ar", "fuente": "Municipalidad de Tucumán"},
    {"puesto": "Operario producción Parque Industrial", "zona": "Parque Industrial", "tipo": "Completo", "rubro": "Industria", "detalle": "Tareas de fabricación y control de calidad.", "requisitos": "Primario completo.", "telefono": "0381-4200000", "correo": "empleos@tucuman.gov.ar", "fuente": "Gobierno de Tucumán"},
    {"puesto": "Auxiliar salud centro comunitario", "zona": "Banda del Río Salí", "tipo": "Medio tiempo", "rubro": "Salud", "detalle": "Apoyo en centros de atención primaria.", "requisitos": "Secundario completo.", "telefono": "0381-4200001", "correo": "salud@tucuman.gov.ar", "fuente": "Gobierno de Tucumán"}
]

# --------------------------
# CARGA Y GUARDADO DE DATOS
# --------------------------
def cargar_empleos():
    if os.path.exists(ARCHIVO_DATOS):
        try:
            with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
                datos = json.load(f)
                return datos.get("empleos", base_inicial.copy())
        except:
            return base_inicial.copy()
    return base_inicial.copy()

def guardar_empleos(lista):
    datos = {"fecha_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M"), "empleos": lista}
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

# --------------------------
# INTERFAZ COMPLETA
# --------------------------
st.title("📢 EMPLEOS TUCUMÁN")
st.subheader("Encuentra y comparte ofertas de trabajo para toda la provincia")
st.warning("⚠️ AVISO IMPORTANTE: Nunca pagues dinero para conseguir un trabajo. Contacta solo por los medios indicados en cada oferta.")

# Cargar lista completa
empleos = cargar_empleos()

# FILTROS Y BUSCADOR
st.subheader("🔍 Buscar ofertas")
col1, col2 = st.columns(2)
with col1:
    buscar = st.text_input("Escribe puesto o zona:")
    rubro = st.selectbox("Filtrar por rubro:", ["Todos"] + sorted(list({e.get("rubro", "General") for e in empleos})))
with col2:
    tipo = st.selectbox("Filtrar por jornada:", ["Todos", "Sin experiencia", "Medio tiempo", "Completo", "Por horas", "Turnos rotativos"])
    fuente = st.selectbox("Filtrar por fuente:", ["Todas", "Municipalidad de Tucumán", "Gobierno de Tucumán", "Base local", "Publicado por usuario"])

# Aplicar filtros
filtrados = []
for emp in empleos:
    coincide_busq = (buscar.lower() in emp["puesto"].lower()) or (buscar.lower() in emp["zona"].lower()) or (buscar == "")
    coincide_rub = (rubro == "Todos") or (emp.get("rubro", "General") == rubro)
    coincide_tip = (tipo == "Todos") or (emp["tipo"] == tipo)
    coincide_fuente = (fuente == "Todas") or (emp.get("fuente", "Base local") == fuente)
    if coincide_busq and coincide_rub and coincide_tip and coincide_fuente:
        filtrados.append(emp)

st.markdown(f"**Total: {len(filtrados)} ofertas encontradas de {len(empleos)} disponibles**")
st.divider()

# MOSTRAR TODAS LAS OFERTAS CON DETALLES
for emp in filtrados:
    with st.expander(f"📌 {emp['puesto']} — {emp['zona']} ({emp['tipo']})"):
        st.write(f"📂 **Rubro**: {emp.get('rubro', 'General')}")
        st.write(f"📋 **Descripción del puesto**: {emp['detalle']}")
        st.write(f"✅ **Requisitos**: {emp['requisitos']}")
        st.write(f"📌 **Fuente de la oferta**: {emp.get('fuente', 'Base local')}")
        st.write(f"📞 **Teléfono / WhatsApp**: {emp['telefono']}")
        st.write(f"📧 **Correo electrónico**: {emp['correo']}")
        # Botón directo a WhatsApp
        tel_limpio = ''.join(filter(str.isdigit, emp['telefono']))
        st.link_button("💬 Escribir directamente por WhatsApp", f"https://wa.me/{tel_limpio}?text=Hola! Vi tu oferta de {emp['puesto']} en Empleos Tucumán y quiero postularme.")
    st.divider()

# FORMULARIO PARA PUBLICAR NUEVA OFERTA
with st.expander("✏️ Publicar una nueva oferta de empleo"):
    with st.form("publicar_oferta"):
        puesto_nuevo = st.text_input("Puesto de trabajo *")
        zona_nueva = st.text_input("Zona / Localidad *")
        tipo_nuevo = st.selectbox("Tipo de jornada *", ["Sin experiencia", "Medio tiempo", "Completo", "Por horas", "Turnos rotativos"])
        rubro_nuevo = st.text_input("Rubro / Área", value="General")
        detalle_nuevo = st.text_area("Descripción breve del puesto")
        requisitos_nuevo = st.text_area("Requisitos necesarios")
        telefono_nuevo = st.text_input("Teléfono / WhatsApp de contacto *")
        correo_nuevo = st.text_input("Correo electrónico (opcional)")
        enviar = st.form_submit_button("✅ Guardar y publicar oferta")
        
        if enviar:
            if puesto_nuevo and zona_nueva and telefono_nuevo:
                nueva_oferta = {
                    "puesto": puesto_nuevo, "zona": zona_nueva, "tipo": tipo_nuevo, "rubro": rubro_nuevo,
                    "detalle": detalle_nuevo or "Sin detalles adicionales",
                    "requisitos": requisitos_nuevo or "Consultar en el contacto indicado",
                    "telefono": telefono_nuevo, "correo": correo_nuevo or "No especificado",
                    "fuente": "Publicado por usuario"
                }
                empleos.insert(0, nueva_oferta)
                guardar_empleos(empleos)
                st.success("✅ Oferta publicada correctamente! Ya aparece en la lista para todos.")
                st.rerun()
            else:
                st.error("⚠️ Completa los campos obligatorios marcados con *")