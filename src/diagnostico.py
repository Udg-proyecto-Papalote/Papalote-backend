import requests
import librosa
import numpy as np
import json
import os
import tempfile

# Texto de referencia y URL fijos
TEXT_REFERENCIA = """
aquí no es Miami, los primeros reportes de actividad aeronáutica irregular detectada sobre los municipios del sotavento veracruz boca del río alvarado y tlalixcoyan principalmente datan de finales de los años ochenta. los habitantes de las zonas agrestes dedicados principalmente a la pesca y la cría de ganado estaban ya habituados a la presencia de las luces nocturnas. los más viejos las llamaban brujas, los más informados avionetas. incluso conocían el lugar en donde las luces descendían: el llano de la víbora, una brecha natural bordeada de matorrales y espinos que el ejército y la policía judicial federal empleaban a menudo como pista de aterrizaje.

en esa planicie natural que se elevaba entre charcas y esteros, la presencia de soldados y agentes federales era algo común para los habitantes de la zona. después de todo, la pista de la víbora era usada por las fuerzas armadas para realizar maniobras especiales. por ello, a nadie le extrañó que a finales de octubre de mil novecientos noventa y uno llegaran cuadrillas de soldados a tusar la maleza tupida a golpe de machete y limpiar el sendero de obstáculos.

pero justo una semana después, la mañana del siete de noviembre de ese mismo año, el ejército, las autoridades federales y una avioneta cessna de origen colombiano se vieron envueltos en un sangriento escándalo que logró burlar el apretado cerco de censura del gobierno. integrantes del batallón de infantería del ejército abrieron fuego contra un grupo de agentes de la procuraduría que habían llegado a la víbora supuestamente a detener a los tripulantes de una avioneta de procedencia colombiana que había sido detectada desde las costas de nicaragua por el servicio de aduanas estadounidense. la avioneta cessna, supuestamente tripulada por traficantes colombianos, aterrizó sobre el llano de la víbora en la mañana de aquel siete de noviembre, seguida de los judiciales. los tripulantes de la avioneta, un hombre afroamericano y una mujer rubia, según los testimonios, abandonaron su cargamento de trescientos cincuenta y cinco kilos de cocaína en costales y desaparecieron en el monte, mientras que los soldados del batallón de infantería, apostados en dos columnas a lo largo de la pista, aguardaron a que los agentes federales descendieran de su aeronave para abrir fuego contra ellos para neutralizarlos.

de aquel suceso recuerdo dos fotos que aparecieron en el periódico local notiver. en una de ellas, siete hombres yacían en hilera sobre el pasto, boca abajo. eran los agentes acribillados por el ejército. cinco de ellos vestían ropas oscuras y los otros dos iban de paisano, y aunque portaban chamarras negras sucias de tierra y zacate, ninguno llevaba zapatos. la segunda fotografía mostraba a un agente federal sentado en el suelo con el cañón de un fusil anónimo apuntándole a la cabeza. el sujeto, que portaba las siglas de la procuraduría en el pecho, miraba directo hacia la lente. sus labios, congelados a mitad de un espasmo de angustia, dejaban entrever una lengua hinchada y reseca: se trataba del único judicial que había sobrevivido al ataque.

era diciembre, o quizás enero o febrero, cuando vi aquellas fotos impresas en una de las páginas de aquel periódico viejo que extendí en el suelo para recoger la hojarasca que pasé la tarde barriendo en el patio. y digo que debió haber sido en estas fechas, porque es la única época del año en que los frentes fríos dejan desnudas las copas, para entonces anaranjadas, de los almendros tropicales en el puerto. me recuerdo acuclillada en aquel patio, mirando las imágenes y leyendo con curiosidad las noticias de la sección policiaca extendida sobre el suelo de cemento, pero tuvieron que pasar más de diez años para que yo pudiera relacionar aquellas dos imágenes: la fotografía de los judiciales muertos y el recuerdo de las extrañas luces de colores que vi en el cielo el verano en que cumplí nueve años y concluir con tristeza que aquel objeto volador no identificado nunca transportó ningún extraterrestre sino puras pacas de cocaína colombiana.

después del tiroteo de la víbora y de otros incidentes semejantes ocurridos en nopaltepec, cosamaloapan y carlos a. carillo, y de varios accidentes automovilísticos protagonizados por adolescentes borrachos, el gobierno de boca del río prohibió las visitas nocturnas a las playas durante algunos meses, así que después de esa última y decepcionante visita, no volvimos a playa del muerto sino hasta finales del noventa y dos, y el sitio para entonces había perdido todo su encanto. nuevas escolleras habían ganado terreno al mar y aquello era un hervidero de vendedores ambulantes y turistas. incluso habían retirado los escabrosos letreros con calaveras que advertían de las pozas, y con el tiempo el nombre de playa del muerto cayó en desuso a favor de un apelativo más turístico y mucho menos tétrico: playa los arcos.

creo que jamás en la vida volví a creer en algo con tanta fe como creí en los extraterrestres. ni siquiera en el ratón de los dientes, en santa claus o en el hombre sin cabeza del que mi padre contaba que todas las noches se aparecía en el playón de hornos buscando entre el agua su testa arrancada por un cañonazo durante la invasión estadounidense del catorce; mucho menos en la mantarraya gigante antropófaga voladora de las islas fiji, y más tarde ni siquiera dios se salvaría de mi incredulidad. todo era pura mentira, inventos de los grandes. todos esos seres maravillosos con poderes inauditos no eran más que el fruto de la imaginación de los padres.

dicen los actuales habitantes de la zona que cuando la luna está ausente, extrañas luces de colores aún atraviesan la noche para aterrizar en el llano. pero yo ya no tengo ánimos para buscar extraterrestres. aquella pequeña y regordeta vigilante intergaláctica ya no existe, como tampoco existe playa del muerto ni los valientes idiotas que ahí se ahogaron.
"""
# # Texto de referencia completo
# AUDIO_URL = "https://res.cloudinary.com/dgojg9f9z/video/upload/v1726968889/mmdsvtap8fujbrwsicod.wav"

# genero = "mujer"

def clasificar_tono_voz(pitch_media, genero):
    if genero == "hombre":
        if pitch_media < 118:
            return "grave"
        elif 118 <= pitch_media <= 164:
            return "moderado"
        else:
            return "agudo"
    elif genero == "mujer":
        if pitch_media < 193:
            return "grave"
        elif 193 <= pitch_media <= 236:
            return "moderado"
        else:
            return "agudo"
    else:
        return "género no especificado"

def procesar_audio_desde_url(url, genero):
    # Crear un archivo temporal para el audio
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio_file:
        filename = temp_audio_file.name
        response = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(response.content)

    # Cargar el archivo de audio
    y, sr = librosa.load(filename, sr=None)

    # Verificar si hay contenido en el audio
    if np.all(y == 0):
        return json.dumps({"mensaje": "El audio está vacío o es silencio", "pitch_medio": None, "filename": filename})

    # Encontrar los segmentos de audio no silenciosos
    intervals = librosa.effects.split(y, top_db=20)

    pitches = []
    
    # Analizar cada segmento no silencioso
    for start, end in intervals:
        segment = y[start:end]
        # Calcular el pitch utilizando YIN
        pitch = librosa.yin(segment, fmin=50, fmax=400, sr=sr)

        # Filtrar las frecuencias válidas
        pitches.extend(pitch[pitch > 0])
    
    # Verificar si hay frecuencias válidas
    if len(pitches) > 0:
        pitch_media = np.nanmedian(pitches)
        tono = clasificar_tono_voz(pitch_media, genero)
        return tono, filename
    else:
        return "No se encontraron frecuencias válidas", filename


def transcribir_audio_a_texto(audio_filename):
    import speech_recognition as sr

    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_filename) as source:
        audio = recognizer.record(source)
        try:
            texto_transcrito = recognizer.recognize_google(audio, language="es-MX")
            return texto_transcrito
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            return ""

def limpiar_texto_de_puntuaciones(texto):
    import string
    return texto.translate(str.maketrans('', '', string.punctuation)).lower()

def evaluar_modulacion(total_palabras_transcritas):
    # Evaluar si la modulación es buena (entre 120 y 150 palabras transcritas dividido entre 3)
    promedio_palabras = total_palabras_transcritas / 2
    return 135 <= promedio_palabras <= 150

# def contar_palabras_con_r(palabras_transcrito, palabras_referencia):
#     """
#     Contar cuántas veces se dijo una palabra con 'r' correctamente o incorrectamente.
#     """
#     palabras_con_r_correctas = 0
#     palabras_con_r_incorrectas = 0
#     palabras_con_r_total = 0

#     for palabra_transcrita in palabras_transcrito:
#         if 'r' in palabra_transcrita:
#             palabras_con_r_total += 1
#             if palabra_transcrita in palabras_referencia:
#                 palabras_con_r_correctas += 1
#             else:
#                 palabras_con_r_incorrectas += 1

#     return palabras_con_r_correctas, palabras_con_r_incorrectas, palabras_con_r_total

def evaluar_diccion(texto_transcrito, texto_referencia):
    palabras_transcrito = limpiar_texto_de_puntuaciones(texto_transcrito).split()
    # Limitar el texto de referencia hasta la cantidad de palabras que el usuario haya leído
    palabras_referencia = limpiar_texto_de_puntuaciones(texto_referencia).split()[:len(palabras_transcrito)]
    
    # Convertir a conjunto para evaluar precisión
    palabras_referencia_set = set(palabras_referencia)

    palabras_reconocidas_correctamente = sum(1 for palabra in palabras_transcrito if palabra in palabras_referencia_set)
    total_palabras_transcritas = len(palabras_transcrito)
    palabras_incorrectas = total_palabras_transcritas - palabras_reconocidas_correctamente

    # Evaluar si al menos el 90% de las palabras fueron entendidas correctamente
    buena_diccion = palabras_reconocidas_correctamente >= (total_palabras_transcritas * 0.9)
    
    
    # Contar las palabras con 'r'
    # palabras_con_r_correctas, palabras_con_r_incorrectas, palabras_con_r_total = contar_palabras_con_r(
    #     palabras_transcrito, palabras_referencia_set)

    return {
        "buena_diccion": buena_diccion,
        "palabras_correctas": palabras_reconocidas_correctamente,
        "palabras_incorrectas": palabras_incorrectas,
        "total_palabras_transcritas": total_palabras_transcritas,
        # "palabras_con_r_correctas": palabras_con_r_correctas,
        # "palabras_con_r_incorrectas": palabras_con_r_incorrectas,
        # "palabras_con_r_total": palabras_con_r_total
    }

def generar_recomendaciones(diccion, modulacion, tono):
    recomendaciones_set = set()  # Conjunto para evitar duplicados

    # 1. Evaluar dicción
    if diccion:  # Buena dicción
        recomendaciones_set.add("Palabras de difícil pronunciación I")  # O cualquier ejercicio de dicción que desees agregar
    else:  # Mala dicción
        recomendaciones_set.update([
            "Respiración I",
            "Articulación I",
            "Articulación II",
            "Vocalización I",
            "Vocalización II",
            "Dicción 1",
            "Dicción 2",
            "Dicción 3",
            "Dicción 6",
            "Dicción 7",
            "Dicción 12",
            "Dicción 13",
            "Dicción 15",
            "Letra R I",
            "Letra R II",
            "Letra R III",
            "Palabras de difícil pronunciación I",
            "Palabras de difícil pronunciación II"
        ])

    # 2. Evaluar modulación
    if modulacion:  # Buena modulación
        recomendaciones_set.add("Palabras de difícil pronunciación II")  # O cualquier ejercicio de modulación que desees agregar
    else:  # Mala modulación
        recomendaciones_set.update([
            "Respiración I",
            "Palabras de difícil pronunciación I",
            "Palabras de difícil pronunciación II",
            "Caudal I",
            "Articulación I",
            "Articulación II",
            "Potencia II",
            "Impostación I"
        ])

    # 3. Evaluar tono de voz
    if tono == "tono_alto":  # Tono agudo
        recomendaciones_set.update([
            "Respiración I",
            "Potencia II",
            "Impostación I"
        ])
    elif tono == "tono_moderado":  # Tono moderado
        recomendaciones_set.add("Respiración I")
    elif tono == "tono_bajo":  # Tono grave
        recomendaciones_set.update([
            "Respiración I",
            "Potencia II",
            "Impostación I"
        ])

    # Convertir el conjunto a lista
    recomendaciones_finales = list(recomendaciones_set)

    return recomendaciones_finales  # Devolver la lista de recomendaciones


def procesar_audio_y_generar_json(url, genero):
    tono_voz, audio_filename = procesar_audio_desde_url(url, genero)
    
    # Transcribir el audio
    texto_transcrito = transcribir_audio_a_texto(audio_filename)
    
    resultado_diccion = {}
    buena_modulacion = False
    
    if texto_transcrito:
        resultado_diccion = evaluar_diccion(texto_transcrito, TEXT_REFERENCIA)
        buena_modulacion = evaluar_modulacion(resultado_diccion["total_palabras_transcritas"])
    else:
        resultado_diccion = {
            "buena_diccion": False,
            "palabras_correctas": 0,
            "palabras_incorrectas": 0,
            "total_palabras_transcritas": 0,
            "palabras_con_r_correctas": 0,
            "palabras_con_r_incorrectas": 0,
            "palabras_con_r_total": 0
        }
    
    try:
        # Generar recomendaciones basadas en los resultados
        recomendaciones = generar_recomendaciones(
            diccion=resultado_diccion["buena_diccion"], 
            modulacion=buena_modulacion, 
            tono=tono_voz
        )
    except Exception as e:
        # En caso de error, devolver una lista vacía de recomendaciones
        recomendaciones = []

    resultado = {
        "tono_voz": tono_voz,
        "buena_diccion": resultado_diccion["buena_diccion"],
        "texto_transcrito": texto_transcrito,
        "palabras_correctas": resultado_diccion["palabras_correctas"],
        "palabras_incorrectas": resultado_diccion["palabras_incorrectas"],
        "total_palabras_transcritas": resultado_diccion["total_palabras_transcritas"],
        # "palabras_con_r_correctas": resultado_diccion["palabras_con_r_correctas"],
        # "palabras_con_r_incorrectas": resultado_diccion["palabras_con_r_incorrectas"],
        # "palabras_con_r_total": resultado_diccion["palabras_con_r_total"],
        "buena_modulacion": buena_modulacion,
        "recomendaciones": recomendaciones
    }

    # Eliminar el archivo de audio temporal
    os.remove(audio_filename)

    # Convertir a JSON asegurando que los caracteres especiales se mantengan
    json_resultado = json.dumps(resultado, ensure_ascii=False, indent=4)

    return json_resultado

