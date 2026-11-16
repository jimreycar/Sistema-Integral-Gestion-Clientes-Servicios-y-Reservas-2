
import logging
import unittest


# ==========================================
# 1. CONFIGURACION DEL ARCHIVO DE LOGS
# ==========================================

logging.basicConfig(
    filename="sistema.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
    force=True
)

logger = logging.getLogger("SistemaSoftwareFJ")


# ==========================================
# 2. EXCEPCION PERSONALIZADA
# ==========================================

class ErrorValidacion(Exception):
    """Controla los errores de validacion."""
    pass


# ==========================================
# 3. CLASE PARA CALCULAR COSTOS
# ==========================================

class CalculadoraCostos:
    """
    Realiza calculos de costos mediante diferentes
    variantes de metodos y parametros opcionales.
    """

    @staticmethod
    def validar_porcentaje(valor, nombre):

        if (
            isinstance(valor, bool)
            or not isinstance(valor, (int, float))
        ):
            mensaje = f"{nombre} debe ser numerico."
            logger.error(mensaje)
            raise ErrorValidacion(mensaje)

        if not 0 <= valor <= 1:
            mensaje = f"{nombre} debe estar entre 0 y 1."
            logger.error(mensaje)
            raise ErrorValidacion(mensaje)

    @staticmethod
    def validar_subtotal(subtotal):

        if (
            isinstance(subtotal, bool)
            or not isinstance(subtotal, (int, float))
        ):
            mensaje = "El subtotal debe ser numerico."
            logger.error(mensaje)
            raise ErrorValidacion(mensaje)

        if subtotal < 0:
            mensaje = "El subtotal no puede ser negativo."
            logger.error(mensaje)
            raise ErrorValidacion(mensaje)

    # ======================================
    # METODO PRINCIPAL DE CALCULO
    # ======================================

    @staticmethod
    def calcular(
        subtotal,
        impuesto=0,
        descuento=0,
        recargo=0
    ):
        """
        Calcula el costo final.

        Permite utilizar impuesto, descuento y recargo
        de manera opcional.

        Los porcentajes se expresan entre 0 y 1.
        """

        try:
            CalculadoraCostos.validar_subtotal(subtotal)

            CalculadoraCostos.validar_porcentaje(
                impuesto, "El impuesto"
            )

            CalculadoraCostos.validar_porcentaje(
                descuento, "El descuento"
            )

            CalculadoraCostos.validar_porcentaje(
                recargo, "El recargo"
            )

            total = subtotal * (1 - descuento)
            total = total * (1 + impuesto)
            total = total * (1 + recargo)

            resultado = round(total, 2)

            logger.info(
                "Calculo exitoso | Subtotal: %.2f | "
                "Impuesto: %.2f | Descuento: %.2f | "
                "Recargo: %.2f | Total: %.2f",
                subtotal,
                impuesto,
                descuento,
                recargo,
                resultado
            )

            return resultado

        except ErrorValidacion:
            raise

        except Exception:
            logger.exception("Error inesperado en el calculo.")
            raise

    # ======================================
    # VARIANTE 1: CALCULO BASICO
    # ======================================

    @staticmethod
    def calcular_basico(subtotal):

        logger.info("Se solicito un calculo basico.")

        return CalculadoraCostos.calcular(subtotal)

    # ======================================
    # VARIANTE 2: CALCULO CON IMPUESTO
    # ======================================

    @staticmethod
    def calcular_con_impuesto(subtotal, impuesto):

        logger.info("Se solicito un calculo con impuesto.")

        return CalculadoraCostos.calcular(
            subtotal,
            impuesto=impuesto
        )

    # ======================================
    # VARIANTE 3: CALCULO CON DESCUENTO
    # ======================================

    @staticmethod
    def calcular_con_descuento(subtotal, descuento):

        logger.info("Se solicito un calculo con descuento.")

        return CalculadoraCostos.calcular(
            subtotal,
            descuento=descuento
        )

    # ======================================
    # VARIANTE 4: CALCULO COMPLETO
    # ======================================

    @staticmethod
    def calcular_completo(
        subtotal,
        impuesto=0,
        descuento=0,
        recargo=0
    ):

        logger.info("Se solicito un calculo completo.")

        return CalculadoraCostos.calcular(
            subtotal,
            impuesto,
            descuento,
            recargo
        )


# ==========================================
# 4. FUNCION PARA REGISTRAR EVENTOS
# ==========================================

def registrar_evento(mensaje):

    logger.info(mensaje)


# ==========================================
# 5. DIEZ PRUEBAS AUTOMATIZADAS
# ==========================================

class PruebasCalculadora(unittest.TestCase):

    def setUp(self):

        registrar_evento("Inicio de una prueba automatizada.")

    # PRUEBA 1: CALCULO BASICO

    def test_calculo_basico(self):

        resultado = CalculadoraCostos.calcular_basico(100000)

        self.assertEqual(resultado, 100000)

    # PRUEBA 2: CALCULO CON IMPUESTO

    def test_calculo_con_impuesto(self):

        resultado = CalculadoraCostos.calcular_con_impuesto(
            100000,
            0.19
        )

        self.assertEqual(resultado, 119000)

    # PRUEBA 3: CALCULO CON DESCUENTO

    def test_calculo_con_descuento(self):

        resultado = CalculadoraCostos.calcular_con_descuento(
            100000,
            0.10
        )

        self.assertEqual(resultado, 90000)

    # PRUEBA 4: CALCULO CON IMPUESTO Y DESCUENTO

    def test_calculo_completo(self):

        resultado = CalculadoraCostos.calcular_completo(
            100000,
            impuesto=0.19,
            descuento=0.10
        )

        self.assertEqual(resultado, 107100)

    # PRUEBA 5: CALCULO CON RECARGO

    def test_calculo_con_recargo(self):

        resultado = CalculadoraCostos.calcular_completo(
            100000,
            recargo=0.10
        )

        self.assertEqual(resultado, 110000)

    # PRUEBA 6: CALCULO CON TODOS LOS PARAMETROS

    def test_calculo_todos_los_parametros(self):

        resultado = CalculadoraCostos.calcular_completo(
            200000,
            impuesto=0.19,
            descuento=0.10,
            recargo=0.05
        )

        self.assertEqual(resultado, 124740)

    # PRUEBA 7: IMPUESTO INCORRECTO

    def test_impuesto_incorrecto(self):

        with self.assertRaises(ErrorValidacion):

            CalculadoraCostos.calcular(
                100000,
                impuesto=1.5
            )

    # PRUEBA 8: DESCUENTO INCORRECTO

    def test_descuento_incorrecto(self):

        with self.assertRaises(ErrorValidacion):

            CalculadoraCostos.calcular(
                100000,
                descuento=-0.20
            )

    # PRUEBA 9: SUBTOTAL NEGATIVO

    def test_subtotal_negativo(self):

        with self.assertRaises(ErrorValidacion):

            CalculadoraCostos.calcular(-50000)

    # PRUEBA 10: PARAMETRO NO NUMERICO

    def test_parametro_no_numerico(self):

        with self.assertRaises(ErrorValidacion):

            CalculadoraCostos.calcular(
                100000,
                impuesto="incorrecto"
            )


# ==========================================
# 6. EJECUCION DE LAS PRUEBAS
# ==========================================

if __name__ == "__main__":

    print("======================================")
    print(" SISTEMA SOFTWARE FJ")
    print(" MODULO DE CALCULOS Y REGISTRO")
    print("======================================")

    registrar_evento("Inicio de ejecucion del modulo.")

    resultado = unittest.TextTestRunner(
        verbosity=2
    ).run(
        unittest.TestLoader().loadTestsFromTestCase(
            PruebasCalculadora
        )
    )

    if resultado.wasSuccessful():

        logger.info("Las diez pruebas fueron aprobadas.")

        print("\nLas pruebas finalizaron correctamente.")

    else:

        logger.error("Se presentaron fallos en las pruebas.")

        print("\nSe encontraron errores en las pruebas.")

    print("\nArchivo de registro generado: sistema.log")
    print("======================================")
