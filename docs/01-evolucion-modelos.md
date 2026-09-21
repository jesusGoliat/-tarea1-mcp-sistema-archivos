# 1. Evolución de los modelos

## De modelo de lenguaje (LM) a modelo de lenguaje grande (LLM)

Un **modelo de lenguaje (LM)** es un sistema estadístico que aprende la distribución de probabilidad de secuencias de texto: dado un fragmento de texto, predice qué palabra (o token) es más probable que siga. Los primeros modelos de lenguaje eran modelos *n-grama*, que estimaban esa probabilidad contando frecuencias de secuencias cortas de palabras en un corpus, sin ninguna noción real de significado ni de contexto largo.

La evolución hacia un **modelo de lenguaje grande (LLM)** ocurrió por la combinación de tres factores:

1. **Arquitectura Transformer** (Vaswani et al., 2017): reemplazó a las redes recurrentes con un mecanismo de *atención* que permite al modelo relacionar cualquier token de la secuencia con cualquier otro, sin importar la distancia entre ellos, y hacerlo en paralelo (lo que aceleró enormemente el entrenamiento).
2. **Escala**: se pasó de modelos con millones de parámetros entrenados en corpus pequeños a modelos con cientos de miles de millones de parámetros entrenados con billones de tokens de texto de internet, código y libros.
3. **Preentrenamiento autosupervisado + ajuste fino**: el modelo primero aprende a predecir el siguiente token sobre texto masivo sin etiquetar (preentrenamiento), y después se ajusta con técnicas como *instruction tuning* y **RLHF** (*Reinforcement Learning from Human Feedback*) para que sus respuestas sean útiles, sigan instrucciones y sean seguras.

El resultado es un modelo que ya no solo predice la siguiente palabra de forma mecánica, sino que exhibe capacidades emergentes de comprensión de lenguaje natural, traducción, resumen, generación de código, etc., simplemente a partir de haber visto suficiente texto y haber sido ajustado para seguir instrucciones.

## Modelos con razonamiento explícito

Un **modelo con razonamiento explícito** (a veces llamado *reasoning model*) es un LLM que, antes de emitir la respuesta final, genera una cadena de pasos intermedios de razonamiento (*chain of thought*) que puede usar más tokens de cómputo para explorar el problema, verificar pasos intermedios o descartar caminos equivocados.

Es un error conceptual pensar que esta capacidad "aparece sola" simplemente por hacer el modelo más grande. La evidencia apunta a que el razonamiento explícito depende de dos cosas adicionales, no solo de la escala del modelo:

- **Técnicas de entrenamiento específicas**: entrenar al modelo con aprendizaje por refuerzo sobre tareas con **recompensas verificables** (por ejemplo, problemas matemáticos o de código donde la respuesta correcta se puede comprobar automáticamente). 
- **Cómputo adicional en el momento de la inferencia** (*test-time compute* / *inference-time compute*): el modelo dedica más tokens y más tiempo de cómputo a "pensar" antes de responder, lo cual es una decisión de diseño del sistema de inferencia, no una propiedad automática del tamaño del modelo.

## Referencias de este documento

- Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I. (2017). *Attention is all you need*. Advances in Neural Information Processing Systems, 30.
