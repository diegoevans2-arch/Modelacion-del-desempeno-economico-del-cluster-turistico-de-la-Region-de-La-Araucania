---
title: Simulador IDEC — Clúster Turístico de La Araucanía
emoji: 🏔️
colorFrom: green
colorTo: blue
sdk: static
app_file: index.html
pinned: false
license: mit
short_description: Desempeño económico del clúster turístico de La Araucanía
---

# Simulador IDEC — Clúster Turístico de La Araucanía

Herramienta de apoyo a la investigación doctoral *Modelación del desempeño
económico del clúster turístico de la Región de La Araucanía mediante técnicas
de Machine Learning aplicadas a datos públicos*.

Permite consultar el **Índice de Desempeño Económico del Clúster (IDEC)** a nivel
comunal y simular escenarios de **Choques Exógenos Territoriales (CET)**.

## Qué hace

- **Simulador de escenarios.** Seleccione comuna y año, ajuste la variable CET y
  observe el efecto estimado sobre el desempeño del clúster.
- **Explorador del panel.** Evolución del IDEC por comuna y comparación entre los
  13 territorios del estudio.

## Cómo funciona

La aplicación es estática: no ejecuta código en servidor. Las predicciones del
modelo Random Forest están **precomputadas** para los 156 pares comuna-año del
panel, y la atenuación por CET es una fórmula cerrada que se evalúa en el
navegador. Esto no supone pérdida de funcionalidad —los escenarios se anclan en
el valor observado y el modelo aparece como contraste— y garantiza carga
instantánea.

Regenerar los datos, desde la raíz del repositorio de investigación:

```bash
python -m deploy_static.generar_datos
```

## Alcance y limitaciones

Esta es una **herramienta de investigación, no de pronóstico**.

- El IDEC mide desempeño económico **estructural** —empleo, ingresos y capacidad
  instalada—. No incorpora flujos de visitantes.
- Cubre **13 comunas** y los años **2013–2024**. El modelo no generaliza a
  territorios ausentes del panel (R² = −0,36 en validación por comuna).
- La variable CET opera con una **elasticidad declarada**, no estimada de los
  datos históricos.
- El modelo comprime los valores extremos hacia la media, por lo que los
  escenarios se anclan en el valor observado.

Detalle completo en la pestaña *Metodología y limitaciones* de la aplicación.

## Datos

Construido exclusivamente con registros administrativos de acceso público:
Servicio de Impuestos Internos · Banco Integrado de Proyectos · Instituto
Nacional de Estadísticas · SERNATUR · CONAF.

No contiene información personal. Las cifras del SII respetan la reserva
tributaria establecida en el Artículo 35 del Código Tributario.

## Cita

```bibtex
@phdthesis{barra2026cluster,
  author = {Barra Ávila, Germán Patricio},
  title  = {Modelación del desempeño económico del clúster turístico de la
            Región de La Araucanía mediante técnicas de machine learning
            aplicadas a datos públicos para la toma de decisiones territoriales},
  school = {TECH Universidad Tecnológica},
  year   = {2026},
  type   = {Tesis Doctoral},
  address = {Santiago, Chile}
}
```
