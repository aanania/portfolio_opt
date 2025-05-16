# portfolio_opt
Optimizacion de Portafolio


## Ejecución 

Primero, debes tener Docker instalado en tu computador y ejecutar los siguiente comandos:

```
docker build -t portfolio-optimizer .
docker run -p 8000:8000 portfolio-optimizer
```

## Detalles de las decisiones

En un modelo de optimización centrado únicamente en retornos, la optimización de 
Markowitz ofrece una solución simple y adecuada para el objetivo planteado.

Además, la decisión de optimizar en función del Ratio de Sharpe se fundamenta en 
su capacidad para encontrar un equilibrio óptimo entre retorno y riesgo. A partir
de este punto, buscar mayores retornos conlleva un aumento significativo del riesgo,
mientras que la optimización exclusiva por riesgo puede resultar en portafolios 
con retornos subóptimos. La estrategia final debe alinearse con el perfil de riesgo 
del inversor.

Para limitar el riesgo, se consideró como métrica de riesgo a la desviación estandar,
ya que es bastante buena para cuantificar la disperción de los retornos (la que puede
asustar a los inversionistas si aumenta mucho).

