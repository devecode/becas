from django.db import models


class Solicitud(models.Model):
    PRI = 'PRIMARIA'
    SEC = 'SECUNDARIA'
    PRE = 'PREPA'
    UNI = 'UNIVERSIDAD'
    GRADO = [
        (PRI, 'PRIMARIA'),
        (SEC, 'SECUNDARIA'),
        (PRE, 'PREPA'),
        (UNI, 'UNIVERSIDAD')
    ]

    AP = 'ARTES PLASTICAS'
    MU = 'MUSICA'
    DA = 'DANZA'
    TE = 'TEATRO'
    LI = 'LITERATURA'
    FORMACION = [
        (AP, 'ARTES PLASTICAS'),
        (MU, 'MUSICA'),
        (DA, 'DANZA'),
        (TE, 'TEATRO'),
        (LI, 'LITERATURA')
    ]

    AE = 'APROVECHAMIENTO ESCOLAR'
    AD = ' APROVECHAMIENTO ACADEMICO DESTACADO'
    AF = 'APOYO ALUMNOS FORANEOS'
    MODALIDAD = [
        (AE, 'APROVECHAMIENTO ESCOLAR'),
        (AD, 'APROVECHAMIENTO ACADEMICO DESTACADO'),
        (AF, 'APOYO ALUMNOS FORANEOS')
    ]

    MA = 'MASCULINO'
    FE = 'FEMENINO'
    GENERO = [
        (MA, 'MASCULINO'),
        (FE, 'FEMENINO')
    ]

    SI = 'ENTREGADO'
    NO = 'NO ENTREGADO'
    ESTADO = [
        (SI, 'ENTREGADO'),
        (NO, 'NO ENTREGADO')
    ]
    nombre = models.CharField('NOMBRE ', max_length=500, unique=True)
    ap = models.CharField('APELLIDO PATERNO ', max_length=500)
    am = models.CharField('APELLIDO MATERNO ', max_length=500)
    domicilio = models.CharField('DOMICILIO', max_length=500)
    colonia = models.CharField('COLONIA', max_length=500)
    telefono = models.CharField('TELEFONO', max_length=15)
    fn = models.DateField('FECHA DE NACIMIENTO')
    ga = models.CharField('GRADO ACADEMICO', max_length=50,
                          choices=GRADO, default=PRI)
    matricula = models.CharField('MATRICULA', max_length=50)
    formacion_artistica = models.CharField(
        'FORMACIÓN ARTISTICA', max_length=50, choices=FORMACION, default=MU)
    modalidad = models.CharField(
        'MODALIDAD DE BECA', max_length=500, choices=MODALIDAD, default=AE)
    genero = models.CharField('GENERO', max_length=500,
                              choices=GENERO, default=FE)
    correo = models.EmailField('CORREO ELECTRONICO')
    entrega = models.CharField(
        'ESTADO DEL APOYO', max_length=50, choices=ESTADO, default=NO, blank=True)

    def __str__(self):
        return self.nombre

    def save(self):
        super(Solicitud, self).save()
