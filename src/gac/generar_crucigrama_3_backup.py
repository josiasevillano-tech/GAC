import os
from .generator import Generator
from .web_exporter import WebExporter
from .exporter import Exporter

datos_crucigrama_3 = {
    "title": "GuÃ­a 2 - Pedro: el apÃ³stol que abriÃ³ el camino",
    "tema": "Pedro: el apÃ³stol que abriÃ³ el camino",
    "resena": (
        "Â¿Por quÃ© Pedro ocupa un lugar tan importante en la expansiÃ³n del evangelio? "
        "La respuesta no se encuentra Ãºnicamente en que fue uno de los doce apÃ³stoles, sino en el papel "
        "que Dios le asignÃ³ dentro de su plan para llevar el mensaje de salvaciÃ³n a todas las naciones.<br><br>"
        "Pedro, llamado originalmente SimÃ³n, era un pescador de Betsaida. Su hermano AndrÃ©s fue quien lo condujo "
        "por primera vez a JesÃºs, y fue entonces cuando el SeÃ±or le anunciÃ³ que serÃ­a llamado Cefas (Pedro), "
        "nombre que significa 'piedra' (Jn. 1:40-42). MÃ¡s adelante, mientras trabajaba en las aguas del mar de Galilea, "
        "JesÃºs lo llamÃ³ a dejar sus redes con una promesa extraordinaria: Â«Venid en pos de mÃ­, y os harÃ© pescadores "
        "de hombresÂ» (Mt. 4:18-20). A partir de ese momento comenzÃ³ un proceso de formaciÃ³n que transformarÃ­a profundamente su vida.<br><br>"
        "Durante el ministerio de JesÃºs, Pedro fue uno de los discÃ­pulos mÃ¡s cercanos al Maestro. PresenciÃ³ acontecimientos "
        "extraordinarios y participÃ³ en momentos decisivos, como la resurrecciÃ³n de la hija de Jairo, la transfiguraciÃ³n "
        "y la oraciÃ³n en GetsemanÃ­ (Mr. 5:37; Mt. 17:1-8; Mt. 26:36-38). Cuando JesÃºs preguntÃ³ a sus discÃ­pulos quiÃ©n creÃ­an "
        "ellos que era, Pedro respondiÃ³ con una de las confesiones mÃ¡s importantes del Nuevo Testamento: Â«TÃº eres el Cristo, "
        "el Hijo del Dios vivienteÂ» (Mt. 16:16). Esa declaraciÃ³n expresÃ³ una verdad fundamental acerca de la identidad de JesÃºs, "
        "aunque Pedro todavÃ­a no comprendÃ­a plenamente el alcance de la misiÃ³n del MesÃ­as.<br><br>"
        "Esa comprensiÃ³n incompleta quedÃ³ en evidencia durante las Ãºltimas horas antes de la crucifixiÃ³n. DespuÃ©s del arresto "
        "de JesÃºs, Pedro no huyÃ³. Por el contrario, siguiÃ³ al Maestro hasta el patio del sumo sacerdote y permaneciÃ³ allÃ­ "
        "mientras se desarrollaba el juicio (Jn. 18:15-16). Ante sus ojos, el panorama resultaba desconcertante: aquel que "
        "habÃ­a manifestado autoridad sobre la enfermedad, la naturaleza y la muerte aceptaba voluntariamente ser arrestado "
        "y condenado sin ofrecer resistencia. En medio de esa crisis, Pedro negÃ³ conocer a JesÃºs en tres ocasiones (Jn. 18:17, 25-27). "
        "MÃ¡s que un simple acto de cobardÃ­a, este episodio refleja el profundo conflicto de un discÃ­pulo cuya comprensiÃ³n del plan "
        "de Dios estaba siendo confrontada por una realidad que aÃºn no alcanzaba a entender.<br><br>"
        "DespuÃ©s de la resurrecciÃ³n, JesÃºs restaurÃ³ pÃºblicamente a Pedro y le encomendÃ³ la responsabilidad de cuidar de sus "
        "seguidores (Jn. 21:15-19). A partir de entonces, y fortalecido por la venida del EspÃ­ritu Santo, Pedro comprendiÃ³ con "
        "mayor claridad el significado de la muerte y resurrecciÃ³n de Cristo. Esa comprensiÃ³n transformÃ³ su ministerio y le "
        "permitiÃ³ proclamar el evangelio con firmeza.<br><br>"
        "El dÃ­a de PentecostÃ©s pronunciÃ³ el primer gran sermÃ³n de la Iglesia (Hch. 2:14-41). Su mensaje anunciÃ³ que JesÃºs, "
        "crucificado y resucitado, es el MesÃ­as prometido y el Ãºnico Salvador. Miles de personas respondieron con fe, y la iglesia "
        "comenzÃ³ a crecer bajo la direcciÃ³n del EspÃ­ritu Santo.<br><br>"
        "Sin embargo, la contribuciÃ³n mÃ¡s trascendental de Pedro fue abrir el camino para que el evangelio llegara oficialmente "
        "a los gentiles. Dios preparÃ³ este momento mediante una visiÃ³n que desafiÃ³ muchas de las ideas que Pedro habÃ­a heredado "
        "de su formaciÃ³n judÃ­a (Hch. 10:9-16). Poco despuÃ©s fue enviado a la casa del centuriÃ³n Cornelio, donde presenciÃ³ cÃ³mo "
        "el EspÃ­ritu Santo descendÃ­a tambiÃ©n sobre personas no judÃ­as (Hch. 10:34-48). AllÃ­ comprendiÃ³ que Â«Dios no hace acepciÃ³n "
        "de personasÂ» (Hch. 10:34-35) y que la salvaciÃ³n en Cristo estaba destinada a todas las naciones.<br><br>"
        "AÃ±os mÃ¡s tarde, Pedro defendiÃ³ esta verdad durante la reuniÃ³n de los apÃ³stoles y ancianos en JerusalÃ©n, afirmando que "
        "Dios habÃ­a concedido la salvaciÃ³n a judÃ­os y gentiles por la misma fe en Jesucristo (Hch. 15:7-11). Su testimonio "
        "confirmÃ³ oficialmente la apertura de la misiÃ³n a todas las naciones y preparÃ³ el camino para el amplio ministerio "
        "que posteriormente desarrollarÃ­a el apÃ³stol Pablo.<br><br>"
        "AdemÃ¡s de su labor como predicador y pastor, Pedro dejÃ³ un legado permanente en las dos cartas que llevan su nombre. "
        "En ellas anima a los creyentes a permanecer firmes en la fe, crecer en santidad y mantener viva la esperanza en medio "
        "de las pruebas (1 P. 1:3-9; 2 P. 1:5-11).<br><br>"
        "La vida de Pedro demuestra que Dios forma a sus siervos mediante un proceso de aprendizaje. El pescador de Galilea "
        "llegÃ³ a ser el apÃ³stol que proclamÃ³ el evangelio con valentÃ­a, fortaleciÃ³ a la Iglesia naciente y abriÃ³ el camino para "
        "que el mensaje de salvaciÃ³n alcanzara a todos los pueblos de la tierra. Su historia tambiÃ©n recuerda que una comprensiÃ³n "
        "cada vez mÃ¡s profunda del propÃ³sito de Dios transforma la manera de vivir y de servir."
    ),
    "rows": 20,
    "cols": 20,
    "words": [
        "SIMON", "PIEDRA", "GALILEA", "PESCADOR", "ANDRES",
        "LLAMAMIENTO", "REDES", "LLAVES", "FE", "CAMINAR",
        "SUEGRA", "CRISTO", "NEGACION", "RESTAURACION", "PENTECOSTES",
        "CORNELIO", "ESPERANZA", "SANTIDAD", "PRIMERA", "SEGUNDA"
    ],
    "clues": {
        "SIMON": "Nombre original del apÃ³stol antes de que JesÃºs le cambiara el nombre.",
        "PIEDRA": "Significado del nombre que JesÃºs dio a SimÃ³n como expresiÃ³n de firmeza y propÃ³sito.",
        "GALILEA": "RegiÃ³n donde Pedro naciÃ³ y desarrollaba su oficio antes de seguir a Cristo.",
        "PESCADOR": "Oficio que Pedro ejercÃ­a cuando JesÃºs lo llamÃ³ para convertirse en discÃ­pulo.",
        "ANDRES": "Hermano de Pedro que lo llevÃ³ primero al encuentro con JesÃºs.",
        "LLAMAMIENTO": "Evento en el que JesÃºs invitÃ³ a Pedro a dejar su antigua vida para seguirle.",
        "REDES": "Instrumentos de trabajo que Pedro utilizaba antes de convertirse en pescador de hombres.",
        "LLAVES": "Lo que JesÃºs prometiÃ³ entregar a Pedro despuÃ©s de su confesiÃ³n de que Ã‰l era el Cristo. (Mt. 16:16-19)",
        "FE": "Cualidad que JesÃºs enseÃ±Ã³ a Pedro cuando tuvo que confiar en Ã‰l mÃ¡s allÃ¡ de sus circunstancias.",
        "CAMINAR": "AcciÃ³n que Pedro intentÃ³ realizar sobre el agua cuando JesÃºs lo invitÃ³ a salir de la barca.",
        "SUEGRA": "Familiar de Pedro a quien JesÃºs curÃ³ de una fiebre en su casa.",
        "CRISTO": "TÃ­tulo que Pedro reconociÃ³ al declarar quiÃ©n era JesÃºs.",
        "NEGACION": "AcciÃ³n que cometiÃ³ tres veces antes del canto del gallo.",
        "RESTAURACION": "Momento posterior a la resurrecciÃ³n donde JesÃºs confirmÃ³ nuevamente a Pedro en su misiÃ³n.",
        "PENTECOSTES": "DÃ­a en que Pedro predicÃ³ con poder y miles de personas respondieron al mensaje del evangelio.",
        "CORNELIO": "Hombre al que Pedro llevÃ³ el evangelio mostrando que Dios tambiÃ©n llamaba a los gentiles.",
        "ESPERANZA": "Tema central que Pedro anima a mantener en medio de las pruebas y sufrimientos.",
        "SANTIDAD": "Llamado que Pedro presenta a los creyentes como consecuencia de pertenecer a Dios.",
        "PRIMERA": "Carta escrita por Pedro para fortalecer a creyentes que enfrentaban sufrimiento por su fe.",
        "SEGUNDA": "Carta donde Pedro advierte sobre falsos maestros y anima al crecimiento espiritual."
    }
}

# --- RUTA PARA LA SEMANA 2 ---
output_dir = "docs/semana-02"
os.makedirs(output_dir, exist_ok=True)

# Generar crucigrama
gen = Generator(datos_crucigrama_3)
resultado = gen.generate()

# Exportar HTMLs
web = WebExporter(resultado, **datos_crucigrama_3)
web.save(os.path.join(output_dir, "crucigrama_3_web.html"))

estatico = Exporter(resultado, **datos_crucigrama_3)
estatico.save(os.path.join(output_dir, "crucigrama_3.html"))

print("âœ… Archivos creados correctamente en la carpeta 'docs/semana-02/'.")
