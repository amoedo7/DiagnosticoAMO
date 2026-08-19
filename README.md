<div align="center">

# DiagnosticoAMO

**Unir señales del dispositivo, la red y el sistema en una lectura única.**

[![CI](https://github.com/amoedo7/DiagnosticoAMO/actions/workflows/ci.yml/badge.svg)](https://github.com/amoedo7/DiagnosticoAMO/actions/workflows/ci.yml)

[`MiDispositivo`](https://github.com/amoedo7/MiDispositivo) + [`MiRed`](https://github.com/amoedo7/MiRed) + [`MiSistema`](https://github.com/amoedo7/MiSistema)
</div>

---

## Qué hace

DiagnosticoAMO **no vuelve a inspeccionar el equipo**. Lee reportes JSON ya generados por la suite `Mi...` y crea una vista consolidada:

- qué reportes recibió;
- sistema y recursos principales;
- salud de red;
- runtimes disponibles;
- capacidades detectadas;
- faltantes relevantes;
- score heurístico con desglose visible.

Todo el procesamiento es local.

## Flujo

```text
MiDispositivo ─┐
MiRed ─────────┼──→ DiagnosticoAMO ──→ lectura única
MiSistema ─────┘
```

## Ejecutar

```bash
python diagnosticoamo.py dispositivo.json red.json sistema.json
```

Guardar informe:

```bash
python diagnosticoamo.py dispositivo.json red.json sistema.json --output diagnostico.json
```

Ver una demostración sin datos reales:

```bash
python diagnosticoamo.py --demo
```

## Score

El score no pretende certificar que una máquina sea "buena" o "mala". Es una lectura transparente para saber si tenemos suficiente información y si ciertas capacidades técnicas están disponibles. El JSON incluye el desglose para que pueda auditarse.

---

**DesarrollAMO** · primero entender el entorno; después decidir qué construir o instalar.
